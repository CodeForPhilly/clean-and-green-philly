import logging as log
import os
import subprocess
import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed

import geopandas as gpd
import pandas as pd
import requests
import sqlalchemy as sa
from google.cloud import storage
from shapely import wkb
from tqdm import tqdm

from config.config import (
    FORCE_RELOAD,
    USE_CRS,
    log_level,
    min_tiles_file_size_in_bytes,
    write_production_tiles_file,
)
from config.psql import conn, local_engine
from new_etl.classes.bucket_manager import GCSBucketManager
from new_etl.database import to_postgis_with_schema

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
        skip_save=False,
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
        self.psql_table = name.lower().replace(" ", "_")
        self.input_crs = "EPSG:4326" if not from_xy else USE_CRS
        self.use_wkb_geom_field = use_wkb_geom_field
        self.max_workers = max_workers
        self.chunk_size = chunk_size
        self.skip_save = skip_save

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
            if force_reload or not self.check_psql():
                self.load_data()
        else:
            log.info(f"Initialized FeatureLayer {self.name} with no data.")

    @classmethod
    def for_validation(
        cls, name, esri_rest_urls=None, carto_sql_queries=None, **kwargs
    ):
        """
        Create a FeatureLayer instance specifically for validation purposes.
        This instance will not save data to PostgreSQL.

        Args:
            name: Name of the feature layer
            esri_rest_urls: ESRI REST URLs to load data from
            carto_sql_queries: Carto SQL queries to load data from
            **kwargs: Additional arguments to pass to the constructor

        Returns:
            FeatureLayer: A FeatureLayer instance configured for validation
        """
        return cls(
            name=name,
            esri_rest_urls=esri_rest_urls,
            carto_sql_queries=carto_sql_queries,
            skip_save=True,
            **kwargs,
        )

    def check_psql(self):
        try:
            if not sa.inspect(local_engine).has_table(self.psql_table):
                log.debug(f"Table {self.psql_table} does not exist")
                return False

            # Get total count first
            count_query = f"SELECT COUNT(*) as count FROM {self.psql_table}"
            total_count = pd.read_sql(count_query, conn).iloc[0]["count"]

            if total_count == 0:
                return False

            log.info(f"Loading data for {self.name} from psql...")

            # Get the most recent timestamp
            latest_timestamp_query = f"""
            SELECT MAX(create_date) as latest_date 
            FROM {self.psql_table}
            """
            latest_date = pd.read_sql(latest_timestamp_query, conn).iloc[0][
                "latest_date"
            ]

            # First, let's check what columns we have
            columns_query = f"""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = '{self.psql_table}'
            ORDER BY ordinal_position
            """
            columns = pd.read_sql(columns_query, conn)
            print(f"\nTable structure for {self.psql_table}:")
            print(columns.to_string())
            print("\n")

            # Column name mappings for different tables
            column_mappings = {
                "opa_properties": {"OPA_ID": "parcel_number"},
                "vacant_properties": {"OPA_ID": "parcel_number"},
            }

            # Use a more efficient query that only selects needed columns and filters by latest timestamp
            if self.cols:
                # Map column names if needed
                mapped_cols = []
                for col in self.cols:
                    if (
                        self.psql_table in column_mappings
                        and col in column_mappings[self.psql_table]
                    ):
                        mapped_cols.append(column_mappings[self.psql_table][col])
                    else:
                        mapped_cols.append(col)

                # Filter cols to only those that exist in the table
                valid_cols = [
                    col
                    for col in mapped_cols
                    if col.lower() in [c.lower() for c in columns["column_name"]]
                ]
                if not valid_cols:
                    print(
                        f"Warning: None of the requested columns {self.cols} exist in table {self.psql_table}"
                    )
                    print("Falling back to selecting all columns")
                    query = f"""
                    SELECT *, 
                           ST_AsText(geometry) as geometry_text,
                           ST_SRID(geometry) as srid
                    FROM {self.psql_table}
                    WHERE create_date = '{latest_date}'
                    AND ST_IsValid(geometry)
                    AND NOT ST_IsEmpty(geometry)
                    """
                else:
                    cols_str = ", ".join([f'"{col}"' for col in valid_cols])
                    query = f"""
                    SELECT {cols_str}, 
                           ST_AsText(geometry) as geometry_text,
                           ST_SRID(geometry) as srid
                    FROM {self.psql_table}
                    WHERE create_date = '{latest_date}'
                    AND ST_IsValid(geometry)
                    AND NOT ST_IsEmpty(geometry)
                    """
            else:
                query = f"""
                SELECT *, 
                       ST_AsText(geometry) as geometry_text,
                       ST_SRID(geometry) as srid
                FROM {self.psql_table}
                WHERE create_date = '{latest_date}'
                AND ST_IsValid(geometry)
                AND NOT ST_IsEmpty(geometry)
                """

            print(f"\nExecuting query:\n{query}\n")

            # Debug: Get a single row to inspect
            debug_query = f"{query} LIMIT 1"
            debug_data = pd.read_sql(debug_query, conn)
            if not debug_data.empty:
                print("\nDEBUG - First row data:")
                for col in debug_data.columns:
                    if col == "geometry_text":
                        print(f"Geometry WKT: {debug_data[col].iloc[0]}")
                    else:
                        print(f"{col}: {debug_data[col].iloc[0]}")

            # Load data with optimized settings and collect all chunks
            chunks = []
            for chunk in pd.read_sql(query, conn, chunksize=10000):
                # Convert WKT to geometry
                chunk["geometry"] = gpd.GeoSeries.from_wkt(chunk["geometry_text"])
                chunk = chunk.drop(columns=["geometry_text"])
                # Set the CRS based on the SRID from the database
                if not chunk.empty and "srid" in chunk.columns:
                    chunk = gpd.GeoDataFrame(
                        chunk, geometry="geometry", crs=f"EPSG:{chunk['srid'].iloc[0]}"
                    )
                    chunk.drop(columns=["srid"], inplace=True)
                chunks.append(chunk)

            # Combine all chunks into a single GeoDataFrame
            if chunks:
                self.gdf = pd.concat(chunks, ignore_index=True)
                return True
            return False

        except Exception as e:
            log.error(f"Error loading data for {self.name}: {e}")
            return False

    def load_data(self):
        """Load data from the appropriate source."""
        if self.type == "esri":
            self._load_esri_data()
        elif self.type == "carto":
            self._load_carto_data()
        elif self.type == "gdf":
            # If gdf is provided, just ensure it's in the right CRS
            if self.gdf is not None:
                self.gdf = self.gdf.to_crs(self.crs)

        # Only save to PostgreSQL if not in validation mode
        if not self.skip_save and self.gdf is not None:
            try:
                to_postgis_with_schema(self.gdf, self.psql_table)
            except Exception as e:
                log.error(f"Error saving {self.name} to PostgreSQL: {str(e)}")
                log.error(traceback.format_exc())

    def _load_esri_data(self):
        """Load data from ESRI REST endpoints."""
        if not self.esri_rest_urls:
            raise ValueError("Must provide ESRI REST URLs to load data")

        from ..loaders import load_esri_data

        self.gdf = load_esri_data(self.esri_rest_urls, self.input_crs, self.crs)

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
            tiles_file_id_prefix (str): The ID prefix used for naming the PMTiles and Parquet files, coming from config.

        Raises:
            ValueError: Raised if the generated PMTiles file is smaller than the minimum allowed size, indicating a potential corruption or incomplete file.
        """
        zoom_threshold: int = 13

        # Export the GeoDataFrame to a temporary GeoJSON file
        temp_geojson_points: str = f"tmp/temp_{tiles_file_id_prefix}_points.geojson"
        temp_geojson_polygons: str = f"tmp/temp_{tiles_file_id_prefix}_polygons.geojson"
        temp_pmtiles_points: str = f"tmp/temp_{tiles_file_id_prefix}_points.pmtiles"
        temp_pmtiles_polygons: str = f"tmp/temp_{tiles_file_id_prefix}_polygons.pmtiles"
        temp_merged_pmtiles: str = f"tmp/temp_{tiles_file_id_prefix}_merged.pmtiles"

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
