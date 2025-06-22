import logging
from typing import Tuple

import geopandas as gpd
import pandas as pd

from src.validation.base import ValidationResult, validate_output
from src.validation.rco_geoms import RCOGeomsOutputValidator

from ..classes.loaders import EsriLoader
from ..constants.services import RCOS_LAYERS_TO_LOAD
from ..utilities import spatial_join

pd.set_option("future.no_silent_downcasting", True)

logger = logging.getLogger(__name__)


@validate_output(RCOGeomsOutputValidator)
def rco_geoms(input_gdf: gpd.GeoDataFrame) -> Tuple[gpd.GeoDataFrame, ValidationResult]:
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
    rco_geoms, input_validation = loader.load_or_fetch()

    logger.debug(f"RCO data loaded: {len(rco_geoms)} RCO records")
    logger.debug(f"RCO columns: {list(rco_geoms.columns)}")
    logger.debug(
        f"RCO geometry types: {rco_geoms.geometry.type.value_counts().to_dict()}"
    )
    logger.debug(f"RCO CRS from loader: {rco_geoms.crs}")
    logger.debug(f"Input data CRS: {input_gdf.crs}")
    logger.debug(f"CRS match: {rco_geoms.crs == input_gdf.crs}")

    # Check actual coordinate values to see if they're really in the expected CRS
    logger.debug(f"RCO geometry bounds: {rco_geoms.total_bounds}")
    logger.debug(f"Input geometry bounds: {input_gdf.total_bounds}")

    # The bounds show the issue: RCO data is in lat/lon but labeled as EPSG:2272
    # RCO bounds: [-75.2803068  39.8674719 -74.9557486  40.1379348] (lat/lon)
    # Input bounds: [2660587.10094233  206332.40609299 2750109.66795983  304914.37510319] (EPSG:2272)

    # Fix the CRS issue - RCO data is actually in lat/lon but labeled as EPSG:2272
    if rco_geoms.total_bounds[0] < -180 or rco_geoms.total_bounds[0] > 180:
        logger.debug("RCO data appears to be in correct CRS (EPSG:2272)")
    else:
        logger.debug(
            "RCO data appears to be in lat/lon but labeled as EPSG:2272 - fixing CRS"
        )
        # Set the correct CRS to lat/lon, then transform to EPSG:2272
        rco_geoms = rco_geoms.set_crs(epsg=4326, inplace=False)
        rco_geoms = rco_geoms.to_crs(epsg=2272)
        logger.debug(
            f"RCO data transformed to EPSG:2272, new bounds: {rco_geoms.total_bounds}"
        )

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

    logger.debug(f"RCO data after processing: {len(rco_geoms)} records")
    logger.debug(f"Sample RCO names: {rco_geoms['rco_names'].head().tolist()}")

    # Perform spatial join
    merged_gdf = spatial_join(input_gdf, rco_geoms)

    logger.debug(f"After spatial join: {len(merged_gdf)} records")
    logger.debug(f"Merged columns: {list(merged_gdf.columns)}")
    logger.debug(
        f"RCO columns present: {[col for col in ['rco_info', 'rco_names'] if col in merged_gdf.columns]}"
    )
    logger.debug(
        f"Records with RCO data: {(merged_gdf['rco_names'].notna() & (merged_gdf['rco_names'] != '')).sum()}"
    )
    logger.debug(
        f"Records without RCO data: {(merged_gdf['rco_names'].isna() | (merged_gdf['rco_names'] == '')).sum()}"
    )
    logger.debug(
        f"Sample RCO names after join: {merged_gdf['rco_names'].head(5).tolist()}"
    )
    logger.debug(
        f"Sample RCO info after join: {merged_gdf['rco_info'].head(5).tolist()}"
    )

    group_columns = [col for col in merged_gdf.columns if col not in rco_use_cols]
    logger.debug(f"Group columns: {group_columns}")
    logger.debug(f"RCO use columns: {rco_use_cols}")

    # Ensure columns are appropriately filled and cast
    for col in group_columns:
        merged_gdf[col] = merged_gdf[col].fillna("").infer_objects(copy=False)

    logger.debug(f"Before grouping: {len(merged_gdf)} records")
    logger.debug(
        f"Sample RCO names before grouping: {merged_gdf['rco_names'].head(5).tolist()}"
    )
    logger.debug(
        f"Sample RCO info before grouping: {merged_gdf['rco_info'].head(5).tolist()}"
    )

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

    logger.debug(f"After grouping: {len(merged_gdf)} records")
    logger.debug(
        f"Sample RCO names after grouping: {merged_gdf['rco_names'].head(5).tolist()}"
    )
    logger.debug(
        f"Sample RCO info after grouping: {merged_gdf['rco_info'].head(5).tolist()}"
    )
    logger.debug(
        f"Records with non-empty RCO names: {(merged_gdf['rco_names'].notna() & (merged_gdf['rco_names'] != '') & (merged_gdf['rco_names'] != 'nan')).sum()}"
    )
    logger.debug(
        f"Records with non-empty RCO info: {(merged_gdf['rco_info'].notna() & (merged_gdf['rco_info'] != '') & (merged_gdf['rco_info'] != 'nan')).sum()}"
    )

    merged_gdf = gpd.GeoDataFrame(merged_gdf, geometry="geometry", crs=input_gdf.crs)
    merged_gdf.drop_duplicates(inplace=True)

    logger.debug(f"Final result: {len(merged_gdf)} records")
    logger.debug(f"Final RCO names null count: {merged_gdf['rco_names'].isna().sum()}")
    logger.debug(f"Final RCO info null count: {merged_gdf['rco_info'].isna().sum()}")
    logger.debug(
        f"Final RCO names empty string count: {(merged_gdf['rco_names'] == '').sum()}"
    )
    logger.debug(
        f"Final RCO info empty string count: {(merged_gdf['rco_info'] == '').sum()}"
    )

    return merged_gdf, input_validation
