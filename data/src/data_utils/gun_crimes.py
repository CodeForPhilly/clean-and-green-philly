import geopandas as gpd

from src.data_utils.kde import apply_kde_to_input
from src.validation.base import validate_output
from src.validation.gun_crimes import GunCrimesOutputValidator

from ..constants.services import GUNCRIME_SQL_QUERY
from ..metadata.metadata_utils import provide_metadata


@provide_metadata()
@validate_output(GunCrimesOutputValidator)
def gun_crimes(input_gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """
    Applies kernel density estimation (KDE) analysis for gun crimes to the primary feature layer.

    Args:
        primary_featurelayer (FeatureLayer): The feature layer containing property data.

    Returns:
        FeatureLayer: The input feature layer with KDE analysis results for gun crimes.

    Tagline:
        Analyzes gun crime density

    Columns added:
        gun_crimes_density (float): KDE density of gun crimes.
        gun_crimes_density_zscore (float): Z-score of gun crime density.
        gun_crimes_density_label (str): Categorized density level.
        gun_crimes_density_percentile (float): Percentile rank of density.

    Primary Feature Layer Columns Referenced:
        geometry

    Source:
        https://phl.carto.com/api/v2/sql
    """
    return apply_kde_to_input(input_gdf, "Gun Crimes", GUNCRIME_SQL_QUERY)
