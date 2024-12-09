import logging as log
import os
from sqlalchemy.sql import text

from .featurelayer import google_cloud_bucket
from config.config import (
    log_level,
    report_to_slack_channel,
)
from config.psql import conn
from slack_sdk import WebClient
import pandas as pd


log.basicConfig(level=log_level)


class DiffTable:
    """Metadata about a table to be run through data-diff"""

    def __init__(self, table: str, pk_cols: list[str], where: str = None):
        """constructor

        Args:
            table (str): the name of the table in postgres
            pk_cols (list[str]): the list of columns in the primary key
            where (str, optional): any additional where clause to limit the rows being compared
        """
        self.table = table
        self.pk_cols = pk_cols
        self.where = where


class DiffReport:
    """
    Class to manage computing data differences for all tables between the newly imported schema and the last schema.
    Build a report of summary differences for all tables.
    Post difference summary to Slack.
    """

    def __init__(self, conn, table_name: str, timestamp_string: str = None):
        """
        Constructor for DiffReport.

        Args:
            conn: SQLAlchemy connection to the database.
            table_name (str): The name of the table to generate the diff report for.
            timestamp_string (str, optional): Specific timestamp to compare against. If None, fetch the latest timestamp.
        """
        self.conn = conn
        self.table_name = table_name
        self.timestamp_string = timestamp_string or self._get_latest_timestamp()
        self.report: str = f"The back-end data has been fully refreshed. Here is the difference report for `{table_name}`.\n\n"
        self.diff_tables = self._list_diff_tables()

    def _get_latest_timestamp(self) -> str:
        """
        Fetch the most recent timestamp from the hypertable.

        Returns:
            str: The latest timestamp as a string.

        Raises:
            ValueError: If no data is found in the table.
        """
        timestamp_query = f"""
        SELECT MAX(create_date) FROM {self.table_name};
        """
        latest_timestamp = self.conn.execute(text(timestamp_query)).scalar()
        if not latest_timestamp:
            raise ValueError(f"No prior data found in {self.table_name}.")
        return str(latest_timestamp)

    def _table_exists(self, table: str) -> bool:
        """
        Check if a table exists in the database.

        Args:
            table (str): Name of the table to check

        Returns:
            bool: True if table exists, False otherwise
        """
        check_table_query = text("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = :table_name
            )
        """)

        try:
            result = self.conn.execute(
                check_table_query, {"table_name": table}
            ).scalar()
            return result
        except Exception as e:
            log.error(f"Error checking table existence for {table}: {e}")
            return False

    def run(self):
        for diff_table in self.diff_tables:
            log.debug(
                "Processing table %s with pks %s", diff_table.table, diff_table.pk_cols
            )

            # Check if table exists
            if not self._table_exists(diff_table.table):
                self.report += (
                    f"{diff_table.table}: Table does not yet exist in the database.\n\n"
                )
                continue

            try:
                summary = self.compare_table(diff_table)
                if "No prior data" in summary:
                    self.report += f"{diff_table.table}:\n{summary}\n"
                    continue

                self.report += f"{diff_table.table}:\n{summary}\n"

                try:
                    self.report += (
                        "Details: " + self.detail_report(diff_table.table) + "\n"
                    )
                except Exception as detail_error:
                    log.error(
                        f"Error generating detail report for {diff_table.table}: {detail_error}"
                    )
                    self.report += (
                        f"Could not generate detailed report for {diff_table.table}.\n"
                    )

                self.report += "\n"

            except Exception as e:
                log.error(f"Error processing table {diff_table.table}: {e}")
                self.report += (
                    f"{diff_table.table}: Error processing table - {str(e)}\n\n"
                )

        log.debug(self.report)
        self.send_report_to_slack()

    def detail_report(self, table: str) -> str:
        """Generate the html from the detail diff report and upload to Google cloud as an html file
        Args:
            table (str): the name of the core table being compared

        Returns:
            str: the full url of the report
        """
        return self._save_detail_report_to_cloud(
            self.generate_table_detail_report(table), table
        )

    def _save_detail_report_to_cloud(self, html: str, table: str) -> str:
        """Save this html to a public cloud folder in Google named with the timestamp of the backup

        Args:
            html (str): the html content
            table (str): the name of the core table being compared

        Returns:
            str: the full url of the report
        """
        path: str = "diff/" + self.timestamp_string + "/" + table + ".html"
        bucket = google_cloud_bucket()
        blob = bucket.blob(path)
        blob.upload_from_string(html, content_type="text/html")
        return "https://storage.googleapis.com/" + bucket.name + "/" + path

    def generate_table_detail_report(self, table: str) -> str:
        """
        generate an html table of the details of differences in this table
        """
        # Directly query the table with differences
        sql: str = f"""
        SELECT * FROM {table}_diff 
        WHERE create_date = '{self.timestamp_string}'
        """
        cur = conn.connection.cursor()
        cur.execute(sql)
        html: str = "<table border=1><tr>"

        column_names = [desc[0] for desc in cur.description]
        for column in column_names:
            html += "<th>" + column + "</th>"
        html += "</tr>"
        for row in cur.fetchall():
            html += "<tr>"
            for value in row:
                html += "<td>" + str(value) + "</td>"
            html += "</tr>"
        html += "</table>"
        return html

    def _list_diff_tables(self) -> list[DiffTable]:
        """
        list table metadata to do the diff on
        Returns:
            list[DiffTable]: the list of metadata
        """
        return [
            DiffTable(
                table="vacant_properties",
                pk_cols=["opa_id", "parcel_type"],
                where="opa_id is not null",
            ),
            DiffTable(table="li_complaints", pk_cols=["service_request_id"]),
            DiffTable(
                table="li_violations",
                pk_cols=["violationnumber", "opa_account_num"],
                where="opa_account_num is not null",
            ),
            DiffTable(table="opa_properties", pk_cols=["parcel_number"]),
            DiffTable(
                table="property_tax_delinquencies",
                pk_cols=["opa_number"],
                where="opa_number <> 0",
            ),
        ]

    def compare_table(self, diff_table: DiffTable):
        # Step 1: Retrieve timestamps
        timestamps = self._get_timestamps(diff_table.table)
        if len(timestamps) < 2:
            return f"No prior data available for comparison in {diff_table.table}.\n"

        latest, second_latest = timestamps

        # Step 2: Fetch data for comparison
        current_query = f"""
        SELECT * FROM {diff_table.table} WHERE create_date = '{latest}';
        """
        past_query = f"""
        SELECT * FROM {diff_table.table} WHERE create_date = '{second_latest}';
        """
        current_data = pd.read_sql(current_query, conn)
        past_data = pd.read_sql(past_query, conn)

        # Step 3: Use DataFrames for comparison
        diffs = current_data.merge(past_data, how="outer", indicator=True)

        summary = {
            "added": diffs[diffs["_merge"] == "left_only"].shape[0],
            "removed": diffs[diffs["_merge"] == "right_only"].shape[0],
            "updated": diffs[diffs["_merge"] == "both"].shape[0],
        }

        # Format as a string for reporting
        summary_str = (
            f"{summary['added']} rows exclusive to the latest data.\n"
            f"{summary['removed']} rows exclusive to the past data.\n"
            f"{summary['updated']} rows present in both datasets.\n"
        )
        return summary_str

    def _get_timestamps(self, table: str) -> list:
        """
        Retrieve timestamps for the given table in descending order.

        Args:
            table (str): Name of the table to retrieve timestamps for

        Returns:
            list: List of timestamps in descending order
        """
        timestamp_query = f"""
        SELECT DISTINCT create_date 
        FROM {table} 
        ORDER BY create_date DESC 
        LIMIT 2;
        """
        timestamps = self.conn.execute(text(timestamp_query)).scalars().all()
        return list(timestamps)

    def send_report_to_slack(self):
        """
        post the summary report to the slack channel if configured.
        """
        if report_to_slack_channel:
            token = os.environ["CAGP_SLACK_API_TOKEN"]
            client = WebClient(token=token)

            # Send a message
            client.chat_postMessage(
                channel=report_to_slack_channel,
                text=self.report,
                username="CAGP Diff Bot",
            )
