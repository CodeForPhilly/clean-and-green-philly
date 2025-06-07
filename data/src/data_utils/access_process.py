from typing import Any

from src.metadata.metadata_utils import provide_metadata


@provide_metadata()
def access_process(dataset: Any) -> Any:
    """
    Process a dataset to determine the access process for each property based on
    city ownership and market value. The result is added as a new column in the dataset.

    Args:
        dataset (Any): The dataset containing a GeoDataFrame named `gdf` with
                       columns "city_owner_agency" and "market_value".

    Returns:
        Any: The updated dataset with an additional "access_process" column.

    Tagline:
        Assigns access processes

    Columns added:
        access_process (str): The access process for each property based on city ownership and market value.

    Primary Feature Layer Columns Referenced:
        city_owner_agency, market_value

    Side Effects:
        Prints the distribution of the "access_process" column.
    """
    access_processes = []

    for _, row in dataset.gdf.iterrows():
        # Decision Points
        city_owner_agency = row["city_owner_agency"]
        market_value_over_1000 = (
            row["market_value"] and float(row["market_value"]) > 1000
        )

        # Simplified decision logic
        if city_owner_agency == "Land Bank (PHDC)":
            access_process = "Go through Land Bank"
        elif city_owner_agency == "PRA":
            access_process = "Do Nothing"
        else:
            if market_value_over_1000:
                access_process = "Private Land Use Agreement"
            else:
                access_process = "Buy Property"

        access_processes.append(access_process)

    dataset.gdf["access_process"] = access_processes

    return dataset
