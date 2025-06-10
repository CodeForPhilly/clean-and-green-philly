import geopandas as gpd

from utilities import opa_join

from ..classes.loaders import CartoLoader
from ..constants.services import DELINQUENCIES_QUERY
from ..metadata.metadata_utils import provide_metadata


@provide_metadata()
def delinquencies(input_gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """
    Adds property tax delinquency information to the primary feature layer by
    joining with a tax delinquencies dataset.

    Args:
        primary_featurelayer (FeatureLayer): The feature layer containing property data.

    Returns:
        FeatureLayer: The input feature layer with added columns for tax delinquency
        information, including total due, actionable status, payment agreements, and more.

    Tagline:
        Summarize tax delinquencies

    Source:
        https://phl.carto.com/api/v2/sql

    Columns Added:
        total_due (float): Total amount owed.
        most_recent_year_owed (str): Most recent year owed.
        num_years_owed (int): Number of years owed.
        payment_agreement (str): Indicates if there is a payment agreement.
        is_actionable (str): Flag for actionable tax delinquency.
        sheriff_sale (str): Indicates if the property is at risk of sheriff sale.
        total_assessment (float): Total property assessment.

    Primary Feature Layer Columns Referenced:
        opa_id
    """

    loader = CartoLoader(
        name="Property Tax Delinquencies",
        carto_queries=DELINQUENCIES_QUERY,
        cols=[
            "opa_number",
            "total_due",
            "is_actionable",
            "payment_agreement",
            "num_years_owed",
            "most_recent_year_owed",
            "total_assessment",
            "sheriff_sale",
        ],
        opa_col="opa_number",
    )

    tax_delinquencies = loader.load_or_fetch()

    merged_gdf = opa_join(
        input_gdf,
        tax_delinquencies,
    )

    delinquency_cols = [
        "total_due",
        "is_actionable",
        "payment_agreement",
        "num_years_owed",
        "most_recent_year_owed",
        "total_assessment",
    ]
    merged_gdf[delinquency_cols] = merged_gdf[delinquency_cols].fillna("NA")

    merged_gdf["sheriff_sale"] = merged_gdf["sheriff_sale"].fillna("N")

    return merged_gdf
