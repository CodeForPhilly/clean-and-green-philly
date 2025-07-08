import io
from typing import Tuple

import geopandas as gpd
import requests

from src.validation.base import ValidationResult, validate_output
from src.validation.ppr_properties import (
    PPRPropertiesInputValidator,
    PPRPropertiesOutputValidator,
)

from ..classes.loaders import EsriLoader, GdfLoader
from ..constants.services import PPR_PROPERTIES_TO_LOAD
from ..utilities import spatial_join


@validate_output(PPRPropertiesOutputValidator)
def ppr_properties(
    input_gdf: gpd.GeoDataFrame,
) -> Tuple[gpd.GeoDataFrame, ValidationResult]:
    """
    Updates the 'vacant' column in the primary feature layer to ensure PPR properties
    are marked as not vacant. This prevents PPR properties from being miscategorized
    as vacant.

    Args:
        primary_featurelayer (FeatureLayer): The primary feature layer to update.

    Returns:
        FeatureLayer: The updated primary feature layer.

    Columns Updated:
        vacant: Updated to False for PPR properties.

    Tagline:
        Mark Parks as Not Vacant

    Source:
        https://services.arcgis.com/fLeGjb7u4uXqeF9q/ArcGIS/rest/services/PPR_Properties/FeatureServer/0

    Known Issues:
        If the Ersi REST URL is not available the function
        will fall back to loading the data from a GeoJSON URL
        https://opendata.arcgis.com/datasets/d52445160ab14380a673e5849203eb64_0.geojson

    Primary Feature Layer Columns Referenced:
        opa_id, geometry, vacant, public_name
    """
    fallback_url = "https://opendata.arcgis.com/datasets/d52445160ab14380a673e5849203eb64_0.geojson"

    try:
        loader = EsriLoader(
            name="PPR Properties",
            esri_urls=PPR_PROPERTIES_TO_LOAD,
            cols=["public_name"],
        )

        ppr_properties, input_validation = loader.load_or_fetch()

        if ppr_properties is None or ppr_properties.empty:
            raise ValueError(
                "PPR properties GeoDataFrame is empty or failed to load from Esri REST URL."
            )

        print("Loaded PPR properties from Esri REST URL.")

    except Exception as e:
        print(f"Error loading PPR properties from Esri REST URL: {e}")
        print("Falling back to loading from GeoJSON URL.")

        response = requests.get(fallback_url)
        response.raise_for_status()

        loader = GdfLoader(
            input=io.BytesIO(response.content),
            name="PPR Properties",
            cols=["public_name"],
            validator=PPRPropertiesInputValidator(),
        )
        ppr_properties, input_validation = loader.load_or_fetch()

    # Perform a spatial join with the primary feature layer
    merged_gdf = spatial_join(input_gdf, ppr_properties)

    # Remove duplicate OPA IDs in the main dataset after spatial join
    before_dedup = len(merged_gdf)
    merged_gdf = merged_gdf.drop_duplicates(subset=["opa_id"], keep="first")
    after_dedup = len(merged_gdf)
    if before_dedup != after_dedup:
        print(
            f"Removed {before_dedup - after_dedup} duplicate OPA IDs from main dataset after spatial join"
        )
        print(f"Main dataset after deduplication: {len(merged_gdf)} records")

    # Ensure the 'vacant' column exists in the primary feature layer
    if "vacant" not in merged_gdf.columns:
        raise ValueError(
            "The 'vacant' column is missing in the primary feature layer. Ensure it exists before running this function."
        )

    # Create a mask for rows where PPR properties are identified
    mask = merged_gdf["public_name"].notnull()

    # Count rows where the garden is identified and 'vacant' is currently True
    count_updated = merged_gdf.loc[mask & merged_gdf["vacant"]].shape[0]

    # Update the 'vacant' column to False for identified PPR properties
    merged_gdf.loc[mask, "vacant"] = False

    # Log results
    print(
        f"Updated 'vacant' column for PPR properties. Total rows updated: {count_updated}"
    )

    # Drop the "public_name" column if it exists, as it's no longer needed
    if "public_name" in merged_gdf.columns:
        merged_gdf = merged_gdf.drop(columns=["public_name"])
    else:
        print("'public_name' column is missing, cannot drop.")

    return merged_gdf, input_validation
