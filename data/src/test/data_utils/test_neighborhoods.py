import unittest

import geopandas as gpd
from shapely.geometry import Polygon

from config.config import USE_CRS
from new_etl.data_utils.nbhoods import transform_neighborhoods_gdf


class TestNeighborhoods(unittest.TestCase):
    def test_transform_neighborhoods_gdf(self):
        data = {
            "MAPNAME": ["Callowhill", "Bartram's Garden", "Fishtown"],
            "removed_field": ["First", "Second", "Third"],
            "geometry": [
                Polygon([(0, 0), (1, 0), (1, 1)]),
                Polygon([(3, 1), (3, 5), (0, 2), (0, 0)]),
                Polygon([(2, 2), (2, 1), (0, 0)]),
            ],
        }
        gdf = gpd.GeoDataFrame()
        gdf = gpd.GeoDataFrame(data, geometry="geometry")

        # Run transformation which mutates result in place
        result = gdf.copy()
        result.crs = USE_CRS
        transformed_gdf = transform_neighborhoods_gdf(result)

        self.assertEquals(
            ["neighborhood", "geometry"], transformed_gdf.columns.tolist()
        )
        self.assertEquals(
            transformed_gdf["neighborhood"].tolist(),
            ["Callowhill", "Bartram's Garden", "Fishtown"],
        )
        self.assertTrue(all(transformed_gdf.geometry.is_valid))
        self.assertTrue(
            all(transformed_gdf.geometry.type.isin(["Polygon", "Multipolygon"]))
        )


if __name__ == "__main__":
    unittest.main()
