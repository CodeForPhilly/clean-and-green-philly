from ..classes.featurelayer import FeatureLayer


def tactical_urbanism(primary_featurelayer: FeatureLayer) -> FeatureLayer:
    """
    Assigns a 'tactical_urbanism' value to each row in the primary feature layer based on specific conditions.

    Tactical urbanism is marked as "Yes" if the property is a parcel of type 'Land',
    and does not have any unsafe or immediately dangerous buildings. Otherwise, it is "No".

    Args:
        primary_featurelayer: A FeatureLayer object containing a GeoDataFrame (`gdf`) as an attribute.

    Returns:
        The input FeatureLayer with a new column 'tactical_urbanism' added to its GeoDataFrame.
    """
    tactical_urbanism_values = []

    for idx, row in primary_featurelayer.gdf.iterrows():
        if (
            row["parcel_type"] == "Land"
            and row["unsafe_building"] == "N"
            and row["imm_dang_building"] == "N"
        ):
            tactical_urbanism = "Yes"
        else:
            tactical_urbanism = "No"

        tactical_urbanism_values.append(tactical_urbanism)

    primary_featurelayer.gdf["tactical_urbanism"] = tactical_urbanism_values
    return primary_featurelayer
