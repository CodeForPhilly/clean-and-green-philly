from typing import Tuple

import geopandas as gpd
import pandas as pd

from src.validation.base import ValidationResult, validate_output
from src.validation.owner_type import OwnerTypeOutputValidator

from ..metadata.metadata_utils import provide_metadata


@provide_metadata()
@validate_output(OwnerTypeOutputValidator)
def owner_type(
    input_gdf: gpd.GeoDataFrame,
) -> Tuple[gpd.GeoDataFrame, ValidationResult]:
    """
    Determines the ownership type for each property in the primary feature layer based on
    the 'owner_1', 'owner_2', and 'city_owner_agency' columns. The ownership type is set as:
    - "Public" if 'city_owner_agency' is not NA.
    - "Business (LLC)" if 'city_owner_agency' is NA and "LLC" is found in 'owner_1' or 'owner_2'.
    - "Individual" if 'city_owner_agency' is NA and "LLC" is not found in 'owner_1' or 'owner_2'.

    Args:
        primary_featurelayer (FeatureLayer): The feature layer containing property ownership data.

    Returns:
        FeatureLayer: The updated feature layer with the 'owner_type' column added.

    Tagline:
        Assigns ownership types

    Columns added:
        owner_type (str): The ownership type of the property: Public, Business (LLC) or Individual.

    Primary Feature Layer Columns Referenced:
        opa_id, owner_1, owner_2, city_owner_agency
    """
    owner_types = []

    for _, row in input_gdf.iterrows():
        # Extract owner1, owner2, and city_owner_agency
        owner1 = str(row["owner_1"]).lower()
        owner2 = str(row["owner_2"]).lower()
        city_owner_agency = row["city_owner_agency"]

        # Determine ownership type based on the conditions
        if pd.notna(city_owner_agency):
            owner_types.append("Public")
        elif " llc" in owner1 or " llc" in owner2:
            owner_types.append("Business (LLC)")
        else:
            owner_types.append("Individual")

    # Add the 'owner_type' column to the GeoDataFrame
    input_gdf["owner_type"] = owner_types

    return input_gdf, ValidationResult(True)
