from sqlalchemy import text
import os
from slack_sdk import WebClient

import pandas as pd


def send_dataframe_profile_to_slack(
    df: pd.DataFrame, df_name: str, channel="clean-and-green-philly-pipeline"
):
    """
    Profiles a DataFrame and sends the QC profile summary to a Slack channel.

    Args:
        df (pd.DataFrame): The DataFrame to profile.
        df_name (str): The name of the DataFrame being profiled.
        channel (str): The Slack channel to post the message to.
    """
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
    token = os.getenv("CAGP_SLACK_API_TOKEN")
    if token:
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
    else:
        raise ValueError("Slack API token not found in environment variables.")


def send_pg_stats_to_slack(conn):
    """
    Report total sizes for all hypertables using hypertable_detailed_size
    and send the result to a Slack channel.
    """
    # Step 1: Get all hypertable names
    hypertable_query = """
    SELECT hypertable_name
    FROM timescaledb_information.hypertables;
    """
    result = conn.execute(text(hypertable_query))
    hypertables = [row[0] for row in result]  # Extract first column of each tuple

    # Step 2: Query detailed size for each hypertable
    detailed_sizes = []
    for hypertable in hypertables:
        size_query = f"SELECT * FROM hypertable_detailed_size('{hypertable}');"
        size_result = conn.execute(text(size_query))
        for row in size_result:
            # Append the total size (row[3] = total_bytes)
            detailed_sizes.append(
                {
                    "hypertable": hypertable,
                    "total_bytes": row[3],
                }
            )

    # Step 3: Format the message for Slack
    message = "*Hypertable Total Sizes:*\n"
    for size in detailed_sizes:
        total_bytes = size["total_bytes"]
        total_size = (
            f"{total_bytes / 1073741824:.2f} GB"
            if total_bytes >= 1073741824
            else f"{total_bytes / 1048576:.2f} MB"
            if total_bytes >= 1048576
            else f"{total_bytes / 1024:.2f} KB"
        )
        message += f"- {size['hypertable']}: {total_size}\n"

    # Step 4: Send to Slack
    token = os.getenv("CAGP_SLACK_API_TOKEN")
    if token:
        client = WebClient(token=token)
        client.chat_postMessage(
            channel="clean-and-green-philly-pipeline",
            text=message,
            username="PG Stats Reporter",
        )
    else:
        raise ValueError("Slack API token not found in environment variables.")


def send_diff_report_to_slack(
    diff_summary: str, report_url: str, channel="clean-and-green-philly-pipeline"
):
    """
    Sends a difference report summary to a Slack channel.

    Args:
        diff_summary (str): The summary of differences to post.
        report_url (str): The URL to the detailed difference report.
        channel (str): The Slack channel to post the message to.
    """
    print(
        f"send_diff_report_to_slack called with:\ndiff_summary:\n{diff_summary}\nreport_url: {report_url}"
    )

    # Step 1: Format the message
    message = f"*Data Difference Report*\n\n{diff_summary}\n\nDetailed report: <{report_url}|View Report>"
    print(f"Formatted Slack message:\n{message}")

    # Step 2: Send the message to Slack
    token = os.getenv("CAGP_SLACK_API_TOKEN")
    if token:
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
    else:
        raise ValueError("Slack API token not found in environment variables.")


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
