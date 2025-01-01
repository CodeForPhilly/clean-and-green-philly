from ..classes.featurelayer import FeatureLayer
from ..constants.services import GUNCRIME_SQL_QUERY
from new_etl.data_utils.kde import apply_kde_to_primary


def gun_crimes(primary_featurelayer: FeatureLayer) -> FeatureLayer:
    """
    Applies kernel density estimation (KDE) analysis for gun crimes to the primary feature layer.

    Args:
        primary_featurelayer (FeatureLayer): The feature layer containing property data.

    Returns:
        FeatureLayer: The input feature layer with KDE analysis results for gun crimes.
    """
    return apply_kde_to_primary(primary_featurelayer, "Gun Crimes", GUNCRIME_SQL_QUERY)
