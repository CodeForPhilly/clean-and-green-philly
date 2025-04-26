import unittest

import geopandas as gpd

from new_etl.classes.featurelayer import FeatureLayer
from new_etl.data_utils.rco_geoms import (
    transform_rco_geoms_gdf,
    transform_merged_rco_geoms_gdf,
)


class TestRcoGeoms(unittest.TestCase):
    def test_transform_rco_geoms_gdf(self):
        data = {}
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

        data = {}
        gdf = gpd.GeoDataFrame(data, geometry="geometry")

        transformed_gdf = transform_merged_rco_geoms_gdf(gdf, rco_use_cols)


if __name__ == "__main__":
    unittest.main()
