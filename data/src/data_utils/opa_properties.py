from classes.featurelayer import FeatureLayer
from constants.services import OPA_PROPERTIES_QUERY


def opa_properties(primary_featurelayer):
    opa = FeatureLayer(
        name="OPA Properties",
        carto_sql_queries=OPA_PROPERTIES_QUERY,
        use_wkb_geom_field="the_geom",
    )

    red_cols_to_keep = [
        "market_value", 
        "sale_date", 
        "sale_price", 
        "parcel_number",
        "geometry"
    ]

    opa.gdf = opa.gdf[red_cols_to_keep]

    primary_featurelayer.spatial_join(opa)

    return primary_featurelayer