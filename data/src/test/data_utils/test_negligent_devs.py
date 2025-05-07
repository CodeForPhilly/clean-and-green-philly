import unittest

import geopandas as gpd

from new_etl.classes.featurelayer import FeatureLayer
from new_etl.data_utils.negligent_devs import negligent_devs


class TestNegligentDevs(unittest.TestCase):
    def test_negligent_devs(self):
        """
        Test the functionality of the negligent_devs service that generates new columns on the dataset relating to the number of properties owned
        and vacant properties owned under one standardized address as well as a classification of the owner type as negligent based on the vacant number.
        """
        data = {
            "opa_id": ["0011", "0012", "0013", "0014", "0015", "0000", "0001", "0032"],
            "vacant": [True, True, True, True, True, False, True, True],
            "city_owner_agency": [
                None,
                None,
                None,
                None,
                None,
                "City of Philadelphia",
                "City of Philadelphia",
                "PRA",
            ],
            "standardized_address": ["1", "1", "1", "1", "1", "6", "6", "8"],
        }
        gdf = gpd.GeoDataFrame(data)
        feature_layer = FeatureLayer(name="test", gdf=gdf)
        # need to add primary merge data
        negligent_devs_feature_layer = negligent_devs(feature_layer)
        expected_gdf = gdf.copy()
        expected_gdf["n_total_properties_owned"] = [5, 5, 5, 5, 5, 2, 2, 1]
        expected_gdf["n_vacant_properties_owned"] = [5, 5, 5, 5, 5, 1, 1, 1]
        expected_gdf["negligent_dev"] = [
            True,
            True,
            True,
            True,
            True,
            False,
            False,
            False,
        ]

        assert expected_gdf.equals(negligent_devs_feature_layer.gdf)


if __name__ == "__main__":
    unittest.main()
