from typing import Tuple

import geopandas as gpd

from src.metadata.metadata_utils import current_metadata, provide_metadata
from src.validation.base import ValidationResult, validate_output
from src.validation.tactical_urbanism import TacticalUrbanismOutputValidator


@validate_output(TacticalUrbanismOutputValidator)
@provide_metadata(current_metadata=current_metadata)
def tactical_urbanism(
    input_gdf: gpd.GeoDataFrame,
) -> Tuple[gpd.GeoDataFrame, ValidationResult]:
    """
    Assigns a 'tactical_urbanism' value to each row in the input GeoDataFrame based on specific conditions.

    Tactical urbanism is marked as True if the property is a parcel of type 'Land',
    and does not have any unsafe or immediately dangerous buildings. Otherwise, it is False.

    Args:
        primary_featurelayer: A GeoDataFrame object containing a GeoDataFrame (`gdf`) as an attribute.

    Columns Added:
        tactical_urbanism (bool): Indicates whether each property qualifies for tactical urbanism (True or False).

    Columns referenced:
        parcel_type, unsafe_building, imm_dang_building

    Tagline:
        Identify tactical urbanism-eligible properties

    Returns:
        The input GeoDataFrame with a new column 'tactical_urbanism' added to its GeoDataFrame.
    """
    tactical_urbanism_values = []

    for idx, row in input_gdf.iterrows():
        if (
            row["parcel_type"] == "Land"
            and not row["unsafe_building"]
            and not row["imm_dang_building"]
        ):
            tactical_urbanism = True
        else:
            tactical_urbanism = False

        tactical_urbanism_values.append(tactical_urbanism)

    input_gdf["tactical_urbanism"] = tactical_urbanism_values
    return input_gdf, ValidationResult(True)
