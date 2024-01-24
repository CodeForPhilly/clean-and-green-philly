import pandas as pd


def llc_owner(primary_featurelayer):
    llc_owners = []

    for _, row in primary_featurelayer.gdf.iterrows():
        # Extracting owner1 and owner2 from the row
        owner1 = str(row["owner_1"]).lower()
        owner2 = str(row["owner_2"]).lower()

        # Checking if " llc" is in either owner1 or owner2
        if " llc" in owner1 or " llc" in owner2:
            llc_owners.append("Yes")
        else:
            llc_owners.append("No")

    primary_featurelayer.gdf["llc_owner"] = llc_owners
    return primary_featurelayer
