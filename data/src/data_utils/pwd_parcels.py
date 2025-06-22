from typing import Tuple

import geopandas as gpd

from src.validation.base import ValidationResult, validate_output
from src.validation.pwd_parcels import PWDParcelsOutputValidator

from ..classes.loaders import CartoLoader
from ..constants.services import PWD_PARCELS_QUERY


def transform_pwd_parcels_gdf(pwd_parcels_gdf: gpd.GeoDataFrame):
    """
    Transforms the PWD parcels GeoDataFrame in place by dropping rows with null 'brt_id' and
    renaming 'brt_id' to 'opa_id'.

    Args:
        gdf (gpd.GeoDataFrame): The input GeoDataFrame containing PWD parcels data.

    """
    # Ensure geometries are polygons or multipolygons
    if not all(pwd_parcels_gdf.geometry.type.isin(["Polygon", "MultiPolygon"])):
        raise ValueError("Some geometries are not polygons or multipolygons.")


def merge_pwd_parcels_gdf(
    primary_gdf: gpd.GeoDataFrame, pwd_parcels_gdf: gpd.GeoDataFrame
) -> gpd.GeoDataFrame:
    """
    Merge geometries from PWD parcels into the primary feature layer.
    Identifies condominium units by checking for "CONDO" in building_code_description.

    Args:
        primary_gdf (GeoDataFrame): The primary feature layer
        pwd_parcels_gdf (GeoDataFrame): The PWD parcels GeoDataFrame

    Returns:
        GeoDataFrame: The merged GeoDataFrame with updated geometries and condo flags

    Note:
        Condo units are identified by properties with "CONDO" in building_code_description.
        Only non-condo units get their geometries updated from PWD parcels where available.
    """
    # Add condo flag column
    primary_gdf["is_condo_unit"] = False

    # Flag properties with "CONDO" in building_code_description
    if "building_code_description" in primary_gdf.columns:
        condo_building_mask = primary_gdf["building_code_description"].str.contains(
            "CONDO", case=False, na=False
        )
        primary_gdf.loc[condo_building_mask, "is_condo_unit"] = True

    # Join geometries from PWD parcels for non-condo units only
    # Temporarily drop geometry from the primary feature layer

    # Filter PWD parcels to just the opa_ids in primary
    opa_ids_in_primary = primary_gdf["opa_id"].unique()
    pwd_subset = pwd_parcels_gdf[pwd_parcels_gdf["opa_id"].isin(opa_ids_in_primary)]

    # Count how many of those are missing geometry
    no_geometry_count = pwd_subset["geometry"].isnull().sum()
    pwd_parcels_gdf_unique_opa_id = pwd_parcels_gdf.drop_duplicates(subset="opa_id")
    primary_gdf_unique_opa_id = primary_gdf.drop_duplicates(subset="opa_id")

    pwd_parcels_gdf_indexed = pwd_parcels_gdf_unique_opa_id.set_index("opa_id")
    merged_gdf_indexed = primary_gdf_unique_opa_id.set_index("opa_id")

    # ISSUE: This update and the other transformations might be incorrect
    merged_gdf_indexed.update(
        pwd_parcels_gdf_indexed[["geometry"]],
    )
    merged_gdf = merged_gdf_indexed.reset_index()

    print("Number of observations retaining point geometry:", no_geometry_count)

    # Calculate the area of the parcel in square feet
    # Data should already be in USE_CRS (EPSG:2272) from the loaders
    merged_gdf["parcel_area_sqft"] = merged_gdf.geometry.area
    # Note: Point geometries return 0.0 from .area, not NaN, so no fillna needed

    return merged_gdf


@validate_output(PWDParcelsOutputValidator)
def pwd_parcels(
    input_gdf: gpd.GeoDataFrame,
) -> Tuple[gpd.GeoDataFrame, ValidationResult]:
    """
    Updates the primary feature layer by replacing its geometry column with validated
    geometries from PWD parcels data. Retains point geometry for rows with no polygon
    geometry available. Identifies and flags condominium units.

    Args:
        primary_featurelayer (FeatureLayer): The primary feature layer to update.

    Returns:
        FeatureLayer: The updated primary feature layer with geometries replaced
                      by those from PWD parcels or retained from the original layer if no match.

    Columns Added:
        is_condo_unit (bool): Flag indicating if the property is a condominium unit.
                             Condo units are identified by duplicate geometries (multiple units at same site)
                             and retain their point geometries.
        parcel_area_sqft (float): The area of the parcel in square feet.
                                 Polygons will have an area value; points will have 0.0.

    Columns Updated:
        geometry: The geometry column is updated with validated geometries from PWD parcels.
                 Condo units retain their original point geometries.

    Primary Feature Layer Columns Referenced:
        opa_id, geometry

    Tagline:
        Improve geometry with PWD parcels data.

    Source:
        https://phl.carto.com/api/v2/sql
    """
    loader = CartoLoader(
        name="PWD Parcels",
        carto_queries=PWD_PARCELS_QUERY,
        opa_col="brt_id",
    )

    pwd_parcels, input_validation = loader.load_or_fetch()

    transform_pwd_parcels_gdf(pwd_parcels)

    input_gdf = merge_pwd_parcels_gdf(input_gdf, pwd_parcels)

    return input_gdf, input_validation
