from typing import Any

import pandas as pd

from new_etl.metadata.metadata_utils import provide_metadata
from new_etl.validators.access_process_validator import validate_access_process


@provide_metadata()
@validate_access_process
def access_process(dataset: Any) -> Any:
    """
    Process a dataset to determine the access process for each property based on
    city ownership and market value. The result is added as a new column in the dataset.
    Non-vacant properties will have NA for access_process.

    Args:
        dataset (Any): The dataset containing a GeoDataFrame named `gdf` with
                       columns "city_owner_agency", "market_value", and "vacant".

    Returns:
        Any: The updated dataset with an additional "access_process" column.

    Tagline:
        Assigns access processes

    Columns added:
        access_process (str): The access process for each property based on city ownership and market value.
                            Will be NA for non-vacant properties.

    Primary Feature Layer Columns Referenced:
        city_owner_agency, market_value, vacant

    Side Effects:
        Prints the distribution of the "access_process" column.
    """
    access_processes = []

    for _, row in dataset.gdf.iterrows():
        # If property is not vacant, set access_process to NA
        if not row.get("vacant", False):
            access_processes.append(pd.NA)
            continue

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
