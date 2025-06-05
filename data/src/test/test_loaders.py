import unittest
from unittest.mock import MagicMock, Mock, patch

import geopandas as gpd

from src.config.config import USE_CRS
from src.new_etl.classes.loaders import (
    BaseLoader,
    EsriLoader,
    GdfLoader,
)


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

    @patch("src.new_etl.classes.loaders.BaseLoader")
    def test_cache_data(self, mock_file_manager: MagicMock):
        mock_instance = mock_file_manager.get_instance.return_value
        loader = EsriLoader(name="TestLoader", esri_urls=["Test"], opa_col="opa")

        loader.file_manager = mock_instance

        gdf = gpd.GeoDataFrame(
            {"opa_id": ["123", "456"], "geometry": gpd.points_from_xy([0, 1], [0, 1])}
        )

        loader.cache_data(gdf)
        mock_instance.save_gdf.assert_called_once()

    @patch("src.new_etl.classes.loaders.load_esri_data")
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

    @patch("src.new_etl.classes.loaders.gpd.read_file")
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


if __name__ == "__main__":
    unittest.main()
