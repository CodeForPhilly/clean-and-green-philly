import geopandas as gpd

from ..classes.loaders import EsriLoader
from ..constants.services import COMMUNITY_GARDENS_TO_LOAD
from ..metadata.metadata_utils import provide_metadata
from ..utilities import spatial_join


@provide_metadata()
def community_gardens(input_gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
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

    loader = EsriLoader(
        name="Community Gardens",
        esri_urls=COMMUNITY_GARDENS_TO_LOAD,
        cols=["site_name"],
    )

    community_gardens = loader.load_or_fetch()

    # Convert any non-point geometries to points using centroid
    community_gardens.loc[
        community_gardens.geometry.geom_type != "Point", "geometry"
    ] = community_gardens[
        community_gardens.geometry.geom_type != "Point"
    ].geometry.centroid

    # Use 'contains' predicate since we want the parcel that contains each point
    merged_gdf = spatial_join(
        input_gdf, community_gardens, predicate="contains", how="inner"
    )

    # Get unique parcels that contain garden points
    garden_parcels = set(merged_gdf["opa_id"])

    # Update vacant status for parcels containing gardens
    mask = input_gdf["opa_id"].isin(garden_parcels)
    input_gdf.loc[mask, "vacant"] = False

    return input_gdf
