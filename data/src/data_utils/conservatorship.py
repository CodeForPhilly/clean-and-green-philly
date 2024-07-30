import datetime
from dateutil.parser import parse
import pytz

est = pytz.timezone("US/Eastern")
six_months_ago = (datetime.datetime.now() - datetime.timedelta(days=180)).astimezone(
    est
)

blight_words = [
    "weed",
    "rubbish",
    "garbage",
    "tire",
    "debris",
    "clean",
    "waste",
    "vegetation",
    "dumping",
    "scrap",
    "auto",
    "vehicle",
    "graffiti",
    "dangerous",
]


def conservatorship(primary_featurelayer):
    conservatorships = []

    for idx, row in primary_featurelayer.gdf.iterrows():
        city_owner_agency = row["city_owner_agency"]
        sheriff_sale = row["sheriff_sale"] == "Y"
        market_value_over_1000 = (
            row["market_value"] and float(row["market_value"]) > 1000
        )
        li_complaints_lower = str(row["li_complaints"]).lower().split(" ")
        contains_blight_word = any(word in li_complaints_lower for word in blight_words)

        try:
            sale_date = parse(row["sale_date"]).astimezone(est)
            sale_date_6_months_ago = sale_date <= six_months_ago
        except (TypeError, ValueError):
            sale_date_6_months_ago = False

        # Simplified decision logic
        if city_owner_agency == "PLB" or (
            not sale_date_6_months_ago and market_value_over_1000
        ):
            conservatorship = "No"
        elif contains_blight_word and not sheriff_sale and sale_date_6_months_ago:
            conservatorship = "Yes"
        else:
            conservatorship = "No"

        conservatorships.append(conservatorship)

    primary_featurelayer.gdf["conservatorship"] = conservatorships
    return primary_featurelayer
