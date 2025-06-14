import os
from typing import List

import pandas as pd
from slack_sdk import WebClient

from src.classes.file_manager import FileManager, FileType, LoadType

file_manager = FileManager()


class SlackReporter:
    def __init__(self, token: str):
        self.token = token
        self.client = WebClient(token=token)

    def send_dataframe_profile_to_slack(
        self,
        df: pd.DataFrame,
        df_name: str,
        channel="clean-and-green-philly-etl",
    ):
        """
        Profiles a DataFrame and sends the QC profile summary to a Slack channel.

        Args:
            df (pd.DataFrame): The DataFrame to profile.
            df_name (str): The name of the DataFrame being profiled.
            channel (str): The Slack channel to post the message to.
            slack_token (str): The Slack API token. If not provided, it will be read from the environment.
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
        try:
            self.client.chat_postMessage(
                channel=channel,
                text=message,
                username="QC Reporter",
            )
            print(f"QC profile for `{df_name}` sent to Slack successfully.")
        except Exception as e:
            print(f"Failed to send QC profile for `{df_name}` to Slack: {e}")

    def send_parquet_stats_to_slack(self, table_names: List[str]):
        """
        Report total sizes for all hypertables using hypertable_detailed_size
        and send the result to a Slack channel.
        """

        detailed_sizes = []

        for table_name in table_names:
            file_name = file_manager.generate_file_label(table_name)
            if not file_manager.check_file_exists(
                file_name, LoadType.SOURCE_CACHE, FileType.PARQUET
            ):
                print(
                    f"Unable to locate cached file for {table_name} from this current run"
                )
                continue

            file_path = file_manager.get_file_path(
                file_name, LoadType.SOURCE_CACHE, FileType.PARQUET
            )
            file_size = os.path.getsize(file_path)
            detailed_sizes.append(
                {
                    "table": table_name,
                    "total_bytes": file_size,
                }
            )

        # Step 3: Format the message for Slack
        message = "*Parquet File Total Sizes:*\n"
        for size in detailed_sizes:
            total_bytes = size["total_bytes"]
            total_size = (
                f"{total_bytes / 1073741824:.2f} GB"
                if total_bytes >= 1073741824
                else f"{total_bytes / 1048576:.2f} MB"
                if total_bytes >= 1048576
                else f"{total_bytes / 1024:.2f} KB"
            )
            message += f"- {size['table']}: {total_size}\n"

        # Step 4: Send to Slack
        self.client.chat_postMessage(
            channel="clean-and-green-philly-pipeline",
            text=message,
            username="PG Stats Reporter",
        )

    def send_diff_report_to_slack(
        self,
        diff_summary: str,
        channel="clean-and-green-philly-etl",
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
            f"send_diff_report_to_slack called with:\ndiff_summary:\n{diff_summary}\n"
        )

        # Step 1: Format the message
        message = f"*Data Difference Report*\n\n{diff_summary}\n"
        print(f"Formatted Slack message:\n{message}")

        try:
            self.client.chat_postMessage(
                channel=channel,
                text=message,
                username="Diff Reporter",
            )
            print("Diff report sent to Slack successfully.")
        except Exception as e:
            print(f"Failed to send diff report to Slack: {e}")

    def send_error_to_slack(self, error_message: str) -> None:
        """Send error message to Slack."""

        if not self.token:
            print("Slack API token not found in environment variables.")
            print("Skipping error report to Slack.")
            print("Error message:")
            print(error_message)
            return
        try:
            self.client.chat_postMessage(
                channel="clean-and-green-philly-etl",  # Replace with actual Slack channel ID
                text=error_message,
                username="Backend Error Reporter",
            )
        except Exception as e:
            print(f"Failsed to send error report to Slack {e}")
