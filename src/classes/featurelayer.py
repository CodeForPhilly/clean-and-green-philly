import requests
import geopandas as gpd
import pandas as pd
from esridump.dumper import EsriDumper
import traceback
from config.config import USE_CRS, FORCE_RELOAD
from config.psql import conn


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
        self.psql_table = name.lower().replace(" ", "_")
        self.input_crs = "EPSG:4326" if not from_xy else USE_CRS

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

                        gdf = gpd.GeoDataFrame(
                            df,
                            geometry=gpd.points_from_xy(df.x, df.y),
                            crs=self.input_crs,
                        )
                        gdf = gdf.to_crs(USE_CRS)

                        gdfs.append(gdf)
                    self.gdf = pd.concat(gdfs, ignore_index=True)

                # save self.gdf to psql
                self.gdf.to_postgis(
                    name=self.psql_table, con=conn, if_exists="replace", chunksize=1000
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
                print(other_layer.gdf)
                raise ValueError(
                    "other_layer.gdf must be a GeoDataFrame or a DataFrame with x and y columns."
                )

        self.gdf = gpd.sjoin(self.gdf, other_layer.gdf, how=how, predicate=predicate)
        self.gdf.drop(columns=["index_right"], inplace=True)
        self.gdf.drop_duplicates(inplace=True)

    def rebuild_gdf(self):
        self.gdf = gpd.GeoDataFrame(self.gdf, geometry="geometry")
