import geopandas as gpd

from config.config import USE_CRS

from ..classes.featurelayer import FeatureLayer
from ..constants.services import NBHOODS_URL
from ..metadata.metadata_utils import provide_metadata


def transform_neighborhoods_gdf(
    neighborhoods_gdf: gpd.GeoDataFrame,
) -> gpd.GeoDataFrame:
    """
    Transforms the neighborhoods GeoDataFrame in place by renaming the MAPNAME column to neighborhood
    and retaining only it and the geometry columns.

    Args:
        gdf (gpd.GeoDataFrame): The input GeoDataFrame containing PWD parcels data.

    Returns:
        gdf (gpd.GeoDataFrame): The output, transformed GeoDataFrame.
    """
    if "MAPNAME" in neighborhoods_gdf.columns:
        neighborhoods_gdf.rename(columns={"MAPNAME": "neighborhood"}, inplace=True)

    neighborhoods_gdf = neighborhoods_gdf.to_crs(USE_CRS)

    neighborhoods_gdf = neighborhoods_gdf[["neighborhood", "geometry"]]

    return neighborhoods_gdf


@provide_metadata()
def nbhoods(primary_featurelayer: FeatureLayer) -> FeatureLayer:
    """
    Adds neighborhood information to the primary feature layer by performing a spatial join
    with a neighborhoods dataset.

    Args:
        primary_featurelayer (FeatureLayer): The feature layer containing property data.

    Returns:
        FeatureLayer: The input feature layer with an added "neighborhood" column,
        containing the name of the neighborhood for each property.

    Tagline:
        Assigns neighborhoods

    Columns added:
        neighborhood (str): The name of the neighborhood associated with the property.

    Primary Feature Layer Columns Referenced:
        opa_id, geometry

    Source:
        https://raw.githubusercontent.com/opendataphilly/open-geo-data/master/philadelphia-neighborhoods/philadelphia-neighborhoods.geojson
    """
    neighborhoods_gdf = gpd.read_file(NBHOODS_URL)
    neighborhoods_gdf = transform_neighborhoods_gdf(neighborhoods_gdf)

    neighborhoods_feature_layer = FeatureLayer("Neighborhoods")
    neighborhoods_feature_layer.gdf = neighborhoods_gdf

    primary_featurelayer.spatial_join(neighborhoods_feature_layer)

    return primary_featurelayer
