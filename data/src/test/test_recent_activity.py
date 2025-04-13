from unittest.mock import Mock, patch
import requests
import pandas as pd
from datetime import datetime
from new_etl.data_utils.recent_activity import recent_activity

# A fixed time for predictable "days since" calculations
FIXED_TIME = datetime(2025, 1, 1)


# Mock for successful API requests
def mock_requests_get_success(url, params):
    response = Mock()
    response.raise_for_status = lambda: None
    q = params.get("q", "")

    # Use fake data based on parts of the query
    if "permitissuedate" in q:
        response.json.return_value = {
            "rows": [{"opa_account_num": 123, "latest_permit_date": "2024-12-31"}]
        }
    elif "mostrecentissuedate" in q:
        response.json.return_value = {
            "rows": [
                {"opa_account_num": 123, "latest_business_license_date": "2024-12-30"}
            ]
        }
    elif "scheduleddate" in q:
        response.json.return_value = {
            "rows": [{"opa_account_num": 123, "latest_appeal_date": "2024-12-29"}]
        }
    else:
        response.json.return_value = {"rows": []}
    return response


# Mock for empty API results
def mock_requests_get_empty(url, params):
    response = Mock()
    response.raise_for_status = lambda: None
    response.json.return_value = {"rows": []}
    return response


# Mock for API errors
def mock_requests_get_error(url, params):
    response = Mock()
    response.raise_for_status.side_effect = requests.exceptions.HTTPError(
        "404 Not Found"
    )
    return response


# Mock for multiple properties with mixed data
def mock_requests_get_mixed_data(url, params):
    response = Mock()
    response.raise_for_status = lambda: None
    q = params.get("q", "")

    if "permitissuedate" in q:
        response.json.return_value = {
            "rows": [
                {"opa_account_num": 123, "latest_permit_date": "2024-12-31"},
                {"opa_account_num": 456, "latest_permit_date": "2024-11-15"},
                {"opa_account_num": 789, "latest_permit_date": None},
            ]
        }
    elif "mostrecentissuedate" in q:
        response.json.return_value = {
            "rows": [
                {"opa_account_num": 123, "latest_business_license_date": "2024-12-30"},
                {"opa_account_num": 456, "latest_business_license_date": None},
                {"opa_account_num": 999, "latest_business_license_date": "2024-10-01"},
            ]
        }
    elif "scheduleddate" in q:
        response.json.return_value = {
            "rows": [
                {"opa_account_num": 123, "latest_appeal_date": "2024-12-29"},
                {"opa_account_num": 789, "latest_appeal_date": "2024-09-15"},
            ]
        }
    else:
        response.json.return_value = {"rows": []}
    return response


# Test for the successful scenario
@patch(
    "new_etl.data_utils.recent_activity.requests.get",
    side_effect=mock_requests_get_success,
)
@patch("new_etl.data_utils.recent_activity.datetime")
def test_recent_activity_success(mock_datetime, mock_get):
    # Set the current time
    mock_datetime.now.return_value = FIXED_TIME
    # Allow datetime calls to work normally
    mock_datetime.side_effect = lambda *args, **kwargs: datetime(*args, **kwargs)

    # Create a more complete mock of FeatureLayer
    mock_feature_layer = Mock()
    mock_feature_layer.gdf = pd.DataFrame({"opa_id": [123]})
    # Initialize collected_metadata as an empty list
    mock_feature_layer.collected_metadata = []

    # Execute the function under test
    result_feature_layer = recent_activity(mock_feature_layer)

    # Assert appropriate values were added to the dataframe
    assert result_feature_layer.gdf.loc[0, "latest_permit_date"] == pd.Timestamp(
        "2024-12-31"
    )
    assert result_feature_layer.gdf.loc[0, "days_since_permit"] == 1
    assert result_feature_layer.gdf.loc[0, "has_permit_record"] == True

    assert result_feature_layer.gdf.loc[
        0, "latest_business_license_date"
    ] == pd.Timestamp("2024-12-30")
    assert result_feature_layer.gdf.loc[0, "days_since_business_license"] == 2
    assert result_feature_layer.gdf.loc[0, "has_business_license_record"] == True

    assert result_feature_layer.gdf.loc[0, "latest_appeal_date"] == pd.Timestamp(
        "2024-12-29"
    )
    assert result_feature_layer.gdf.loc[0, "days_since_appeal"] == 3
    assert result_feature_layer.gdf.loc[0, "has_appeal_record"] == True

    # Verify metadata was collected
    assert len(result_feature_layer.collected_metadata) == 1


# Test for empty API results
@patch(
    "new_etl.data_utils.recent_activity.requests.get",
    side_effect=mock_requests_get_empty,
)
@patch("new_etl.data_utils.recent_activity.datetime")
def test_recent_activity_empty_results(mock_datetime, mock_get):
    mock_datetime.now.return_value = FIXED_TIME
    mock_feature_layer = Mock()
    mock_feature_layer.gdf = pd.DataFrame({"opa_id": [123]})
    mock_feature_layer.collected_metadata = []

    result_feature_layer = recent_activity(mock_feature_layer)

    # Should have NaT for dates and 9999 for days_since columns
    assert pd.isna(result_feature_layer.gdf.loc[0, "latest_permit_date"])
    assert result_feature_layer.gdf.loc[0, "days_since_permit"] == 9999
    assert result_feature_layer.gdf.loc[0, "has_permit_record"] == False

    assert pd.isna(result_feature_layer.gdf.loc[0, "latest_business_license_date"])
    assert result_feature_layer.gdf.loc[0, "days_since_business_license"] == 9999
    assert result_feature_layer.gdf.loc[0, "has_business_license_record"] == False

    assert pd.isna(result_feature_layer.gdf.loc[0, "latest_appeal_date"])
    assert result_feature_layer.gdf.loc[0, "days_since_appeal"] == 9999
    assert result_feature_layer.gdf.loc[0, "has_appeal_record"] == False


# Test error handling
@patch(
    "new_etl.data_utils.recent_activity.requests.get",
    side_effect=mock_requests_get_error,
)
@patch("new_etl.data_utils.recent_activity.datetime")
def test_recent_activity_api_error(mock_datetime, mock_get):
    mock_datetime.now.return_value = FIXED_TIME
    mock_feature_layer = Mock()
    mock_feature_layer.gdf = pd.DataFrame({"opa_id": [123]})
    mock_feature_layer.collected_metadata = []

    result_feature_layer = recent_activity(mock_feature_layer)

    # Should handle errors gracefully and set values to NaT/9999
    assert pd.isna(result_feature_layer.gdf.loc[0, "latest_permit_date"])
    assert result_feature_layer.gdf.loc[0, "days_since_permit"] == 9999
    assert result_feature_layer.gdf.loc[0, "has_permit_record"] == False


# Test with different opa_id values
@patch(
    "new_etl.data_utils.recent_activity.requests.get",
    side_effect=mock_requests_get_success,
)
@patch("new_etl.data_utils.recent_activity.datetime")
def test_recent_activity_id_handling(mock_datetime, mock_get):
    mock_datetime.now.return_value = FIXED_TIME
    mock_feature_layer = Mock()

    # Create test data with string IDs
    mock_feature_layer.gdf = pd.DataFrame(
        {
            "opa_id": ["123", "456", "789-ABC", "00123"]  # Different formats
        }
    )
    mock_feature_layer.collected_metadata = []

    # Modify the mock to return data that matches string IDs
    def string_based_mock(url, params):
        response = Mock()
        response.raise_for_status = lambda: None
        q = params.get("q", "")

        if "permitissuedate" in q:
            response.json.return_value = {
                "rows": [
                    {"opa_account_num": "123", "latest_permit_date": "2024-12-31"},
                    {
                        "opa_account_num": "00123",
                        "latest_permit_date": "2024-12-15",
                    },  # Leading zeros preserved
                ]
            }
        # Other queries...

        return response

    # Use the string-based mock
    mock_get.side_effect = string_based_mock

    result_feature_layer = recent_activity(mock_feature_layer)

    # Should match string IDs correctly without numeric conversion
    assert result_feature_layer.gdf.loc[0, "latest_permit_date"] == pd.Timestamp(
        "2024-12-31"
    )
    assert result_feature_layer.gdf.loc[3, "latest_permit_date"] == pd.Timestamp(
        "2024-12-15"
    )


# Test with multiple properties and mixed data
@patch(
    "new_etl.data_utils.recent_activity.requests.get",
    side_effect=mock_requests_get_mixed_data,
)
@patch("new_etl.data_utils.recent_activity.datetime")
def test_recent_activity_multiple_properties(mock_datetime, mock_get):
    mock_datetime.now.return_value = FIXED_TIME
    mock_feature_layer = Mock()
    mock_feature_layer.gdf = pd.DataFrame({"opa_id": [123, 456, 789, 999]})
    mock_feature_layer.collected_metadata = []

    result_feature_layer = recent_activity(mock_feature_layer)

    # Property 123 should have all three dates
    assert result_feature_layer.gdf.loc[0, "latest_permit_date"] == pd.Timestamp(
        "2024-12-31"
    )
    assert result_feature_layer.gdf.loc[
        0, "latest_business_license_date"
    ] == pd.Timestamp("2024-12-30")
    assert result_feature_layer.gdf.loc[0, "latest_appeal_date"] == pd.Timestamp(
        "2024-12-29"
    )

    # Property 456 should have permit date but null business license date
    assert result_feature_layer.gdf.loc[1, "latest_permit_date"] == pd.Timestamp(
        "2024-11-15"
    )
    assert pd.isna(result_feature_layer.gdf.loc[1, "latest_business_license_date"])
    assert pd.isna(result_feature_layer.gdf.loc[1, "latest_appeal_date"])

    # Property 789 should have null permit date but have an appeal date
    assert pd.isna(result_feature_layer.gdf.loc[2, "latest_permit_date"])
    assert pd.isna(result_feature_layer.gdf.loc[2, "latest_business_license_date"])
    assert result_feature_layer.gdf.loc[2, "latest_appeal_date"] == pd.Timestamp(
        "2024-09-15"
    )

    # Property 999 should only have business license date
    assert pd.isna(result_feature_layer.gdf.loc[3, "latest_permit_date"])
    assert result_feature_layer.gdf.loc[
        3, "latest_business_license_date"
    ] == pd.Timestamp("2024-10-01")
    assert pd.isna(result_feature_layer.gdf.loc[3, "latest_appeal_date"])

    # Check days calculation for property 456 with permit from Nov 15
    expected_days = (FIXED_TIME - datetime(2024, 11, 15)).days
    assert result_feature_layer.gdf.loc[1, "days_since_permit"] == expected_days

    # Check has_record flags
    assert result_feature_layer.gdf.loc[0, "has_permit_record"] == True
    assert result_feature_layer.gdf.loc[1, "has_business_license_record"] == False
    assert result_feature_layer.gdf.loc[2, "has_appeal_record"] == True


@patch(
    "new_etl.data_utils.recent_activity.requests.get",
    side_effect=mock_requests_get_success,
)
@patch("new_etl.data_utils.recent_activity.datetime")
def test_recent_activity_schema_and_types(mock_datetime, mock_get):
    mock_datetime.now.return_value = FIXED_TIME
    mock_feature_layer = Mock()
    mock_feature_layer.gdf = pd.DataFrame({"opa_id": [123]})
    mock_feature_layer.collected_metadata = []

    result = recent_activity(mock_feature_layer)
    gdf = result.gdf

    expected_columns = {
        "latest_permit_date": "datetime64[ns]",
        "days_since_permit": "int64",
        "has_permit_record": "bool",
        "latest_business_license_date": "datetime64[ns]",
        "days_since_business_license": "int64",
        "has_business_license_record": "bool",
        "latest_appeal_date": "datetime64[ns]",
        "days_since_appeal": "int64",
        "has_appeal_record": "bool",
    }

    for col, expected_type in expected_columns.items():
        assert col in gdf.columns, f"Missing expected column: {col}"
        assert str(gdf[col].dtype) == expected_type, (
            f"{col} dtype is {gdf[col].dtype}, expected {expected_type}"
        )


@patch(
    "new_etl.data_utils.recent_activity.requests.get",
    side_effect=mock_requests_get_success,
)
@patch("new_etl.data_utils.recent_activity.datetime")
def test_recent_activity_merge_mismatch(mock_datetime, mock_get):
    mock_datetime.now.return_value = FIXED_TIME
    mock_feature_layer = Mock()
    # opa_id doesn't match any returned opa_account_num
    mock_feature_layer.gdf = pd.DataFrame({"opa_id": [99999]})
    mock_feature_layer.collected_metadata = []

    result = recent_activity(mock_feature_layer)
    gdf = result.gdf

    # Should still have valid schema
    assert "latest_permit_date" in gdf.columns
    assert pd.isna(gdf.loc[0, "latest_permit_date"])
    assert gdf.loc[0, "days_since_permit"] == 9999
    assert gdf.loc[0, "has_permit_record"] == False


@patch(
    "new_etl.data_utils.recent_activity.requests.get",
    side_effect=mock_requests_get_success,
)
@patch("new_etl.data_utils.recent_activity.datetime")
def test_recent_activity_opa_id_type_mismatch(mock_datetime, mock_get):
    mock_datetime.now.return_value = FIXED_TIME
    mock_feature_layer = Mock()
    # String opa_id, but mock returns int
    mock_feature_layer.gdf = pd.DataFrame({"opa_id": ["123"]})
    mock_feature_layer.collected_metadata = []

    result = recent_activity(mock_feature_layer)
    gdf = result.gdf

    # Should not match, expect NaT
    assert pd.isna(gdf.loc[0, "latest_permit_date"])
    assert gdf.loc[0, "days_since_permit"] == 9999
    assert gdf.loc[0, "has_permit_record"] == False


def mock_requests_get_missing_column(url, params):
    response = Mock()
    response.raise_for_status = lambda: None
    q = params.get("q", "")
    if "permitissuedate" in q:
        response.json.return_value = {
            "rows": [{"opa_account_num": 123}]
        }  # Missing latest_permit_date
    elif "mostrecentissuedate" in q:
        response.json.return_value = {
            "rows": [
                {"opa_account_num": 123, "latest_business_license_date": "2024-12-30"}
            ]
        }
    elif "scheduleddate" in q:
        response.json.return_value = {
            "rows": [{"opa_account_num": 123, "latest_appeal_date": "2024-12-29"}]
        }
    return response


@patch(
    "new_etl.data_utils.recent_activity.requests.get",
    side_effect=mock_requests_get_missing_column,
)
@patch("new_etl.data_utils.recent_activity.datetime")
def test_recent_activity_missing_column_in_response(mock_datetime, mock_get):
    mock_datetime.now.return_value = FIXED_TIME
    mock_feature_layer = Mock()
    mock_feature_layer.gdf = pd.DataFrame({"opa_id": [123]})
    mock_feature_layer.collected_metadata = []

    result = recent_activity(mock_feature_layer)
    gdf = result.gdf

    # Should have NaT because permit date was missing
    assert "latest_permit_date" in gdf.columns
    assert pd.isna(gdf.loc[0, "latest_permit_date"])
    assert gdf.loc[0, "days_since_permit"] == 9999
    assert gdf.loc[0, "has_permit_record"] == False
