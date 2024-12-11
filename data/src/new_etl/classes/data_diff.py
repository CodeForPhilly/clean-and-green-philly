from slack_sdk import WebClient
import pandas as pd
from sqlalchemy import text
import os

from config.psql import conn


class DiffReport:
    def __init__(
        self, conn=conn, table_name="all_properties_end", unique_id_col="opa_id"
    ):
        """
        Initialize the DiffReport.

        Args:
            conn: SQLAlchemy connection to the database.
            table_name (str): The name of the table to analyze.
            unique_id_col (str): Column used as a unique identifier.
        """
        self.conn = conn
        self.table_name = table_name
        self.unique_id_col = unique_id_col
        self.latest_timestamp = None
        self.previous_timestamp = None
        self.summary_text = ""

    def generate_diff(self):
        """
        Generate the data diff and summarize changes.
        """
        # Step 1: Retrieve the two most recent timestamps
        query_timestamps = text(f"""
        SELECT DISTINCT create_date 
        FROM {self.table_name}
        ORDER BY create_date DESC
        LIMIT 2;
        """)

        timestamps = pd.read_sql(query_timestamps, self.conn)["create_date"].tolist()

        if len(timestamps) < 2:
            print(
                f"Table '{self.table_name}' has less than two timestamps. Cannot perform comparison."
            )
            return

        self.latest_timestamp, self.previous_timestamp = timestamps[0], timestamps[1]

        print("Last two timestamps are:")
        print(self.latest_timestamp)
        print(self.previous_timestamp)

        # Step 2: Load data for the two timestamps into DataFrames
        query_latest = text(f"""
        SELECT * FROM {self.table_name} WHERE create_date = '{self.latest_timestamp}';
        """)
        query_previous = text(f"""
        SELECT * FROM {self.table_name} WHERE create_date = '{self.previous_timestamp}';
        """)

        df_latest = pd.read_sql(query_latest, self.conn)
        df_previous = pd.read_sql(query_previous, self.conn)

        # Step 3: Ensure DataFrames are aligned on the same index and columns
        common_columns = [
            col for col in df_latest.columns if col in df_previous.columns
        ]
        df_latest = df_latest[common_columns]
        df_previous = df_previous[common_columns]

        # Align indexes to include all rows from both DataFrames
        df_latest = df_latest.set_index(self.unique_id_col).reindex(
            df_previous.index.union(df_latest.index)
        )
        df_previous = df_previous.set_index(self.unique_id_col).reindex(
            df_previous.index.union(df_latest.index)
        )

        # Ensure columns are in the same order
        df_latest = df_latest[sorted(df_latest.columns)]
        df_previous = df_previous[sorted(df_previous.columns)]

        # Step 4: Perform the comparison
        diff = df_latest.compare(
            df_previous, align_axis=1, keep_shape=False, keep_equal=False
        )

        if diff.empty:
            print("No changes detected between the two timestamps.")
            self.summary_text = "No changes detected between the two timestamps."
            return

        # Step 5: Calculate percentage changes
        print("Calculating percentages...")
        total_rows = len(df_latest)
        changes_by_column = {
            col: (diff.xs(col, level=0, axis=1).notna().sum().sum() / total_rows) * 100
            for col in diff.columns.get_level_values(0).unique()
        }

        # Step 6: Create plain text summary
        summary_lines = [
            f"Diff Report for {self.table_name}",
            f"Latest timestamp: {self.latest_timestamp}",
            f"Previous timestamp: {self.previous_timestamp}",
            "",
            "Comparison Summary (% of rows with changes per column):",
        ]

        for col, pct_change in sorted(
            changes_by_column.items(), key=lambda x: x[1], reverse=True
        ):
            summary_lines.append(f"  - {col}: {pct_change:.2f}%")

        self.summary_text = "\n".join(summary_lines)

    def send_to_slack(self, channel="clean-and-green-philly-pipeline"):
        """
        Sends the diff summary to a Slack channel.

        Args:
            channel (str): The Slack channel to post the message to.
        """
        token = os.getenv("CAGP_SLACK_API_TOKEN")
        if token:
            client = WebClient(token=token)
            try:
                client.chat_postMessage(
                    channel=channel,
                    text=f"*Data Difference Report*\n\n{self.summary_text}",
                    username="Diff Reporter",
                )
                print("Diff report sent to Slack successfully.")
            except Exception as e:
                print(f"Failed to send diff report to Slack: {e}")
        else:
            raise ValueError("Slack API token not found in environment variables.")

    def run(self, send_to_slack=True, slack_channel="clean-and-green-philly-pipeline"):
        """
        Orchestrates the diff generation and optional Slack notification.

        Args:
            send_to_slack (bool): Whether to send the diff summary to Slack.
            slack_channel (str): The Slack channel to post the message to.
        """
        self.generate_diff()

        if send_to_slack and self.summary_text:
            print(f"Sending report to Slack channel: {slack_channel}...")
            self.send_to_slack(channel=slack_channel)
