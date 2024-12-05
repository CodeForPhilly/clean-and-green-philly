from sqlalchemy import text
import os
from slack_sdk import WebClient


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
            channel="clean-and-green-philly-back-end",
            text=message,
            username="PG Stats Reporter",
        )
    else:
        raise ValueError("Slack API token not found in environment variables.")
