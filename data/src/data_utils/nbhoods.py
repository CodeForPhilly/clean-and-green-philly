import geopandas as gpd

from src.validation.base import validate_output
from src.validation.nbhoods import NeighborhoodsOutputValidator

from ..classes.loaders import GdfLoader
from ..constants.services import NBHOODS_URL
from ..metadata.metadata_utils import provide_metadata
from ..utilities import spatial_join


@provide_metadata()
@validate_output(NeighborhoodsOutputValidator)
def nbhoods(input_gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
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

    loader = GdfLoader(name="Neighborhoods", input=NBHOODS_URL, cols=["mapname"])
    phl_nbhoods = loader.load_or_fetch()

    # Correct the column name to lowercase if needed
    if "mapname" in phl_nbhoods.columns:
        phl_nbhoods.rename(columns={"mapname": "neighborhood"}, inplace=True)

    merged_gdf = spatial_join(input_gdf, phl_nbhoods)

    return merged_gdf
