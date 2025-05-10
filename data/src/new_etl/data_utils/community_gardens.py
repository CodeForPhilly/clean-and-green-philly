from config.config import USE_CRS

from ..classes.featurelayer import FeatureLayer
from ..constants.services import COMMUNITY_GARDENS_TO_LOAD
from ..metadata.metadata_utils import provide_metadata


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
    # Load community gardens
    community_gardens = FeatureLayer(
        name="Community Gardens", esri_rest_urls=COMMUNITY_GARDENS_TO_LOAD
    )

    # Ensure both layers are in the same CRS
    if community_gardens.gdf.crs != USE_CRS:
        community_gardens.gdf = community_gardens.gdf.to_crs(USE_CRS)

    # Convert any non-point geometries to points using centroid
    community_gardens.gdf.loc[
        community_gardens.gdf.geometry.geom_type != "Point", "geometry"
    ] = community_gardens.gdf[
        community_gardens.gdf.geometry.geom_type != "Point"
    ].geometry.centroid

    # Limit the community gardens data to relevant columns
    community_gardens.gdf = community_gardens.gdf[["site_name", "geometry"]]

    # Use 'contains' predicate since we want the parcel that contains each point
    joined_gdf = primary_featurelayer.gdf.sjoin(
        community_gardens.gdf, predicate="contains", how="inner"
    )

    # Get unique parcels that contain garden points
    garden_parcels = set(joined_gdf["opa_id"])

    # Update vacant status for parcels containing gardens
    mask = primary_featurelayer.gdf["opa_id"].isin(garden_parcels)
    primary_featurelayer.gdf.loc[mask, "vacant"] = False

    return primary_featurelayer
