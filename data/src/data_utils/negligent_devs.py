import pandas as pd


def negligent_devs(primary_featurelayer):
    devs = primary_featurelayer.gdf

    print("Columns in 'devs' DataFrame:", devs.columns)

    print("Initial properties data:")
    print(
        devs[["opa_id", "city_owner_agency", "standardized_address", "vacant"]].head(10)
    )

    # Count observations where vacant == 1 by standardized_address
    vacant_counts = (
        devs[devs["vacant"] == 1]
        .groupby("standardized_address")
        .size()
        .reset_index(name="vacant_property_count")
    )

    print("Head of resulting DataFrame with vacant counts:")
    print(vacant_counts.head(10))

    # Merge the vacant counts back to the main DataFrame
    primary_featurelayer.gdf = primary_featurelayer.gdf.merge(
        vacant_counts, on="standardized_address", how="left"
    )

    # Identify negligent developers: non-city owned entities owning 5+ vacant properties
    primary_featurelayer.gdf["n_properties_owned"] = primary_featurelayer.gdf.groupby(
        "opa_id"
    )["vacant_property_count"].transform("sum")

    primary_featurelayer.gdf["negligent_dev"] = (
        primary_featurelayer.gdf["n_properties_owned"] >= 5
    ) & (
        primary_featurelayer.gdf["city_owner_agency"].isna()
        | (primary_featurelayer.gdf["city_owner_agency"] == "")
    )

    print("Final feature layer data with negligent_dev flag:")
    print(
        primary_featurelayer.gdf[
            ["opa_id", "n_properties_owned", "negligent_dev"]
        ].head(10)
    )

    return primary_featurelayer
