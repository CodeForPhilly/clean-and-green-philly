import logging
import os
from pathlib import Path

FORCE_RELOAD = True
USE_CRS = "EPSG:2272"
MAPBOX_TOKEN = os.environ.get("CFP_MAPBOX_TOKEN_UPLOADER")

# overall log level for the project
log_level: int = logging.DEBUG

# max days to keep backed up schemas archived in plsql
max_backup_schema_days:int = 365

# if this is not blank, send the data-diff summary report to this Slack channel
report_to_slack_channel:str = ''

# a standard from email
from_email: str = 'no_reply@cleanandgreenphilly.org'

# if this is not blank, email the data-diff summary report to this csv list of emails
report_to_email: str = ''

# sendmail server
smtp_server: str = ''

def is_docker():
    """
    whether we are running in Docker or not, e.g. in ide or cl environment
    """
    cgroup = Path('/proc/self/cgroup')
    return Path('/.dockerenv').is_file() or cgroup.is_file() and 'docker' in cgroup.read_text(encoding='utf-8')
