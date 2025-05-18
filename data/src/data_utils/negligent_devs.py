import re

import pandas as pd

replacements = {
    "STREET": "ST",
    "AVENUE": "AVE",
    "ROAD": "RD",
    "BOULEVARD": "BLVD",
    "PLACE": "PL",
    "FLOOR": "FL",
    "FLR": "FL",
    "FIRST": "1ST",
    "SECOND": "2ND",
    "THIRD": "3RD",
    "FOURTH": "4TH",
    "FIFTH": "5TH",
    "SIXTH": "6TH",
    "SEVENTH": "7TH",
    "EIGHTH": "8TH",
    "NINTH": "9TH",
    "NORTH": "N",
    "SOUTH": "S",
    "EAST": "E",
    "WEST": "W",
    "SUITE": "STE",
    "LA": "LN",
    "LANE": "LN",
    "PARKWAY": "PKY",
}


def standardize_street(street):
    if not isinstance(street, str):
        return ""
    for full, abbr in replacements.items():
        street = re.sub(r"\b{}\b".format(full), abbr, street, flags=re.IGNORECASE)
    return street


def create_standardized_mailing_address(row):
    parts = [
        row["mailing_address_1"].strip()
        if pd.notnull(row["mailing_address_1"])
        else "",
        row["mailing_address_2"].strip()
        if pd.notnull(row["mailing_address_2"])
        else "",
        row["mailing_street"].strip() if pd.notnull(row["mailing_street"]) else "",
        row["mailing_city_state"].strip()
        if pd.notnull(row["mailing_city_state"])
        else "",
        row["mailing_zip"].strip() if pd.notnull(row["mailing_zip"]) else "",
    ]
    standardized_mailing_address = ", ".join([part for part in parts if part])
    return standardized_mailing_address.lower()


def negligent_devs(primary_featurelayer):
    devs = primary_featurelayer.gdf

    print("Columns in 'devs' DataFrame:", devs.columns)

    print("Initial properties data:")
    print(devs[["opa_id", "city_owner_agency", "mailing_street"]].head(10))

    city_owners = devs.loc[
        ~devs["city_owner_agency"].isna() & (devs["city_owner_agency"] != "")
    ].copy()
    non_city_owners = devs.loc[
        devs["city_owner_agency"].isna() | (devs["city_owner_agency"] == "")
    ].copy()

    print(
        f"City owners shape: {city_owners.shape}, Non-city owners shape: {non_city_owners.shape}"
    )

    # Log before standardizing addresses
    print("Non-city owners mailing streets before standardization:")
    print(non_city_owners[["opa_id", "mailing_street"]].head(10))

    non_city_owners.loc[:, "mailing_street"] = (
        non_city_owners["mailing_street"].astype(str).apply(standardize_street)
    )

    print("Non-city owners mailing streets after standardization:")
    print(non_city_owners[["opa_id", "mailing_street"]].head(10))

    for term in ["ST", "AVE", "RD", "BLVD"]:
        non_city_owners.loc[:, "mailing_street"] = non_city_owners[
            "mailing_street"
        ].replace(regex={f"{term}.*": term})

    # Log after applying term replacement
    print("Non-city owners mailing streets after term replacement:")
    print(non_city_owners[["opa_id", "mailing_street"]].head(10))

    # Fill missing address components
    non_city_owners.loc[:, "mailing_address_1"] = non_city_owners[
        "mailing_address_1"
    ].fillna("")
    non_city_owners.loc[:, "mailing_address_2"] = non_city_owners[
        "mailing_address_2"
    ].fillna("")
    non_city_owners.loc[:, "mailing_street"] = non_city_owners["mailing_street"].fillna(
        ""
    )
    non_city_owners.loc[:, "mailing_city_state"] = non_city_owners[
        "mailing_city_state"
    ].fillna("")
    non_city_owners.loc[:, "mailing_zip"] = non_city_owners["mailing_zip"].fillna("")

    # Log addresses before creating standardized address
    print("Non-city owners mailing details before creating standardized address:")
    print(
        non_city_owners[
            ["opa_id", "mailing_street", "mailing_city_state", "mailing_zip"]
        ].head(10)
    )

    non_city_owners.loc[:, "standardized_mailing_address"] = non_city_owners.apply(
        create_standardized_mailing_address, axis=1
    )

    # Log standardized addresses and counts
    print("Standardized addresses with counts:")
    address_counts = (
        non_city_owners.groupby("standardized_mailing_address")
        .size()
        .reset_index(name="property_count")
    )
    print(address_counts.head(10))

    sorted_address_counts = address_counts.sort_values(
        by="property_count", ascending=False
    )
    print("Top standardized addresses by property count:")
    print(sorted_address_counts.head(10))

    non_city_owners = non_city_owners.merge(
        sorted_address_counts, on="standardized_mailing_address", how="left"
    )

    # Log merged data for city owners
    city_owner_counts = (
        city_owners.groupby("city_owner_agency")
        .size()
        .reset_index(name="property_count")
    )
    print("City owner counts:")
    print(city_owner_counts.head(10))

    city_owners = city_owners.merge(
        city_owner_counts, on="city_owner_agency", how="left"
    )

    devs_combined = pd.concat([city_owners, non_city_owners], axis=0)

    # Final check on the merged data before updating primary_featurelayer
    print("Combined data with property counts:")
    print(devs_combined[["opa_id", "property_count"]].head(10))

    primary_featurelayer.gdf = primary_featurelayer.gdf.merge(
        devs_combined[["opa_id", "property_count"]], on="opa_id", how="left"
    )
    primary_featurelayer.gdf.rename(
        columns={"property_count": "n_properties_owned"}, inplace=True
    )
    primary_featurelayer.gdf.loc[:, "negligent_dev"] = (
        primary_featurelayer.gdf["n_properties_owned"] > 5
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
