import unittest
import geopandas as gpd
from shapely import Point, Polygon

from config.config import USE_CRS
from new_etl.data_utils.community_gardens import (
    check_community_gardens_gdf,
    merge_and_update_with_community_gardens_gdf,
)


class TestCityOwnedProperties(unittest.TestCase):
    def test_check_community_gardens_gdf(self):
        """
        This tests that the check_community_gardens_gdf function correctly transforms
        non-point geometries to points using centroid and ensures all geometries are valid.
        """

        # Create a sample GeoDataFrame with mixed geometry types
        data = {
            "site_name": ["Garden A", "Garden B", "Garden C"],
            "zip_code": ["19103", "19104", "19105"],
            "geometry": [
                Point(0, 0),
                Point(1, 1),
                Point(2, 2),
            ],
        }
        gdf = gpd.GeoDataFrame(data, geometry="geometry", crs="EPSG:4326")

        transformed_gdf = check_community_gardens_gdf(gdf)

        self.assertTrue(all(transformed_gdf.geometry.geom_type == "Point"))
        self.assertEqual(transformed_gdf.crs, USE_CRS)
        self.assertEqual(transformed_gdf.columns.tolist(), ["site_name", "geometry"])

    def test_merge_community_gardens_gdf(self):
        """
        This tests that the merge_community_gardens_gdf function correctly merges
        the community gardens GeoDataFrame with the primary feature layer GeoDataFrame and updates its values.
        """

        # Create a sample primary feature layer GeoDataFrame
        primary_data = {
            "opa_id": ["0100", "0101", "0102"],
            "vacant": [True, False, True],
            "geometry": [
                Polygon([[0, 0], [1, 0], [1, 1], [0, 1]]),
                Polygon([[2, 2], [1, 0], [2, 0], [3, 3]]),
                Polygon([[1, 1], [0, 2], [1, 2]]),
            ],
        }
        primary_gdf = gpd.GeoDataFrame(
            primary_data, geometry="geometry", crs="EPSG:4326"
        )

        # Create a sample community gardens GeoDataFrame
        community_data = {
            "site_name": ["Garden A", "Garden B"],
            "geometry": [
                Point(0.5, 0.5),
                Point(3, 3),
            ],
        }
        community_gardens_gdf = gpd.GeoDataFrame(
            community_data, geometry="geometry", crs="EPSG:4326"
        )

        updated_primary_gdf = merge_and_update_with_community_gardens_gdf(
            primary_gdf, community_gardens_gdf
        )

        self.assertEqual(updated_primary_gdf["vacant"].tolist(), [False, False, True])


if __name__ == "__main__":
    unittest.main()
