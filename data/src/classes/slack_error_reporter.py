import os

from slack_sdk import WebClient


def send_error_to_slack(error_message: str, slack_token: str | None = None) -> None:
    """Send error message to Slack."""
    token = slack_token or os.getenv("CAGP_SLACK_API_TOKEN")
    if not token:
        print("Slack API token not found in environment variables.")
        print("Skipping QC profile report to Slack.")
        return

    client = WebClient(token=token)
    client.chat_postMessage(
        channel="clean-and-green-philly-back-end",  # Replace with actual Slack channel ID
        text=error_message,
        username="Backend Error Reporter",
    )
