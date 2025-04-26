import unittest

import geopandas as gpd

from new_etl.classes.featurelayer import FeatureLayer
from new_etl.data_utils.tactical_urbanism import tactical_urbanism


class TestTacticalUrbanism(unittest.TestCase):
    def test_tactical_urbanism(self):
        data = {
            "parcel_type": ["Land", "Building", "Land", None],
            "unsafe_building": ["N", "Y", "N", "N"],
            "imm_dang_building": ["Y", "N", "N", "Y"],
        }
        gdf = gpd.GeoDataFrame(data)
        feature_layer = FeatureLayer(name="test", gdf=gdf)

        tactical_urbanism_feature_layer = tactical_urbanism(feature_layer)
        expected_gdf = gdf.copy()
        expected_gdf["tactical_urbanism"] = ["No", "Yes", "Yes", "Yes"]

        assert expected_gdf.equals(tactical_urbanism_feature_layer.gdf)


if __name__ == "__main__":
    unittest.main()
