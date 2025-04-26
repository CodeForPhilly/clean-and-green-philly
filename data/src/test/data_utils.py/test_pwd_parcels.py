import unittest

import numpy as np
import geopandas as gpd
from shapely.geometry import Point, Polygon, MultiPolygon, LineString

from new_etl.data_utils.pwd_parcels import (
    merge_pwd_parcels_gdf,
    transform_pwd_parcels_gdf,
)


class TestPwcParcels(unittest.TestCase):
    def test_pwd_parcels_merge(self):
        """
        This tests that the merge_pwd_parcels_gdf function correctly retains
        existing point geometries in the primary GeoDataFrame when no better
        geometry is available in the PWD parcels GeoDataFrame.
        """

        parcel_type_sample_data = ["Land", "Building", "Land", "Building"]
        primary_data = {
            "opa_id": ["0100", "0101", "0102", "0103"],
            "geometry": [Point(0, 0), Point(1, 1), Point(2, 2), Point(3, 3)],
            "parcel_type": parcel_type_sample_data,
        }

        # CRS we don't use is chosen since we are just checking it doesn't change:
        test_crs = "EPSG:2002"
        primary_gdf = gpd.GeoDataFrame(primary_data, geometry="geometry", crs=test_crs)

        # Simulate dropped rows by having a gapped index.
        primary_gdf.index = [0, 2, 3, 5]

        # Create pwd_parcels_gdf with a continuous index.
        pwd_data = {
            "opa_id": ["0100", "0101", "0102", "0103"],
            "geometry": [
                np.nan,  # For opa 0100, no better geometry
                MultiPolygon(
                    [Polygon([(10, 10), (20, 10), (20, 20), (10, 20)])]
                ),  # For opa 0101, a multipolygon available
                np.nan,
                np.nan,
            ],
        }
        pwd_gdf = gpd.GeoDataFrame(pwd_data, geometry="geometry")
        assert list(pwd_gdf.index) == list(range(4))  # Continuous index: 0,1,2,3

        # Call the merge function under test.
        merged_gdf = merge_pwd_parcels_gdf(primary_gdf, pwd_gdf)

        # Expected geometries:
        # For opa_id "0010", we expect the multipolygon from pwd_gdf.
        # For the other opa_id's we expect the point geometries from primary_gdf.
        expected_geometries = {
            "0100": primary_gdf.loc[0, "geometry"],
            "0101": pwd_gdf.loc[1, "geometry"],  # pwd geometry used when available
            "0102": primary_gdf.loc[3, "geometry"],
            "0103": primary_gdf.loc[5, "geometry"],
        }

        assert merged_gdf.crs == primary_gdf.crs
        assert merged_gdf.crs == test_crs

        # Verify each row of the merged GeoDataFrame.
        for idx, row in merged_gdf.iterrows():
            opa_id = row["opa_id"]
            actual_geom = row["geometry"]
            expected_geom = expected_geometries[opa_id]
            # Use shapely's equals() to check geometry equivalence.
            assert actual_geom.equals(expected_geom), (
                f"Mismatch for opa_id {opa_id}: "
                f"expected {expected_geom}, got {actual_geom}"
            )

        opa_id_values = ["0100", "0101", "0102", "0103"]
        data = {
            "opa_id": opa_id_values,
            "geometry": [expected_geometries[opa_id] for opa_id in opa_id_values],
            "parcel_type": parcel_type_sample_data,
        }
        expected_df = gpd.GeoDataFrame(
            data=data,
            geometry="geometry",
        )

        assert expected_df.equals(merged_gdf)

    def test_transform_pwd_parcels_gdf_basic(self):
        """
        Check the basic functionality of the transform_pwd_parcels_gdf function.
        This function is expected to mutate the input GeoDataFrame in place.
        It should drop rows with null 'brt_id', rename 'brt_id' to 'opa_id',
        and ensure all geometries are valid polygons or multipolygons.
        """
        # Create test data
        data = {
            "brt_id": [None, "1234", "5678"],
            "geometry": [
                Polygon(
                    [(0, 0), (1, 0), (1, 1), (0, 1)]
                ),  # Will be dropped (null brt_id)
                Polygon([(0, 0), (2, 0), (2, 2), (0, 2)]),  # Valid polygon
                LineString([(0, 0), (1, 1)]),  # Invalid type (not a polygon)
            ],
        }
        gdf = gpd.GeoDataFrame()
        gdf = gpd.GeoDataFrame(data, geometry="geometry")

        # Expect a ValueError because LineString is not allowed
        with self.assertRaises(ValueError) as context:
            transform_pwd_parcels_gdf(gdf.copy())

        self.assertIn("not polygons or multipolygons", str(context.exception))

        # Now fix the invalid geometry to test normal flow
        gdf.loc[2, "geometry"] = Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])

        # Run transformation which mutates result in place
        result = gdf.copy()
        transform_pwd_parcels_gdf(result)

        # Check the rows were filtered
        self.assertEqual(len(result), 2)  # One row was dropped
        self.assertNotIn("brt_id", result.columns)
        self.assertIn("opa_id", result.columns)
        self.assertListEqual(sorted(result["opa_id"].tolist()), ["1234", "5678"])
        self.assertTrue(all(result.geometry.is_valid))
        self.assertTrue(all(result.geometry.type.isin(["Polygon", "MultiPolygon"])))


if __name__ == "__main__":
    unittest.main()
