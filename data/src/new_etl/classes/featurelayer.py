import logging as log
import os
import subprocess
import traceback

import geopandas as gpd
import pandas as pd
import requests
import sqlalchemy as sa
from config.config import (
    FORCE_RELOAD,
    USE_CRS,
    log_level,
    min_tiles_file_size_in_bytes,
    write_production_tiles_file,
)
from config.psql import conn, local_engine
from esridump.dumper import EsriDumper
from google.cloud import storage
from google.cloud.storage.bucket import Bucket
from shapely import wkb
from sqlalchemy.sql import text
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm


log.basicConfig(level=log_level)


def google_cloud_bucket() -> Bucket:
    """Build the google cloud bucket with name configured in your environ or default of cleanandgreenphl

    Returns:
        Bucket: the gcp bucket
    """
    credentials_path = os.path.expanduser("/app/service-account-key.json")

    if not os.path.exists(credentials_path):
        raise FileNotFoundError(f"Credentials file not found at {credentials_path}")

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
    bucket_name = os.getenv("GOOGLE_CLOUD_BUCKET_NAME", "cleanandgreenphl")
    project_name = os.getenv("GOOGLE_CLOUD_PROJECT", "clean-and-green-philly")

    storage_client = storage.Client(project=project_name)
    return storage_client.bucket(bucket_name)


bucket = google_cloud_bucket()


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
    ):
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

    def check_psql(self):
        try:
            if not sa.inspect(local_engine).has_table(self.psql_table):
                log.debug(f"Table {self.psql_table} does not exist")
                return False
            psql_table = gpd.read_postgis(
                f"SELECT * FROM {self.psql_table}", conn, geom_col="geometry"
            )
            if len(psql_table) == 0:
                return False
            log.info(f"Loading data for {self.name} from psql...")
            self.gdf = psql_table
            return True
        except Exception as e:
            log.error(f"Error loading data for {self.name}: {e}")
            return False

    def load_data(self):
        log.info(f"Loading data for {self.name} from {self.type}...")

        if self.type == "gdf":
            return  # Skip processing for gdf type

        try:
            if self.type == "esri":
                if not self.esri_rest_urls:
                    raise ValueError("Must provide a URL to load data from Esri")
                gdfs = []
                for url in self.esri_rest_urls:
                    print(f"Processing URL: {url}")

                    # Use EsriDumper to get features
                    dumper = EsriDumper(url)
                    features = [feature for feature in dumper]
                    if not features:
                        log.error(f"No features returned for URL: {url}")
                        continue

                    geojson_features = {
                        "type": "FeatureCollection",
                        "features": features,
                    }
                    gdf = gpd.GeoDataFrame.from_features(
                        geojson_features, crs=self.input_crs
                    )
                    gdf = gdf.to_crs(self.crs)

                    # Add parcel_type based on the URL
                    if "Vacant_Indicators_Land" in url:
                        gdf["parcel_type"] = "Land"
                    elif "Vacant_Indicators_Bldg" in url:
                        gdf["parcel_type"] = "Building"

                    gdfs.append(gdf)

                # Concatenate all dataframes
                self.gdf = pd.concat(gdfs, ignore_index=True)

            elif self.type == "carto":
                self._load_carto_data()

            # Convert all column names to lowercase
            if not self.gdf.empty:
                self.gdf.columns = [col.lower() for col in self.gdf.columns]

                # Drop columns not in self.cols, if specified
                if self.cols:
                    self.cols = [col.lower() for col in self.cols]
                    self.cols.append("geometry")
                    self.gdf = self.gdf[
                        [col for col in self.cols if col in self.gdf.columns]
                    ]

                # Save GeoDataFrame to PostgreSQL
                self.gdf.to_postgis(
                    name=self.psql_table,
                    con=conn,
                    if_exists="replace",  # Replace the table if it already exists
                    chunksize=1000,
                )

                # Ensure the `create_date` column exists
                conn.execute(
                    text(f"""
                    DO $$
                    BEGIN
                    IF NOT EXISTS (
                        SELECT 1
                        FROM information_schema.columns
                        WHERE table_name = '{self.psql_table}' AND column_name = 'create_date'
                    ) THEN
                    ALTER TABLE {self.psql_table}
                    ADD COLUMN create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
                    END IF;
                    END $$;
                    """)
                )

                # Convert the table to a hypertable
                try:
                    conn.execute(
                        text(f"""
                        SELECT create_hypertable('{self.psql_table}', 'create_date', migrate_data => true);
                        """)
                    )
                    print(
                        f"Table {self.psql_table} successfully converted to a hypertable."
                    )
                except Exception as e:
                    if "already a hypertable" in str(e):
                        print(f"Table {self.psql_table} is already a hypertable.")
                    else:
                        raise

                # Set chunk interval to 1 month
                try:
                    conn.execute(
                        text(f"""
                        SELECT set_chunk_time_interval('{self.psql_table}', INTERVAL '1 month');
                        """)
                    )
                    print(
                        f"Chunk time interval set to 1 month for table {self.psql_table}."
                    )
                except Exception as e:
                    print(
                        f"Error setting chunk interval for table {self.psql_table}: {e}"
                    )

                # Enable compression on the hypertable
                try:
                    conn.execute(
                        text(f"""
                        ALTER TABLE {self.psql_table} SET (
                            timescaledb.compress
                        );
                        """)
                    )
                    print(f"Compression enabled on table {self.psql_table}.")
                except Exception as e:
                    print(f"Error enabling compression on table {self.psql_table}: {e}")

                # Add compression policy for chunks older than 3 months
                try:
                    conn.execute(
                        text(f"""
                        SELECT add_compression_policy('{self.psql_table}', INTERVAL '3 months');
                        """)
                    )
                    print(
                        f"Compression policy added for chunks older than 3 months on table {self.psql_table}."
                    )
                except Exception as e:
                    print(
                        f"Error adding compression policy for table {self.psql_table}: {e}"
                    )

                # Commit the transaction
                conn.commit()

        except Exception as e:
            log.error(f"Error loading data for {self.name}: {e}")
            traceback.print_exc()
            conn.rollback()  # Rollback the transaction in case of failure
            self.gdf = gpd.GeoDataFrame()

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

        # Upload PMTiles to Google Cloud Storage
        for file in write_files:
            blob = bucket.blob(file)
            try:
                blob.upload_from_filename(temp_merged_pmtiles)
                print(f"PMTiles upload successful for {file}!")
            except Exception as e:
                print(f"PMTiles upload failed for {file}: {e}")
