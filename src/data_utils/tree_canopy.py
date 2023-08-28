import requests
import io
import zipfile
import geopandas as gpd
from classes.featurelayer import FeatureLayer
from config.config import USE_CRS


def tree_canopy(primary_featurelayer):
    tree_url = (
        "https://national-tes-data-share.s3.amazonaws.com/national_tes_share/pa.zip.zip"
    )

    tree_response = requests.get(tree_url)

    with io.BytesIO(tree_response.content) as f:
        with zipfile.ZipFile(f, "r") as zip_ref:
            zip_ref.extractall("tmp/")

    pa_trees = gpd.read_file("tmp/pa.shp")
    pa_trees = pa_trees.to_crs(USE_CRS)
    phl_trees = pa_trees[pa_trees["county"] == "Philadelphia County"]
    phl_trees = phl_trees[["tc_gap", "geometry"]]

    phl_trees.rename(columns={"tc_gap": "tree_canopy_gap"}, inplace=True)

    tree_canopy = FeatureLayer("Tree Canopy")
    tree_canopy.gdf = phl_trees

    primary_featurelayer.spatial_join(tree_canopy)

    return primary_featurelayer
