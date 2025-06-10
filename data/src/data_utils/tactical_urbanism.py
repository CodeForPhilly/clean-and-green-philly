import geopandas as gpd

from ..metadata.metadata_utils import provide_metadata


@provide_metadata()
def tactical_urbanism(input_gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """
    Assigns a 'tactical_urbanism' value to each row in the primary feature layer based on specific conditions.

    Tactical urbanism is marked as "Yes" if the property is a parcel of type 'Land',
    and does not have any unsafe or immediately dangerous buildings. Otherwise, it is "No".

    Args:
        primary_featurelayer: A FeatureLayer object containing a GeoDataFrame (`gdf`) as an attribute.

    Columns Added:
        tactical_urbanism (str): Indicates whether each property qualifies for tactical urbanism ("Yes" or "No").

    Primary Feature Layer Columns Referenced:
        parcel_type, unsafe_building, imm_dang_building

    Tagline:
        Identify tactical urbanism-eligible properties

    Returns:
        The input FeatureLayer with a new column 'tactical_urbanism' added to its GeoDataFrame.
    """
    tactical_urbanism_values = []

    for idx, row in input_gdf.iterrows():
        if (
            row["parcel_type"] == "Land"
            and row["unsafe_building"] == "N"
            and row["imm_dang_building"] == "N"
        ):
            tactical_urbanism = "Yes"
        else:
            tactical_urbanism = "No"

        tactical_urbanism_values.append(tactical_urbanism)

    input_gdf["tactical_urbanism"] = tactical_urbanism_values
    return input_gdf
