import geopandas as gpd

from ..classes.featurelayer import FeatureLayer
from ..constants.services import PWD_PARCELS_QUERY
from ..metadata.metadata_utils import provide_metadata


def transform_pwd_parcels_gdf(pwd_parcels_gdf: gpd.GeoDataFrame):
    """
    Transforms the PWD parcels GeoDataFrame in place by dropping rows with null 'brt_id' and
    renaming 'brt_id' to 'opa_id'.

    Args:
        gdf (gpd.GeoDataFrame): The input GeoDataFrame containing PWD parcels data.

    """
    # Drop rows with null brt_id, rename to opa_id, and validate geometries
    pwd_parcels_gdf.dropna(subset=["brt_id"], inplace=True)
    pwd_parcels_gdf.rename(columns={"brt_id": "opa_id"}, inplace=True)
    pwd_parcels_gdf["geometry"] = pwd_parcels_gdf["geometry"].make_valid()

    # Ensure geometries are polygons or multipolygons
    if not all(pwd_parcels_gdf.geometry.type.isin(["Polygon", "MultiPolygon"])):
        raise ValueError("Some geometries are not polygons or multipolygons.")


def merge_pwd_parcels_gdf(primary_gdf, pwd_parcels_gdf):
    """
    Merge geometries from PWD parcels into the primary feature layer.
    Identifies condominium units by finding duplicate geometries in the primary layer
    and replacing them with parcel geometries from PWD.

    Args:
        primary_gdf (GeoDataFrame): The primary feature layer
        pwd_parcels_gdf (GeoDataFrame): The PWD parcels GeoDataFrame

    Returns:
        GeoDataFrame: The merged GeoDataFrame with updated geometries and condo flags
    """
    # Add condo flag column
    primary_gdf["is_condo_unit"] = False

    # Find duplicate geometries in primary layer
    duplicate_geoms = primary_gdf.groupby(primary_gdf.geometry.astype(str)).filter(
        lambda x: len(x) > 1
    )

    # For each duplicate geometry
    for geom_str, group in duplicate_geoms.groupby(primary_gdf.geometry.astype(str)):
        # Get the matching parcel from PWD
        matching_parcel = pwd_parcels_gdf[
            pwd_parcels_gdf["brt_id"].isin(group["opa_id"])
        ]

        if not matching_parcel.empty:
            # Get the parcel geometry
            parcel_geom = matching_parcel.iloc[0]["geometry"]

            # Update all units with this geometry to use the parcel geometry
            primary_gdf.loc[group.index, "geometry"] = parcel_geom
            primary_gdf.loc[group.index, "is_condo_unit"] = True

    # For non-condo units, update geometries from PWD parcels where available
    for idx, row in primary_gdf.iterrows():
        if not row["is_condo_unit"]:
            pwd_geom = (
                pwd_parcels_gdf[pwd_parcels_gdf["brt_id"] == row["opa_id"]][
                    "geometry"
                ].iloc[0]
                if not pwd_parcels_gdf[pwd_parcels_gdf["brt_id"] == row["opa_id"]].empty
                else None
            )

            if pwd_geom:
                primary_gdf.loc[idx, "geometry"] = pwd_geom

    return primary_gdf


@provide_metadata()
def pwd_parcels(primary_feature_layer):
    """
    Updates the primary feature layer with validated geometries from PWD parcels.
    Identifies condominium units by finding duplicate geometries and replacing them
    with parcel geometries from PWD. We discovered that approximately 33,000 condo units
    were listed with duplicate point geometries in various locations. This function
    replaces these geometries with the associated parcel geometries from PWD and adds
    a flag to identify condominium units.

    Args:
        primary_feature_layer: The primary feature layer to update

    Returns:
        The updated primary feature layer with:
        - Updated geometries from PWD parcels
        - New field:
          - is_condo_unit (boolean): Whether the property is a condominium unit

    Columns updated:
        geometry: Replaces point geometries with parcel geometries from PWD for condominium units
        is_condo_unit (boolean): Flags properties that are condominium units, identified by having duplicate geometries

    Known issues:
        Approximately 33,000 condominium units were originally listed with duplicate point geometries
        in various locations. These have been replaced with the associated parcel geometries from PWD
        and flagged as condominium units.
    """
    # Get PWD parcels data
    pwd_parcels = FeatureLayer(
        name="PWD Parcels",
        carto_sql_queries=PWD_PARCELS_QUERY,
        use_wkb_geom_field="the_geom",
        cols=["brt_id"],
    )

    # Transform PWD parcels data
    pwd_parcels_gdf = transform_pwd_parcels_gdf(pwd_parcels.gdf)

    # Merge geometries and identify condos
    primary_feature_layer.gdf = merge_pwd_parcels_gdf(
        primary_feature_layer.gdf, pwd_parcels_gdf
    )

    return primary_feature_layer
