import pandas as pd
import datetime
from dateutil.parser import parse

six_months_ago = datetime.datetime.now() - datetime.timedelta(days=180)

blight_words = ['weed',
                'rubbish',
                'garbage',
                'tire',
                'debris',
                'clean',
                'waste',
                'vegetation',
                'dumping',
                'scrap',
                'auto',
                'vehicle',
                'graffiti',
                'dangerous',
                ]


def access_process(dataset):
    access_processes = []
    for idx, row in dataset.gdf.iterrows():
        access_process = ""

        # Decision Points
        city_owner_agency_is_plb = row["city_owner_agency"] == 'PLB'
        sheriff_sale = row["sheriff_sale"] == 'Y'
        sale_price_over_1000 = row["sale_price"] is not None and float(
            row["sale_price"]) > 1000
        li_complaints_lower = str(row["li_complaints"]).lower()
        contains_blight_word = any(
            word in li_complaints_lower for word in blight_words)

        try:
            sale_date = parse(row["sale_date"])
            sale_date_6_months_ago = sale_date >= six_months_ago
        except (TypeError, ValueError):
            sale_date_6_months_ago = False

        if city_owner_agency_is_plb:
            # City Agency Owner is PLB
            access_process = "Land Bank"
        else:
            if sale_date_6_months_ago:
                if sheriff_sale:
                    if sale_price_over_1000:
                        access_process = "Private Land Use Agreement"
                    else:
                        access_process = "Buy Property"
                else:
                    if contains_blight_word:
                        access_process = "Conservatorship"
                    else:
                        if sale_price_over_1000:
                            access_process = "Private Land Use Agreement"
                        else:
                            access_process = "Buy Property"
            else:
                if sale_price_over_1000:
                    access_process = "Private Land Use Agreement"
                else:
                    access_process = "Buy Property"

        access_processes.append(access_process)

    dataset.gdf["access_process"] = access_processes
    return dataset
