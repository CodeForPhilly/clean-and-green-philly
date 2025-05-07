import unittest

import geopandas as gpd

from new_etl.data_utils.delinquencies import transform_delinquencies_gdf


class TestCouncilDists(unittest.TestCase):
    def test_transform_delinquencies_gdf(self):
        """
        This tests that the relevant deliquency data columns which are missing are filled with the necessary defaults.
        """

        data = {
            "total_due": [100, None, 200],
            "is_actionable": [None, "Y", "N"],
            "payment_agreement": ["N", None, "Y"],
            "num_years_owed": [1, 2, None],
            "most_recent_year_owed": [None, 2020, 2021],
            "sheriff_sale": ["N", None, "Y"],
            "total_assessment": [300, 400, None],
        }
        gdf = gpd.GeoDataFrame(data)

        expected_data = {
            "total_due": [100, "NA", 200],
            "is_actionable": ["NA", "Y", "N"],
            "payment_agreement": ["N", "NA", "Y"],
            "num_years_owed": [1, 2, "NA"],
            "most_recent_year_owed": ["NA", 2020, 2021],
            "sheriff_sale": ["N", "N", "Y"],
            "total_assessment": [300, 400, "NA"],
        }
        expected_gdf = gpd.GeoDataFrame(expected_data)

        transform_delinquencies_gdf(gdf)

        assert gdf.equals(expected_gdf), (
            "The transformed GeoDataFrame does not match the expected output."
        )


if __name__ == "__main__":
    unittest.main()
