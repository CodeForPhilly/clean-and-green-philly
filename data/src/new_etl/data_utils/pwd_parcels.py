import geopandas as gpd

from ..classes.featurelayer import FeatureLayer
from ..constants.services import PWD_PARCELS_QUERY
from ..metadata.metadata_utils import provide_metadata


@provide_metadata()
def pwd_parcels(primary_featurelayer: FeatureLayer) -> FeatureLayer:
    """
    Updates the primary feature layer by replacing its geometry column with validated
    geometries from PWD parcels data. Retains point geometry for rows with no polygon
    geometry available.

    Args:
        primary_featurelayer (FeatureLayer): The primary feature layer to update.

    Returns:
        FeatureLayer: The updated primary feature layer with geometries replaced
                      by those from PWD parcels or retained from the original layer if no match.

    Columns Updated:
        geometry: The geometry column is updated with validated geometries from PWD parcels.

    Primary Feature Layer Columns Referenced:
        opa_id, geometry

    Tagline:
        Improve geometry with PWD parcels data.

    Source:
        https://phl.carto.com/api/v2/sql
    """
    # Load PWD parcels
    pwd_parcels = FeatureLayer(
        name="PWD Parcels",
        carto_sql_queries=PWD_PARCELS_QUERY,
        use_wkb_geom_field="the_geom",
        cols=["brt_id"],
    )

    # Drop rows with null brt_id, rename to opa_id, and validate geometries
    pwd_parcels.gdf.dropna(subset=["brt_id"], inplace=True)
    pwd_parcels.gdf.rename(columns={"brt_id": "opa_id"}, inplace=True)
    pwd_parcels.gdf["geometry"] = pwd_parcels.gdf["geometry"].make_valid()

    # Ensure geometries are polygons or multipolygons
    if not all(pwd_parcels.gdf.geometry.type.isin(["Polygon", "MultiPolygon"])):
        raise ValueError("Some geometries are not polygons or multipolygons.")

    # Temporarily drop geometry from the primary feature layer
    primary_df = primary_featurelayer.gdf.drop(columns=["geometry"])

    # Join geometries from PWD parcels
    merged_gdf = primary_df.merge(
        pwd_parcels.gdf[["opa_id", "geometry"]],
        on="opa_id",
        how="left",
    )

    # Coerce merged_gdf into a GeoDataFrame
    merged_gdf = gpd.GeoDataFrame(
        merged_gdf,
        geometry="geometry",
        crs=primary_featurelayer.gdf.crs,  # Ensure the CRS matches the original
    )

    # Log observations with no polygon geometry
    no_geometry_count = merged_gdf["geometry"].isnull().sum()

    # Retain point geometry for rows with no polygon geometry
    merged_gdf["geometry"] = merged_gdf["geometry"].combine_first(
        primary_featurelayer.gdf["geometry"]
    )
    print("Number of observations retaining point geometry:", no_geometry_count)
    primary_featurelayer.gdf = merged_gdf
    # Wrap the GeoDataFrame back into a FeatureLayer
    return primary_featurelayer
