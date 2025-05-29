from src.classes.featurelayer import FeatureLayer
from src.constants.services import UNSAFE_BUILDINGS_QUERY


def unsafe_buildings(primary_featurelayer):
    unsafe_buildings = FeatureLayer(
        name="Unsafe Buildings",
        carto_sql_queries=UNSAFE_BUILDINGS_QUERY,
        use_wkb_geom_field="the_geom",
        cols=["opa_account_num"],
    )

    unsafe_buildings.gdf.loc[:, "unsafe_building"] = "Y"

    unsafe_buildings.gdf = unsafe_buildings.gdf.rename(
        columns={"opa_account_num": "opa_number"}
    )

    primary_featurelayer.opa_join(
        unsafe_buildings.gdf,
        "opa_number",
    )

    primary_featurelayer.gdf.loc[:, "unsafe_building"] = primary_featurelayer.gdf[
        "unsafe_building"
    ].fillna("N")

    return primary_featurelayer
