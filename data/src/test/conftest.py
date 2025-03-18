from unittest.mock import MagicMock

import pytest
from google.cloud.storage import Bucket


@pytest.fixture(autouse=True)
def mock_gcp_bucket(monkeypatch):
    mock_bucket = MagicMock(spec=Bucket)

    monkeypatch.setattr("classes.featurelayer.google_cloud_bucket", lambda: mock_bucket)

    return mock_bucket


# Tell vulture this is used:
_ = mock_gcp_bucket  # Used indirectly by pytest
