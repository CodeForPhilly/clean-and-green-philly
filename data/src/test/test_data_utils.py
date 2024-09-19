import unittest
import zipfile
from io import BytesIO
from unittest.mock import MagicMock, patch

import geopandas as gpd
from config.config import USE_CRS
from data_utils.park_priority import get_latest_shapefile_url, park_priority
from data_utils.ppr_properties import ppr_properties
from data_utils.vacant_properties import vacant_properties
from shapely.geometry import Point


class TestDataUtils(unittest.TestCase):
    """
    Test methods for data utils feature layer classes
    """

    @patch("data_utils.park_priority.requests.get")
    def test_get_latest_shapefile_url(self, mock_get):
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
        mock_makedirs,
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


if __name__ == "__main__":
    unittest.main()
