from ..classes.featurelayer import FeatureLayer


def negligent_devs(primary_featurelayer: FeatureLayer) -> FeatureLayer:
    """
    Identifies negligent developers based on the number of vacant properties owned
    and flags them in the primary feature layer.

    Args:
        primary_featurelayer (FeatureLayer): The feature layer containing property data.

    Returns:
        FeatureLayer: The input feature layer with additional columns for total properties
        owned, vacant properties owned, and a "negligent_dev" flag.
    """
    devs = primary_featurelayer.gdf

    # Count total properties and vacant properties by standardized_address
    property_counts = (
        devs.groupby("standardized_address")
        .agg(
            n_total_properties_owned=("opa_id", "size"),
            n_vacant_properties_owned=("vacant", "sum"),
        )
        .reset_index()
    )

    # Merge the property counts back to the main DataFrame
    primary_featurelayer.gdf = primary_featurelayer.gdf.merge(
        property_counts, on="standardized_address", how="left"
    )

    # Identify negligent developers: non-city owned entities owning 5+ vacant properties
    primary_featurelayer.gdf["negligent_dev"] = (
        primary_featurelayer.gdf["n_vacant_properties_owned"] >= 5
    ) & (
        primary_featurelayer.gdf["city_owner_agency"].isna()
        | (primary_featurelayer.gdf["city_owner_agency"] == "")
    )

    return primary_featurelayer
