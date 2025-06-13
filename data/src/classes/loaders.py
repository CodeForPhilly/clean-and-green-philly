import logging as log
import os
import subprocess
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Tuple

import geopandas as gpd
import pandas as pd
import requests
from esridump.dumper import EsriDumper
from google.cloud import storage
from shapely import wkb
from tqdm import tqdm

from src.classes.bucket_manager import GCSBucketManager
from src.classes.file_manager import FileManager, FileType, LoadType
from src.config.config import (
    FORCE_RELOAD,
    USE_CRS,
    log_level,
    min_tiles_file_size_in_bytes,
    write_production_tiles_file,
)
from src.validation.base import BaseValidator, ValidationResult

log.basicConfig(level=log_level)


# Esri data loader
def load_esri_data(esri_urls: List[str], input_crs: str):
    """
    Load data from Esri REST URLs and add a parcel_type column based on the URL.

    Args:
        esri_rest_urls (list[str]): List of Esri REST URLs to fetch data from.
        input_crs (str): CRS of the source data.
    Returns:
        GeoDataFrame: Combined GeoDataFrame with data from all URLs.
    """
    gdfs = []
    for url in esri_urls:
        # Determine parcel_type based on URL patterns
        parcel_type = (
            "Land"
            if "Vacant_Indicators_Land" in url
            else "Building"
            if "Vacant_Indicators_Bldg" in url
            else None
        )

        dumper = EsriDumper(url)
        features = [feature for feature in dumper]

        if not features:
            continue  # Skip if no features were found

        geojson_features = {"type": "FeatureCollection", "features": features}
        gdf = gpd.GeoDataFrame.from_features(geojson_features, crs=input_crs)

        if parcel_type:
            gdf["parcel_type"] = parcel_type  # Add the parcel_type column

        gdfs.append(gdf)

    return pd.concat(gdfs, ignore_index=True)


# Carto data loader
def load_carto_data(
    queries: List[str],
    input_crs: str,
    wkb_geom_field: str | None = "the_geom",
    max_workers: int = os.cpu_count(),
    chunk_size: int = 100000,
):
    gdfs = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for query in queries:
            total_rows = get_carto_total_rows(query)
            for offset in range(0, total_rows, chunk_size):
                futures.append(
                    executor.submit(
                        fetch_carto_chunk,
                        query,
                        offset,
                        input_crs,
                        wkb_geom_field,
                        chunk_size,
                    )
                )
        for future in tqdm(
            as_completed(futures), total=len(futures), desc="Processing Carto chunks"
        ):
            gdfs.append(future.result())
    return pd.concat(gdfs, ignore_index=True)


def fetch_carto_chunk(
    query: str,
    offset: int,
    input_crs: str,
    wkb_geom_field: str | None = "the_geom",
    chunk_size: int = 100000,
):
    chunk_query = f"{query} LIMIT {chunk_size} OFFSET {offset}"
    response = requests.get(
        "https://phl.carto.com/api/v2/sql", params={"q": chunk_query}
    )
    response.raise_for_status()
    data = response.json().get("rows", [])
    if not data:
        return gpd.GeoDataFrame()
    df = pd.DataFrame(data)
    geometry = (
        wkb.loads(df[wkb_geom_field], hex=True)
        if wkb_geom_field
        else gpd.points_from_xy(df.x, df.y)
    )
    return gpd.GeoDataFrame(df, geometry=geometry, crs=input_crs)


def get_carto_total_rows(query):
    count_query = f"SELECT COUNT(*) as count FROM ({query}) as subquery"
    response = requests.get(
        "https://phl.carto.com/api/v2/sql", params={"q": count_query}
    )
    response.raise_for_status()
    return response.json()["rows"][0]["count"]


def google_cloud_bucket(require_write_access: bool = False) -> storage.Bucket | None:
    """
    Initialize a Google Cloud Storage bucket client using Application Default Credentials.
    If a writable bucket is requested and the user does not have write access None is returned.

    Args:
        require_write_access (bool): Whether it is required that the bucket should be writable. Defaults to False.
    """

    bucket_manager = GCSBucketManager()
    if require_write_access and bucket_manager.read_only:
        return None
    return bucket_manager.bucket


class BaseLoader(ABC):
    def __init__(
        self,
        name: str,
        cols: List[str] = [],
        input_crs: str | None = USE_CRS,
        opa_col: str | None = None,
        validator: BaseValidator | None = None,
    ):
        self.name = name
        self.table_name = name.lower().replace(" ", "_")
        self.cols = cols
        self.opa_col = opa_col
        self.input_crs = input_crs
        self.file_manager = FileManager()
        self.validator = validator

    def cache_data(self, gdf: gpd.GeoDataFrame) -> None:
        if gdf is None or gdf.empty:
            log.info("No data to cache")
            return

        # Save sourced data to a local parquet file in the storage/source_cache directory
        file_label = self.file_manager.generate_file_label(self.table_name)
        self.file_manager.save_gdf(
            gdf, file_label, LoadType.SOURCE_CACHE, FileType.PARQUET
        )

    def load_or_fetch(self) -> Tuple[gpd.GeoDataFrame, ValidationResult]:
        if not FORCE_RELOAD and self.file_manager.check_source_cache_file_exists(
            self.table_name, LoadType.SOURCE_CACHE
        ):
            print(f"Loading data for {self.name} from cache...")
            gdf = self.file_manager.get_most_recent_cache(self.table_name)
        else:
            print("Loading fresh data now...")
            gdf = self.load_data()
            print("Caching fresh data now...")
            self.cache_data(gdf)

        validation_result = (
            self.validator.validate(gdf) if self.validator else ValidationResult(True)
        )

        return gdf, validation_result

    def standardize_opa(self, gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
        """
        Standardize the OPA column in the GeoDataFrame to be a string and renamed properly to "opa_id".
        """
        if self.opa_col:
            gdf.rename(columns={self.opa_col: "opa_id"}, inplace=True)

        if "opa_id" in gdf.columns:
            gdf["opa_id"] = gdf["opa_id"].map(
                lambda x: str(x) if x is not None else None
            )
            gdf.dropna(subset=["opa_id"], inplace=True)

        return gdf

    @abstractmethod
    def load_data(self):
        pass

    @staticmethod
    def string_to_list(input: str | List[str]) -> List[str]:
        return [input] if isinstance(input, str) else input

    @staticmethod
    def lowercase_column_names(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
        # Standardize column names
        if not gdf.empty:
            gdf.columns = [col.lower() for col in gdf.columns]
        return gdf

    @staticmethod
    def filter_columns(gdf: gpd.GeoDataFrame, cols: List[str]) -> gpd.GeoDataFrame:
        # Filter columns if specified
        if cols:
            cols = [col.lower() for col in cols]
            cols.append("geometry")
            gdf = gdf[[col for col in cols if col in gdf.columns]]
        return gdf

    @classmethod
    def normalize_columns(
        cls, gdf: gpd.GeoDataFrame, cols: List[str]
    ) -> gpd.GeoDataFrame:
        """
        Normalize the columns of the GeoDataFrame to lowercase.
        """
        gdf = cls.lowercase_column_names(gdf)
        gdf = cls.filter_columns(gdf, cols)

        return gdf


class GdfLoader(BaseLoader):
    def __init__(self, input: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.input = input

    def load_data(self):
        gdf = gpd.read_file(self.input)
        gdf = self.normalize_columns(gdf, self.cols)

        if not gdf.crs:
            raise AttributeError("Input data doesn't have an original CRS set")

        gdf = gdf.to_crs(USE_CRS)
        gdf["geometry"] = gdf.geometry.make_valid()

        return gdf


class EsriLoader(BaseLoader):
    def __init__(self, esri_urls: List[str], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.esri_urls = esri_urls

    def load_data(self):
        gdf = load_esri_data(self.esri_urls, self.input_crs)
        gdf = self.normalize_columns(gdf, self.cols)

        gdf = gdf.to_crs(USE_CRS)
        gdf = self.standardize_opa(gdf)
        gdf["geometry"] = gdf.geometry.make_valid()

        return gdf


class CartoLoader(BaseLoader):
    def __init__(
        self,
        carto_queries: str | List[str],
        *args,
        wkb_geom_field: str | None = "the_geom",
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.carto_queries = BaseLoader.string_to_list(carto_queries)
        self.wkb_geom_field = wkb_geom_field

    def load_data(self):
        gdf = load_carto_data(self.carto_queries, self.input_crs, self.wkb_geom_field)
        gdf = self.normalize_columns(gdf, self.cols)

        gdf = gdf.to_crs(USE_CRS)
        gdf = self.standardize_opa(gdf)
        gdf["geometry"] = gdf.geometry.make_valid()

        return gdf

    def build_and_publish(self, tiles_file_id_prefix: str) -> None:
        """
        Builds PMTiles and a Parquet file from a GeoDataFrame and publishes them to Google Cloud Storage.

        Args:
            tiles_file_id_prefix (str): The ID prefix used for naming the PMTiles and Parquet files, coming from src.config.

        Raises:
            ValueError: Raised if the generated PMTiles file is smaller than the minimum allowed size, indicating a potential corruption or incomplete file.
        """
        zoom_threshold: int = 13

        # Export the GeoDataFrame to a temporary GeoJSON file
        temp_geojson_points: str = (
            f"storage/temp/temp_{tiles_file_id_prefix}_points.geojson"
        )
        temp_geojson_polygons: str = (
            f"storage/temp/temp_{tiles_file_id_prefix}_polygons.geojson"
        )
        temp_pmtiles_points: str = (
            f"storage/temp/temp_{tiles_file_id_prefix}_points.pmtiles"
        )
        temp_pmtiles_polygons: str = (
            f"storage/temp/temp_{tiles_file_id_prefix}_polygons.pmtiles"
        )
        temp_merged_pmtiles: str = (
            f"storage/temp/temp_{tiles_file_id_prefix}_merged.pmtiles"
        )

        # Reproject
        gdf_wm = self.gdf.to_crs(epsg=4326)
        gdf_wm.to_file(temp_geojson_polygons, driver="GeoJSON")

        # Create points dataset
        self.centroid_gdf = self.gdf.copy()
        self.centroid_gdf["geometry"] = self.centroid_gdf["geometry"].centroid
        self.centroid_gdf = self.centroid_gdf.to_crs(epsg=4326)
        self.centroid_gdf.to_file(temp_geojson_points, driver="GeoJSON")

        # Command for generating PMTiles for points up to zoom level zoom_threshold
        points_command: list[str] = [
            "tippecanoe",
            f"--output={temp_pmtiles_points}",
            f"--maximum-zoom={zoom_threshold}",
            "--minimum-zoom=10",
            "-zg",
            "-aC",
            "-r0",
            temp_geojson_points,
            "-l",
            "vacant_properties_tiles_points",
            "--force",
        ]

        # Command for generating PMTiles for polygons from zoom level zoom_threshold
        polygons_command: list[str] = [
            "tippecanoe",
            f"--output={temp_pmtiles_polygons}",
            f"--minimum-zoom={zoom_threshold}",
            "--maximum-zoom=16",
            "-zg",
            "--no-tile-size-limit",
            temp_geojson_polygons,
            "-l",
            "vacant_properties_tiles_polygons",
            "--force",
        ]

        # Command for merging the two PMTiles files into a single output file
        merge_command: list[str] = [
            "tile-join",
            f"--output={temp_merged_pmtiles}",
            "--no-tile-size-limit",
            temp_pmtiles_polygons,
            temp_pmtiles_points,
            "--force",
        ]

        # Run the commands
        for command in [points_command, polygons_command, merge_command]:
            subprocess.run(command)

        write_files: list[str] = [f"{tiles_file_id_prefix}_staging.pmtiles"]

        if write_production_tiles_file:
            write_files.append(f"{tiles_file_id_prefix}.pmtiles")

        # Check whether the temp saved tiles files is big enough.
        file_size: int = os.stat(temp_merged_pmtiles).st_size
        if file_size < min_tiles_file_size_in_bytes:
            raise ValueError(
                f"{temp_merged_pmtiles} is {file_size} bytes in size but should be at least {min_tiles_file_size_in_bytes}. Therefore, we are not uploading any files to the GCP bucket. The file may be corrupt or incomplete."
            )

        bucket = google_cloud_bucket(require_write_access=True)
        if bucket is None:
            print("Skipping PMTiles upload due to read-only bucket access.")
            return

        # Upload PMTiles to Google Cloud Storage
        bucket = google_cloud_bucket()
        for file in write_files:
            blob = bucket.blob(file)
            try:
                blob.upload_from_filename(temp_merged_pmtiles)
                print(f"PMTiles upload successful for {file}!")
            except Exception as e:
                print(f"PMTiles upload failed for {file}: {e}")
