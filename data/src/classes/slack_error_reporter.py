import os
from slack_sdk import WebClient


def send_error_to_slack(error_message: str) -> None:
    """Send error message to Slack."""
    token: str | None = os.getenv("CAGP_SLACK_API_TOKEN")  # token can be None
    if token:
        client = WebClient(token=token)
        client.chat_postMessage(
            channel="clean-and-green-philly-back-end",  # Replace with actual Slack channel ID
            text=error_message,
            username="Backend Error Reporter",
        )
    else:
        raise ValueError("Slack API token not found in environment variables.")
