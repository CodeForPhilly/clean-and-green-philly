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
                Point(2710000, 230000),  # Philadelphia coordinates in EPSG:2272
                Point(2715000, 235000),  # Philadelphia coordinates in EPSG:2272
                Point(2720000, 240000),  # Philadelphia coordinates in EPSG:2272
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


@pytest.fixture
def large_test_data():
    """Larger test dataset with realistic distributions for statistical validation tests."""
    return pd.DataFrame(
        {
            "opa_id": [f"35124320{i:02d}" for i in range(30)],  # 30 unique OPA IDs
            "market_value": [150000 + i * 5000 for i in range(30)],
            "sale_price": [80000 + i * 2000 for i in range(30)],
            "sale_date": [
                pd.Timestamp("2012-06-01 00:00:00+0000", tz="UTC")
                + pd.Timedelta(days=i)
                for i in range(30)
            ],
            "zip_code": ["19124", "19125", "19126"]
            * 10,  # Cycle through a few zip codes
            "zoning": ["RSA5", "RMX1", "RSA3"] * 10,  # Cycle through zoning types
            "standardized_street_address": [f"{1000 + i} test st" for i in range(30)],
            "standardized_mailing_address": [
                f"{1000 + i} test st, philadelphia pa, 19124" for i in range(30)
            ],
            "owner_1": [f"TEST OWNER {i}" for i in range(30)],
            "owner_2": [None] * 30,
            "building_code_description": ["ROW B/GAR 2 STY MASONRY"] * 30,
            "geometry": [
                Point(2710000 + i * 1000, 230000 + i * 1000)
                for i in range(30)  # Spread out in Philadelphia
            ],
        }
    )
