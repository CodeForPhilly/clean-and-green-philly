import pandas as pd
import pytest
from shapely.geometry import Point


@pytest.fixture
def base_test_data():
    """Base test data that can be reused across different validator tests."""
    return pd.DataFrame(
        {
            "opa_id": ["351243200", "351121400", "212525650"],
            "market_value": [144800, 158800, 382000],
            "sale_price": [37000.0, 79900.0, 1.0],
            "sale_date": [
                pd.Timestamp("2012-05-15 00:00:00+0000", tz="UTC"),
                pd.Timestamp("2012-05-23 00:00:00+0000", tz="UTC"),
                pd.Timestamp("2012-06-01 00:00:00+0000", tz="UTC"),
            ],
            "zip_code": ["19124", "19124", "19128"],
            "zoning": ["RSA5", "RSA5", "RMX1"],
            "standardized_street_address": [
                "936 carver st",
                "882 marcella st",
                "9120 ayrdale crescent",
            ],
            "standardized_mailing_address": [
                "5956 harbison ave, philadelphia pa, 19135",
                "882 marcella st, philadelphia pa, 19124-1733",
                "9120 ayrdalecrescent st, philadelphia pa, 19128-1027",
            ],
            "owner_1": [
                "SKYLUCK HORIZON REALTY IN",
                "PRESLEY MARY",
                "AMOROSO JOSEPH A JR",
            ],
            "owner_2": [None, None, "AMOROSO JACQUELINE MARIA"],
            "building_code_description": [
                "ROW B/GAR 2 STY MASONRY",
                "ROW B/GAR 2 STY MASONRY",
                "ROW W/GAR 3 STY MASONRY",
            ],
            "geometry": [
                Point(-75.089, 40.033),
                Point(-75.093, 40.031),
                Point(-75.244, 40.072),
            ],
        }
    )


@pytest.fixture
def empty_dataframe():
    """Empty dataframe with required columns."""
    return pd.DataFrame(
        columns=[
            "opa_id",
            "market_value",
            "sale_price",
            "zip_code",
            "zoning",
            "geometry",
        ]
    )
