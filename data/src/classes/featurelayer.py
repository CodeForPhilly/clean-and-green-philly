import logging as log
import os
import subprocess
import traceback

import geopandas as gpd
import pandas as pd
import requests
import sqlalchemy as sa
from esridump.dumper import EsriDumper
from google.cloud import storage
from google.cloud.storage.bucket import Bucket
from shapely import Point, wkb

from config.config import (
    FORCE_RELOAD,
    USE_CRS,
    log_level,
    min_tiles_file_size_in_bytes,
    write_production_tiles_file,
)
from config.psql import conn, local_engine
from new_etl.classes.file_manager import FileManager, FileType, LoadType

log.basicConfig(level=log_level)

file_manager = FileManager()


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


class FeatureLayer:
    """
    FeatureLayer is a class to represent a GIS dataset. It can be initialized with a URL to an Esri Feature Service, a SQL query to Carto, or a GeoDataFrame.
    """

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
        bucket: Bucket = None,
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
        self.bucket = bucket or google_cloud_bucket()

        inputs = [self.esri_rest_urls, self.carto_sql_queries, self.gdf]
        non_none_inputs = [i for i in inputs if i is not None]

        if len(non_none_inputs) > 0:
            if self.esri_rest_urls is not None:
                self.type = "esri"
            elif self.carto_sql_queries is not None:
                self.type = "carto"
            elif self.gdf is not None:
                self.type = "gdf"

            if force_reload:
                self.load_data()
            else:
                psql_exists = self.check_psql()
                if not psql_exists:
                    self.load_data()
        else:
            print(f"Initialized FeatureLayer {self.name} with no data.")

    def check_psql(self):
        try:
            if not sa.inspect(local_engine).has_table(self.psql_table):
                print(f"Table {self.psql_table} does not exist")
                return False
            psql_table = gpd.read_postgis(
                f"SELECT * FROM {self.psql_table}", conn, geom_col="geometry"
            )
            if len(psql_table) == 0:
                return False
            else:
                print(f"Loading data for {self.name} from psql...")
                self.gdf = psql_table
                return True
        except Exception as e:
            print(f"Error loading data for {self.name}: {e}")
            return False

    def load_data(self):
        print(f"Loading data for {self.name} from {self.type}...")
        if self.type == "gdf":
            pass
        else:
            try:
                if self.type == "esri":
                    if self.esri_rest_urls is None:
                        raise ValueError("Must provide a URL to load data from Esri")

                    gdfs = []
                    for url in self.esri_rest_urls:
                        parcel_type = (
                            "Land"
                            if "Vacant_Indicators_Land" in url
                            else "Building"
                            if "Vacant_Indicators_Bldg" in url
                            else None
                        )
                        self.dumper = EsriDumper(url)
                        features = [feature for feature in self.dumper]

                        geojson_features = {
                            "type": "FeatureCollection",
                            "features": features,
                        }

                        this_gdf = gpd.GeoDataFrame.from_features(
                            geojson_features, crs=self.input_crs
                        )

                        # Check if 'X' and 'Y' columns exist and create geometry if necessary
                        if "X" in this_gdf.columns and "Y" in this_gdf.columns:
                            this_gdf["geometry"] = this_gdf.apply(
                                lambda row: Point(row["X"], row["Y"]), axis=1
                            )
                        elif "geometry" not in this_gdf.columns:
                            raise ValueError(
                                "No geometry information found in the data."
                            )

                        this_gdf = this_gdf.to_crs(USE_CRS)

                        # Assign the parcel_type to the GeoDataFrame
                        if parcel_type:
                            this_gdf["parcel_type"] = parcel_type

                        gdfs.append(this_gdf)

                    self.gdf = pd.concat(gdfs, ignore_index=True)

                elif self.type == "carto":
                    if self.carto_sql_queries is None:
                        raise ValueError(
                            "Must provide a SQL query to load data from Carto"
                        )

                    gdfs = []
                    for sql_query in self.carto_sql_queries:
                        response = requests.get(
                            "https://phl.carto.com/api/v2/sql", params={"q": sql_query}
                        )

                        data = response.json()["rows"]
                        df = pd.DataFrame(data)
                        geometry = (
                            wkb.loads(df[self.use_wkb_geom_field], hex=True)
                            if self.use_wkb_geom_field
                            else gpd.points_from_xy(df.x, df.y)
                        )

                        gdf = gpd.GeoDataFrame(
                            df,
                            geometry=geometry,
                            crs=self.input_crs,
                        )
                        gdf = gdf.to_crs(USE_CRS)

                        gdfs.append(gdf)
                    self.gdf = pd.concat(gdfs, ignore_index=True)

                # Drop columns
                if self.cols:
                    self.cols.append("geometry")
                    self.gdf = self.gdf[self.cols]

                # save self.gdf to psql
                # rename columns to lowercase for table creation in postgres
                if self.cols:
                    self.gdf = self.gdf.rename(
                        columns={x: x.lower() for x in self.cols}
                    )
                self.gdf.to_postgis(
                    name=self.psql_table,
                    con=conn,
                    if_exists="replace",
                    chunksize=1000,
                )
            except Exception as e:
                print(f"Error loading data for {self.name}: {e}")
                traceback.print_exc()
                self.gdf = None

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

        # Export the GeoDataFrames to a temporary GeoJSON files
        temp_geojson_points_file_name: str = f"temp_{tiles_file_id_prefix}_points"
        temp_geojson_polygons_file_name: str = f"temp_{tiles_file_id_prefix}_polygons"
        temp_parquet_file_name: str = f"{tiles_file_id_prefix}"

        # Reproject
        gdf_wm = self.gdf.to_crs(epsg=4326)
        file_manager.save_gdf(
            gdf_wm, temp_geojson_polygons_file_name, LoadType.TEMP, FileType.GEOJSON
        )
        gdf_wm.to_file(temp_geojson_polygons_file_name, driver="GeoJSON")

        # Create points dataset
        centroid_gdf = self.gdf.copy()
        centroid_gdf["geometry"] = centroid_gdf["geometry"].centroid
        centroid_gdf = centroid_gdf.to_crs(epsg=4326)
        centroid_gdf.to_file(temp_geojson_points_file_name, driver="GeoJSON")
        file_manager.save_gdf(
            centroid_gdf, temp_geojson_points_file_name, LoadType.TEMP, FileType.GEOJSON
        )

        # Drop geometry, and save as Parquet
        df_no_geom = gdf_wm.drop(columns=["geometry"])

        # Check if the DataFrame has fewer than 25,000 rows
        num_rows, num_cols = df_no_geom.shape
        if num_rows < 25000:
            print(
                f"Parquet file has {num_rows} rows, which is fewer than 25,000. Skipping upload."
            )
            return

        # Save the DataFrame as Parquet
        file_manager.save_gdf(
            df_no_geom, temp_parquet_file_name, LoadType.TEMP, FileType.PARQUET
        )

        # Upload Parquet to Google Cloud Storage
        blob_parquet = self.bucket.blob(f"{tiles_file_id_prefix}.parquet")
        temp_parquet_file_path = file_manager.get_file_path(
            temp_parquet_file_name, LoadType.TEMP, FileType.PARQUET
        )
        try:
            blob_parquet.upload_from_filename(temp_parquet_file_path)
            parquet_size = os.stat(temp_parquet_file_path).st_size
            parquet_size_mb = parquet_size / (1024 * 1024)
            print(
                f"Parquet upload successful! Size: {parquet_size} bytes ({parquet_size_mb:.2f} MB), Dimensions: {num_rows} rows, {num_cols} columns."
            )
        except Exception as e:
            print(f"Parquet upload failed: {e}")
            return

        temp_pmtiles_points_file_name: str = f"temp_{tiles_file_id_prefix}_points"
        temp_pmtiles_polygons_file_name: str = f"temp_{tiles_file_id_prefix}_polygons"
        temp_merged_pmtiles_file_name: str = f"temp_{tiles_file_id_prefix}_merged"

        temp_pmtiles_points_file_path = file_manager.get_file_path(
            temp_pmtiles_points_file_name, LoadType.TEMP, FileType.PMTILES
        )
        temp_pmtiles_polygons_file_path = file_manager.get_file_path(
            temp_pmtiles_points_file_name, LoadType.TEMP, FileType.PMTILES
        )
        temp_merged_pmtiles_file_path = file_manager.get_file_path(
            temp_pmtiles_points_file_name, LoadType.TEMP, FileType.PMTILES
        )

        temp_geojson_points_file_path = file_manager.get_file_path(
            temp_geojson_points_file_name, LoadType.TEMP, FileType.GEOJSON
        )
        temp_geojson_polygons_file_path = file_manager.get_file_path(
            temp_geojson_points_file_name, LoadType.TEMP, FileType.GEOJSON
        )

        # Command for generating PMTiles for points up to zoom level zoom_threshold
        points_command: list[str] = [
            "tippecanoe",
            f"--output={temp_pmtiles_points_file_path}",
            f"--maximum-zoom={zoom_threshold}",
            "--minimum-zoom=10",
            "-zg",
            "-aC",
            "-r0",
            temp_geojson_points_file_path,
            "-l",
            "vacant_properties_tiles_points",
            "--force",
        ]

        # Command for generating PMTiles for polygons from zoom level zoom_threshold
        polygons_command: list[str] = [
            "tippecanoe",
            f"--output={temp_pmtiles_polygons_file_path}",
            f"--minimum-zoom={zoom_threshold}",
            "--maximum-zoom=16",
            "-zg",
            "--no-tile-size-limit",
            temp_geojson_polygons_file_path,
            "-l",
            "vacant_properties_tiles_polygons",
            "--force",
        ]

        # Command for merging the two PMTiles files into a single output file
        merge_command: list[str] = [
            "tile-join",
            f"--output={temp_merged_pmtiles_file_path}",
            "--no-tile-size-limit",
            temp_pmtiles_polygons_file_path,
            temp_pmtiles_points_file_path,
            "--force",
        ]

        # Run the commands
        for command in [points_command, polygons_command, merge_command]:
            subprocess.run(command)

        write_files: list[str] = [f"{tiles_file_id_prefix}_staging.pmtiles"]

        if write_production_tiles_file:
            write_files.append(f"{tiles_file_id_prefix}.pmtiles")

        # Check whether the temp saved tiles files is big enough.
        file_size: int = os.stat(temp_merged_pmtiles_file_path).st_size
        if file_size < min_tiles_file_size_in_bytes:
            raise ValueError(
                f"{temp_merged_pmtiles_file_path} is {file_size} bytes in size but should be at least {min_tiles_file_size_in_bytes}. Therefore, we are not uploading any files to the GCP bucket. The file may be corrupt or incomplete."
            )

        # Upload PMTiles to Google Cloud Storage
        for file in write_files:
            blob = self.bucket.blob(file)
            try:
                blob.upload_from_filename(temp_merged_pmtiles_file_path)
                print(f"PMTiles upload successful for {file}!")
            except Exception as e:
                print(f"PMTiles upload failed for {file}: {e}")
