import unittest
import geopandas as gpd

from new_etl.data_utils.city_owned_properties import transform_city_owned_properties


class TestCityOwnedProperties(unittest.TestCase):
    def test_transform_city_owned_properties(self):
        """
        This tests that the transform_city_owned_properties function correctly
        transforms the city-owned properties data by renaming columns and updating
        access information for properties based on ownership.
        """

        # Sample data
        data = {
            "owner_1": [
                "PHILADELPHIA HOUSING AUTH",
                "PHILADELPHIA LAND BANK",
                "CITY OF PHILA",
                "REDEVELOPMENT AUTHORITY",
            ],
            "owner_2": ["PUBLIC PROP", "PUBLC PROP", "PUBLIC PROP", None],
            "agency": [
                "PHILADELPHIA HOUSING AUTH",
                "PLB",
                "CITY OF PHILA",
                "REDEVELOPMENT AUTHORITY",
            ],
            "sideyardeligible": [None, "Yes", None, "No"],
        }

        gdf = gpd.GeoDataFrame(data)

        # Call the function under test
        transform_city_owned_properties(gdf)

        expected_gdf = gpd.GeoDataFrame(
            {
                "owner_1": [
                    "PHILADELPHIA HOUSING AUTH",
                    "PHILADELPHIA LAND BANK",
                    "CITY OF PHILA",
                    "REDEVELOPMENT AUTHORITY",
                ],
                "owner_2": ["PUBLIC PROP", "PUBLC PROP", "PUBLIC PROP", None],
                "city_owner_agency": [
                    "PHA",
                    "Land Bank (PHDC)",
                    "DPP",
                    "PRA",
                ],
                "side_yard_eligible": ["No", "Yes", "No", "No"],
            }
        )

        assert expected_gdf.equals(gdf)


if __name__ == "__main__":
    unittest.main()
