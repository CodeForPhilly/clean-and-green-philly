from ..classes.featurelayer import FeatureLayer
from ..constants.services import IMMINENT_DANGER_BUILDINGS_QUERY
from ..metadata.metadata_utils import provide_metadata


@provide_metadata()
def imm_dang_buildings(primary_featurelayer: FeatureLayer) -> FeatureLayer:
    """
    Adds information about imminently dangerous buildings to the primary feature layer
    by joining with a dataset of dangerous buildings.

    Args:
        primary_featurelayer (FeatureLayer): The feature layer containing property data.

    Returns:
        FeatureLayer: The input feature layer with an added "imm_dang_building" column,
        indicating whether each property is categorized as imminently dangerous ("Y" or "N").

    Tagline:
        Identify imminently dangerous buildings

    Columns Added:
        imm_dang_building (str): Indicates whether each property is categorized as imminently dangerous ("Y" or "N").

    Primary Feature Layer Columns Referenced:
        opa_id

    Source:
        https://phl.carto.com/api/v2/sql
    """
    imm_dang_buildings = FeatureLayer(
        name="Imminently Dangerous Buildings",
        use_wkb_geom_field="the_geom",
        carto_sql_queries=IMMINENT_DANGER_BUILDINGS_QUERY,
        cols=["opa_account_num"],
    )

    imm_dang_buildings.gdf.loc[:, "imm_dang_building"] = True

    imm_dang_buildings.gdf = imm_dang_buildings.gdf.rename(
        columns={"opa_account_num": "opa_number"}
    )

    primary_featurelayer.opa_join(
        imm_dang_buildings.gdf,
        "opa_number",
    )

    primary_featurelayer.gdf.loc[:, "imm_dang_building"] = primary_featurelayer.gdf[
        "imm_dang_building"
    ].fillna(False)

    return primary_featurelayer
