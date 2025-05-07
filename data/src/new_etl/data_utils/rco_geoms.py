from typing import List
import pandas as pd
import geopandas as gpd

from ..classes.featurelayer import FeatureLayer
from ..constants.services import RCOS_LAYERS_TO_LOAD
from ..metadata.metadata_utils import provide_metadata

pd.set_option("future.no_silent_downcasting", True)


def transform_rco_geoms_gdf(
    rco_geoms_gdf: gpd.GeoDataFrame,
    aggregate_columns: List[str],
    output_columns: List[str],
) -> gpd.GeoDataFrame:
    # Aggregate RCO information into a single column
    rco_geoms_gdf["rco_info"] = rco_geoms_gdf[aggregate_columns].apply(
        lambda x: "; ".join(map(str, x)), axis=1
    )

    rco_geoms_gdf.rename(columns={"organization_name": "rco_names"}, inplace=True)
    rco_geoms_gdf = rco_geoms_gdf[output_columns].copy()

    return rco_geoms_gdf


def transform_merged_rco_geoms_gdf(
    primary_featurelayer_gdf: gpd.GeoDataFrame, rco_columns: List[str]
) -> gpd.GeoDataFrame:
    group_columns = [
        col for col in primary_featurelayer_gdf.columns if col not in rco_columns
    ]

    # Ensure columns are appropriately filled and cast
    for col in group_columns:
        primary_featurelayer_gdf[col] = (
            primary_featurelayer_gdf[col].fillna("").infer_objects(copy=False)
        )

    # Group by non-RCO columns and aggregate RCO data
    transformed_gdf = (
        primary_featurelayer_gdf.groupby(group_columns)
        .agg(
            {
                "rco_info": lambda x: "|".join(map(str, x)),
                "rco_names": lambda x: "|".join(map(str, x)),
                "geometry": "first",
            }
        )
        .reset_index()
    )

    transformed_gdf.drop_duplicates(inplace=True)

    return transformed_gdf


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

    rco_geoms_gdf = transform_rco_geoms_gdf(
        rco_geoms.gdf, rco_aggregate_cols, rco_use_cols
    )
    rco_geoms.gdf = rco_geoms_gdf
    rco_geoms.rebuild_gdf()

    # Perform spatial join
    primary_featurelayer.spatial_join(rco_geoms)

    transformed_gdf = transform_merged_rco_geoms_gdf(
        primary_featurelayer.gdf, rco_use_cols
    )
    primary_featurelayer.gdf = transformed_gdf
    primary_featurelayer.rebuild_gdf()

    return primary_featurelayer
