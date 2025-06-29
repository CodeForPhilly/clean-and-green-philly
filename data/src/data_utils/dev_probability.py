from typing import Tuple

import geopandas as gpd
import jenkspy
import pandas as pd
import requests

from src.config.config import USE_CRS
from src.validation.base import ValidationResult

from ..classes.loaders import GdfLoader
from ..constants.services import CENSUS_BGS_URL, PERMITS_QUERY
from ..utilities import spatial_join


# @validate_output(DevProbabilityOutputValidator)
def dev_probability(
    input_gdf: gpd.GeoDataFrame,
) -> Tuple[gpd.GeoDataFrame, ValidationResult]:
    """
    Calculates development probability based on permit counts and assigns
    development ranks to census block groups. The results are joined to the
    primary feature layer.

    Args:
        primary_featurelayer (FeatureLayer): The feature layer containing property data.

    Returns:
        FeatureLayer: The input feature layer with added spatial join data for
        development probability and ranks.

    Tagline:
        Calculate development probability

    Columns Added:
        permit_count (int): The number of permits issued in the census block group.
        dev_rank (str): The development rank of the census block group.

    Primary Feature Layer Columns Referenced:
        opa_id, geometry

    Source:
        https://phl.carto.com/api/v2/sql
    """

    loader = GdfLoader(name="Census BGs", input=CENSUS_BGS_URL)
    census_bgs_gdf, census_input_validation = loader.load_or_fetch()

    base_url = "https://phl.carto.com/api/v2/sql"
    response = requests.get(f"{base_url}?q={PERMITS_QUERY}&format=GeoJSON")

    if response.status_code == 200:
        try:
            permits_gdf = gpd.GeoDataFrame.from_features(
                response.json(), crs="EPSG:4326"
            )
            print("GeoDataFrame created successfully.")
        except Exception as e:
            print(f"Failed to convert response to GeoDataFrame: {e}")
            return input_gdf, ValidationResult(True)
    else:
        truncated_response = response.content[:500]
        print(
            f"Failed to fetch permits data. HTTP status code: {response.status_code}. Response text: {truncated_response}"
        )
        return input_gdf, ValidationResult(True)

    permits_gdf = permits_gdf.to_crs(USE_CRS)

    joined_gdf = gpd.sjoin(permits_gdf, census_bgs_gdf, how="inner", predicate="within")

    permit_counts = joined_gdf.groupby("index_right").size()
    census_bgs_gdf["permit_count"] = census_bgs_gdf.index.map(permit_counts)

    # Fill NaN values with 0 and ensure integer type
    census_bgs_gdf["permit_count"] = (
        census_bgs_gdf["permit_count"].fillna(0).astype(int)
    )

    # Classify development probability using Jenks natural breaks
    # Only use non-zero permit counts for classification to avoid issues with all zeros
    non_zero_permit_counts = census_bgs_gdf["permit_count"][
        census_bgs_gdf["permit_count"] > 0
    ]

    if len(non_zero_permit_counts) > 0:
        breaks = jenkspy.jenks_breaks(non_zero_permit_counts, n_classes=3)
        # Jenks breaks with n_classes=3 creates 4 bin edges
        # We need to handle zero values separately

        # Create a custom binning that includes 0
        all_breaks = [0] + list(breaks)

        # Create dev_rank with proper handling of edge cases
        dev_rank_series = pd.cut(
            census_bgs_gdf["permit_count"],
            bins=all_breaks,
            labels=["Low", "Low", "Medium", "High"],
            include_lowest=True,
            ordered=False,  # Allow duplicate labels
        )

        # Convert to string and handle any NaN values
        census_bgs_gdf["dev_rank"] = dev_rank_series.astype(str)
        # Replace any "nan" strings with "Low" (default for zero permit counts)
        census_bgs_gdf["dev_rank"] = census_bgs_gdf["dev_rank"].replace("nan", "Low")
    else:
        # If no non-zero permit counts, assign all to "Low"
        census_bgs_gdf["dev_rank"] = "Low"

    # Ensure dev_rank only contains valid values
    valid_ranks = ["Low", "Medium", "High"]
    census_bgs_gdf["dev_rank"] = census_bgs_gdf["dev_rank"].apply(
        lambda x: "Low" if x not in valid_ranks else x
    )

    census_bgs_gdf = census_bgs_gdf[["permit_count", "dev_rank", "geometry"]]

    merged_gdf = spatial_join(input_gdf, census_bgs_gdf)

    return merged_gdf, ValidationResult(True)
