import geopandas as gpd

from src.metadata.metadata_utils import provide_metadata
from src.validation.access_process import AccessProcessOutputValidator
from src.validation.base import validate_output


@provide_metadata()
@validate_output(AccessProcessOutputValidator)
def access_process(dataset: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """
    Process a dataset to determine the access process for each property based on
    city ownership and market value. The result is added as a new column in the dataset.

    Args:
        dataset (GeoDataFrame): The input GeoDataFrame dataset with
        columns "city_owner_agency" and "market_value".

    Returns:
        GeoDataFrame: The updated dataset with an additional "access_process" column.

    Tagline:
        Assigns access processes

    Columns added:
        access_process (str): The access process for each property based on city ownership and market value.

    Primary Feature Layer Columns Referenced:
        city_owner_agency, market_value

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

    for _, row in dataset.iterrows():
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

    dataset["access_process"] = access_processes

    return dataset
