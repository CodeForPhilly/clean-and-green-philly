import unittest
import os
import tempfile
import datetime
from unittest.mock import patch, MagicMock

import numpy as np
import geopandas as gpd
import xarray as xr
from shapely.geometry import Polygon

from data_utils.ndvi import (
    get_current_summer_year,
    is_cache_valid,
    get_bbox_from_census_data,
    extract_ndvi_to_parcels,
    generate_ndvi_data,
    ndvi,
)
from config.config import USE_CRS
from classes.featurelayer import FeatureLayer


class TestNDVIExtraction(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_polygon = Polygon(
            [(-75.2, 39.9), (-75.2, 40.0), (-75.1, 40.0), (-75.1, 39.9), (-75.2, 39.9)]
        )
        cls.test_parcels = gpd.GeoDataFrame(
            {
                "id": [1, 2, 3],
                "geometry": [
                    cls.test_polygon,
                    Polygon(
                        [
                            (-75.15, 39.95),
                            (-75.15, 39.96),
                            (-75.14, 39.96),
                            (-75.14, 39.95),
                            (-75.15, 39.95),
                        ]
                    ),
                    Polygon(
                        [
                            (-75.12, 39.92),
                            (-75.12, 39.93),
                            (-75.11, 39.93),
                            (-75.11, 39.92),
                            (-75.12, 39.92),
                        ]
                    ),
                ],
            },
            crs="EPSG:4326",
        )
        cls.temp_dir = tempfile.mkdtemp()
        cls.test_raster_path = os.path.join(cls.temp_dir, "ndvi_data_summer_2025.tif")
        cls.ndvi_array = np.ones((2, 10, 10)) * -99
        cls.ndvi_array[0, 0:5, 0:5] = 0.8
        cls.ndvi_array[0, 0:5, 5:10] = 0.3
        cls.ndvi_array[0, 5:10, 0:5] = 0.0
        cls.ndvi_array[0, 5:10, 5:10] = -0.2
        cls.ndvi_array[1, 0:5, 0:5] = 0.1
        cls.ndvi_array[1, 0:5, 5:10] = -0.1
        cls.ndvi_array[1, 5:10, 0:5] = 0.0
        cls.ndvi_array[1, 5:10, 5:10] = -0.3
        lon = np.linspace(-75.25, -75.05, 10)
        lat = np.linspace(39.85, 40.05, 10)
        da = xr.DataArray(
            data=cls.ndvi_array,
            dims=["band", "y", "x"],
            coords={"band": [1, 2], "y": lat, "x": lon},
        )
        da.rio.write_crs("EPSG:4326", inplace=True)
        da.rio.write_nodata(-99, inplace=True)
        da.attrs["long_name"] = ["ndvi", "ndvi_one_year_change"]
        da.rio.to_raster(cls.test_raster_path)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.test_raster_path):
            os.remove(cls.test_raster_path)

    @patch("data_utils.ndvi.datetime.datetime")
    def test_get_current_summer_year(self, mock_datetime):
        mock_datetime.now.return_value = datetime.datetime(2025, 5, 1)
        self.assertEqual(get_current_summer_year(), 2024)
        mock_datetime.now.return_value = datetime.datetime(2025, 7, 1)
        self.assertEqual(get_current_summer_year(), 2025)

    def test_is_cache_valid(self):
        self.assertFalse(is_cache_valid("nonexistent_file.tif", 2025))
        wrong_year_path = os.path.join(self.temp_dir, "ndvi_data_summer_2024.tif")
        with open(wrong_year_path, "w") as f:
            f.write("test")
        self.assertFalse(is_cache_valid(wrong_year_path, 2025))
        self.assertTrue(is_cache_valid(self.test_raster_path, 2025))

    @patch("geopandas.read_file")
    def test_get_bbox_from_census_data(self, mock_read_file):
        poly = Polygon([(-75.2, 39.9), (-75.2, 40.0), (-75.1, 40.0), (-75.1, 39.9)])
        gdf = gpd.GeoDataFrame({"geometry": [poly]}, crs="EPSG:4326")
        gdf.total_bounds = (-75.2, 39.9, -75.1, 40.0)
        mock_read_file.return_value = gdf
        boundary, bbox_coords = get_bbox_from_census_data()
        self.assertIsInstance(boundary, Polygon)
        self.assertEqual(bbox_coords, (-75.2, 39.9, -75.1, 40.0))

    def test_extract_ndvi_to_parcels(self):
        results = extract_ndvi_to_parcels(self.test_raster_path, self.test_parcels)
        self.assertEqual(len(results), 3)
        self.assertIn("ndvi_mean", results.columns)
        self.assertIn("ndvi_one_year_change_mean", results.columns)
        for idx in results.index:
            self.assertGreaterEqual(results.loc[idx, "ndvi_mean"], -0.2)
            self.assertLessEqual(results.loc[idx, "ndvi_mean"], 0.8)

    def test_extract_ndvi_to_parcels_reprojection(self):
        parcels_use_crs = self.test_parcels.to_crs(USE_CRS)
        with patch("rioxarray.open_rasterio") as mock_open:
            mock_dataset = MagicMock()
            mock_dataset.rio.crs = "EPSG:4326"
            mock_dataset.rio.reproject.return_value = mock_dataset
            mock_dataset.rio.to_raster.return_value = None
            mock_open.return_value.__enter__.return_value = mock_dataset
            with patch("exactextract.exact_extract") as mock_extract:
                mock_extract.return_value = gpd.GeoDataFrame(
                    {
                        "id": [1, 2, 3],
                        "ndvi_mean": [0.5, 0.7, -0.1],
                        "ndvi_one_year_change_mean": [0.0, 0.1, -0.2],
                    }
                )
                extract_ndvi_to_parcels(self.test_raster_path, parcels_use_crs)
                mock_dataset.rio.reproject.assert_called_once_with(USE_CRS)
                mock_dataset.rio.to_raster.assert_called_once()

    def test_extract_ndvi_invalid_raster(self):
        with self.assertRaises(FileNotFoundError):
            extract_ndvi_to_parcels("nonexistent_raster.tif", self.test_parcels)

    @patch("data_utils.ndvi.odc.stac.stac_load")
    @patch("data_utils.ndvi.get_current_summer_year")
    def test_generate_ndvi_data_failure(self, mock_get_year, mock_stac_load):
        mock_get_year.return_value = 2025
        mock_stac_load.side_effect = Exception("Test exception in stac_load")
        with self.assertRaises(Exception) as context:
            generate_ndvi_data(
                os.path.join(self.temp_dir, "dummy.tif"),
                self.test_polygon,
                (-75.2, 39.9, -75.1, 40.0),
            )
        self.assertIn("Test exception", str(context.exception))

    @patch("tempfile.gettempdir")
    @patch("data_utils.ndvi.get_current_summer_year")
    @patch("data_utils.ndvi.get_bbox_from_census_data")
    @patch("data_utils.ndvi.is_cache_valid")
    @patch("data_utils.ndvi.generate_ndvi_data")
    @patch("data_utils.ndvi.extract_ndvi_to_parcels")
    def test_ndvi_integration(
        self,
        mock_extract,
        mock_generate,
        mock_is_valid,
        mock_get_bbox,
        mock_get_year,
        mock_tempdir,
    ):
        mock_tempdir.return_value = self.temp_dir
        mock_get_year.return_value = 2025
        mock_get_bbox.return_value = (self.test_polygon, (-75.2, 39.9, -75.1, 40.0))
        mock_is_valid.return_value = True
        mock_results = self.test_parcels.copy()
        mock_results["ndvi_mean"] = [0.5, 0.7, -0.1]
        mock_results["ndvi_one_year_change_mean"] = [0.0, 0.1, -0.2]
        mock_extract.return_value = mock_results
        test_layer = FeatureLayer(self.test_parcels)
        result_layer = ndvi(test_layer)
        mock_is_valid.assert_called_once()
        mock_generate.assert_not_called()
        mock_extract.assert_called_once()
        self.assertIn("ndvi_mean", result_layer.gdf.columns)
        self.assertIn("ndvi_one_year_change_mean", result_layer.gdf.columns)
        mock_is_valid.return_value = False
        ndvi(test_layer)
        mock_generate.assert_called_once()


if __name__ == "__main__":
    unittest.main()
