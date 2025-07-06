import unittest
from unittest.mock import MagicMock, Mock, patch

import geopandas as gpd
from shapely.geometry import Point

from src.classes.loaders import (
    BaseLoader,
    EsriLoader,
    GdfLoader,
)
from src.config.config import USE_CRS


class TestBaseLoader(unittest.TestCase):
    def test_string_to_list(self):
        test_column = "test_column"
        result = BaseLoader.string_to_list(test_column)
        self.assertIsInstance(result, list)
        self.assertEqual(result, [test_column])

    def test_lowercase_column_names(self):
        gdf = BaseLoader.lowercase_column_names(
            gpd.GeoDataFrame(
                {"Column1": ["test1", "test2"], "Column2": ["test1", "test2"]}
            )
        )
        self.assertListEqual(list(gdf.columns), ["column1", "column2"])

    def test_filter_columns(self):
        cols = ["column1", "column2"]
        gdf = gpd.GeoDataFrame(columns=["column1", "column2", "column3"])
        filtered_gdf = BaseLoader.filter_columns(gdf, cols)
        self.assertListEqual(list(filtered_gdf.columns), ["column1", "column2"])

    def test_normalize_columns(self):
        gdf = gpd.GeoDataFrame(
            columns=["Column1", "Column2", "geometry"],
            data=[[1, 2, None], [3, 4, None]],
        )
        cols = ["column1", "column2"]
        normalized_gdf = BaseLoader.normalize_columns(gdf, cols)
        self.assertListEqual(
            list(normalized_gdf.columns), ["column1", "column2", "geometry"]
        )

    def test_standardize_opa(self):
        gdf = gpd.GeoDataFrame(
            columns=["opa", "geometry"],
            data=[["354", None], [243, None], [None, None]],
        )
        loader = EsriLoader(name="TestLoader", esri_urls=["Test"], opa_col="opa")
        standardized_gdf = loader.standardize_opa(gdf)
        self.assertListEqual(list(standardized_gdf.columns), ["opa_id", "geometry"])
        self.assertTrue(standardized_gdf["opa_id"].is_unique)
        self.assertTrue(standardized_gdf["opa_id"].isnull().sum() == 0)
        self.assertTrue(
            standardized_gdf["opa_id"].apply(lambda x: isinstance(x, str)).all()
        )

    @patch("src.classes.loaders.BaseLoader")
    def test_cache_data(self, mock_file_manager: MagicMock):
        mock_instance = mock_file_manager.get_instance.return_value
        loader = EsriLoader(name="TestLoader", esri_urls=["Test"], opa_col="opa")

        loader.file_manager = mock_instance

        gdf = gpd.GeoDataFrame(
            {"opa_id": ["123", "456"], "geometry": gpd.points_from_xy([0, 1], [0, 1])}
        )

        loader.cache_data(gdf)
        mock_instance.save_gdf.assert_called_once()

    @patch("src.classes.loaders.load_esri_data")
    def test_load(self, mock_load: Mock):
        mock_gdf = gpd.GeoDataFrame(
            {
                "address": ["123 Cherry St", "341 Chestnut St"],
                "opa": ["123", "456"],
                "geometry": gpd.points_from_xy([0, 1], [0, 1]),
            },
            crs=USE_CRS,
        )
        mock_load.return_value = mock_gdf

        loader = EsriLoader(
            name="TestLoader", esri_urls=["http://example.com/arcgis"], opa_col="opa"
        )
        gdf = loader.load_data()

        self.assertEqual(gdf.crs, USE_CRS)
        self.assertTrue("opa_id" in gdf.columns)
        self.assertListEqual(list(gdf.columns), ["address", "opa_id", "geometry"])
        self.assertTrue(gdf["opa_id"].isnull().sum() == 0)

        self.assertTrue(gdf.geometry.is_valid.all())

    @patch("src.classes.loaders.gpd.read_file")
    def test_load_no_crs(self, mock_load: Mock):
        mock_load.return_value = gpd.GeoDataFrame(
            {
                "address": ["123 Cherry St", "341 Chestnut St"],
                "opa": ["123", "456"],
                "geometry": gpd.points_from_xy([0, 1], [0, 1]),
            }
        )

        with self.assertRaises(AttributeError) as context:
            loader = GdfLoader(
                input="test_file.geojson", name="TestLoader", opa_col="opa"
            )
            _ = loader.load_data()

        self.assertEqual(
            "Input data doesn't have an original CRS set", str(context.exception)
        )

    def test_crs_reprojection_actual_conversion(self):
        """
        Test that loaders actually reproject data, not just relabel it.

        This test simulates the PHS properties issue where data comes in with
        lat/lon coordinates but is labeled as EPSG:2272. The loader should
        detect this and properly reproject the coordinates.
        """
        # Create test data with lat/lon coordinates (Philadelphia area)
        # but labeled as EPSG:2272 (incorrectly)
        lat_lon_coords = [
            (-75.1652, 39.9526),
            (-75.1801, 39.9612),
            (-75.1500, 39.9400),
        ]

        # Create GeoDataFrame with lat/lon coordinates but labeled as EPSG:2272
        test_data = {
            "address": ["123 Test St", "456 Test Ave", "789 Test Blvd"],
            "opa": ["123", "456", "789"],
            "geometry": [Point(x, y) for x, y in lat_lon_coords],
        }

        # This is the key: data has lat/lon coordinates but is labeled as EPSG:2272
        incorrectly_labeled_gdf = gpd.GeoDataFrame(test_data, crs="EPSG:2272")

        # Verify the coordinates are actually lat/lon (should be roughly -180 to 180 for x, -90 to 90 for y)
        bounds = incorrectly_labeled_gdf.total_bounds
        self.assertTrue(
            -180 <= bounds[0] <= 180,
            f"X coordinates should be lat/lon, got {bounds[0]}",
        )
        self.assertTrue(
            -90 <= bounds[1] <= 90, f"Y coordinates should be lat/lon, got {bounds[1]}"
        )

        # Test EsriLoader with mocked load_esri_data
        with patch("src.classes.loaders.load_esri_data") as mock_load_esri:
            mock_load_esri.return_value = incorrectly_labeled_gdf

            loader = EsriLoader(
                name="TestLoader",
                esri_urls=["http://example.com/arcgis"],
                opa_col="opa",
            )
            result_gdf = loader.load_data()

            # Verify the result has the correct CRS
            self.assertEqual(result_gdf.crs, USE_CRS)

            # Verify the coordinates were actually reprojected (should be in EPSG:2272 range)
            result_bounds = result_gdf.total_bounds
            # EPSG:2272 coordinates for Philadelphia area should be roughly:
            # X: 2,600,000 to 2,800,000, Y: 200,000 to 400,000
            self.assertTrue(
                result_bounds[0] > 2000000,
                f"X coordinates should be reprojected to EPSG:2272 range, got {result_bounds[0]}",
            )
            self.assertTrue(
                result_bounds[1] > 100000,
                f"Y coordinates should be reprojected to EPSG:2272 range, got {result_bounds[1]}",
            )

            # Verify the coordinates changed significantly (not just relabeled)
            original_coords = [(p.x, p.y) for p in incorrectly_labeled_gdf.geometry]
            reprojected_coords = [(p.x, p.y) for p in result_gdf.geometry]

            for orig, reproj in zip(original_coords, reprojected_coords):
                # Coordinates should be significantly different after reprojection
                self.assertNotAlmostEqual(
                    orig[0],
                    reproj[0],
                    places=0,
                    msg="X coordinates should be different after reprojection",
                )
                self.assertNotAlmostEqual(
                    orig[1],
                    reproj[1],
                    places=0,
                    msg="Y coordinates should be different after reprojection",
                )

                # Reprojected coordinates should be in EPSG:2272 range
                self.assertTrue(
                    reproj[0] > 2000000,
                    f"Reprojected X coordinate {reproj[0]} should be in EPSG:2272 range",
                )
                self.assertTrue(
                    reproj[1] > 100000,
                    f"Reprojected Y coordinate {reproj[1]} should be in EPSG:2272 range",
                )

    def test_crs_reprojection_from_epsg_4326(self):
        """
        Test that loaders properly handle data that comes in with correct EPSG:4326 label.
        """
        # Create test data with lat/lon coordinates and correct EPSG:4326 label
        lat_lon_coords = [
            (-75.1652, 39.9526),  # Philadelphia City Hall
            (-75.1801, 39.9612),  # Another Philly location
        ]

        test_data = {
            "address": ["123 Test St", "456 Test Ave"],
            "opa": ["123", "456"],
            "geometry": [Point(x, y) for x, y in lat_lon_coords],
        }

        # Data with correct EPSG:4326 label
        correctly_labeled_gdf = gpd.GeoDataFrame(test_data, crs="EPSG:4326")

        # Test EsriLoader with mocked load_esri_data
        with patch("src.classes.loaders.load_esri_data") as mock_load_esri:
            mock_load_esri.return_value = correctly_labeled_gdf

            loader = EsriLoader(
                name="TestLoader",
                esri_urls=["http://example.com/arcgis"],
                opa_col="opa",
            )
            result_gdf = loader.load_data()

            # Verify the result has the correct CRS
            self.assertEqual(result_gdf.crs, USE_CRS)

            # Verify the coordinates were actually reprojected
            result_bounds = result_gdf.total_bounds
            self.assertTrue(
                result_bounds[0] > 2000000,
                f"X coordinates should be reprojected to EPSG:2272 range, got {result_bounds[0]}",
            )
            self.assertTrue(
                result_bounds[1] > 100000,
                f"Y coordinates should be reprojected to EPSG:2272 range, got {result_bounds[1]}",
            )

            # Verify the coordinates changed from lat/lon to projected
            original_coords = [(p.x, p.y) for p in correctly_labeled_gdf.geometry]
            reprojected_coords = [(p.x, p.y) for p in result_gdf.geometry]

            for orig, reproj in zip(original_coords, reprojected_coords):
                # Lat/lon coordinates should be different from projected coordinates
                self.assertNotAlmostEqual(orig[0], reproj[0], places=0)
                self.assertNotAlmostEqual(orig[1], reproj[1], places=0)

                # Original should be lat/lon range
                self.assertTrue(-180 <= orig[0] <= 180)
                self.assertTrue(-90 <= orig[1] <= 90)

                # Reprojected should be in EPSG:2272 range
                self.assertTrue(reproj[0] > 2000000)
                self.assertTrue(reproj[1] > 100000)

    def test_crs_reprojection_gdf_loader(self):
        """
        Test that GdfLoader also properly handles CRS reprojection.
        """
        # Create test data with lat/lon coordinates but labeled as EPSG:2272
        lat_lon_coords = [
            (-75.1652, 39.9526),  # Philadelphia City Hall
        ]

        test_data = {
            "address": ["123 Test St"],
            "opa": ["123"],
            "geometry": [Point(x, y) for x, y in lat_lon_coords],
        }

        # This simulates the PHS properties issue
        incorrectly_labeled_gdf = gpd.GeoDataFrame(test_data, crs="EPSG:2272")

        # Add debug logging
        print(f"Test: Original CRS: {incorrectly_labeled_gdf.crs}")
        print(f"Test: Original bounds: {incorrectly_labeled_gdf.total_bounds}")
        print(
            f"Test: Original coordinates: {[(p.x, p.y) for p in incorrectly_labeled_gdf.geometry]}"
        )

        # Test GdfLoader with mocked gpd.read_file
        with patch("src.classes.loaders.gpd.read_file") as mock_read_file:
            mock_read_file.return_value = incorrectly_labeled_gdf

            loader = GdfLoader(
                input="test_file.geojson", name="TestLoader", opa_col="opa"
            )
            result_gdf = loader.load_data()

            # Add debug logging
            print(f"Test: Result CRS: {result_gdf.crs}")
            print(f"Test: Result bounds: {result_gdf.total_bounds}")
            print(
                f"Test: Result coordinates: {[(p.x, p.y) for p in result_gdf.geometry]}"
            )

            # Verify the result has the correct CRS
            self.assertEqual(result_gdf.crs, USE_CRS)

            # Verify the coordinates were actually reprojected
            result_bounds = result_gdf.total_bounds
            self.assertTrue(
                result_bounds[0] > 2000000,
                f"X coordinates should be reprojected to EPSG:2272 range, got {result_bounds[0]}",
            )
            self.assertTrue(
                result_bounds[1] > 100000,
                f"Y coordinates should be reprojected to EPSG:2272 range, got {result_bounds[1]}",
            )


if __name__ == "__main__":
    unittest.main()
