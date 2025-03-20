import pandas as pd

from ..classes.featurelayer import FeatureLayer
from ..constants.services import RCOS_LAYERS_TO_LOAD
from ..metadata.metadata_utils import provide_metadata

pd.set_option("future.no_silent_downcasting", True)


@provide_metadata()
def rco_geoms(primary_featurelayer: FeatureLayer) -> FeatureLayer:
    """
    Adds Registered Community Organization (RCO) information to the primary feature layer
    by performing a spatial join and aggregating RCO data.

    Args:
        primary_featurelayer (FeatureLayer): The feature layer containing property data.

    Returns:
        FeatureLayer: The input feature layer with added RCO-related columns,
        including aggregated RCO information and names.

    Tagline:
        Assigns Community Org Info

    Columns added:
        rco_names (str): Names of RCOs associated with the property.
        rco_info (str): Additional RCO-related information.

    Source:
        "https://services.arcgis.com/fLeGjb7u4uXqeF9q/ArcGIS/rest/services/Zoning_RCO/FeatureServer/0/"

    Notes:
        Modifies various columns. Fillna and infer_objects is applied to most columns.

    Primary Feature Layer Columns Referenced:
        opa_id, geometry
    """
    rco_geoms = FeatureLayer(name="RCOs", esri_rest_urls=RCOS_LAYERS_TO_LOAD)

    rco_aggregate_cols = [
        "organization_name",
        "organization_address",
        "primary_email",
        "primary_phone",
    ]

    rco_use_cols = ["rco_info", "rco_names", "geometry"]

    # Aggregate RCO information into a single column
    rco_geoms.gdf["rco_info"] = rco_geoms.gdf[rco_aggregate_cols].apply(
        lambda x: "; ".join(map(str, x)), axis=1
    )

    rco_geoms.gdf["rco_names"] = rco_geoms.gdf["organization_name"]

    rco_geoms.gdf = rco_geoms.gdf[rco_use_cols].copy()
    rco_geoms.rebuild_gdf()

    # Perform spatial join
    primary_featurelayer.spatial_join(rco_geoms)

    group_columns = [
        col for col in primary_featurelayer.gdf.columns if col not in rco_use_cols
    ]

    # Ensure columns are appropriately filled and cast
    for col in group_columns:
        primary_featurelayer.gdf[col] = (
            primary_featurelayer.gdf[col].fillna("").infer_objects(copy=False)
        )

    # Group by non-RCO columns and aggregate RCO data
    primary_featurelayer.gdf = (
        primary_featurelayer.gdf.groupby(group_columns)
        .agg(
            {
                "rco_info": lambda x: "|".join(map(str, x)),
                "rco_names": lambda x: "|".join(map(str, x)),
                "geometry": "first",
            }
        )
        .reset_index()
    )

    primary_featurelayer.gdf.drop_duplicates(inplace=True)
    primary_featurelayer.rebuild_gdf()

    return primary_featurelayer
