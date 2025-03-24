import io

import geopandas as gpd
import requests

from config.config import USE_CRS

from ..classes.featurelayer import FeatureLayer
from ..constants.services import PPR_PROPERTIES_TO_LOAD
from ..metadata.metadata_utils import provide_metadata


@provide_metadata()
def ppr_properties(primary_featurelayer: FeatureLayer) -> FeatureLayer:
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
        # Load PPR properties from Esri REST URLs
        ppr_properties = FeatureLayer(
            name="PPR Properties",
            esri_rest_urls=PPR_PROPERTIES_TO_LOAD,
            cols=["PUBLIC_NAME"],
        )

        if ppr_properties.gdf is None or ppr_properties.gdf.empty:
            raise ValueError(
                "PPR properties GeoDataFrame is empty or failed to load from Esri REST URL."
            )

        print("Loaded PPR properties from Esri REST URL.")

    except Exception as e:
        print(f"Error loading PPR properties from Esri REST URL: {e}")
        print("Falling back to loading from GeoJSON URL.")

        response = requests.get(fallback_url)
        response.raise_for_status()
        ppr_properties_gdf = gpd.read_file(io.BytesIO(response.content))

        ppr_properties = FeatureLayer(name="PPR Properties")
        ppr_properties.gdf = ppr_properties_gdf

    # Limit PPR properties to relevant columns and apply CRS
    ppr_properties.gdf = ppr_properties.gdf[["public_name", "geometry"]]
    ppr_properties.gdf = ppr_properties.gdf.to_crs(USE_CRS)

    # Perform a spatial join with the primary feature layer
    primary_featurelayer.spatial_join(ppr_properties)

    # Ensure the 'vacant' column exists in the primary feature layer
    if "vacant" not in primary_featurelayer.gdf.columns:
        raise ValueError(
            "The 'vacant' column is missing in the primary feature layer. Ensure it exists before running this function."
        )

    # Create a mask for rows where PPR properties are identified
    mask = primary_featurelayer.gdf["public_name"].notnull()

    # Count rows where the garden is identified and 'vacant' is currently True
    count_updated = primary_featurelayer.gdf.loc[
        mask & primary_featurelayer.gdf["vacant"]
    ].shape[0]

    # Update the 'vacant' column to False for identified PPR properties
    primary_featurelayer.gdf.loc[mask, "vacant"] = False

    # Log results
    print(
        f"Updated 'vacant' column for PPR properties. Total rows updated: {count_updated}"
    )

    # Drop the "public_name" column if it exists, as it's no longer needed
    if "public_name" in primary_featurelayer.gdf.columns:
        primary_featurelayer.gdf = primary_featurelayer.gdf.drop(
            columns=["public_name"]
        )
    else:
        print("'public_name' column is missing, cannot drop.")

    return primary_featurelayer
