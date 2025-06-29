import unittest
from unittest.mock import MagicMock, patch

import geopandas as gpd
import numpy as np
import pandas as pd
import pytest
from shapely.geometry import LineString, MultiPolygon, Point, Polygon

from src.config.config import USE_CRS
from src.constants.services import PARK_PRIORITY_AREAS_URBAN_PHL

# Import the raw business logic function (no decorator)
from src.data_utils.park_priority import _park_priority_logic
from src.data_utils.ppr_properties import ppr_properties
from src.data_utils.pwd_parcels import (
    merge_pwd_parcels_gdf,
    transform_pwd_parcels_gdf,
)
from src.data_utils.vacant_properties import vacant_properties
from src.validation.base import ValidationResult


class TestDataUtils(unittest.TestCase):
    """
    Test methods for data utils feature layer classes
    """

    @classmethod
    def setUpClass(cls):
        # Create the mock GeoDataFrame that will be reused
        cls.mock_gdf = gpd.GeoDataFrame(
            {
                "ADDRESS": ["123 Main St"],
                "OWNER1": ["John Doe"],
                "OWNER2": ["Jane Doe"],
                "BLDG_DESC": ["House"],
                "CouncilDistrict": [1],
                "ZoningBaseDistrict": ["R1"],
                "ZipCode": ["19107"],
                "OPA_ID": ["12345"],
                "geometry": [Point(-75.1652, 39.9526)],
            },
            crs="EPSG:4326",
        )

    @patch("src.data_utils.park_priority.EsriLoader")
    @patch("src.data_utils.park_priority.spatial_join")
    def test_park_priority_basic_functionality(
        self, mock_spatial_join, mock_esri_loader_class
    ):
        """Test core workflow: load data, rename column, spatial join, return tuple"""

        # Setup mock input data
        input_gdf = gpd.GeoDataFrame(
            {"opa_id": ["123", "456"], "geometry": [Point(0, 0), Point(1, 1)]},
            crs=USE_CRS,
        )

        # Setup mock EsriLoader
        mock_loader_instance = MagicMock()
        mock_esri_loader_class.return_value = mock_loader_instance

        # Mock the park priority data returned by loader
        park_priority_gdf = gpd.GeoDataFrame(
            {
                "id": ["PA001", "PA002"],
                "parkneed": [5.0, 3.0],
                "rg_abbrev": ["PA", "PA"],
                "geometry": [Point(0, 0), Point(1, 1)],
            },
            crs=USE_CRS,
        )

        # Create a mock validation result
        mock_validation_result = ValidationResult(True)
        mock_loader_instance.load_or_fetch.return_value = (
            park_priority_gdf,
            mock_validation_result,
        )

        # Setup mock spatial join result
        expected_result_gdf = gpd.GeoDataFrame(
            {
                "opa_id": ["123", "456"],
                "park_priority": [5.0, 3.0],
                "geometry": [Point(0, 0), Point(1, 1)],
            },
            crs=USE_CRS,
        )
        mock_spatial_join.return_value = expected_result_gdf

        # Call the raw business logic function (no decorator)
        result_gdf, validation_result = _park_priority_logic(input_gdf)

        # Assertions
        # Check EsriLoader was called with correct parameters
        mock_esri_loader_class.assert_called_once_with(
            name="Park Priority Areas - Philadelphia",
            esri_urls=PARK_PRIORITY_AREAS_URBAN_PHL,
            cols=["id", "parkneed", "rg_abbrev"],
            extra_query_args={"where": "rg_abbrev = 'PA'"},
        )

        # Check loader was called
        mock_loader_instance.load_or_fetch.assert_called_once()

        # Check spatial join was called with correct data
        # Note: The function renames 'parkneed' to 'park_priority' before calling spatial_join
        call_args = mock_spatial_join.call_args
        second_arg = call_args[0][1]  # The second argument to spatial_join
        self.assertIn("park_priority", second_arg.columns)
        self.assertNotIn("parkneed", second_arg.columns)

        # Check return values - use data equality instead of object identity
        self.assertIsInstance(result_gdf, gpd.GeoDataFrame)
        self.assertIsInstance(validation_result, ValidationResult)

        # Check data equality for the GeoDataFrame
        pd.testing.assert_frame_equal(
            result_gdf.drop(columns=["geometry"]),
            expected_result_gdf.drop(columns=["geometry"]),
            check_dtype=False,
        )

        # Check geometry column separately
        for i, (expected_geom, actual_geom) in enumerate(
            zip(expected_result_gdf.geometry, result_gdf.geometry)
        ):
            self.assertTrue(
                expected_geom.equals(actual_geom), f"Geometry mismatch at index {i}"
            )

        # Check validation result
        self.assertIs(validation_result, mock_validation_result)

    @patch("src.data_utils.park_priority.EsriLoader")
    @patch("src.data_utils.park_priority.spatial_join")
    def test_park_priority_column_renaming(
        self, mock_spatial_join, mock_esri_loader_class
    ):
        """Test parkneed → park_priority column renaming"""

        # Setup mock input data
        input_gdf = gpd.GeoDataFrame(
            {"opa_id": ["123"], "geometry": [Point(0, 0)]}, crs=USE_CRS
        )

        # Setup mock EsriLoader
        mock_loader_instance = MagicMock()
        mock_esri_loader_class.return_value = mock_loader_instance

        # Mock the park priority data with 'parkneed' column
        park_priority_gdf = gpd.GeoDataFrame(
            {
                "id": ["PA001"],
                "parkneed": [5.0],  # This should be renamed to 'park_priority'
                "rg_abbrev": ["PA"],
                "geometry": [Point(0, 0)],
            },
            crs=USE_CRS,
        )

        mock_validation_result = ValidationResult(True)
        mock_loader_instance.load_or_fetch.return_value = (
            park_priority_gdf,
            mock_validation_result,
        )

        # Setup mock spatial join result
        expected_result_gdf = gpd.GeoDataFrame(
            {
                "opa_id": ["123"],
                "park_priority": [5.0],  # Should be renamed from 'parkneed'
                "geometry": [Point(0, 0)],
            },
            crs=USE_CRS,
        )
        mock_spatial_join.return_value = expected_result_gdf

        # Call the raw business logic function
        result_gdf, validation_result = _park_priority_logic(input_gdf)

        # Check that the column was renamed in the data passed to spatial_join
        # The function should rename 'parkneed' to 'park_priority' before calling spatial_join
        call_args = mock_spatial_join.call_args
        second_arg = call_args[0][1]  # The second argument to spatial_join

        # Check that the column was renamed
        self.assertIn("park_priority", second_arg.columns)
        self.assertNotIn("parkneed", second_arg.columns)
        self.assertEqual(second_arg["park_priority"].iloc[0], 5.0)

        # Check return value - use data equality instead of object identity
        self.assertIsInstance(result_gdf, gpd.GeoDataFrame)

        # Check data equality for the GeoDataFrame
        pd.testing.assert_frame_equal(
            result_gdf.drop(columns=["geometry"]),
            expected_result_gdf.drop(columns=["geometry"]),
            check_dtype=False,
        )

        # Check geometry column separately
        for i, (expected_geom, actual_geom) in enumerate(
            zip(expected_result_gdf.geometry, result_gdf.geometry)
        ):
            self.assertTrue(
                expected_geom.equals(actual_geom), f"Geometry mismatch at index {i}"
            )

        # Check validation result
        self.assertIs(validation_result, mock_validation_result)

    @patch("src.data_utils.park_priority.EsriLoader")
    @patch("src.data_utils.park_priority.spatial_join")
    def test_park_priority_pennsylvania_filtering(
        self, mock_spatial_join, mock_esri_loader_class
    ):
        """Test EsriLoader called with correct PA filter"""

        # Setup mock input data
        input_gdf = gpd.GeoDataFrame(
            {"opa_id": ["123"], "geometry": [Point(0, 0)]}, crs=USE_CRS
        )

        # Setup mock EsriLoader
        mock_loader_instance = MagicMock()
        mock_esri_loader_class.return_value = mock_loader_instance

        # Mock the park priority data
        park_priority_gdf = gpd.GeoDataFrame(
            {
                "id": ["PA001"],
                "parkneed": [5.0],
                "rg_abbrev": ["PA"],
                "geometry": [Point(0, 0)],
            },
            crs=USE_CRS,
        )

        mock_validation_result = ValidationResult(True)
        mock_loader_instance.load_or_fetch.return_value = (
            park_priority_gdf,
            mock_validation_result,
        )
        mock_spatial_join.return_value = input_gdf

        # Call the raw business logic function
        _park_priority_logic(input_gdf)

        # Check that EsriLoader was called with the Pennsylvania filter
        mock_esri_loader_class.assert_called_once()
        call_args = mock_esri_loader_class.call_args

        # Check the extra_query_args parameter
        self.assertEqual(
            call_args[1]["extra_query_args"], {"where": "rg_abbrev = 'PA'"}
        )

        # Check the columns parameter includes rg_abbrev for filtering
        self.assertIn("rg_abbrev", call_args[1]["cols"])

    @patch("src.data_utils.park_priority.EsriLoader")
    @patch("src.data_utils.park_priority.spatial_join")
    def test_park_priority_empty_data(self, mock_spatial_join, mock_esri_loader_class):
        """Test behavior when no park priority data available"""

        # Setup mock input data
        input_gdf = gpd.GeoDataFrame(
            {"opa_id": ["123"], "geometry": [Point(0, 0)]}, crs=USE_CRS
        )

        # Setup mock EsriLoader
        mock_loader_instance = MagicMock()
        mock_esri_loader_class.return_value = mock_loader_instance

        # Mock empty park priority data
        empty_park_priority_gdf = gpd.GeoDataFrame(
            columns=["id", "parkneed", "rg_abbrev", "geometry"], crs=USE_CRS
        )

        mock_validation_result = ValidationResult(True)
        mock_loader_instance.load_or_fetch.return_value = (
            empty_park_priority_gdf,
            mock_validation_result,
        )

        # Setup mock spatial join result (should be same as input when no data)
        mock_spatial_join.return_value = input_gdf

        # Call the raw business logic function
        result_gdf, validation_result = _park_priority_logic(input_gdf)

        # Check that the function handles empty data gracefully
        self.assertIsInstance(result_gdf, gpd.GeoDataFrame)
        self.assertIsInstance(validation_result, ValidationResult)

        # Check data equality for the GeoDataFrame
        pd.testing.assert_frame_equal(
            result_gdf.drop(columns=["geometry"]),
            input_gdf.drop(columns=["geometry"]),
            check_dtype=False,
        )

        # Check geometry column separately
        for i, (expected_geom, actual_geom) in enumerate(
            zip(input_gdf.geometry, result_gdf.geometry)
        ):
            self.assertTrue(
                expected_geom.equals(actual_geom), f"Geometry mismatch at index {i}"
            )

        # Check validation result
        self.assertIs(validation_result, mock_validation_result)

        # Check that spatial_join was still called (even with empty data)
        mock_spatial_join.assert_called_once()

    @patch("src.data_utils.park_priority.EsriLoader")
    @patch("src.data_utils.park_priority.spatial_join")
    def test_park_priority_return_format(
        self, mock_spatial_join, mock_esri_loader_class
    ):
        """Test returns correct tuple structure"""

        # Setup mock input data
        input_gdf = gpd.GeoDataFrame(
            {"opa_id": ["123"], "geometry": [Point(0, 0)]}, crs=USE_CRS
        )

        # Setup mock EsriLoader
        mock_loader_instance = MagicMock()
        mock_esri_loader_class.return_value = mock_loader_instance

        # Mock the park priority data
        park_priority_gdf = gpd.GeoDataFrame(
            {
                "id": ["PA001"],
                "parkneed": [5.0],
                "rg_abbrev": ["PA"],
                "geometry": [Point(0, 0)],
            },
            crs=USE_CRS,
        )

        mock_validation_result = ValidationResult(True)
        mock_loader_instance.load_or_fetch.return_value = (
            park_priority_gdf,
            mock_validation_result,
        )

        # Setup mock spatial join result
        expected_result_gdf = gpd.GeoDataFrame(
            {"opa_id": ["123"], "park_priority": [5.0], "geometry": [Point(0, 0)]},
            crs=USE_CRS,
        )
        mock_spatial_join.return_value = expected_result_gdf

        # Call the raw business logic function
        result = _park_priority_logic(input_gdf)

        # Check return type and structure
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)

        result_gdf, validation_result = result

        # Check first element is GeoDataFrame
        self.assertIsInstance(result_gdf, gpd.GeoDataFrame)

        # Check second element is ValidationResult
        self.assertIsInstance(validation_result, ValidationResult)

        # Check the actual values - use data equality instead of object identity
        # Check data equality for the GeoDataFrame
        pd.testing.assert_frame_equal(
            result_gdf.drop(columns=["geometry"]),
            expected_result_gdf.drop(columns=["geometry"]),
            check_dtype=False,
        )

        # Check geometry column separately
        for i, (expected_geom, actual_geom) in enumerate(
            zip(expected_result_gdf.geometry, result_gdf.geometry)
        ):
            self.assertTrue(
                expected_geom.equals(actual_geom), f"Geometry mismatch at index {i}"
            )

        # Check validation result
        self.assertIs(validation_result, mock_validation_result)

    @pytest.mark.skip
    def test_ppr_properties(self):
        """
        Test the ppr properties layer. Simply construct the class for now to see if it works.
        """
        ppr_properties(vacant_properties())

    @pytest.mark.skip
    def test_vacant_properties(self):
        """
        Test the vacant properties layer. Simply construct the class to see if it works.
        """
        vacant_properties()

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
            "is_condo_unit": [
                False,
                False,
                False,
                False,
            ],  # No condo units in our test data
            "parcel_area_sqft": [
                0.0,
                100.0,
                0.0,
                0.0,
            ],  # Points get 0.0, polygon gets area
        }
        expected_df = gpd.GeoDataFrame(
            data=data,
            geometry="geometry",
        )

        # Debug: Print both DataFrames to see what's different
        print("Expected DataFrame:")
        print(expected_df)
        print("\nActual DataFrame:")
        print(merged_gdf)
        print("\nExpected columns:", list(expected_df.columns))
        print("Actual columns:", list(merged_gdf.columns))
        print("\nExpected index:", list(expected_df.index))
        print("Actual index:", list(merged_gdf.index))

        # Use proper DataFrame comparison instead of .equals()
        pd.testing.assert_frame_equal(
            expected_df.drop(columns=["geometry"]),
            merged_gdf.drop(columns=["geometry"]),
            check_dtype=False,
        )

        # Check geometry column separately since it's not a regular column
        for i, (expected_geom, actual_geom) in enumerate(
            zip(expected_df.geometry, merged_gdf.geometry)
        ):
            assert expected_geom.equals(actual_geom), f"Geometry mismatch at index {i}"

    def test_transform_pwd_parcels_gdf_error(self):
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
        gdf = gpd.GeoDataFrame(data, geometry="geometry")

        with self.assertRaises(ValueError) as context:
            transform_pwd_parcels_gdf(gdf)

        self.assertEqual(
            "Some geometries are not polygons or multipolygons.", str(context.exception)
        )


if __name__ == "__main__":
    unittest.main()
