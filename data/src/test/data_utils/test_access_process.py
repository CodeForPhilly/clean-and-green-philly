import unittest

import geopandas as gpd

from new_etl.classes.featurelayer import FeatureLayer
from new_etl.data_utils.access_process import access_process


class TestAccessProcess(unittest.TestCase):
    def test_access_process(self):
        """
        Test the functionality of the access_process service that generates a new column for the dataset
        on the basis of existing values in the corresponding row for city_owner_agency and market_value.
        """
        # Create test data
        data = {
            "city_owner_agency": [
                "Land Bank (PHDC)",
                "PRA",
                None,
                "City of Philadelphia",
                None,
            ],
            "market_value": [1500, 500, 2000, None, None],
        }
        gdf = gpd.GeoDataFrame(data)
        feature_layer = FeatureLayer(name="test", gdf=gdf)

        access_process_feature_layer = access_process(feature_layer)
        expected_gdf = gdf.copy()
        expected_gdf["access_process"] = [
            "Go through Land Bank",
            "Do Nothing",
            "Private Land Use Agreement",
            "Buy Property",
            "Buy Property",
        ]

        assert expected_gdf.equals(access_process_feature_layer.gdf)


if __name__ == "__main__":
    unittest.main()
