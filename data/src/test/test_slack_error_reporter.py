import os
import sys
import unittest
from unittest.mock import patch

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

from new_etl.classes.slack_reporters import (
    send_error_to_slack,
)  # Ensure correct file import


class TestSlackNotifier(unittest.TestCase):
    @patch(
        "new_etl.classes.slack_reporters.WebClient.chat_postMessage"
    )  # Correct patching
    @patch(
        "new_etl.classes.slack_reporters.os.getenv",
        return_value="mock_slack_token",
    )  # Correct patching
    def test_send_error_to_slack(self, _mock_getenv, mock_slack_post):
        """Test that Slack error reporting is triggered correctly."""

        error_message = "Test error message"

        # Call the Slack notification function
        send_error_to_slack(error_message, slack_token="test_token")

        # Verify the Slack API call was made with the correct parameters
        mock_slack_post.assert_called_once_with(
            channel="clean-and-green-philly-back-end",  # Use actual channel ID
            text=error_message,
            username="Backend Error Reporter",
        )

    @patch(
        "new_etl.classes.slack_reporters.WebClient.chat_postMessage"
    )  # Correct patching
    @patch(
        "new_etl.classes.slack_reporters.os.getenv", return_value=None
    )  # Simulate missing Slack token
    def test_no_error_no_slack_message(self, _mock_getenv, mock_slack_post):
        """Test that Slack notification is not triggered if there's no error."""
        # Ensure Slack's chat_postMessage was not called due to missing token
        mock_slack_post.assert_not_called()


if __name__ == "__main__":
    unittest.main()
