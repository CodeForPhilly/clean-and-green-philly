import unittest

import geopandas as gpd
from shapely.geometry import Polygon

from new_etl.data_utils.nbhoods import transform_neighborhoods_gdf


class TestNeighborhoods(unittest.TestCase):
    def test_transform_neighborhoods_gdf(self):
        data = {
            "MAPNAME": ["Callowhill", "Bartram's Garden", "Fishtown"],
            "removed_field": ["First", "Second", "Third"],
            "geometry": [
                Polygon([(0, 0), (1, 0), (1, 1)]),
                Polygon([(3, 1), (3, 5), (0, 2), (5, 4)]),
                Polygon([(2, 2), (2, 1), (0, 0)]),
            ],
        }
        gdf = gpd.GeoDataFrame()
        gdf = gpd.GeoDataFrame(data, geometry="geometry")

        # Run transformation which mutates result in place
        result = gdf.copy()
        transform_neighborhoods_gdf(result)

        self.assertEquals(["neighborhood", "geometry"], result.columns)
        self.assertEquals(
            result["neighborhood"].tolist(),
            ["Callowhill", "Bartram's Garden", "Fishtown"],
        )
        self.assertTrue(all(result.geometry.is_valid))
        self.assertTrue(all(result.geometry.type.isin(["Polygon", "Multipolygon"])))


if __name__ == "__main__":
    unittest.main()
