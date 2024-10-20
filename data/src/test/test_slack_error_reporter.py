import unittest
from unittest.mock import patch

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

from classes.slack_error_reporter import (
    send_error_to_slack,
)  # Ensure correct file import


class TestSlackNotifier(unittest.TestCase):
    @patch(
        "classes.slack_error_reporter.WebClient.chat_postMessage"
    )  # Correct patching
    @patch(
        "classes.slack_error_reporter.os.getenv", return_value="mock_slack_token"
    )  # Correct patching
    def test_send_error_to_slack(self, mock_getenv, mock_slack_post):
        """Test that Slack error reporting is triggered correctly."""

        error_message = "Test error message"

        # Call the Slack notification function
        send_error_to_slack(error_message)

        # Verify the Slack API call was made with the correct parameters
        mock_slack_post.assert_called_once_with(
            channel="clean-and-green-philly-back-end",  # Use actual channel ID
            text=error_message,
            username="Backend Error Reporter",
        )

    @patch(
        "classes.slack_error_reporter.WebClient.chat_postMessage"
    )  # Correct patching
    @patch(
        "classes.slack_error_reporter.os.getenv", return_value=None
    )  # Simulate missing Slack token
    def test_no_error_no_slack_message(self, mock_getenv, mock_slack_post):
        """Test that Slack notification is not triggered if there's no error."""

        # Call the Slack notification function (with no valid token)
        with self.assertRaises(ValueError):
            send_error_to_slack("Test error message")

        # Ensure Slack's chat_postMessage was not called due to missing token
        mock_slack_post.assert_not_called()


if __name__ == "__main__":
    unittest.main()
