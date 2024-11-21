import pandas as pd

def negligent_devs(primary_featurelayer):
    devs = primary_featurelayer.gdf

    print("Columns in 'devs' DataFrame:", devs.columns)

    print("Initial properties data:")
    print(
        devs[["opa_id", "city_owner_agency", "standardized_address", "vacant"]].head(10)
    )

    # Count total properties and vacant properties by standardized_address
    property_counts = (
        devs.groupby("standardized_address")
        .agg(
            n_total_properties_owned=("opa_id", "size"),
            n_vacant_properties_owned=("vacant", "sum"),
        )
        .reset_index()
    )

    print("Head of resulting DataFrame with property counts:")
    print(property_counts.head(10))

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

    print("Final feature layer data with negligent_dev flag:")
    print(
        primary_featurelayer.gdf[
            ["opa_id", "n_total_properties_owned", "n_vacant_properties_owned", "negligent_dev"]
        ].head(10)
    )

    return primary_featurelayer
