import logging
import os
from pathlib import Path

FORCE_RELOAD = False
USE_CRS = "EPSG:2272"
MAPBOX_TOKEN = os.environ.get("CFP_MAPBOX_TOKEN_UPLOADER")

log_level: int = logging.WARN
""" overall log level for the project """

max_backup_schema_days: int = 365
""" max days to keep backed up schemas archived in plsql """

report_to_slack_channel: str = ""
""" if this is not blank, send the data-diff summary report to this Slack channel.
The CAGP_SLACK_API_TOKEN environment variable must be set """

from_email: str = "no_reply@cleanandgreenphilly.org"
""" a standard from email """

report_to_email: str = ""
""" if this is not blank, email the data-diff summary report to this csv list of emails """

smtp_server: str = "localhost"
""" sendmail server """


def is_docker() -> bool:
    """
    whether we are running in Docker or not, e.g. in ide or cl environment
    """
    cgroup = Path("/proc/self/cgroup")
    return (
        Path("/.dockerenv").is_file()
        or cgroup.is_file()
        and "docker" in cgroup.read_text(encoding="utf-8")
    )
