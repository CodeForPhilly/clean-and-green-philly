from new_etl.data_utils.kde import apply_kde_to_primary

from ..classes.featurelayer import FeatureLayer
from ..constants.services import DRUGCRIME_SQL_QUERY
from ..metadata.metadata_utils import provide_metadata


@provide_metadata()
def drug_crimes(primary_featurelayer: FeatureLayer) -> FeatureLayer:
    """
    Applies kernel density estimation (KDE) analysis for drug crimes to the primary feature layer.

    Args:
        primary_featurelayer (FeatureLayer): The feature layer containing property data.

    Returns:
        FeatureLayer: The input feature layer with KDE analysis results for drug crimes.

    Tagline:
        Density analysis for drug crimes

    Columns added:
        drug_crimes_density (float): KDE density of drug crimes.
        drug_crimes_density_zscore (float): Z-score of drug crime density.
        drug_crimes_density_label (str): Categorized density level.
        drug_crimes_density_percentile (float): Percentile rank of density.

    Primary Feature Layer Columns Referenced:
        geometry

    Source:
        https://phl.carto.com/api/v2/sql

    """
    return apply_kde_to_primary(
        primary_featurelayer, "Drug Crimes", DRUGCRIME_SQL_QUERY
    )
