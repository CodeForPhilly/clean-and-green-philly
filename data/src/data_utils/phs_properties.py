from ..classes.featurelayer import FeatureLayer
from ..constants.services import PHS_LAYERS_TO_LOAD
from ..metadata.metadata_utils import provide_metadata


@provide_metadata()
def phs_properties(primary_featurelayer: FeatureLayer) -> FeatureLayer:
    """
    Perform a spatial join between the primary feature layer and the PHS properties layer,
    then update the primary feature layer with a new column 'phs_care_program' indicating
    if the property is part of the PHS care program.

    Args:
        primary_featurelayer (FeatureLayer): The primary feature layer to join with the PHS properties layer.

    Returns:
        FeatureLayer: The updated primary feature layer with the 'phs_care_program' column.

    Tagline:
        Identifies PHS Care properties

    Columns added:
        phs_care_program (str): The PHS care program associated with the property.

    Primary Feature Layer Columns Referenced:
        opa_id, geometry
    """

    phs_properties = FeatureLayer(
        name="PHS Properties", esri_rest_urls=PHS_LAYERS_TO_LOAD, cols=["program"]
    )

    # Perform spatial join between primary feature layer and PHS properties
    primary_featurelayer.spatial_join(phs_properties)

    # Create 'phs_care_program' column with values from 'program', drop 'program'
    primary_featurelayer.gdf["phs_care_program"] = primary_featurelayer.gdf.pop(
        "program"
    )

    # Rebuild the GeoDataFrame after updates
    primary_featurelayer.rebuild_gdf()

    return primary_featurelayer
