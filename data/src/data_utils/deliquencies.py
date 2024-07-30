from classes.featurelayer import FeatureLayer
from constants.services import DELINQUENCIES_QUERY


def deliquencies(primary_featurelayer):
    tax_deliquencies = FeatureLayer(
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
        tax_deliquencies.gdf,
        "opa_number",
    )

    primary_featurelayer.gdf["sheriff_sale"].fillna("N", inplace=True)

    return primary_featurelayer
