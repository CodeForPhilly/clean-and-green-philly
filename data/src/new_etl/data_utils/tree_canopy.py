import io
import zipfile

import geopandas as gpd
import requests

from config.config import USE_CRS
from new_etl.classes.file_manager import FileManager
from new_etl.utilities import spatial_join

from ..classes.featurelayer import FeatureLayer
from ..metadata.metadata_utils import provide_metadata

file_manager = FileManager.get_instance()


@provide_metadata()
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
    # loader = GdfLoader(url=)
    pa_trees = gpd.read_file("storage/temp/pa.shp")
    pa_trees = pa_trees.to_crs(USE_CRS)
    phl_trees = pa_trees[pa_trees["county"] == "Philadelphia County"]
    phl_trees = phl_trees[["tc_gap", "geometry"]]

    # Rename column to match intended output
    phl_trees.rename(columns={"tc_gap": "tree_canopy_gap"}, inplace=True)

    # Create a FeatureLayer for tree canopy data
    tree_canopy = FeatureLayer("Tree Canopy")
    tree_canopy.gdf = phl_trees

    # Perform spatial join
    merged_gdf = spatial_join(input_gdf, tree_canopy)

    return merged_gdf
