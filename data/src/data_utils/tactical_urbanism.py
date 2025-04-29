def tactical_urbanism(dataset):
    unsafe_words = [
        "dangerous",
    ]

    tactical_urbanism_values = []

    for _, row in dataset.gdf.iterrows():
        li_complaints_lower = str(row["li_complaints"]).lower().split(" ")
        contains_unsafe_word = any(word in li_complaints_lower for word in unsafe_words)

        if (
            row["parcel_type"] == "Land"
            and row["unsafe_building"] == "N"
            and row["imm_dang_building"] == "N"
            and not contains_unsafe_word
        ):
            tactical_urbanism = "Yes"
        else:
            tactical_urbanism = "No"

        tactical_urbanism_values.append(tactical_urbanism)

    dataset.gdf["tactical_urbanism"] = tactical_urbanism_values
    return dataset
