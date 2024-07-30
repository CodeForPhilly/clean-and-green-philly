def negligent_devs(primary_featurelayer):
    devs = primary_featurelayer.gdf

    devs = devs[devs["city_owner_agency"].isna()]

    devs["full_mailing_address"] = (
        devs["mailing_address_1"].str.strip()
        + ", "
        + devs["mailing_street"].str.strip()
        + ", "
        + devs["mailing_city_state"].str.strip()
        + ", "
        + devs["mailing_zip"].str.strip()
    )

    devs["standardized_address"] = devs["full_mailing_address"].str.lower().str.strip()

    address_counts = (
        devs.groupby("standardized_address").size().reset_index(name="property_count")
    )

    sorted_address_counts = address_counts.sort_values(
        by="property_count", ascending=False
    )

    devs = devs.merge(sorted_address_counts, on="standardized_address", how="left")

    primary_featurelayer.gdf = primary_featurelayer.gdf.merge(
        devs[["opa_id", "property_count"]], on="opa_id", how="left"
    )

    primary_featurelayer.gdf.rename(
        columns={"property_count": "n_properties_owned"}, inplace=True
    )

    primary_featurelayer.gdf["negligent_dev"] = (
        primary_featurelayer.gdf["n_properties_owned"] > 5
    )

    return primary_featurelayer
