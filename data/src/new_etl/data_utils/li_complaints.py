from ..classes.featurelayer import FeatureLayer
from ..constants.services import COMPLAINTS_SQL_QUERY
from ..data_utils.kde import apply_kde_to_primary


def li_complaints(primary_featurelayer: FeatureLayer) -> FeatureLayer:
    """
    Applies kernel density estimation (KDE) analysis for L&I complaints to the primary feature layer.

    Args:
        primary_featurelayer (FeatureLayer): The feature layer containing property data.

    Returns:
        FeatureLayer: The input feature layer with KDE analysis results for L&I complaints,
        including density and derived metrics.
    """
    return apply_kde_to_primary(
        primary_featurelayer, "L and I Complaints", COMPLAINTS_SQL_QUERY
    )
