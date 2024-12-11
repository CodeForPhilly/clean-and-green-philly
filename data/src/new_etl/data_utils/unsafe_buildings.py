from ..classes.featurelayer import FeatureLayer
from ..constants.services import UNSAFE_BUILDINGS_QUERY


def unsafe_buildings(primary_featurelayer: FeatureLayer) -> FeatureLayer:
    """
    Adds unsafe building information to the primary feature layer by joining with a dataset
    of unsafe buildings.

    Args:
        primary_featurelayer (FeatureLayer): The feature layer containing property data.

    Returns:
        FeatureLayer: The input feature layer with an added "unsafe_building" column,
        indicating whether each property is categorized as an unsafe building ("Y" or "N").
    """
    unsafe_buildings = FeatureLayer(
        name="Unsafe Buildings",
        carto_sql_queries=UNSAFE_BUILDINGS_QUERY,
        use_wkb_geom_field="the_geom",
        cols=["opa_account_num"],
    )

    # Mark unsafe buildings
    unsafe_buildings.gdf.loc[:, "unsafe_building"] = "Y"

    # Rename column for consistency
    unsafe_buildings.gdf = unsafe_buildings.gdf.rename(
        columns={"opa_account_num": "opa_number"}
    )

    # Join unsafe buildings data with primary feature layer
    primary_featurelayer.opa_join(
        unsafe_buildings.gdf,
        "opa_number",
    )

    # Fill missing values with "N" for non-unsafe buildings
    primary_featurelayer.gdf.loc[:, "unsafe_building"] = primary_featurelayer.gdf[
        "unsafe_building"
    ].fillna("N")

    return primary_featurelayer
