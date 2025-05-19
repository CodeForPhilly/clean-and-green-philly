from src.classes.featurelayer import FeatureLayer
from src.constants.services import OPA_PROPERTIES_QUERY


def opa_properties(primary_featurelayer):
    opa = FeatureLayer(
        name="OPA Properties",
        carto_sql_queries=OPA_PROPERTIES_QUERY,
        use_wkb_geom_field="the_geom",
        cols=[
            "market_value",
            "sale_date",
            "sale_price",
            "parcel_number",
            "mailing_address_1",
            "mailing_address_2",
            "mailing_care_of",
            "mailing_city_state",
            "mailing_street",
            "mailing_zip",
        ],
    )

    primary_featurelayer.opa_join(
        opa.gdf,
        "parcel_number",
    )

    return primary_featurelayer
