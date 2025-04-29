import unittest

import geopandas as gpd

from new_etl.classes.featurelayer import FeatureLayer
from new_etl.data_utils.priority_level import priority_level


class TestPriorityLevel(unittest.TestCase):
    def test_priority_level(self):
        pass
        """
            Test the functionality of the priority_level service that generates a new column for the 
            dataset on the basis of some branching logic in existing column values in the corresponding row 
            (see priority_level function for more details).
            """
        data = {
            "gun_crimes_density_zscore": [-0.5, 1.1, 0.5, 2.1, 0.4],
            "all_violations_past_year": [3, 2, 0, 0, 5],
            "l_and_i_complaints_density_zscore": [0, 0.1, 2.1, -1, 0.3],
            "tree_canopy_gap": [0.1, 0, 0.4, 0.5, 0.2],
            "phs_care_program": [
                None,
                "Trees for Watersheds",
                "Rain Check",
                "Trees for Watersheds",
                None,
            ],
        }

        gdf = gpd.GeoDataFrame(data)
        feature_layer = FeatureLayer(name="test", gdf=gdf)

        priority_level_feature_layer = priority_level(feature_layer)
        expected_gdf = gdf.copy()
        expected_gdf["priority_level"] = [
            "Low",
            "High",
            "Medium",
            "High",
            "Medium",
        ]

        assert expected_gdf.equals(priority_level_feature_layer.gdf)


if __name__ == "__main__":
    unittest.main()
