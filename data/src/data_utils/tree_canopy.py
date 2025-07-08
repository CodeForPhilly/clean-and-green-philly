import io
import os
import zipfile
from typing import Tuple

import geopandas as gpd
import requests

from src.classes.file_manager import FileManager, LoadType
from src.validation.base import ValidationResult, validate_output
from src.validation.tree_canopy import TreeCanopyOutputValidator

from ..classes.loaders import GdfLoader
from ..utilities import spatial_join

file_manager = FileManager()


@validate_output(TreeCanopyOutputValidator)
def tree_canopy(
    input_gdf: gpd.GeoDataFrame,
) -> Tuple[gpd.GeoDataFrame, ValidationResult]:
    """
    Adds tree canopy gap information to the input GeoDataFrame by downloading,
    processing, and spatially joining tree canopy data for Philadelphia County.

    Args:
        input_gdf (GeoDataFrame): The GeoDataFrame containing property data.

    Returns:
        GeoDataFrame: The input GeoDataFrame with an added "tree_canopy_gap" column
        indicating the tree canopy gap for each property.

    Tagline:
        Measures tree canopy gaps.

    Columns added:
        tree_canopy_gap (float): The amount of tree canopy lacking.

    Columns Referenced:
        opa_id, geometry

    Source:
        https://national-tes-data-share.s3.amazonaws.com/national_tes_share/pa.zip.zip
    """
    tree_url = (
        "https://national-tes-data-share.s3.amazonaws.com/national_tes_share/pa.zip.zip"
    )

    print(f"[TREE_CANOPY] FileManager temp directory: {file_manager.temp_directory}")
    print(f"[TREE_CANOPY] Current working directory: {os.getcwd()}")

    # Check if pa.shp already exists
    shapefile_file_path = file_manager.get_file_path(
        file_name="pa.shp", load_type=LoadType.TEMP
    )
    print(f"[TREE_CANOPY] Expected shapefile path: {shapefile_file_path}")
    print(f"[TREE_CANOPY] Shapefile exists: {os.path.exists(shapefile_file_path)}")

    # List contents of temp directory before extraction
    print("[TREE_CANOPY] Contents of temp directory before extraction:")
    if os.path.exists(file_manager.temp_directory):
        for file in os.listdir(file_manager.temp_directory):
            print(f"  - {file}")
    else:
        print("  Temp directory does not exist!")

    # Download and extract tree canopy data
    print(f"[TREE_CANOPY] Downloading from: {tree_url}")
    tree_response = requests.get(tree_url)
    print(
        f"[TREE_CANOPY] Download completed, content length: {len(tree_response.content)}"
    )

    with io.BytesIO(tree_response.content) as f:
        with zipfile.ZipFile(f, "r") as zip_ref:
            print("[TREE_CANOPY] Zip file contents:")
            for file_info in zip_ref.filelist:
                print(f"  - {file_info.filename}")
            print(f"[TREE_CANOPY] Extracting to: {file_manager.temp_directory}")
            zip_ref.extractall(file_manager.temp_directory)

    # List contents of temp directory after extraction
    print("[TREE_CANOPY] Contents of temp directory after extraction:")
    if os.path.exists(file_manager.temp_directory):
        for file in os.listdir(file_manager.temp_directory):
            print(f"  - {file}")
    else:
        print("  Temp directory does not exist!")

    # Check if pa.shp exists after extraction
    print(
        f"[TREE_CANOPY] Shapefile exists after extraction: {os.path.exists(shapefile_file_path)}"
    )

    # Load and process the tree canopy shapefile
    loader = GdfLoader(
        name="Tree Canopy", input=shapefile_file_path, cols=["county", "tc_gap"]
    )
    pa_trees, input_validation = loader.load_or_fetch()

    phl_trees = pa_trees[pa_trees["county"] == "Philadelphia County"]

    # Rename column to match intended output
    phl_trees.rename(columns={"tc_gap": "tree_canopy_gap"}, inplace=True)

    # Perform spatial join
    merged_gdf = spatial_join(input_gdf, phl_trees)

    # Remove duplicate OPA IDs in the main dataset after spatial join
    before_dedup = len(merged_gdf)
    merged_gdf = merged_gdf.drop_duplicates(subset=["opa_id"], keep="first")
    after_dedup = len(merged_gdf)
    if before_dedup != after_dedup:
        print(
            f"Removed {before_dedup - after_dedup} duplicate OPA IDs from main dataset after spatial join"
        )
        print(f"Main dataset after deduplication: {len(merged_gdf)} records")

    return merged_gdf, input_validation
