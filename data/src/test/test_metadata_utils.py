import unittest

import geopandas as gpd
import pytest

from src.new_etl.metadata.metadata_utils import (
    get_column_details,
    get_description_from_docstring,
    get_sections_from_docstring,
    normalize_whitespace,
    parse_docstring,
    provide_metadata,
)

# Stub functions with actual docstrings used for parsing tests


def stub_update_vacant_community(primary_featurelayer):
    """
    Updates the 'vacant' column in the primary feature layer to ensure community gardens
    are marked as not vacant. This protects known community gardens from being categorized
    as vacant, preventing potential predatory development.

    Args:
        primary_featurelayer (FeatureLayer): The feature layer containing property data.

    Returns:
        FeatureLayer: The input feature layer with the 'vacant' column updated to False
        for parcels containing community gardens.

    Tagline:
        Mark Community Gardens as Not Vacant

    Columns updated:
        vacant: Updated to False for parcels containing community gardens.

    Primary Feature Layer Columns Referenced:
        vacant, ipa_id
    """
    pass


def stub_kde_analysis(primary_featurelayer):
    """
    Applies kernel density estimation (KDE) analysis for drug crimes to the primary feature layer.

    Args:
        primary_featurelayer (FeatureLayer): The feature layer containing property data.

    Returns:
        FeatureLayer: The input feature layer with KDE analysis results for drug crimes.

    Tagline:
        Density analysis for drug crimes

    Source:
        https://phl.carto.com/api/v2/sql
    """
    pass


def stub_load_opa():
    """
    Loads and processes OPA property data, standardizing addresses and cleaning geometries.

    Returns:
        FeatureLayer: A feature layer containing processed OPA property data.

    Columns added:
        opa_id (type): desc
        market_value (type): desc
        sale_date (type): desc
        sale_price (numeric): desc
        parcel_type (type): desc
        zip_code (type): desc
        zoning (type): desc
        owner_1 (type): desc
        owner_2 (type): desc
        building_code_description (str): desc
        standardized_address (str): A standardized mailing address
        geometry (type): desc

    Source:
        https://phl.carto.com/api/v2/sql

    Tagline:
        Load OPA data
    """
    pass


def stub_update_vacant_ppr(primary_featurelayer):
    """
    Updates the 'vacant' column in the primary feature layer to ensure PPR properties
    are marked as not vacant. This prevents PPR properties from being miscategorized as vacant.

    Args:
        primary_featurelayer (FeatureLayer): The primary feature layer to update.

    Returns:
        FeatureLayer: The updated primary feature layer.

    Columns updated:
        vacant: Updated to False for PPR properties.

    Tagline:
        Mark Parks as Not Vacant

    Source:
        https://services.arcgis.com/fLeGjb7u4uXqeF9q/ArcGIS/rest/services/PPR_Properties/FeatureServer/0

    Known issues:
        If the Ersi REST URL is not available the function
        will fall back to loading the data from a GeoJSON URL:
        https://opendata.arcgis.com/datasets/d52445160ab14380a673e5849203eb64_0.geojson
    """
    pass


def stub_columns_added_variation(primary_featurelayer):
    """
    Function with a docstring that uses 'Columns Added:' key variation.

    Args:
        primary_featurelayer (FeatureLayer): The feature layer.

    Returns:
        FeatureLayer: The updated feature layer.

    Columns Added:
        column_x (int): Some description for column_x.
        column_y (float): Some description for column_y.

    Tagline:
        Example tagline
    """
    pass


def stub_only_args_and_returns(primary_featurelayer):
    """
    Function with only args and returns sections.

    Args:
        primary_featurelayer (FeatureLayer): The feature layer.

    Returns:
        FeatureLayer: The updated feature layer.
    """
    pass


@provide_metadata()
@pytest.mark.skip
def sample_add_columns(primary_featurelayer):
    """
    Adds columns to the primary feature layer.

    Args:
        primary_featurelayer (FeatureLayer): The feature layer to update.

    Returns:
        FeatureLayer: The updated primary feature layer.

    Columns added:
        column1 (int): Description for column1.

    Tagline:
        Example tagline
    """
    new_layer = FeatureLayer(  # noqa: F821
        name="stub_add_columns",
    )

    new_layer.gdf = gpd.GeoDataFrame(
        data={"opa_number": ["1", "2", "3"], "column1": [1, 2, 3]}
    )
    primary_featurelayer.opa_join(
        new_layer.gdf,
        "opa_number",
    )

    return primary_featurelayer


class TestMetadataUtils(unittest.TestCase):
    def test_normalize_whitespace(self):
        test_cases = [
            ("Hello   world", "Hello world"),
            ("Line1\nLine2", "Line1 Line2"),
            ("  Leading and   multiple   spaces ", "Leading and multiple spaces"),
        ]
        for input_text, expected in test_cases:
            with self.subTest(input_text=input_text):
                result = normalize_whitespace(input_text)
                self.assertEqual(result, expected)

    def test_get_description_from_docstring(self):
        # Ensure description extraction stops before a section header.
        docstring = (
            "This is the function description.\n\n"
            "Args:\n    param (int): parameter description"
        )
        expected = "This is the function description."
        result = get_description_from_docstring(docstring)
        self.assertEqual(result, expected)

    def test_get_sections_from_docstring(self):
        # Test that sections are correctly extracted.
        docstring = (
            "This is a description.\n\n"
            "Args:\n    param (int): description\n\n"
            "Returns:\n    int: result"
        )
        sections = get_sections_from_docstring(docstring)
        self.assertIn("args", sections)
        self.assertIn("returns", sections)
        self.assertTrue(sections["args"].strip())
        self.assertTrue(sections["returns"].strip())

    def test_get_column_details(self):
        # Test column details extraction.
        text = "col1 (int): description for col1\ncol2 (str): description for col2"
        expected = [
            {"name": "col1", "type": "int", "description": "description for col1"},
            {"name": "col2", "type": "str", "description": "description for col2"},
        ]
        result = get_column_details(text)
        self.assertEqual(result, expected)

    def test_parse_docstring(self):
        test_cases = [
            (
                stub_update_vacant_community.__doc__,
                {
                    "description": (
                        "Updates the 'vacant' column in the primary feature layer to ensure community gardens "
                        "are marked as not vacant. This protects known community gardens from being categorized as "
                        "vacant, preventing potential predatory development."
                    ),
                    "returns": (
                        "FeatureLayer: The input feature layer with the 'vacant' column updated to False for parcels "
                        "containing community gardens."
                    ),
                    "tagline": "Mark Community Gardens as Not Vacant",
                    "columns updated": [
                        {
                            "name": "vacant",
                            "description": "Updated to False for parcels containing community gardens.",
                        }
                    ],
                    "columns added": [],
                    "source": "",
                    "known issues": "",
                    "primary feature layer columns referenced": ["vacant", "ipa_id"],
                },
            ),
            (
                stub_kde_analysis.__doc__,
                {
                    "description": "Applies kernel density estimation (KDE) analysis for drug crimes to the primary feature layer.",
                    "returns": "FeatureLayer: The input feature layer with KDE analysis results for drug crimes.",
                    "tagline": "Density analysis for drug crimes",
                    "source": "https://phl.carto.com/api/v2/sql",
                    "columns added": [],
                    "columns updated": [],
                    "known issues": "",
                    "primary feature layer columns referenced": [],
                },
            ),
            (
                stub_load_opa.__doc__,
                {
                    "description": "Loads and processes OPA property data, standardizing addresses and cleaning geometries.",
                    "returns": "FeatureLayer: A feature layer containing processed OPA property data.",
                    "tagline": "Load OPA data",
                    "source": "https://phl.carto.com/api/v2/sql",
                    # For columns added, we expect a list of 12 dictionaries.
                    "columns added": "list_of_12",
                    "columns updated": [],
                    "known issues": "",
                    "primary feature layer columns referenced": [],
                },
            ),
            (
                stub_update_vacant_ppr.__doc__,
                {
                    "description": (
                        "Updates the 'vacant' column in the primary feature layer to ensure PPR properties "
                        "are marked as not vacant. This prevents PPR properties from being miscategorized as vacant."
                    ),
                    "returns": "FeatureLayer: The updated primary feature layer.",
                    "tagline": "Mark Parks as Not Vacant",
                    "source": "https://services.arcgis.com/fLeGjb7u4uXqeF9q/ArcGIS/rest/services/PPR_Properties/FeatureServer/0",
                    "columns updated": [
                        {
                            "name": "vacant",
                            "description": "Updated to False for PPR properties.",
                        }
                    ],
                    "columns added": [],
                    "known issues": (
                        "If the Ersi REST URL is not available the function"  # NOTE: because the next line has a colon, only the first line is captured
                    ),
                    "primary feature layer columns referenced": [],
                },
            ),
            (
                stub_columns_added_variation.__doc__,
                {
                    "description": "Function with a docstring that uses 'Columns Added:' key variation.",
                    "returns": "FeatureLayer: The updated feature layer.",
                    "tagline": "Example tagline",
                    "columns added": [
                        {
                            "name": "column_x",
                            "type": "int",
                            "description": "Some description for column_x.",
                        },
                        {
                            "name": "column_y",
                            "type": "float",
                            "description": "Some description for column_y.",
                        },
                    ],
                    "columns updated": [],
                    "source": "",
                    "known issues": "",
                    "primary feature layer columns referenced": [],
                },
            ),
            (
                stub_only_args_and_returns.__doc__,
                {
                    "description": "Function with only args and returns sections.",
                    "returns": "FeatureLayer: The updated feature layer.",
                    "tagline": "",
                    "columns added": [],
                    "columns updated": [],
                    "source": "",
                    "known issues": "",
                    "primary feature layer columns referenced": [],
                },
            ),
        ]
        for docstring, expected_metadata in test_cases:
            with self.subTest(docstring=docstring):
                print(expected_metadata["description"])
                metadata = parse_docstring(docstring)
                # For stub_load_opa, we expect a list of 12 columns.
                if expected_metadata["columns added"] == "list_of_12":
                    self.assertIsInstance(metadata.get("columns added"), list)
                    self.assertEqual(len(metadata.get("columns added")), 12)
                else:
                    self.assertEqual(
                        metadata.get("columns added"),
                        expected_metadata["columns added"],
                    )
                fields = metadata.keys()
                for field in fields:
                    if field == "columns added":
                        continue
                    self.assertEqual(metadata.get(field), expected_metadata[field])

    @pytest.mark.skip
    def test_provide_metadata_with_sample_add_columns(self):
        # Test that the metadata is correctly added to the function output.
        primary_featurelayer = FeatureLayer(name="stub")  # noqa F821
        primary_featurelayer.gdf = gpd.GeoDataFrame(
            data={
                "opa_id": ["1", "2", "3"],
                "existing_field": [1, 2, 3],
                "geometry": gpd.points_from_xy([1, 2, 3], [1, 2, 3]),
            }
        )
        result = sample_add_columns(primary_featurelayer)
        metadata = result.collected_metadata

        expected_metadata = {
            "name": "sample_add_columns",
            "description": "Adds columns to the primary feature layer.",
            "returns": "FeatureLayer: The updated primary feature layer.",
            "start_time": "2021-10-01 00:00:00",
            "end_time": "2021-10-01 00:00:00",
            "duration_in_seconds": 0.0,
            "tagline": "Example tagline",
            "columns_added": [
                {
                    "name": "column1",
                    "type": "int",
                    "description": "Description for column1.",
                }
            ],
            "columns_updated": [],
            "source": "",
            "known_issues": "",
            "primary_feature_layer_columns_referenced": [],
        }
        most_recent_metadata = metadata[-1]
        fields = most_recent_metadata.keys()
        assert sorted(fields) == sorted(expected_metadata.keys())
        for field in fields:
            if field in ["start_time", "end_time", "duration_in_seconds"]:
                continue
            self.assertEqual(most_recent_metadata.get(field), expected_metadata[field])
            self.assertEqual(most_recent_metadata.get(field), expected_metadata[field])
