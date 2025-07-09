import logging as log
import os
import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed

import geopandas as gpd
import pandas as pd
import requests
from google.cloud import storage
from shapely import wkb
from tqdm import tqdm

from src.classes.bucket_manager import GCSBucketManager
from src.classes.file_manager import FileManager, FileType, LoadType
from src.classes.loaders import generate_pmtiles
from src.config.config import (
    FORCE_RELOAD,
    USE_CRS,
    log_level,
)
from src.loaders import load_carto_data, load_esri_data

log.basicConfig(level=log_level)


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


class FeatureLayer:
    def __init__(
        self,
        name,
        esri_rest_urls=None,
        carto_sql_queries=None,
        gdf=None,
        crs=USE_CRS,
        force_reload=FORCE_RELOAD,
        from_xy=False,
        use_wkb_geom_field=None,
        cols: list[str] = None,
        max_workers=os.cpu_count(),
        chunk_size=100000,
        collected_metadata=None,
    ):
        if collected_metadata is None:
            self.collected_metadata = []
        else:
            self.collected_metadata = collected_metadata
        self.name = name
        self.esri_rest_urls = (
            [esri_rest_urls] if isinstance(esri_rest_urls, str) else esri_rest_urls
        )
        self.carto_sql_queries = (
            [carto_sql_queries]
            if isinstance(carto_sql_queries, str)
            else carto_sql_queries
        )
        self.gdf = gdf
        self.crs = crs
        self.cols = cols
        self.table_name = name.lower().replace(" ", "_")
        self.input_crs = "EPSG:4326" if not from_xy else USE_CRS
        self.use_wkb_geom_field = use_wkb_geom_field
        self.max_workers = max_workers
        self.chunk_size = chunk_size
        self.file_manager = FileManager()

        inputs = [self.esri_rest_urls, self.carto_sql_queries, self.gdf]
        non_none_inputs = [i for i in inputs if i is not None]
        if len(non_none_inputs) > 0:
            self.type = (
                "esri"
                if self.esri_rest_urls
                else "carto"
                if self.carto_sql_queries
                else "gdf"
            )
            if not force_reload and self.file_manager.check_source_cache_file_exists(
                self.table_name, LoadType.SOURCE_CACHE
            ):
                log.info(f"Loading data for {self.name} from cache...")
                print(f"Loading data for {self.name} from cache...")
                self.gdf = self.file_manager.get_most_recent_cache(self.table_name)
            else:
                print("Loading data now...")
                self.load_data()
                print("Caching data now...")
                self.cache_data()
        else:
            log.info(f"Initialized FeatureLayer {self.name} with no data.")

    def load_data(self):
        log.info(f"Loading data for {self.name} from {self.type}...")

        if self.type == "gdf":
            return  # Skip processing for gdf type

        try:
            # Load data based on the source type
            if self.type == "esri":
                self.gdf = load_esri_data(self.esri_rest_urls, self.input_crs, self.crs)
            elif self.type == "carto":
                self.gdf = load_carto_data(
                    self.carto_sql_queries,
                    self.max_workers,
                    self.chunk_size,
                    self.use_wkb_geom_field,
                    self.input_crs,
                    self.crs,
                )

            # Standardize column names
            if not self.gdf.empty:
                self.gdf.columns = [col.lower() for col in self.gdf.columns]

                # Filter columns if specified
                if self.cols:
                    self.cols = [col.lower() for col in self.cols]
                    self.cols.append("geometry")
                    self.gdf = self.gdf[
                        [col for col in self.cols if col in self.gdf.columns]
                    ]

        except Exception as e:
            log.error(f"Error loading data for {self.name}: {e}")
            traceback.print_exc()
            self.gdf = gpd.GeoDataFrame()  # Reset to an empty GeoDataFrame

    def cache_data(self):
        log.info(f"Caching data for {self.name} to local file system...")

        if self.gdf is None and self.gdf.empty:
            log.info("No data to cache.")
            return

        # Save sourced data to a local parquet file in the storage/source_cache directory
        file_label = self.file_manager.generate_file_label(self.table_name)
        self.file_manager.save_gdf(
            self.gdf, file_label, LoadType.SOURCE_CACHE, FileType.PARQUET
        )

    def _load_carto_data(self):
        if not self.carto_sql_queries:
            raise ValueError("Must provide SQL query to load data from Carto")
        gdfs = []
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = []
            for query in self.carto_sql_queries:
                total_rows = self._get_carto_total_rows(query)
                for offset in range(0, total_rows, self.chunk_size):
                    futures.append(
                        executor.submit(
                            self._fetch_carto_chunk, query, offset, self.chunk_size
                        )
                    )
            for future in tqdm(
                as_completed(futures),
                total=len(futures),
                desc="Processing Carto chunks",
            ):
                try:
                    gdfs.append(future.result())
                except Exception as e:
                    log.error(f"Error processing Carto chunk: {e}")
        self.gdf = pd.concat(gdfs, ignore_index=True)

    def _fetch_carto_chunk(self, query, offset, chunk_size):
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
            wkb.loads(df[self.use_wkb_geom_field], hex=True)
            if self.use_wkb_geom_field
            else gpd.points_from_xy(df.x, df.y)
        )
        return gpd.GeoDataFrame(df, geometry=geometry, crs=self.input_crs).to_crs(
            self.crs
        )

    def _get_carto_total_rows(self, query):
        count_query = f"SELECT COUNT(*) as count FROM ({query}) as subquery"
        response = requests.get(
            "https://phl.carto.com/api/v2/sql", params={"q": count_query}
        )
        response.raise_for_status()
        return response.json()["rows"][0]["count"]

    def spatial_join(self, other_layer, how="left", predicate="intersects"):
        """
        Spatial joins in this script are generally left intersect joins.
        They also can create duplicates, so we drop duplicates after the join.
        Note: We may want to revisit the duplicates.
        """

        # If other_layer.gdf isn't a geodataframe, try to make it one
        if not isinstance(other_layer.gdf, gpd.GeoDataFrame):
            try:
                other_layer.rebuild_gdf()

            except Exception as e:
                print(f"Error converting other_layer to GeoDataFrame: {e}")
                return

        self.gdf = gpd.sjoin(self.gdf, other_layer.gdf, how=how, predicate=predicate)
        self.gdf.drop(columns=["index_right"], inplace=True)
        self.gdf.drop_duplicates(inplace=True)

        # Coerce opa_id to integer and drop rows where opa_id is null or non-numeric
        self.gdf.loc[:, "opa_id"] = pd.to_numeric(self.gdf["opa_id"], errors="coerce")
        self.gdf = self.gdf.dropna(subset=["opa_id"])

    def opa_join(self, other_df, opa_column):
        """
        Join 2 dataframes based on opa_id and keep the 'geometry' column from the left dataframe if it exists in both.
        """

        # Coerce opa_column to integer and drop rows where opa_column is null or non-numeric
        other_df.loc[:, opa_column] = pd.to_numeric(
            other_df[opa_column], errors="coerce"
        )
        other_df = other_df.dropna(subset=[opa_column])

        # Coerce opa_id to integer and drop rows where opa_id is null or non-numeric
        self.gdf.loc[:, "opa_id"] = pd.to_numeric(self.gdf["opa_id"], errors="coerce")
        self.gdf = self.gdf.dropna(subset=["opa_id"])

        # Perform the merge
        joined = self.gdf.merge(
            other_df, how="left", right_on=opa_column, left_on="opa_id"
        )

        # Check if 'geometry' column exists in both dataframes and clean up
        if "geometry_x" in joined.columns and "geometry_y" in joined.columns:
            joined = joined.drop(columns=["geometry_y"]).copy()  # Ensure a full copy
            joined = joined.rename(columns={"geometry_x": "geometry"})

        if opa_column != "opa_id":
            joined = joined.drop(columns=[opa_column])

        # Assign the joined DataFrame to self.gdf as a full copy
        self.gdf = joined.copy()
        self.rebuild_gdf()

    def rebuild_gdf(self):
        self.gdf = gpd.GeoDataFrame(self.gdf, geometry="geometry", crs=self.crs)

    def create_centroid_gdf(self):
        """
        Convert the geometry of the GeoDataFrame to centroids.
        """
        self.centroid_gdf = self.gdf.copy()
        self.centroid_gdf.loc[:, "geometry"] = self.gdf["geometry"].centroid

    def build_and_publish(self, tiles_file_id_prefix: str) -> None:
        """
        Builds PMTiles and a Parquet file from a GeoDataFrame and publishes them to Google Cloud Storage.

        Args:
            tiles_file_id_prefix (str): The ID prefix used for naming the PMTiles and Parquet files, coming from src.config.

        Raises:
            ValueError: Raised if the generated PMTiles file is smaller than the minimum allowed size, indicating a potential corruption or incomplete file.
        """
        generate_pmtiles(self.gdf, tiles_file_id_prefix)
