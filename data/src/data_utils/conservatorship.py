import datetime

import geopandas as gpd
import pytz
from dateutil.parser import parse

from src.validation.base import validate_output
from src.validation.conservatorship import ConservatorshipOutputValidator

from ..metadata.metadata_utils import provide_metadata

est = pytz.timezone("US/Eastern")
six_months_ago = (datetime.datetime.now() - datetime.timedelta(days=180)).astimezone(
    est
)


@provide_metadata()
@validate_output(ConservatorshipOutputValidator)
def conservatorship(input_gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """
    Determines conservatorship eligibility for properties in a feature layer.

    Args:
        primary_featurelayer (FeatureLayer): A feature layer containing property data in a GeoDataFrame (`gdf`).

    Columns Added:
        conservatorship (str): Indicates whether each property qualifies for conservatorship ("Yes" or "No").

    Primary Feature Layer Columns Referenced:
        city_owner_agency, sheriff_sale, market_value, all_violations_past_year, sale_date

    Tagline:
        Identify conservatorship-eligible properties

    Returns:
        FeatureLayer: The input feature layer with an added "conservatorship" column indicating
        whether each property qualifies for conservatorship ("Yes" or "No").
    """
    conservatorships = []

    for idx, row in input_gdf.iterrows():
        city_owner_agency = row["city_owner_agency"]
        sheriff_sale = row["sheriff_sale"] == "Y"
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
            conservatorship = "No"
        elif violations_exist and not sheriff_sale and sale_date_6_months_ago:
            conservatorship = "Yes"
        else:
            conservatorship = "No"

        conservatorships.append(conservatorship)

    input_gdf["conservatorship"] = conservatorships
    return input_gdf
