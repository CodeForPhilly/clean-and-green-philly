import datetime
from typing import Tuple

import geopandas as gpd
import pytz
from dateutil.parser import parse

from src.validation.base import ValidationResult, validate_output
from src.validation.conservatorship import ConservatorshipOutputValidator

est = pytz.timezone("US/Eastern")
six_months_ago = (datetime.datetime.now() - datetime.timedelta(days=180)).astimezone(
    est
)


@validate_output(ConservatorshipOutputValidator)
def conservatorship(
    input_gdf: gpd.GeoDataFrame,
) -> Tuple[gpd.GeoDataFrame, ValidationResult]:
    """
    Determines conservatorship eligibility for properties in a GeoDataFrame.

    Args:
        input_gdf (GeoDataFrame): A GeoDataFrame containing property data in a GeoDataFrame (`gdf`).

    Columns Added:
        conservatorship (bool): Indicates whether each property qualifies for conservatorship (True or False).

    Columns Referenced:
        city_owner_agency, sheriff_sale, market_value, all_violations_past_year, sale_date

    Tagline:
        Identify conservatorship-eligible properties

    Returns:
        GeoDataFrame: The input GeoDataFrame with an added "conservatorship" column indicating
        whether each property qualifies for conservatorship (True or False).
    """
    conservatorships = []

    for idx, row in input_gdf.iterrows():
        city_owner_agency = row["city_owner_agency"]
        sheriff_sale = row["sheriff_sale"]  # Now boolean
        market_value_over_1000 = (
            row["market_value"] and float(row["market_value"]) > 1000
        )
        violations_exist = float(row["all_violations_past_year"]) > 0

        try:
            sale_date = parse(row["sale_date"]).astimezone(est)
            sale_date_6_months_ago = sale_date <= six_months_ago
        except (TypeError, ValueError):
            sale_date_6_months_ago = False

        # Simplified decision logic
        if city_owner_agency == "Land Bank (PHDC)" or (
            not sale_date_6_months_ago and market_value_over_1000
        ):
            conservatorship = False
        elif violations_exist and not sheriff_sale and sale_date_6_months_ago:
            conservatorship = True
        else:
            conservatorship = False

        conservatorships.append(conservatorship)

    input_gdf["conservatorship"] = conservatorships
    return input_gdf, ValidationResult(True)
