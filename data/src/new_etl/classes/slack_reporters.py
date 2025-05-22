import os

import pandas as pd
from slack_sdk import WebClient


def send_dataframe_profile_to_slack(
    df: pd.DataFrame,
    df_name: str,
    channel="clean-and-green-philly-pipeline",
    slack_token: str | None = None,
):
    """
    Profiles a DataFrame and sends the QC profile summary to a Slack channel.

    Args:
        df (pd.DataFrame): The DataFrame to profile.
        df_name (str): The name of the DataFrame being profiled.
        channel (str): The Slack channel to post the message to.
        slack_token (str): The Slack API token. If not provided, it will be read from the environment.
    """
    token = slack_token or os.getenv("CAGP_SLACK_API_TOKEN")
    if not token:
        print("Slack API token not found in environment variables.")
        print("Skipping QC profile report to Slack.")
        return
    # Step 1: Profile the DataFrame
    profile_summary = {}

    # Count NA values
    profile_summary["na_counts"] = df.isna().sum().to_dict()

    # Numeric stats
    numeric_columns = df.select_dtypes(include=["number"]).columns
    profile_summary["numeric_stats"] = {}
    for column in numeric_columns:
        profile_summary["numeric_stats"][column] = {
            "mean": df[column].mean(),
            "median": df[column].median(),
            "std": df[column].std(),
        }

    # Unique values in string columns
    string_columns = df.select_dtypes(include=["object", "string"]).columns
    profile_summary["unique_values"] = df[string_columns].nunique().to_dict()

    # Step 2: Format the message
    message = f"*Dataset QC Summary: `{df_name}`*\n"

    # Missing Values
    message += "*Missing Values:*\n"
    for col, count in profile_summary["na_counts"].items():
        message += f"  - `{col}`: {count} missing\n"

    # Numeric Summary
    message += "\n*Numeric Summary:*\n"
    for col, stats in profile_summary["numeric_stats"].items():
        message += (
            f"  - `{col}`: Mean: {stats['mean']:.2f}, "
            f"Median: {stats['median']:.2f}, Std: {stats['std']:.2f}\n"
        )

    # Unique Values
    message += "\n*Unique Values in String Columns:*\n"
    for col, unique_count in profile_summary["unique_values"].items():
        message += f"  - `{col}`: {unique_count} unique values\n"

    # Step 3: Send to Slack
    client = WebClient(token=token)
    try:
        client.chat_postMessage(
            channel=channel,
            text=message,
            username="QC Reporter",
        )
        print(f"QC profile for `{df_name}` sent to Slack successfully.")
    except Exception as e:
        print(f"Failed to send QC profile for `{df_name}` to Slack: {e}")


def send_diff_report_to_slack(
    diff_summary: str,
    report_url: str,
    channel="clean-and-green-philly-pipeline",
    slack_token: str | None = None,
):
    """
    Sends a difference report summary to a Slack channel.

    Args:
        diff_summary (str): The summary of differences to post.
        report_url (str): The URL to the detailed difference report.
        channel (str): The Slack channel to post the message to.
        slack_token (str): The Slack API token. If not provided, it will be read from the environment.
    """
    print(
        f"send_diff_report_to_slack called with:\ndiff_summary:\n{diff_summary}\nreport_url: {report_url}"
    )
    token = slack_token or os.getenv("CAGP_SLACK_API_TOKEN")
    if not token:
        print("Slack API token not found in environment variables.")
        print("Skipping diff report to Slack.")
        return

    # Step 1: Format the message
    message = f"*Data Difference Report*\n\n{diff_summary}\n\nDetailed report: <{report_url}|View Report>"
    print(f"Formatted Slack message:\n{message}")

    # Step 2: Send the message to Slack
    client = WebClient(token=token)
    try:
        client.chat_postMessage(
            channel=channel,
            text=message,
            username="Diff Reporter",
        )
        print("Diff report sent to Slack successfully.")
    except Exception as e:
        print(f"Failed to send diff report to Slack: {e}")


def send_error_to_slack(error_message: str, slack_token: str | None = None) -> None:
    """Send error message to Slack."""

    token = slack_token or os.getenv("CAGP_SLACK_API_TOKEN")
    if not token:
        print("Slack API token not found in environment variables.")
        print("Skipping error report to Slack.")
        print("Error message:")
        print(error_message)
        return

    client = WebClient(token=token)
    client.chat_postMessage(
        channel="clean-and-green-philly-back-end",  # Replace with actual Slack channel ID
        text=error_message,
        username="Backend Error Reporter",
    )
