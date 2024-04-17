import requests
import io
import zipfile
import geopandas as gpd
from classes.featurelayer import FeatureLayer
from config.config import USE_CRS


def park_priority_areas(primary_featurelayer):
    park_url = "https://www.tpl.org/sites/default/files/park-serve/downloads/park-serve-10-min-walk-buffers.zip"

    park_response = requests.get(park_url)

    with io.BytesIO(park_response.content) as f:
        with zipfile.ZipFile(f, "r") as zip_ref:
            zip_ref.extractall("tmp/")

    park_priority = gpd.read_file("tmp/park-serve-10-min-walk-buffers.shp")
    park_priority = park_priority.to_crs(USE_CRS)
    phl_park_priority = park_priority[park_priority["GEOID"].str.startswith("42101")]
    phl_park_priority = phl_park_priority[["PPRIORITY", "geometry"]]

    phl_park_priority.rename(columns={"PPRIORITY": "park_priority_area"}, inplace=True)

    park_priority_layer = FeatureLayer("Park Priority Areas")
    park_priority_layer.gdf = phl_park_priority

    primary_featurelayer.spatial_join(park_priority_layer)

    return primary_featurelayer