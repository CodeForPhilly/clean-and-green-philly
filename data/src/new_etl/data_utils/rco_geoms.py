import geopandas as gpd
import pandas as pd

from new_etl.utilities import spatial_join

from ..classes.loaders import EsriLoader
from ..constants.services import RCOS_LAYERS_TO_LOAD
from ..metadata.metadata_utils import provide_metadata

pd.set_option("future.no_silent_downcasting", True)


@provide_metadata()
def rco_geoms(input_gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
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
    loader = EsriLoader(name="RCOs", esri_urls=RCOS_LAYERS_TO_LOAD)
    rco_geoms = loader.load_or_fetch()

    rco_aggregate_cols = [
        "organization_name",
        "organization_address",
        "primary_email",
        "primary_phone",
    ]

    rco_use_cols = ["rco_info", "rco_names", "geometry"]

    # Aggregate RCO information into a single column
    rco_geoms["rco_info"] = rco_geoms[rco_aggregate_cols].apply(
        lambda x: "; ".join(map(str, x)), axis=1
    )

    rco_geoms["rco_names"] = rco_geoms["organization_name"]

    rco_geoms = rco_geoms[rco_use_cols].copy()

    # Perform spatial join
    merged_gdf = spatial_join(input_gdf, rco_geoms)

    group_columns = [col for col in merged_gdf.columns if col not in rco_use_cols]

    # Ensure columns are appropriately filled and cast
    for col in group_columns:
        merged_gdf[col] = merged_gdf[col].fillna("").infer_objects(copy=False)

    # Group by non-RCO columns and aggregate RCO data
    merged_gdf = (
        merged_gdf.groupby(group_columns)
        .agg(
            {
                "rco_info": lambda x: "|".join(map(str, x)),
                "rco_names": lambda x: "|".join(map(str, x)),
                "geometry": "first",
            }
        )
        .reset_index()
    )

    merged_gdf = gpd.GeoDataFrame(merged_gdf, geometry="geometry", crs=input_gdf.crs)
    merged_gdf.drop_duplicates(inplace=True)

    return merged_gdf
