import time
from typing import Tuple

import geopandas as gpd

from src.metadata.metadata_utils import current_metadata, provide_metadata
from src.validation.base import ValidationResult, validate_output
from src.validation.park_priority import ParkPriorityOutputValidator

from ..classes.loaders import EsriLoader
from ..constants.services import PARK_PRIORITY_AREAS_URBAN_PHL
from ..utilities import spatial_join


def _park_priority_logic(
    input_gdf: gpd.GeoDataFrame,
) -> Tuple[gpd.GeoDataFrame, ValidationResult]:
    """
    Core business logic for park priority processing.

    This function contains the actual logic for:
    - Loading park priority data from ESRI
    - Renaming columns
    - Performing spatial joins
    - Returning results

    This function can be tested independently without the validation decorator.

    Args:
        input_gdf (gpd.GeoDataFrame): The input GeoDataFrame containing property data.

    Returns:
        Tuple[gpd.GeoDataFrame, ValidationResult]: The input GeoDataFrame with park
        priority data joined and the validation result.
    """
    start_time = time.time()
    print(f"Starting park_priority function at {time.strftime('%H:%M:%S')}")

    # Initialize the ESRI loader with Pennsylvania filter
    loader_start = time.time()
    print("Initializing EsriLoader for Park Priority Areas...")

    loader = EsriLoader(
        name="Park Priority Areas - Philadelphia",
        esri_urls=PARK_PRIORITY_AREAS_URBAN_PHL,
        cols=["id", "parkneed", "rg_abbrev"],  # Include rg_abbrev for filtering
        extra_query_args={"where": "rg_abbrev = 'PA'"},
    )

    loader_init_time = time.time() - loader_start
    print(f"EsriLoader initialization took {loader_init_time:.2f}s")

    # Load or fetch the park priority data
    load_start = time.time()
    print("Loading park priority data from ESRI FeatureServer...")

    park_priority_gdf, input_validation = loader.load_or_fetch()

    load_time = time.time() - load_start
    print(f"Data loading took {load_time:.2f}s")
    print(f"Loaded {len(park_priority_gdf)} park priority areas")

    # Log data quality information
    if not park_priority_gdf.empty:
        print(f"Columns in park priority data: {list(park_priority_gdf.columns)}")
        print(f"CRS: {park_priority_gdf.crs}")
        print(
            f"Geometry types: {park_priority_gdf.geometry.geom_type.value_counts().to_dict()}"
        )

        # Check for null values in key columns
        null_counts = park_priority_gdf[["parkneed", "id"]].isnull().sum()
        print(f"Null values in key columns: {null_counts.to_dict()}")

    # Rename columns as needed
    rename_start = time.time()
    if "parkneed" in park_priority_gdf.columns:
        park_priority_gdf.rename(columns={"parkneed": "park_priority"}, inplace=True)
        print("Renamed 'parkneed' column to 'park_priority'")

    rename_time = time.time() - rename_start
    print(f"Column renaming took {rename_time:.2f}s")

    # Perform spatial join
    join_start = time.time()
    print("Performing spatial join between input data and park priority areas...")

    merged_gdf = spatial_join(input_gdf, park_priority_gdf)

    join_time = time.time() - join_start
    print(f"Spatial join took {join_time:.2f}s")

    # Deduplicate by OPA ID to keep only the first occurrence
    merged_gdf = merged_gdf.drop_duplicates(subset=["opa_id"], keep="first")
    print(f"After OPA ID deduplication: {len(merged_gdf)} properties")

    # Log join results
    if "park_priority" in merged_gdf.columns:
        matched_count = merged_gdf["park_priority"].notna().sum()
        total_count = len(merged_gdf)
        match_rate = (matched_count / total_count) * 100 if total_count > 0 else 0
        print(
            f"Spatial join results: {matched_count}/{total_count} properties matched ({match_rate:.1f}%)"
        )

        if matched_count > 0:
            priority_stats = merged_gdf["park_priority"].describe()
            print(
                f"Park priority statistics: min={priority_stats['min']:.2f}, max={priority_stats['max']:.2f}, mean={priority_stats['mean']:.2f}"
            )

    total_time = time.time() - start_time
    print(f"Total park_priority function execution time: {total_time:.2f}s")
    print(f"Function completed at {time.strftime('%H:%M:%S')}")

    return merged_gdf, input_validation


@validate_output(ParkPriorityOutputValidator)
@provide_metadata(current_metadata=current_metadata)
def park_priority(
    input_gdf: gpd.GeoDataFrame,
) -> Tuple[gpd.GeoDataFrame, ValidationResult]:
    """
    Associates properties with park priority areas for Philadelphia using TPL's FeatureServer.

    This function loads park priority data from TPL's ESRI FeatureServer and performs
    a spatial join with the input GeoDataFrame to associate properties with their
    park priority scores.

    Args:
        input_gdf (gpd.GeoDataFrame): The input GeoDataFrame containing property data.

    Returns:
        Tuple[gpd.GeoDataFrame, ValidationResult]: The input GeoDataFrame with park
        priority data joined and the validation result.

    Tagline:
        Labels high-priority park areas.

    Columns Added:
        park_priority (float): The park priority score from TPL's analysis.

    Columns referenced:
        opa_id, geometry

    Source:
        https://server7.tplgis.org/arcgis7/rest/services/ParkServe/ParkServe_ProdNew/FeatureServer/6/
    """
    return _park_priority_logic(input_gdf)
