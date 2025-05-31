from src.data_utils.kde import apply_kde_to_primary

from ..classes.featurelayer import FeatureLayer
from ..constants.services import GUNCRIME_SQL_QUERY
from ..metadata.metadata_utils import provide_metadata


@provide_metadata()
def gun_crimes(primary_featurelayer: FeatureLayer) -> FeatureLayer:
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
    return apply_kde_to_primary(primary_featurelayer, "Gun Crimes", GUNCRIME_SQL_QUERY)
