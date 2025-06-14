from typing import Tuple

import geopandas as gpd

from src.validation.base import ValidationResult, validate_output
from src.validation.negligent_devs import NegligentDevsOutputValidator


@validate_output(NegligentDevsOutputValidator)
def negligent_devs(
    input_gdf: gpd.GeoDataFrame,
) -> Tuple[gpd.GeoDataFrame, ValidationResult]:
    """
    Identifies negligent developers based on the number of vacant properties owned
    and flags them in the primary feature layer.

    Args:
        primary_featurelayer (FeatureLayer): The feature layer containing property data.

    Columns Added:
        negligent_dev (bool): non-city owned entities owning 5+ vacant properties
        n_total_properties_owned (int): Total number of properties owned by the developer
        n_vacant_properties_owned (int): Number of vacant properties owned by the developer

    Primary Feature Layer Columns Referenced:
        opa_id, vacant, city_owner_agency, standardized_address

    Tagline:
        Identify negligent developers

    Returns:
        FeatureLayer: The input feature layer with additional columns for total properties
        owned, vacant properties owned, and a "negligent_dev" flag.
    """
    # Count total properties and vacant properties by standardized_address
    property_counts = (
        input_gdf.groupby("standardized_address")
        .agg(
            n_total_properties_owned=("opa_id", "size"),
            n_vacant_properties_owned=("vacant", "sum"),
        )
        .reset_index()
    )

    # Merge the property counts back to the main DataFrame
    input_gdf = input_gdf.merge(property_counts, on="standardized_address", how="left")

    # Identify negligent developers: non-city owned entities owning 5+ vacant properties
    input_gdf["negligent_dev"] = (input_gdf["n_vacant_properties_owned"] >= 5) & (
        input_gdf["city_owner_agency"].isna() | (input_gdf["city_owner_agency"] == "")
    )

    return input_gdf
