import os
import subprocess
import requests
import geopandas as gpd
import pandas as pd
from esridump.dumper import EsriDumper
import traceback
from config.config import USE_CRS, FORCE_RELOAD
from config.psql import conn
from shapely import wkb, Point
from google.cloud import storage

# Configure Google
key = os.environ["CLEAN_GREEN_GOOGLE_KEY"]
credentials_path = os.path.expanduser("/app/service-account-key.json")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
bucket_name = os.environ["GOOGLE_CLOUD_BUCKET_NAME"] if os.environ["GOOGLE_CLOUD_BUCKET_NAME"] != None else "cleanandgreenphl"
storage_client = storage.Client(project="clean-and-green-philly")
bucket = storage_client.bucket(bucket_name)


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
        cols=None,
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
            print("Initialized FeatureLayer with no data.")

    def check_psql(self):
        try:
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
                            else "Building" if "Vacant_Indicators_Bldg" in url else None
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

        # Coerce OPA_ID to integer and drop rows where OPA_ID is null or non-numeric
        self.gdf["OPA_ID"] = pd.to_numeric(self.gdf["OPA_ID"], errors="coerce")
        self.gdf = self.gdf.dropna(subset=["OPA_ID"])

    def opa_join(self, other_df, opa_column):
        """
        Join 2 dataframes based on OPA_ID and keep the 'geometry' column from the left dataframe if it exists in both.
        """

        # Coerce opa_column to integer and drop rows where opa_column is null or non-numeric
        other_df[opa_column] = pd.to_numeric(other_df[opa_column], errors="coerce")
        other_df = other_df.dropna(subset=[opa_column])

        # Coerce OPA_ID to integer and drop rows where OPA_ID is null or non-numeric
        self.gdf["OPA_ID"] = pd.to_numeric(self.gdf["OPA_ID"], errors="coerce")
        self.gdf = self.gdf.dropna(subset=["OPA_ID"])

        # Perform the merge
        joined = self.gdf.merge(
            other_df, how="left", right_on=opa_column, left_on="OPA_ID"
        )

        # Check if 'geometry' column exists in both dataframes and clean up
        if "geometry_x" in joined.columns and "geometry_y" in joined.columns:
            joined = joined.drop(columns=["geometry_y"])
            joined = joined.rename(columns={"geometry_x": "geometry"})

        if opa_column != "OPA_ID":
            joined = joined.drop(columns=[opa_column])

        self.gdf = joined
        self.rebuild_gdf()

    def rebuild_gdf(self):
        self.gdf = gpd.GeoDataFrame(self.gdf, geometry="geometry", crs=self.crs)

    def create_centroid_gdf(self):
        """
        Convert the geometry of the GeoDataFrame to centroids.
        """
        self.centroid_gdf = self.gdf.copy()
        self.centroid_gdf["geometry"] = self.gdf["geometry"].centroid

    def build_and_publish_pmtiles(self, tileset_id):
        zoom_threshold = 13

        # Export the GeoDataFrame to a temporary GeoJSON file
        temp_geojson_points = f"tmp/temp_{tileset_id}_points.geojson"
        temp_geojson_polygons = f"tmp/temp_{tileset_id}_polygons.geojson"
        temp_pmtiles_points = f"tmp/temp_{tileset_id}_points.pmtiles"
        temp_pmtiles_polygons = f"tmp/temp_{tileset_id}_polygons.pmtiles"
        temp_merged_pmtiles = f"tmp/temp_{tileset_id}_merged.pmtiles"

        # Reproject
        gdf_wm = self.gdf.to_crs(epsg=4326)
        gdf_wm.to_file(temp_geojson_polygons, driver="GeoJSON")

        # Create points dataset
        self.centroid_gdf = self.gdf.copy()
        self.centroid_gdf["geometry"] = self.centroid_gdf["geometry"].centroid
        self.centroid_gdf = self.centroid_gdf.to_crs(epsg=4326)
        self.centroid_gdf.to_file(temp_geojson_points, driver="GeoJSON")

        # Command for generating PMTiles for points up to zoom level zoom_threshold
        points_command = [
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
        polygons_command = [
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
        merge_command = [
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

        # Upload to Google Cloud Storage
        blob = bucket.blob(f"{tileset_id}_staging.pmtiles")
        blob.upload_from_filename(temp_merged_pmtiles)
