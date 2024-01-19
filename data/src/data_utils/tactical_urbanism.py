import pandas as pd


def tactical_urbanism(dataset):
    tactical_urbanism_values = []

    for idx, row in dataset.gdf.iterrows():
        tactical_urbanism = "No"

        if (row["parcel_type"] == "Land" and
            row["unsafe_building"] == "N" and
                row["imm_dang_building"] == "N"):
            tactical_urbanism = "Yes"

        tactical_urbanism_values.append(tactical_urbanism)

    dataset.gdf["tactical_urbanism"] = tactical_urbanism_values
    return dataset
