import unittest

import geopandas as gpd
from shapely import Polygon

from new_etl.data_utils.rco_geoms import (
    transform_rco_geoms_gdf,
    transform_merged_rco_geoms_gdf,
)


class TestRcoGeoms(unittest.TestCase):
    def test_transform_rco_geoms_gdf(self):
        data = {
            "organization_name": ["Org 1", "Org 2", "Org 3"],
            "organization_address": ["31", "34", "56"],
            "primary_email": ["org1@gmail.com", "org2@yahoo.com", "org3@gmail.com"],
            "primary_phone": ["2136758831", "3546754431", "3045678812"],
            "geometry": [
                Polygon([(0, 0), (1, 0), (0, 1)]),
                Polygon([(1, 0), (1, 1), (2, 1)]),
                Polygon([(2, 2), (1, 2), (1, 3)]),
            ],
        }
        rco_geoms_gdf = gpd.GeoDataFrame(data, geometry="geometry")

        rco_aggregate_cols = [
            "organization_name",
            "organization_address",
            "primary_email",
            "primary_phone",
        ]

        rco_use_cols = ["rco_info", "rco_names", "geometry"]

        transformed_gdf = transform_rco_geoms_gdf(
            rco_geoms_gdf, rco_aggregate_cols, rco_use_cols
        )

        self.assertEqual(transformed_gdf.columns.tolist(), rco_use_cols)
        self.assertTrue(
            all([type(entry) is str for entry in transformed_gdf["rco_info"].tolist()])
        )

    def test_transform_merged_rco_geom_gdf(self):
        rco_use_cols = ["rco_info", "rco_names", "geometry"]

        data = {
            "opa_id": ["001123", "004435", "04531", None, "001123"],
            "rco_info": ["Info 1", "Info 2", "Info 3", "Info 4", "Info 5"],
            "rco_names": ["Name 1", "Name 2", "Name 3", "Name 4", "Name 5"],
            "geometry": [
                Polygon([(0, 0), (2, 0), (2, 2), (0, 2)]),
                Polygon([(1, 0), (2, 0), (2, 2), (0, 2)]),
                Polygon([(0, 0), (2, 0), (1, 1)]),
                Polygon([(3, 4), (3, 2), (5, 4)]),
                Polygon([(0, 1), (1, 0), (1, 1)]),
            ],
        }
        gdf = gpd.GeoDataFrame(data, geometry="geometry")

        transformed_gdf = transform_merged_rco_geoms_gdf(gdf, rco_use_cols)

        print(transformed_gdf.head())

        self.assertEqual(transformed_gdf.shape[0], 4)
        self.assertIn("opa_id", transformed_gdf.columns)
        self.assertListEqual(
            sorted(transformed_gdf["opa_id"].tolist()),
            ["", "001123", "004435", "04531"],
        )
        # Add check that geometry of repeated opa_id is the first one


if __name__ == "__main__":
    unittest.main()
