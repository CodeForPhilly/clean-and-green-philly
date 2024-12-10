import logging as log
import os
import re
import subprocess
from sqlalchemy.sql import text
from slack_sdk import WebClient

from config.psql import conn, url
from new_etl.data_utils.utils import mask_password

from .featurelayer import google_cloud_bucket

log.basicConfig(level=log.DEBUG)


class DiffTable:
    """Metadata about a table to be run through data-diff."""

    def __init__(self, table: str, pk_cols: list[str], where: str = None):
        self.table = table
        self.pk_cols = pk_cols
        self.where = where


class DiffReport:
    """
    Class to compute and report data differences for TimescaleDB hypertables.
    Compares current data with the most recent historical chunk.
    """

    def __init__(self, timestamp_string: str = None):
        self.diff_tables = self._list_diff_tables()
        self.timestamp_string = timestamp_string or self._get_current_timestamp()
        self.report: str = "The back-end data has been refreshed. Here is the difference report on key tables:\n\n"

    def _get_current_timestamp(self) -> str:
        """
        Retrieve the current timestamp for the report.
        Uses the most recent create_date across all diff tables.
        """
        try:
            # Collect all tables' timestamps
            table_queries = [
                f"SELECT MAX(create_date) as latest_timestamp FROM public.{diff_table.table}"
                for diff_table in self.diff_tables
            ]
            union_query = " UNION ALL ".join(table_queries)
            query = f"SELECT to_char(MAX(latest_timestamp), 'YYYY-MM-DD_HH24-MI-SS') FROM ({union_query}) as combined"

            result = conn.execute(text(query))
            timestamp = result.scalar()
            return timestamp or "unknown_timestamp"
        except Exception as e:
            log.warning(f"Could not retrieve timestamp: {e}")
            return "unknown_timestamp"

    def run(self):
        """
        Run the report and send it to Slack.
        """
        for diff_table in self.diff_tables:
            log.debug(
                f"Processing table {diff_table.table} with pks {diff_table.pk_cols}"
            )
            try:
                summary = diff_table.table + "\n" + self.compare_table(diff_table)
                if self._summary_shows_differences(summary):
                    report_url = self.detail_report(diff_table.table)
                    self.report += f"{summary}\nDetails: {report_url}\n\n"
                else:
                    self.report += f"{diff_table.table}\nNo differences found.\n\n"
            except RuntimeError as e:
                self.report += f"{diff_table.table}\n{str(e)}\n\n"
                log.warning(f"Error processing {diff_table.table}: {e}")

        log.debug(self.report)
        self.send_report_to_slack()

    def _summary_shows_differences(self, summary: str) -> bool:
        """
        Check if the data-diff summary shows any differences.
        """
        return not (
            "0 rows exclusive to table A" in summary
            and "0 rows exclusive to table B" in summary
            and "0 rows updated" in summary
        )

    def detail_report(self, table: str) -> str:
        """
        Generate and upload a detailed difference report to Google Cloud.
        """
        html = self.generate_table_detail_report(table)
        return self._save_detail_report_to_cloud(html, table)

    def _save_detail_report_to_cloud(self, html: str, table: str) -> str:
        """
        Save the HTML report to Google Cloud Storage.
        """
        path = f"diff/{self.timestamp_string}/{table}.html"
        bucket = google_cloud_bucket()
        blob = bucket.blob(path)
        blob.upload_from_string(html, content_type="text/html")
        return f"https://storage.googleapis.com/{bucket.name}/{path}"

    def generate_table_detail_report(self, table: str) -> str:
        """
        Generate an HTML table of differences, pulling from a specific
        diff tracking table or view if available.
        """
        try:
            # Check for a dedicated diff tracking table or view
            diff_table_name = f"{table}_diff"
            sql = f"SELECT * FROM {diff_table_name}"
            result = conn.execute(text(sql))
            rows = result.fetchall()
            columns = result.keys()

            html = "<table border=1><tr>"
            html += "".join(f"<th>{col}</th>" for col in columns)
            html += "</tr>"
            for row in rows:
                html += "<tr>" + "".join(f"<td>{value}</td>" for value in row) + "</tr>"
            html += "</table>"
            return html
        except Exception as e:
            log.warning(f"Could not generate detailed diff report: {e}")
            return f"<p>Could not generate detailed report: {e}</p>"

    def _list_diff_tables(self) -> list[DiffTable]:
        """
        List the tables to compare using data-diff.
        """
        return [
            DiffTable(
                table="vacant_properties",
                pk_cols=["opa_id", "parcel_type"],
                where="opa_id IS NOT NULL",
            ),
            DiffTable(table="opa_properties", pk_cols=["parcel_number"]),
        ]

    def compare_table(self, diff_table: DiffTable) -> str:
        """
        Compare the current hypertable data with the most recent historical chunk using data-diff CLI.
        """
        table = diff_table.table
        pks = diff_table.pk_cols
        where_clause = f" -w '{diff_table.where}'" if diff_table.where else ""

        try:
            # Get the most recent historical chunk for comparison
            get_last_chunk_query = f"""
            SELECT create_date as last_chunk_date 
            FROM public.{table} 
            ORDER BY create_date DESC 
            LIMIT 2
            """
            result = conn.execute(text(get_last_chunk_query))
            chunks = [row[0] for row in result]

            if len(chunks) < 2:
                log.warning(
                    f"Not enough historical data for {table} to perform comparison."
                )
                return f"No differences found for {table} (insufficient historical data).\n"

            last_chunk = chunks[1]

            # Construct the data-diff command to compare
            data_diff_command = (
                f"data-diff {url} "
                f"'public.{table} WHERE create_date > {last_chunk}' "
                f"'public.{table} WHERE create_date <= {last_chunk}' "
                f"-k {' -k '.join(pks)} {where_clause} --stats"
            )

            log.debug(mask_password(data_diff_command))
            result = subprocess.run(
                data_diff_command, shell=True, capture_output=True, text=True
            )

            if result.returncode != 0:
                error_msg = result.stderr.strip()
                log.warning(f"data-diff failed for {table}: {error_msg}")
                return f"data-diff failed for {table}: {error_msg}\n"

            # Remove extra info from output if present
            return re.sub(r"\nExtra-Info:.*", "", result.stdout, flags=re.DOTALL)

        except Exception as e:
            log.warning(f"Error comparing {table}: {str(e)}")
            return f"Error comparing {table}: {str(e)}\n"

    def send_report_to_slack(self):
        """
        Send the full report to Slack.
        """
        token = os.getenv("CAGP_SLACK_API_TOKEN")
        if token:
            client = WebClient(token=token)
            client.chat_postMessage(
                channel="clean-and-green-philly-pipeline",
                text=self.report,
                username="Diff Reporter",
            )
        else:
            raise ValueError("Slack API token not found in environment variables.")
