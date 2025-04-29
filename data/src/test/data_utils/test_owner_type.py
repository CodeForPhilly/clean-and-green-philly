import unittest

import geopandas as gpd

from new_etl.classes.featurelayer import FeatureLayer
from new_etl.data_utils.owner_type import owner_type


class TestOwnerType(unittest.TestCase):
    def test_owner_type(self):
        """
        Test the functionality of the owner_type service that generates a new column for the dataset
        on the basis of existing ownership and opa_id data in the corresponding row.
        """
        data = {
            "owner_1": ["John Smith", None, "Costco llc", "Jeff Roe"],
            "owner_2": ["Jane Doe", "Tom Hink", "Sixers", "Jefferson llc"],
            "city_owner_agency": [None, "City of Philadelphia", "PRA", None],
        }
        gdf = gpd.GeoDataFrame(data)
        feature_layer = FeatureLayer(name="test", gdf=gdf)

        owner_type_feature_layer = owner_type(feature_layer)
        expected_gdf = gdf.copy()
        expected_gdf["owner_type"] = [
            "Individual",
            "Public",
            "Public",
            "Business (LLC)",
        ]

        assert expected_gdf.equals(owner_type_feature_layer.gdf)


if __name__ == "__main__":
    unittest.main()
