from ..classes.featurelayer import FeatureLayer
from ..constants.services import DRUGCRIME_SQL_QUERY
from new_etl.data_utils.kde import apply_kde_to_primary


def drug_crimes(primary_featurelayer: FeatureLayer) -> FeatureLayer:
    """
    Applies kernel density estimation (KDE) analysis for drug crimes to the primary feature layer.

    Args:
        primary_featurelayer (FeatureLayer): The feature layer containing property data.

    Returns:
        FeatureLayer: The input feature layer with KDE analysis results for drug crimes.
    """
    return apply_kde_to_primary(
        primary_featurelayer, "Drug Crimes", DRUGCRIME_SQL_QUERY
    )
