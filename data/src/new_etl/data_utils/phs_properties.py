import geopandas as gpd

from new_etl.utilities import spatial_join
from ..classes.featurelayer import EsriLoader
from ..constants.services import PHS_LAYERS_TO_LOAD
from ..metadata.metadata_utils import provide_metadata


@provide_metadata()
def phs_properties(input_gdf: gpd.GeoDatamFrame) -> gpd.GeoDatamFrame:
    """
    Perform a spatial join between the primary feature layer and the PHS properties layer,
    then update the primary feature layer with a new column 'phs_care_program' indicating
    if the property is part of the PHS care program.

    Args:
        merged_gdf (FeatureLayer): The primary feature layer to join with the PHS properties layer.

    Returns:
        FeatureLayer: The updated primary feature layer with the 'phs_care_program' column.

    Tagline:
        Identifies PHS Care properties

    Columns added:
        phs_care_program (str): The PHS care program associated with the property.

    Primary Feature Layer Columns Referenced:
        opa_id, geometry
    """

    loader = EsriLoader(
        name="PHS Properties", esri_urls=PHS_LAYERS_TO_LOAD, cols=["program"]
    )

    phs_properties = loader.load_or_fetch()

    # Perform spatial join between primary feature layer and PHS properties
    merged_gdf = spatial_join(input_gdf, phs_properties)

    # Create 'phs_care_program' column with values from 'program', drop 'program'
    merged_gdf["phs_care_program"] = merged_gdf.pop("program")

    # Rebuild the GeoDataFrame after updates
    merged_gdf.rebuild_gdf()

    return merged_gdf
