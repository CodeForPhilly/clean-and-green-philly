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


def create_standardized_address(row):
    parts = [
        row["mailing_address_1"].strip(),
        row["mailing_address_2"].strip(),
        row["mailing_street"].strip(),
        row["mailing_city_state"].strip(),
        row["mailing_zip"].strip(),
    ]
    standardized_address = ", ".join(part for part in parts if part)
    return standardized_address.lower()


def negligent_devs(primary_featurelayer):
    devs = primary_featurelayer.gdf
    city_owners = devs[~devs["city_owner_agency"].isna()]
    non_city_owners = devs[devs["city_owner_agency"].isna()]

    non_city_owners["mailing_street"] = (
        non_city_owners["mailing_street"].astype(str).apply(standardize_street)
    )
    for term in ["ST", "AVE", "RD", "BLVD"]:
        non_city_owners["mailing_street"] = non_city_owners["mailing_street"].replace(
            regex={f"{term}.*": term}
        )
    non_city_owners["mailing_address_1"] = non_city_owners["mailing_address_1"].fillna(
        ""
    )
    non_city_owners["mailing_address_2"] = non_city_owners["mailing_address_2"].fillna(
        ""
    )
    non_city_owners["mailing_street"] = non_city_owners["mailing_street"].fillna("")
    non_city_owners["mailing_city_state"] = non_city_owners[
        "mailing_city_state"
    ].fillna("")
    non_city_owners["mailing_zip"] = non_city_owners["mailing_zip"].fillna("")

    non_city_owners["standardized_address"] = non_city_owners.apply(
        create_standardized_address, axis=1
    )

    address_counts = (
        non_city_owners.groupby("standardized_address")
        .size()
        .reset_index(name="property_count")
    )
    sorted_address_counts = address_counts.sort_values(
        by="property_count", ascending=False
    )

    non_city_owners = non_city_owners.merge(
        sorted_address_counts, on="standardized_address", how="left"
    )

    city_owner_counts = (
        city_owners.groupby("city_owner_agency")
        .size()
        .reset_index(name="property_count")
    )
    city_owners = city_owners.merge(
        city_owner_counts, on="city_owner_agency", how="left"
    )

    devs_combined = pd.concat([city_owners, non_city_owners], axis=0)
    primary_featurelayer.gdf = primary_featurelayer.gdf.merge(
        devs_combined[["opa_id", "property_count"]], on="opa_id", how="left"
    )
    primary_featurelayer.gdf.rename(
        columns={"property_count": "n_properties_owned"}, inplace=True
    )
    primary_featurelayer.gdf["negligent_dev"] = (
        primary_featurelayer.gdf["n_properties_owned"] > 5
    ) & (primary_featurelayer.gdf["city_owner_agency"].isna())

    return primary_featurelayer
