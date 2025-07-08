import os
import subprocess
import time
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Optional, Tuple

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
    get_logger,
    min_tiles_file_size_in_bytes,
    write_production_tiles_file,
)
from src.validation.base import BaseValidator, ValidationResult


# Esri data loader
def load_esri_data(esri_urls: List[str], input_crs: str, extra_query_args: dict = None):
    """
    Load data from Esri REST URLs and add a parcel_type column based on the URL.

    Args:
        esri_rest_urls (list[str]): List of Esri REST URLs to fetch data from.
        input_crs (str): CRS of the source data.
        extra_query_args (dict): Additional query parameters to pass to the ESRI service.
    Returns:
        GeoDataFrame: Combined GeoDataFrame with data from all URLs.
    """
    geometry_logger = get_logger("geometry_debug")
    gdfs = []

    for url in esri_urls:
        geometry_logger.info(f"Processing ESRI URL: {url}")

        # Determine parcel_type based on URL patterns
        parcel_type = (
            "Land"
            if "Vacant_Indicators_Land" in url
            else "Building"
            if "Vacant_Indicators_Bldg" in url
            else None
        )

        # Create dumper with query parameters if provided
        dumper_kwargs = {
            "url": url,
            "pause_seconds": 1,
            "requests_to_pause": 10,
            "max_page_size": 2000,
        }

        # Pass extra_query_args as the extra_query_args parameter, not as direct kwargs
        if extra_query_args:
            dumper_kwargs["extra_query_args"] = extra_query_args

        geometry_logger.info("Creating EsriDumper...")
        dumper = EsriDumper(**dumper_kwargs)

        geometry_logger.info("Fetching features from ESRI service...")
        features = [feature for feature in dumper]
        geometry_logger.info(f"Fetched {len(features)} features from ESRI service")

        if not features:
            geometry_logger.warning("No features found, skipping this URL")
            continue  # Skip if no features were found

        geojson_features = {"type": "FeatureCollection", "features": features}

        geometry_logger.info("Creating GeoDataFrame from features...")
        # Let the service determine its own CRS first
        gdf = gpd.GeoDataFrame.from_features(geojson_features)

        geometry_logger.info(
            f"Initial GeoDataFrame CRS: EPSG:{gdf.crs.to_epsg() if gdf.crs else 'None'}"
        )
        geometry_logger.info(f"Initial GeoDataFrame shape: {gdf.shape}")

        if not gdf.empty:
            geometry_logger.info(
                f"Initial geometry types: {gdf.geometry.geom_type.value_counts().to_dict()}"
            )
            geometry_logger.info(f"Initial bounds: {gdf.total_bounds}")

            # Sample coordinates to check if they look like lat/lon or projected
            geometry_logger.info("Sample coordinates from first 3 features:")
            for i in range(min(3, len(gdf))):
                geom = gdf.iloc[i].geometry
                try:
                    if geom.geom_type == "Point":
                        coords = list(geom.coords)[0]
                    elif geom.geom_type == "Polygon":
                        coords = list(geom.exterior.coords)[0]
                    elif geom.geom_type == "MultiPolygon":
                        # For MultiPolygon, get first coordinate of first polygon's exterior
                        coords = list(geom.geoms[0].exterior.coords)[0]
                    elif geom.geom_type in ["LineString", "MultiLineString"]:
                        coords = list(geom.coords)[0]
                    else:
                        coords = "unknown geometry type"
                    geometry_logger.info(f"  Feature {i}: {coords}")

                    # Check if coordinates look like lat/lon (should be roughly -180 to 180 for x, -90 to 90 for y)
                    if isinstance(coords, tuple) and len(coords) >= 2:
                        x, y = coords[0], coords[1]
                        looks_like_latlon = (-180 <= x <= 180) and (-90 <= y <= 90)
                        geometry_logger.info(
                            f"    Coordinates look like lat/lon: {looks_like_latlon} (x: {x}, y: {y})"
                        )
                except Exception as e:
                    geometry_logger.warning(
                        f"  Feature {i}: Error sampling coordinates: {e}"
                    )
                    coords = "error sampling coordinates"

        # If no CRS is set, assume EPSG:4326 (most ESRI services use this)
        if gdf.crs is None:
            geometry_logger.warning("No CRS detected, assuming EPSG:4326")
            gdf.set_crs("EPSG:4326", inplace=True)
            geometry_logger.info(
                f"Set CRS to EPSG:4326, new CRS: EPSG:{gdf.crs.to_epsg() if gdf.crs else 'None'}"
            )

        # Check if coordinates are in lat/lon range but labeled as a projected CRS
        # This handles the case where data comes in with lat/lon coordinates but is incorrectly labeled
        if not gdf.empty and gdf.crs and gdf.crs != "EPSG:4326":
            bounds = gdf.total_bounds
            x_in_latlon_range = -180 <= bounds[0] <= 180 and -180 <= bounds[2] <= 180
            y_in_latlon_range = -90 <= bounds[1] <= 90 and -90 <= bounds[3] <= 90

            if x_in_latlon_range and y_in_latlon_range:
                geometry_logger.warning(
                    f"Coordinates are in lat/lon range but labeled as {gdf.crs}. "
                    f"Bounds: {bounds}. Fixing CRS label to EPSG:4326."
                )
                gdf.set_crs("EPSG:4326", inplace=True, allow_override=True)
                geometry_logger.info(
                    f"Fixed CRS label to EPSG:4326, new CRS: EPSG:{gdf.crs.to_epsg() if gdf.crs else 'None'}"
                )

        # Now convert to the target CRS
        if gdf.crs and gdf.crs != input_crs:
            geometry_logger.info(
                f"Converting from EPSG:{gdf.crs.to_epsg() if gdf.crs else 'None'} to {input_crs}"
            )
            geometry_logger.info(f"Before conversion - bounds: {gdf.total_bounds}")

            # Sample coordinates before conversion
            geometry_logger.info("Sample coordinates before CRS conversion:")
            for i in range(min(3, len(gdf))):
                geom = gdf.iloc[i].geometry
                try:
                    if geom.geom_type == "Point":
                        coords = list(geom.coords)[0]
                    elif geom.geom_type == "Polygon":
                        coords = list(geom.exterior.coords)[0]
                    elif geom.geom_type == "MultiPolygon":
                        # For MultiPolygon, get first coordinate of first polygon's exterior
                        coords = list(geom.geoms[0].exterior.coords)[0]
                    elif geom.geom_type in ["LineString", "MultiLineString"]:
                        coords = list(geom.coords)[0]
                    else:
                        coords = "unknown geometry type"
                    geometry_logger.info(f"  Feature {i}: {coords}")
                except Exception as e:
                    geometry_logger.warning(
                        f"  Feature {i}: Error sampling coordinates: {e}"
                    )
                    coords = "error sampling coordinates"

            gdf = gdf.to_crs(input_crs)
            geometry_logger.info(
                f"After conversion - CRS: EPSG:{gdf.crs.to_epsg() if gdf.crs else 'None'}"
            )
            geometry_logger.info(f"After conversion - bounds: {gdf.total_bounds}")

            # Sample coordinates after conversion
            geometry_logger.info("Sample coordinates after CRS conversion:")
            for i in range(min(3, len(gdf))):
                geom = gdf.iloc[i].geometry
                try:
                    if geom.geom_type == "Point":
                        coords = list(geom.coords)[0]
                    elif geom.geom_type == "Polygon":
                        coords = list(geom.exterior.coords)[0]
                    elif geom.geom_type == "MultiPolygon":
                        # For MultiPolygon, get first coordinate of first polygon's exterior
                        coords = list(geom.geoms[0].exterior.coords)[0]
                    elif geom.geom_type in ["LineString", "MultiLineString"]:
                        coords = list(geom.coords)[0]
                    else:
                        coords = "unknown geometry type"
                    geometry_logger.info(f"  Feature {i}: {coords}")
                except Exception as e:
                    geometry_logger.warning(
                        f"  Feature {i}: Error sampling coordinates: {e}"
                    )
                    coords = "error sampling coordinates"
        else:
            geometry_logger.info(
                f"CRS already matches target ({input_crs}), no conversion needed"
            )

        if parcel_type:
            gdf["parcel_type"] = parcel_type  # Add the parcel_type column
            geometry_logger.info(f"Added parcel_type: {parcel_type}")

        gdfs.append(gdf)
        geometry_logger.info(f"Completed processing URL, final shape: {gdf.shape}")

    geometry_logger.info(f"Combining {len(gdfs)} GeoDataFrames...")
    combined_gdf = pd.concat(gdfs, ignore_index=True)
    geometry_logger.info(f"Combined GeoDataFrame shape: {combined_gdf.shape}")
    geometry_logger.info(
        f"Combined GeoDataFrame CRS: EPSG:{combined_gdf.crs.to_epsg() if combined_gdf.crs else 'None'}"
    )

    if not combined_gdf.empty:
        geometry_logger.info(
            f"Combined geometry types: {combined_gdf.geometry.geom_type.value_counts().to_dict()}"
        )
        geometry_logger.info(f"Combined bounds: {combined_gdf.total_bounds}")

    return combined_gdf


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
            get_logger("cache").info("No data to cache")
            return

        performance_logger = get_logger("performance")
        start_time = time.time()
        performance_logger.info(f"Starting cache operation for {self.name}...")

        # Save sourced data to a local parquet file in the storage/source_cache directory
        file_label = self.file_manager.generate_file_label(self.table_name)
        performance_logger.info(f"Generated file label: {file_label}")

        cache_start = time.time()
        self.file_manager.save_gdf(
            gdf, file_label, LoadType.SOURCE_CACHE, FileType.PARQUET
        )
        cache_time = time.time() - cache_start

        total_time = time.time() - start_time
        performance_logger.info(
            f"Cache operation completed in {total_time:.2f}s (save: {cache_time:.2f}s)"
        )

    def load_or_fetch(self) -> Tuple[gpd.GeoDataFrame, ValidationResult]:
        cache_logger = get_logger("cache")
        cache_logger.info(f"=== Starting load_or_fetch for: {self.name} ===")
        total_start_time = time.time()

        # Check if we should use cached data
        cache_check_start = time.time()
        use_cache = (
            not FORCE_RELOAD
            and self.file_manager.check_source_cache_file_exists(
                self.table_name, LoadType.SOURCE_CACHE
            )
        )
        cache_check_time = time.time() - cache_check_start
        cache_logger.info(f"Cache check took: {cache_check_time:.2f}s")

        if use_cache:
            cache_logger.info(f"Loading data for {self.name} from cache...")
            cache_load_start = time.time()
            gdf = self.file_manager.get_most_recent_cache(self.table_name)
            cache_load_time = time.time() - cache_load_start
            cache_logger.info(f"Cache load took: {cache_load_time:.2f}s")

            if gdf is not None:
                cache_logger.info(f"Successfully loaded from cache ({len(gdf)} rows)")
            else:
                cache_logger.info("Cache file not found, loading fresh data...")
                gdf = self._load_fresh_data()
        else:
            cache_logger.info("Loading fresh data now...")
            gdf = self._load_fresh_data()

        print(gdf.info())

        # Validation
        validation_start = time.time()
        validation_result = (
            self.validator.validate(gdf) if self.validator else ValidationResult(True)
        )
        validation_time = time.time() - validation_start
        cache_logger.info(f"Validation took: {validation_time:.2f}s")

        total_time = time.time() - total_start_time
        cache_logger.info(f"=== Completed {self.name} in {total_time:.2f}s ===")

        return gdf, validation_result

    def _load_fresh_data(self) -> gpd.GeoDataFrame:
        """Helper method to load fresh data with timing"""
        cache_logger = get_logger("cache")
        load_start = time.time()
        cache_logger.info(f"Starting load_data() for {self.name}...")

        gdf = self.load_data()

        load_time = time.time() - load_start
        cache_logger.info(
            f"load_data() completed in {load_time:.2f}s ({len(gdf)} rows)"
        )

        cache_logger.info("Caching fresh data now...")
        self.cache_data(gdf)

        return gdf

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
        performance_logger = get_logger("performance")
        performance_logger.info(f"Starting for {self.name} from {self.input}")
        start_time = time.time()

        read_start = time.time()
        gdf = gpd.read_file(self.input)
        read_time = time.time() - read_start
        performance_logger.info(
            f"gpd.read_file took {read_time:.2f}s ({len(gdf)} rows)"
        )

        normalize_start = time.time()
        gdf = self.normalize_columns(gdf, self.cols)
        normalize_time = time.time() - normalize_start
        performance_logger.info(f"normalize_columns took {normalize_time:.2f}s")

        if not gdf.crs:
            raise AttributeError("Input data doesn't have an original CRS set")

        # Add CRS detection logic similar to EsriLoader
        geometry_logger = get_logger("geometry_debug")
        geometry_logger.info(f"GdfLoader: Original CRS: {gdf.crs}")
        geometry_logger.info(f"GdfLoader: Original bounds: {gdf.total_bounds}")

        # Check if coordinates are in lat/lon range but labeled as a projected CRS
        # This handles the case where data comes in with lat/lon coordinates but is incorrectly labeled
        if not gdf.empty and gdf.crs and gdf.crs != "EPSG:4326":
            bounds = gdf.total_bounds
            x_in_latlon_range = -180 <= bounds[0] <= 180 and -180 <= bounds[2] <= 180
            y_in_latlon_range = -90 <= bounds[1] <= 90 and -90 <= bounds[3] <= 90

            if x_in_latlon_range and y_in_latlon_range:
                geometry_logger.warning(
                    f"GdfLoader: Coordinates are in lat/lon range but labeled as {gdf.crs}. "
                    f"Bounds: {bounds}. Fixing CRS label to EPSG:4326."
                )
                gdf.set_crs("EPSG:4326", inplace=True, allow_override=True)
                geometry_logger.info(
                    f"GdfLoader: Fixed CRS label to EPSG:4326, new CRS: EPSG:{gdf.crs.to_epsg() if gdf.crs else 'None'}"
                )

        crs_start = time.time()
        geometry_logger.info(f"GdfLoader: Converting from {gdf.crs} to {USE_CRS}")
        geometry_logger.info(
            f"GdfLoader: Before CRS conversion - bounds: {gdf.total_bounds}"
        )

        gdf = gdf.to_crs(USE_CRS)

        geometry_logger.info(f"GdfLoader: After CRS conversion - CRS: {gdf.crs}")
        geometry_logger.info(
            f"GdfLoader: After CRS conversion - bounds: {gdf.total_bounds}"
        )

        crs_time = time.time() - crs_start
        performance_logger.info(f"CRS conversion took {crs_time:.2f}s")

        geometry_start = time.time()
        gdf["geometry"] = gdf.geometry.make_valid()
        geometry_time = time.time() - geometry_start
        performance_logger.info(f"Geometry validation took {geometry_time:.2f}s")

        total_time = time.time() - start_time
        performance_logger.info(f"Total load_data took {total_time:.2f}s")

        return gdf


class EsriLoader(BaseLoader):
    def __init__(
        self, esri_urls: List[str], extra_query_args: dict = None, *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.esri_urls = esri_urls
        self.extra_query_args = extra_query_args

    def load_data(self):
        performance_logger = get_logger("performance")
        performance_logger.info(
            f"Starting for {self.name} with {len(self.esri_urls)} URLs"
        )
        start_time = time.time()

        esri_start = time.time()
        gdf = load_esri_data(self.esri_urls, self.input_crs, self.extra_query_args)
        esri_time = time.time() - esri_start
        performance_logger.info(
            f"load_esri_data took {esri_time:.2f}s ({len(gdf)} rows)"
        )
        geometry_logger = get_logger("geometry_debug")
        geometry_logger.info(f"After load_esri_data CRS: {gdf.crs}")

        normalize_start = time.time()
        gdf = self.normalize_columns(gdf, self.cols)
        normalize_time = time.time() - normalize_start
        performance_logger.info(f"normalize_columns took {normalize_time:.2f}s")
        geometry_logger.info(f"After normalize_columns CRS: {gdf.crs}")

        crs_start = time.time()
        geometry_logger = get_logger("geometry_debug")
        geometry_logger.info(f"Converting from {gdf.crs} to {USE_CRS}")
        geometry_logger.info(f"Before CRS conversion - bounds: {gdf.total_bounds}")
        geometry_logger.info("Before CRS conversion - sample coordinates:")
        for i in range(min(3, len(gdf))):
            geom = gdf.iloc[i].geometry
            geometry_logger.info(f"  Row {i} geometry type: {type(geom).__name__}")

            try:
                if geom.geom_type == "Point":
                    coords = list(geom.coords)[0]
                elif geom.geom_type == "Polygon":
                    coords = list(geom.exterior.coords)[0]
                elif geom.geom_type == "MultiPolygon":
                    # For MultiPolygon, get first coordinate of first polygon's exterior
                    coords = list(geom.geoms[0].exterior.coords)[0]
                elif geom.geom_type in ["LineString", "MultiLineString"]:
                    coords = list(geom.coords)[0]
                else:
                    coords = "unknown geometry type"
                geometry_logger.info(f"  Row {i}: {coords}")
            except Exception as e:
                geometry_logger.warning(f"  Row {i}: Error sampling coordinates: {e}")
                coords = "error sampling coordinates"

        # Check if coordinates are in lat/lon range but labeled as a projected CRS
        # This handles the case where data comes in with lat/lon coordinates but is incorrectly labeled
        if not gdf.empty and gdf.crs and gdf.crs != "EPSG:4326":
            bounds = gdf.total_bounds
            x_in_latlon_range = -180 <= bounds[0] <= 180 and -180 <= bounds[2] <= 180
            y_in_latlon_range = -90 <= bounds[1] <= 90 and -90 <= bounds[3] <= 90

            if x_in_latlon_range and y_in_latlon_range:
                geometry_logger.warning(
                    f"Coordinates are in lat/lon range but labeled as {gdf.crs}. "
                    f"Bounds: {bounds}. Fixing CRS label to EPSG:4326."
                )
                gdf.set_crs("EPSG:4326", inplace=True, allow_override=True)
                geometry_logger.info(
                    f"Fixed CRS label to EPSG:4326, new CRS: EPSG:{gdf.crs.to_epsg() if gdf.crs else 'None'}"
                )

        # Debug: Check if CRS conversion is actually needed
        if gdf.crs == USE_CRS:
            geometry_logger.info(f"CRS already matches {USE_CRS}, skipping conversion")
        else:
            geometry_logger.info(
                f"Performing CRS conversion from {gdf.crs} to {USE_CRS}"
            )
            gdf = gdf.to_crs(USE_CRS)
            geometry_logger.info(f"CRS conversion completed, new CRS: {gdf.crs}")

        geometry_logger.info(f"After CRS conversion - bounds: {gdf.total_bounds}")
        geometry_logger.info("After CRS conversion - sample coordinates:")
        for i in range(min(3, len(gdf))):
            geom = gdf.iloc[i].geometry
            geometry_logger.info(f"  Row {i} geometry type: {type(geom).__name__}")

            try:
                if geom.geom_type == "Point":
                    coords = list(geom.coords)[0]
                elif geom.geom_type == "Polygon":
                    coords = list(geom.exterior.coords)[0]
                elif geom.geom_type == "MultiPolygon":
                    # For MultiPolygon, get first coordinate of first polygon's exterior
                    coords = list(geom.geoms[0].exterior.coords)[0]
                elif geom.geom_type in ["LineString", "MultiLineString"]:
                    coords = list(geom.coords)[0]
                else:
                    coords = "unknown geometry type"
                geometry_logger.info(f"  Row {i}: {coords}")
            except Exception as e:
                geometry_logger.warning(f"  Row {i}: Error sampling coordinates: {e}")
                coords = "error sampling coordinates"

        crs_time = time.time() - crs_start
        performance_logger.info(f"CRS conversion took {crs_time:.2f}s")
        geometry_logger.info(f"After CRS conversion CRS: {gdf.crs}")

        opa_start = time.time()
        gdf = self.standardize_opa(gdf)
        opa_time = time.time() - opa_start
        performance_logger.info(f"OPA standardization took {opa_time:.2f}s")

        geometry_start = time.time()
        gdf["geometry"] = gdf.geometry.make_valid()
        geometry_time = time.time() - geometry_start
        performance_logger.info(f"Geometry validation took {geometry_time:.2f}s")

        total_time = time.time() - start_time
        performance_logger.info(f"Total load_data took {total_time:.2f}s")

        return gdf


class CartoLoader(BaseLoader):
    def __init__(
        self,
        carto_queries: str | List[str],
        *args,
        wkb_geom_field: str | None = "the_geom",
        **kwargs,
    ):
        # Carto data comes in EPSG:4326 (geographic coordinates)
        kwargs["input_crs"] = kwargs.get("input_crs", "EPSG:4326")
        super().__init__(*args, **kwargs)
        self.carto_queries = BaseLoader.string_to_list(carto_queries)
        self.wkb_geom_field = wkb_geom_field

    def load_data(self):
        performance_logger = get_logger("performance")
        performance_logger.info(
            f"Starting for {self.name} with {len(self.carto_queries)} queries"
        )
        start_time = time.time()

        carto_start = time.time()
        gdf = load_carto_data(self.carto_queries, self.input_crs, self.wkb_geom_field)
        carto_time = time.time() - carto_start
        performance_logger.info(
            f"load_carto_data took {carto_time:.2f}s ({len(gdf)} rows)"
        )

        normalize_start = time.time()
        gdf = self.normalize_columns(gdf, self.cols)
        normalize_time = time.time() - normalize_start
        performance_logger.info(f"normalize_columns took {normalize_time:.2f}s")

        crs_start = time.time()
        gdf = gdf.to_crs(USE_CRS)
        crs_time = time.time() - crs_start
        performance_logger.info(f"CRS conversion took {crs_time:.2f}s")

        opa_start = time.time()
        gdf = self.standardize_opa(gdf)
        opa_time = time.time() - opa_start
        performance_logger.info(f"OPA standardization took {opa_time:.2f}s")

        geometry_start = time.time()
        gdf["geometry"] = gdf.geometry.make_valid()
        geometry_time = time.time() - geometry_start
        performance_logger.info(f"Geometry validation took {geometry_time:.2f}s")

        total_time = time.time() - start_time
        performance_logger.info(f"Total load_data took {total_time:.2f}s")

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

    def _load_from_cache(self, cache_key: str) -> Optional[gpd.GeoDataFrame]:
        """
        Load data from cache if available.
        """
        cache_logger = get_logger("cache")
        cache_file = self.file_manager.get_cache_file_path(cache_key)

        if cache_file.exists():
            cache_logger.info(f"Loading from cache: {cache_file}")
            try:
                return gpd.read_parquet(cache_file)
            except Exception as e:
                cache_logger.warning(f"Failed to load cache file {cache_file}: {e}")
                return None
        else:
            cache_logger.info(f"No cache file found: {cache_file}")
            return None

    def _save_to_cache(self, data: gpd.GeoDataFrame, cache_key: str) -> None:
        """
        Save data to cache.
        """
        cache_logger = get_logger("cache")
        cache_file = self.file_manager.get_cache_file_path(cache_key)

        cache_logger.info(f"Saving to cache: {cache_file}")
        try:
            data.to_parquet(cache_file)
            cache_logger.info(f"Successfully saved to cache: {cache_file}")
        except Exception as e:
            cache_logger.error(f"Failed to save to cache {cache_file}: {e}")

    def _load_from_arcgis(self, layer_url: str) -> gpd.GeoDataFrame:
        """
        Load data from ArcGIS feature layer.
        """
        performance_logger = get_logger("performance")
        time.time()
        performance_logger.info(f"Loading from ArcGIS: {layer_url}")

        # Implementation of _load_from_arcgis method
        # This method should return a GeoDataFrame loaded from the ArcGIS feature layer
        # based on the layer_url
        # You can use the ArcGIS Python API to load the data
        # For example, you can use the arcgis.features.FeatureLayer and arcgis.gis.GIS classes
        # to load the data from the ArcGIS feature layer
        # This method should return the loaded GeoDataFrame

    def _load_from_arcgis_with_pagination(self, layer_url: str) -> gpd.GeoDataFrame:
        """
        Load data from ArcGIS feature layer with pagination for large datasets.
        """
        performance_logger = get_logger("performance")
        time.time()
        performance_logger.info(f"Loading from ArcGIS with pagination: {layer_url}")

        # Implementation of _load_from_arcgis_with_pagination method
        # This method should return a GeoDataFrame loaded from the ArcGIS feature layer
        # based on the layer_url with pagination
        # You can use the ArcGIS Python API to load the data with pagination
        # This method should return the loaded GeoDataFrame

    def _load_from_arcgis_with_chunking(
        self, layer_url: str, chunk_size: int = 1000
    ) -> gpd.GeoDataFrame:
        """
        Load data from ArcGIS feature layer with chunking for very large datasets.
        """
        performance_logger = get_logger("performance")
        time.time()
        performance_logger.info(f"Loading from ArcGIS with chunking: {layer_url}")

        # Implementation of _load_from_arcgis_with_chunking method
        # This method should return a GeoDataFrame loaded from the ArcGIS feature layer
        # based on the layer_url with chunking
        # You can use the ArcGIS Python API to load the data with chunking
        # This method should return the loaded GeoDataFrame
