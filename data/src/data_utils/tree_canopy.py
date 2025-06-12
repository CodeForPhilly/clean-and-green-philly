import io
import zipfile

import geopandas as gpd
import requests

from src.classes.file_manager import FileManager, LoadType

from ..classes.loaders import GdfLoader
from ..utilities import spatial_join

file_manager = FileManager()


def tree_canopy(input_gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """
    Adds tree canopy gap information to the primary feature layer by downloading,
    processing, and spatially joining tree canopy data for Philadelphia County.

    Args:
        primary_featurelayer (FeatureLayer): The feature layer containing property data.

    Returns:
        FeatureLayer: The input feature layer with an added "tree_canopy_gap" column
        indicating the tree canopy gap for each property.

    Tagline:
        Measures tree canopy gaps.

    Columns added:
        tree_canopy_gap (float): The amount of tree canopy lacking.

    Primary Feature Layer Columns Referenced:
        opa_id, geometry

    Source:
        https://national-tes-data-share.s3.amazonaws.com/national_tes_share/pa.zip.zip
    """
    tree_url = (
        "https://national-tes-data-share.s3.amazonaws.com/national_tes_share/pa.zip.zip"
    )

    # Download and extract tree canopy data
    tree_response = requests.get(tree_url)

    with io.BytesIO(tree_response.content) as f:
        with zipfile.ZipFile(f, "r") as zip_ref:
            zip_ref.extractall("storage/temp")

    # Load and process the tree canopy shapefile
    shapefile_file_path = file_manager.get_file_path(
        file_name="pa.shp", load_type=LoadType.TEMP
    )
    loader = GdfLoader(
        name="Tree Canopy", input=shapefile_file_path, cols=["county", "tc_gap"]
    )
    pa_trees = loader.load_or_fetch()

    phl_trees = pa_trees[pa_trees["county"] == "Philadelphia County"]

    # Rename column to match intended output
    phl_trees.rename(columns={"tc_gap": "tree_canopy_gap"}, inplace=True)

    # Perform spatial join
    merged_gdf = spatial_join(input_gdf, phl_trees)

    return merged_gdf
