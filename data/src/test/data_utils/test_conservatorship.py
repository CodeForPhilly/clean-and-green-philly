import unittest

import geopandas as gpd

from new_etl.classes.featurelayer import FeatureLayer
from new_etl.data_utils.conservatorship import conservatorship


class TestConservatorship(unittest.TestCase):
    def test_conservatorship(self):
        data = {
            "city_owner_agency": [
                "Land Bank (PHDC)",
                "PRA",
                None,
                "City of Philadelphia",
                "PRA",
            ],
            "sheriff_sale": ["Y", "N", "N", "N", "Y"],
            "market_value": [2000, 500, 800, 200, 1000],
            "all_violations_past_year": [5, 0, 2, 1, None],
            "sale_date": ["2020-01-01", "2021-03-10", "2024-09-30", "2004-09-10", None],
        }
        gdf = gpd.GeoDataFrame(data)
        feature_layer = FeatureLayer(name="test", gdf=gdf)

        conservatorship_feature_layer = conservatorship(feature_layer)
        expected_gdf = gdf.copy()
        expected_gdf["conservatorship"] = ["No", "No", "Yes", "Yes", "No"]

        assert expected_gdf.equals(conservatorship_feature_layer.gdf)


if __name__ == "__main__":
    unittest.main()
