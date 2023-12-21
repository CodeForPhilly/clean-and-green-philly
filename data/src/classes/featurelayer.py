import requests
import json
import geopandas as gpd
import pandas as pd
from esridump.dumper import EsriDumper
import traceback
from config.config import USE_CRS, FORCE_RELOAD, MAPBOX_TOKEN
from config.psql import local_conn
from mapbox import Uploader
from shapely import wkb


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
    ):
        self.name = name
        self.esri_rest_urls = (
            [esri_rest_urls] if isinstance(
                esri_rest_urls, str) else esri_rest_urls
        )
        self.carto_sql_queries = (
            [carto_sql_queries]
            if isinstance(carto_sql_queries, str)
            else carto_sql_queries
        )
        self.gdf = gdf
        self.crs = crs
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
                f"SELECT * FROM {self.psql_table}", local_conn, geom_col="geometry"
            )
            if len(psql_table) == 0:
                return False
            else:
                print(f"Loading data for {self.name} from psql...")
                self.gdf = psql_table
                return True
        except:
            return False

    def load_data(self):
        print(f"Loading data for {self.name} from {self.type}...")
        if self.type == "gdf":
            self.gdf = gdf
        else:
            try:
                if self.type == "esri":
                    if self.esri_rest_urls is None:
                        raise ValueError("Must provide a URL to load data from Esri")

                    gdfs = []
                    for url in self.esri_rest_urls:
                        parcel_type = "Land" if "Vacant_Indicators_Land" in url else "Building" if "Vacant_Indicators_Bldg" in url else None
                        self.dumper = EsriDumper(url)
                        features = [feature for feature in self.dumper]

                        geojson_features = {
                            "type": "FeatureCollection",
                            "features": features,
                        }

                        this_gdf = gpd.GeoDataFrame.from_features(
                            geojson_features, crs=self.input_crs
                        )
                        this_gdf = this_gdf.to_crs(USE_CRS)
                        
                        # Assign the parcel_type to the GeoDataFrame
                        if parcel_type:
                            this_gdf['parcel_type'] = parcel_type

                        gdfs.append(this_gdf)

                    self.gdf = pd.concat(gdfs, ignore_index=True)

                elif self.type == "carto":
                    if self.carto_sql_queries is None:
                        raise ValueError("Must provide a SQL query to load data from Carto")

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

                # save self.gdf to psql
                self.gdf.to_postgis(
                    name=self.psql_table, con=local_conn, if_exists="replace", chunksize=1000
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

            except:
                raise ValueError(
                    "other_layer.gdf must be a GeoDataFrame or a DataFrame with x and y columns."
                )

        self.gdf = gpd.sjoin(self.gdf, other_layer.gdf,
                             how=how, predicate=predicate)
        self.gdf.drop(columns=["index_right"], inplace=True)
        self.gdf.drop_duplicates(inplace=True)

    def rebuild_gdf(self):
        self.gdf = gpd.GeoDataFrame(
            self.gdf, geometry="geometry", crs=self.crs)

    def upload_to_mapbox(self, tileset_id):
        """Upload GeoDataFrame to Mapbox as Tileset."""

        # Initialize Mapbox Uploader
        uploader = Uploader()
        uploader.session.params.update(access_token=MAPBOX_TOKEN)

        # Reproject
        self.gdf_wm = self.gdf.to_crs(epsg=4326)

        # Convert to GeoJSON
        geojson_data = json.loads(self.gdf_wm.to_json())

        # Save to a temporary file
        with open("tmp/temp.geojson", "w") as f:
            json.dump(geojson_data, f)

        # Stage the data on S3
        print("Beginning Mapbox upload.")
        s3_url = uploader.stage(open("tmp/temp.geojson", "rb"))

        # Create Tileset
        response = uploader.create(s3_url, tileset_id)
        print("Uploaded gdf tileset to Mapbox.")

        return response

    def drop_columns(self):
        """
        Method to clean up the database by dropping columns that are not needed.
        Ideally we'll do this in each data_utils file, but for now we'll do it here.
        """
        columns = [
            "OBJECTID_left",
            "Shape__Area_left",
            "Shape__Length_left",
            "OBJECTID_right",
            "Shape__Area_right",
            "Shape__Length_right",
            "MAPREG_1",
            "shape_leng",
            "shape_area",
            "cartodb_id",
            "created_at",
            "updated_at",
            "name",
            "listname",
            "PIN",
            "MAPREG_1",
            "LOCATION",
        ]

        self.gdf.drop(columns=columns, inplace=True)
