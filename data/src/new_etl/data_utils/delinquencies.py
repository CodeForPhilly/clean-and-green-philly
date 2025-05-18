from ..classes.featurelayer import FeatureLayer
from ..constants.services import DELINQUENCIES_QUERY
from ..metadata.metadata_utils import provide_metadata


@provide_metadata()
def delinquencies(primary_featurelayer: FeatureLayer) -> FeatureLayer:
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
    tax_delinquencies = FeatureLayer(
        name="Property Tax Delinquencies",
        carto_sql_queries=DELINQUENCIES_QUERY,
        use_wkb_geom_field="the_geom",
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
    )

    primary_featurelayer.opa_join(
        tax_delinquencies.gdf,
        "opa_number",
    )

    # Convert string columns to boolean
    primary_featurelayer.gdf["is_actionable"] = primary_featurelayer.gdf[
        "is_actionable"
    ].map({"Y": True, "N": False, "NA": False})
    primary_featurelayer.gdf["sheriff_sale"] = primary_featurelayer.gdf[
        "sheriff_sale"
    ].map({"Y": True, "N": False})
    primary_featurelayer.gdf["payment_agreement"] = primary_featurelayer.gdf[
        "payment_agreement"
    ].map({"Y": True, "N": False, "NA": False})

    delinquency_cols = [
        "total_due",
        "num_years_owed",
        "most_recent_year_owed",
        "total_assessment",
    ]
    primary_featurelayer.gdf[delinquency_cols] = primary_featurelayer.gdf[
        delinquency_cols
    ].fillna("NA")

    return primary_featurelayer
