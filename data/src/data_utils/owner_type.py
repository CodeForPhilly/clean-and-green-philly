from typing import Tuple

import geopandas as gpd
import pandas as pd

from src.validation.base import ValidationResult, validate_output
from src.validation.owner_type import OwnerTypeOutputValidator


@validate_output(OwnerTypeOutputValidator)
def owner_type(
    input_gdf: gpd.GeoDataFrame,
) -> Tuple[gpd.GeoDataFrame, ValidationResult]:
    """
    Determines the ownership type for each property in the input GeoDataFrame based on
    the 'owner_1', 'owner_2', 'city_owner_agency', and 'standardized_mailing_address' columns.
    The ownership type is set as:
    - "Public" if 'city_owner_agency' is not NA or if the mailing address matches specific
      public agency addresses (PA Dept of Transportation, Commonwealth of PA, Amtrak, PennDOT).
    - "Nonprofit/Civic" if the owner names match specific nonprofit organizations or contain
      "civic" or "CDC" patterns.
    - "Business (LLC)" if 'city_owner_agency' is NA, not nonprofit/civic, and "LLC" is found
      in 'owner_1' or 'owner_2'.
    - "Individual" if none of the above conditions are met.

    Args:
        input_gdf (GeoDataFrame): The GeoDataFrame containing property ownership data.

    Returns:
        GeoDataFrame: The updated GeoDataFrame with the 'owner_type' column added.

    Tagline:
        Assigns ownership types

    Columns added:
        owner_type (str): The ownership type of the property: Public, Nonprofit/Civic,
                         Business (LLC), or Individual.

    Columns Referenced:
        opa_id, owner_1, owner_2, city_owner_agency, standardized_mailing_address
    """
    owner_types = []

    for _, row in input_gdf.iterrows():
        # Extract owner1, owner2, and city_owner_agency
        owner1 = str(row["owner_1"]).lower()
        owner2 = str(row["owner_2"]).lower()
        city_owner_agency = row["city_owner_agency"]
        standardized_mailing_address = str(
            row.get("standardized_mailing_address", "")
        ).lower()

        # Determine ownership type based on the conditions
        if pd.notna(city_owner_agency):
            owner_types.append("Public")
        elif (
            "po box 3362, harrisburg pa, 17105"
            in standardized_mailing_address  # PA Dept of Transportation
            or "7000 geerdes blvd" in standardized_mailing_address  # Commonwealth of PA
            or "400 n capitol st nw, washington dc, 20001"
            in standardized_mailing_address  # Amtrak
            or "200 n radnor chester rd, st davids pa, 19087"
            in standardized_mailing_address  # PennDOT
        ):
            owner_types.append("Public")
        elif (
            "new kensington cdc" in owner1  # New Kensington CDC
            or (
                "strawberry mansion" in owner1 and "citizens council" in owner2
            )  # Strawberry Mansion Citizens Council
            or "habitat for humanity" in owner1  # Habitat for Humanity
            or "norris square civic assoc" in owner1  # Norris Square Civic Association
            or (
                "neighborhood gardens asso" in owner1
                or "neighborhood gardens trust" in owner1
            )  # Neighborhood Gardens Association/Trust
            or "east parkside community r" in owner1  # East Parkside Community
            or "civic" in owner1
            or "civic" in owner2  # Generic civic organizations
            or "cdc" in owner1
            or "cdc" in owner2  # Generic CDC organizations
        ):
            owner_types.append("Nonprofit/Civic")
        elif " llc" in owner1 or " llc" in owner2:
            owner_types.append("Business (LLC)")
        else:
            owner_types.append("Individual")

    # Add the 'owner_type' column to the GeoDataFrame
    input_gdf["owner_type"] = owner_types

    return input_gdf, ValidationResult(True)
