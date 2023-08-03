import requests
import geopandas as gpd
import pandas as pd
import datetime
from esridump.dumper import EsriDumper


# Set the CRS to use for all layers
use_crs = "EPSG:2272"


class FeatureLayer:
    """
    FeatureLayer is a class to represent a GIS dataset. It can be initialized with a URL to an Esri Feature Service, a SQL query to Carto, or a GeoDataFrame.
    """

    def __init__(
        self, name, esri_rest_urls=None, carto_sql_queries=None, gdf=None, crs=use_crs
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

        inputs = [self.esri_rest_urls, self.carto_sql_queries, self.gdf]
        non_none_inputs = [i for i in inputs if i is not None]

        if len(non_none_inputs) != 1:
            raise ValueError(
                "Exactly one of esri_rest_urls, carto_sql_queries, or gdf must be provided."
            )

        if self.esri_rest_urls is not None:
            self.type = "esri"
        elif self.carto_sql_queries is not None:
            self.type = "carto"
        elif self.gdf is not None:
            self.type = "gdf"

        self.load_data()

    def load_data(self):
        print(f"Loading data for {self.name}...")
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
                        gdfs.append(
                            gpd.GeoDataFrame.from_features(
                                geojson_features, crs=self.crs
                            )
                        )

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
                            df, geometry=gpd.points_from_xy(df.x, df.y), crs=self.crs
                        )

                        gdfs.append(gdf)
                    self.gdf = pd.concat(gdfs, ignore_index=True)

            except Exception as e:
                print(f"Error loading data for {self.name}: {e}")
                self.gdf = None

    def spatial_join(self, other_layer, how="left", predicate="intersects"):
        """
        Spatial joins in this script are generally left intersect joins.
        They also can create duplicates, so we drop duplicates after the join.
        Note: We may want to revisit the duplicates.
        """
        self.gdf = gpd.sjoin(self.gdf, other_layer.gdf, how=how, predicate=predicate)
        self.gdf.drop(columns=["index_right"], inplace=True)
        self.gdf.drop_duplicates(inplace=True)


"""
Load Vacant Properties Datasets
"""

vacant_props_layers_to_load = [
    "https://services.arcgis.com/fLeGjb7u4uXqeF9q/ArcGIS/rest/services/Vacant_Indicators_Land/FeatureServer/0/",
    "https://services.arcgis.com/fLeGjb7u4uXqeF9q/ArcGIS/rest/services/Vacant_Indicators_Bldg/FeatureServer/0/",
]


vacant_properties = FeatureLayer(
    name="Vacant Properties", esri_rest_urls=vacant_props_layers_to_load
)


"""
Load City Owned Properties
"""
city_owned_properties = FeatureLayer(
    name="City Owned Properties",
    esri_rest_urls="https://services.arcgis.com/fLeGjb7u4uXqeF9q/ArcGIS/rest/services/LAMAAssets/FeatureServer/0/",
)

# Discover which vacant properties are city owned using a spatial join
vacant_properties.spatial_join(city_owned_properties)

# There are some matches which aren't valid because of imprecise parcel boundaries. Use a match on OPA_ID and OPABRT to remove these.
vacant_properties.gdf = vacant_properties.gdf.loc[
    ~(
        (vacant_properties.gdf["OPABRT"].notnull())
        & (vacant_properties.gdf["OPA_ID"] != vacant_properties.gdf["OPABRT"])
    )
]

# Note: This removes some entries from the dataset, need to revisit this


"""
Load PHS Data
"""

phs_layers_to_load = [
    "https://services.arcgis.com/fLeGjb7u4uXqeF9q/ArcGIS/rest/services/PHS_CommunityLandcare/FeatureServer/0/",
    "https://services.arcgis.com/fLeGjb7u4uXqeF9q/ArcGIS/rest/services/PHS_PhilaLandCare_Maintenance/FeatureServer/0/",
]

phs_properties = FeatureLayer(name="PHS Properties", esri_rest_urls=phs_layers_to_load)

phs_properties.gdf["COMM_PARTN"] = "PHS"
phs_properties.gdf = phs_properties.gdf[["COMM_PARTN", "geometry"]]

vacant_properties.spatial_join(phs_properties)
vacant_properties.gdf["COMM_PARTN"].fillna("None", inplace=True)
