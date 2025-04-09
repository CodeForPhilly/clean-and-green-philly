import unittest
import zipfile
from io import BytesIO
from unittest.mock import MagicMock, Mock, patch

import geopandas as gpd
import numpy as np
from shapely.geometry import LineString, MultiPolygon, Point, Polygon

from config.config import USE_CRS
from data_utils.park_priority import get_latest_shapefile_url, park_priority
from data_utils.ppr_properties import ppr_properties
from data_utils.vacant_properties import vacant_properties
from new_etl.data_utils.pwd_parcels import (
    merge_pwd_parcels_gdf,
    transform_pwd_parcels_gdf,
)


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

    def setUp(self):
        # Set up the mocks that will be used in each test
        self.patcher1 = patch("data_utils.vacant_properties.google_cloud_bucket")
        self.patcher2 = patch("geopandas.read_file")

        self.mock_gcs = self.patcher1.start()
        self.mock_gpd = self.patcher2.start()

        # Set up the mock chain
        mock_blob = Mock()
        mock_blob.exists.return_value = True
        mock_blob.download_as_bytes.return_value = b"dummy bytes"

        mock_bucket = Mock()
        mock_bucket.blob.return_value = mock_blob

        self.mock_gcs.return_value = mock_bucket
        self.mock_gpd.return_value = self.mock_gdf

    def tearDown(self):
        self.patcher1.stop()
        self.patcher2.stop()

    def test_get_latest_shapefile_url(self):
        """
        Test the get_latest_shapefile_url function.
        """
        url = get_latest_shapefile_url()
        self.assertTrue(url.startswith("https://"))
        self.assertTrue(url.endswith(".zip"))

    @patch("data_utils.park_priority.requests.get")
    def test_get_latest_shapefile_url_mock(self, mock_get):
        """
        Test the get_latest_shapefile_url function.
        """
        mock_response = MagicMock()
        mock_response.content = (
            b'<html><a href="https://example.com/shapefile.zip">Shapefile</a></html>'
        )
        mock_get.return_value = mock_response

        url = get_latest_shapefile_url()
        self.assertEqual(url, "https://example.com/shapefile.zip")

    @patch(
        "data_utils.park_priority.requests.get"
    )  # Mock requests.get globally in park_priority
    @patch("geopandas.read_file")
    @patch("geopandas.GeoDataFrame.to_file")  # Mock to_file to prevent actual writing
    @patch("os.path.exists")
    @patch("os.makedirs")
    @patch("zipfile.ZipFile.extract")
    def test_park_priority(
        self,
        mock_extract,
        _mock_makedirs,
        mock_exists,
        mock_to_file,
        mock_read_file,
        mock_get,
    ):
        """
        Test the park_priority function with mocking.
        """

        # Simulate that the GeoJSON file does not exist
        mock_exists.return_value = False

        # First call to requests.get (HTML page to get the shapefile URL)
        mock_html_response = MagicMock()
        mock_html_response.content = (
            b'<html><a href="https://example.com/shapefile.zip">Shapefile</a></html>'
        )

        # test comment to see how vulture config works in precommit hook

        # Second call to requests.get (actual shapefile download)
        mock_zip_content = BytesIO()
        with zipfile.ZipFile(mock_zip_content, "w") as zf:
            zf.writestr("Parkserve_ParkPriorityAreas.shp", b"mock shapefile content")

        mock_response = MagicMock()
        mock_response.headers.get.return_value = "1000"  # Mock content-length
        mock_response.iter_content.return_value = [mock_zip_content.getvalue()]

        # Set the side effect for requests.get to return the two different responses
        mock_get.side_effect = [mock_html_response, mock_response]

        # Create a real mock GeoDataFrame with geometries and a CRS
        mock_gdf = gpd.GeoDataFrame(
            {
                "ID": ["42101ABC", "42101DEF", "12345XYZ"],
                "ParkNeed": [5, 3, 1],
                "geometry": [
                    Point(0, 0),
                    Point(1, 1),
                    Point(2, 2),
                ],  # Use actual Point geometries
            },
            crs=USE_CRS,  # Assign the expected CRS
        )

        mock_read_file.return_value = mock_gdf  # Return the mock GeoDataFrame

        # Create a mock primary feature layer
        mock_primary_layer = MagicMock()

        # Run the function
        result = park_priority(mock_primary_layer)

        # Assert that requests.get was called twice (once for HTML, once for shapefile)
        self.assertEqual(mock_get.call_count, 2)

        # Assert that to_file was called once (simulating the write operation)
        mock_to_file.assert_called_once_with("tmp/phl_parks.geojson", driver="GeoJSON")

        # Assert other function calls were made correctly
        mock_read_file.assert_called_once()
        mock_primary_layer.spatial_join.assert_called_once()
        mock_extract.assert_called()

        self.assertEqual(result, mock_primary_layer)

    def test_ppr_properties(self):
        """
        Test the ppr properties layer. Simply construct the class for now to see if it works.
        """
        ppr_properties(vacant_properties())

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
