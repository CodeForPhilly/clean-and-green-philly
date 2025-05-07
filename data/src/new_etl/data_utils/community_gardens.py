import geopandas as gpd

from config.config import USE_CRS

from ..classes.featurelayer import FeatureLayer
from ..constants.services import COMMUNITY_GARDENS_TO_LOAD
from ..metadata.metadata_utils import provide_metadata


def check_community_gardens_gdf(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """
    Validates the community gardens GeoDataFrame by transforming all non-point geoemtries to their centroids and doing other naming transformations.

    Args:
        gdf (gpd.GeoDataFrame): The input GeoDataFrame containing community gardens data.

    Returns:
        gpd.GeoDataFrame: The transformed GeoDataFrame with only point geometries and relevant columns.
    """

    # Ensure both layers are in the same CRS
    if gdf.crs != USE_CRS:
        print(f"Transforming community gardens from {gdf.crs} to {USE_CRS}")
        gdf = gdf.to_crs(USE_CRS)

    # Identify problematic gardens
    geom_types = gdf.geometry.geom_type.value_counts()

    if len(geom_types) > 1:
        # Convert any non-point geometries to points using centroid
        gdf.loc[gdf.geometry.geom_type != "Point", "geometry"] = gdf[
            gdf.geometry.geom_type != "Point"
        ].geometry.centroid

    # Verify all geometries are now points
    if not all(gdf.geometry.geom_type == "Point"):
        raise ValueError("Failed to convert all geometries to points")

    # Limit the community gardens data to relevant columns
    gdf = gdf[["site_name", "geometry"]]

    print(f"\nTotal community gardens: {len(gdf)}")

    return gdf


def merge_and_update_with_community_gardens_gdf(
    primary_featurelayer_gdf: gpd.GeoDataFrame, community_gardens_gdf: gpd.GeoDataFrame
) -> gpd.GeoDataFrame:
    """
    Merges the community gardens GeoDataFrame with the primary feature layer GeoDataFrame and performs and masking update.

    Args:
        primary_featurelayer_gdf (gpd.GeoDataFrame): The primary feature layer GeoDataFrame.
        community_gardens_gdf (gpd.GeoDataFrame): The community gardens GeoDataFrame.

    Returns:
        gpd.GeoDataFrame: The updated, masked primary feature layer GeoDataFrame.
    """
    # Use 'contains' predicate since we want the parcel that contains each point
    joined_gdf = primary_featurelayer_gdf.sjoin(
        community_gardens_gdf, predicate="contains", how="inner"
    )

    # Get unique parcels that contain garden points
    garden_parcels = set(joined_gdf["opa_id"])
    print(f"\nUnique parcels containing gardens: {len(garden_parcels)}")

    if len(garden_parcels) > len(community_gardens_gdf):
        print(
            "\nWARNING: More matching parcels than gardens. This suggests possible data issues."
        )

    # Update vacant status for parcels containing gardens
    mask = primary_featurelayer_gdf["opa_id"].isin(garden_parcels)
    primary_featurelayer_gdf.loc[mask, "vacant"] = False

    print(f"\nTotal parcels updated: {mask.sum()}")

    return primary_featurelayer_gdf


@provide_metadata()
def community_gardens(primary_featurelayer: FeatureLayer) -> FeatureLayer:
    """
    Updates the 'vacant' column in the primary feature layer to ensure community gardens
    are marked as not vacant. This protects known community gardens from being categorized
    as vacant, preventing potential predatory development.

    Args:
        primary_featurelayer (FeatureLayer): The feature layer containing property data.

    Returns:
        FeatureLayer: The input feature layer with the 'vacant' column updated to False
        for parcels containing community gardens.

    Tagline:
        Mark Community Gardens as Not Vacant

    Columns updated:
        vacant: Updated to False for parcels containing community gardens.

    Primary Feature Layer Columns Referenced:
        opa_id, vacant

    Source:
        https://services2.arcgis.com/qjOOiLCYeUtwT7x7/arcgis/rest/services/PHS_NGT_Supported_Current_view/FeatureServer/0/
    """
    if "vacant" not in primary_featurelayer.gdf.columns:
        raise ValueError("The 'vacant' column is missing in the primary feature layer.")

    # Load community gardens
    community_gardens = FeatureLayer(
        name="Community Gardens", esri_rest_urls=COMMUNITY_GARDENS_TO_LOAD
    )

    transformed_gdf = check_community_gardens_gdf(community_gardens.gdf)
    community_gardens.gdf = transformed_gdf

    updated_primary_featurelayer_gdf = merge_and_update_with_community_gardens_gdf(
        primary_featurelayer.gdf, community_gardens.gdf
    )
    primary_featurelayer.gdf = updated_primary_featurelayer_gdf

    return primary_featurelayer
