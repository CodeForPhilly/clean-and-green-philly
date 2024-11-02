from classes.featurelayer import FeatureLayer
from constants.services import PHS_LAYERS_TO_LOAD

def phs_properties(primary_featurelayer: FeatureLayer) -> FeatureLayer:
    """
    Perform a spatial join between the primary feature layer and the PHS properties layer,
    then update the primary feature layer with a new column 'phs_care_program' indicating
    if the property is part of the PHS care program.

    Args:
        primary_featurelayer (FeatureLayer): The primary feature layer to join with the PHS properties layer.

    Returns:
        FeatureLayer: The updated primary feature layer with the 'phs_care_program' column.
    """
    
    phs_properties = FeatureLayer(
        name="PHS Properties", esri_rest_urls=PHS_LAYERS_TO_LOAD, cols=["program"]
    )

    # Perform spatial join between primary feature layer and PHS properties
    primary_featurelayer.spatial_join(phs_properties)

    # Initialize 'phs_care_program' column with default "no" for all rows
    primary_featurelayer.gdf["phs_care_program"] = "No"
    
    # Set 'phs_care_program' to "yes" for matched rows
    primary_featurelayer.gdf.loc[primary_featurelayer.gdf["program"].notna(), "phs_care_program"] = "Yes"

    # Rebuild the GeoDataFrame after updates
    primary_featurelayer.rebuild_gdf()

    return primary_featurelayer
