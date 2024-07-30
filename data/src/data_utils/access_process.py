def access_process(dataset):
    access_processes = []

    for _, row in dataset.gdf.iterrows():
        # Decision Points
        city_owner_agency = row["city_owner_agency"]
        market_value_over_1000 = (
            row["market_value"] and float(row["market_value"]) > 1000
        )

        # Simplified decision logic
        if city_owner_agency == "PLB":
            access_process = "Land Bank"
        elif city_owner_agency in ["PRA", "PHDC"]:
            access_process = "Do Nothing"
        else:
            if market_value_over_1000:
                access_process = "Private Land Use Agreement"
            else:
                access_process = "Buy Property"

        access_processes.append(access_process)

    dataset.gdf["access_process"] = access_processes
    return dataset
