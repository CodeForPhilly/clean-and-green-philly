import unittest

import geopandas as gpd
from shapely import Point

from src.validation.base import BaseValidator


class TestValidation(unittest.TestCase):
    def test_geometry_validation(self):
        data = {
            "opa_id": ["314", "013", "004"],
            "geometry": [Point(0, 0), Point(3, 1), Point(4, 5)],
        }

        gdf = gpd.GeoDataFrame(data, crs="EPSG:4326")

        validator = BaseValidator()
        validator.validate_geometry(gdf)

        self.assertListEqual(
            validator.errors,
            [
                "Geodataframe for BaseValidator is not using the correct coordinate system pegged to Philadelphia",
                "Dataframe for BaseValidator contains observations outside Philadelphia limits.",
            ],
        )

    def test_opa_string_validation(self):
        data = {
            "opa_id": ["314", 1, "004"],
            "geometry": [Point(0, 0), Point(3, 1), Point(4, 5)],
        }

        gdf = gpd.GeoDataFrame(data)

        validator = BaseValidator()
        validator.opa_validation(gdf)

        self.assertListEqual(
            validator.errors, ["OPA ids are not all typed as strings for BaseValidator"]
        )

    def test_opa_unique_validation(self):
        data = {
            "opa_id": ["314", "314", "004"],
            "geometry": [Point(0, 0), Point(3, 1), Point(4, 5)],
        }

        gdf = gpd.GeoDataFrame(data)

        validator = BaseValidator()
        validator.opa_validation(gdf)

        self.assertListEqual(
            validator.errors, ["OPA ids contain some duplicates for BaseValidator"]
        )


if __name__ == "__main__":
    unittest.main()
