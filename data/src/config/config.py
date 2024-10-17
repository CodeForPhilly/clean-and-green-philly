import logging
import os
from pathlib import Path

FORCE_RELOAD = False
""" During the data load, whether to query the various GIS API services for the data to load into the postgres tables.  If True, will query the API services, backup the database, reload the database and report on data differences.  If false will read the data from postgres."""

USE_CRS = "EPSG:2272"
""" the standard geospatial code for Pennsylvania South (ftUS) """

MAPBOX_TOKEN = os.environ.get("CFP_MAPBOX_TOKEN_UPLOADER")
""" The location of the token for your mapbox account in your environment """

log_level: int = logging.WARN
""" overall log level for the project """

max_backup_schema_days: int = 365
""" max days to keep backed up schemas archived in psql """

report_to_slack_channel: str = ""
""" if this is not blank, send the data-diff summary report to this Slack channel.
The CAGP_SLACK_API_TOKEN environment variable must be set """

from_email: str = "no_reply@cleanandgreenphilly.org"
""" a standard from email """

report_to_email: str = ""
""" if this is not blank, email the data-diff summary report to this csv list of emails """

smtp_server: str = "localhost"
""" sendmail server """

tiles_file_id_prefix: str = "vacant_properties_tiles"
""" the prefix of the name of the tiles file generated and saved to GCP """

write_production_tiles_file: bool = False
""" Whether to write the main vacant_properties_tiles.pmtiles as well as the staging vacant_properties_tiles_staging.pmtiles. 
BE CAREFUL, if true this writes the production file.
"""
tile_file_backup_directory: str = "backup"
""" The name of the directory in GCP to store timestamped backups of the tiles file """

min_tiles_file_size_in_bytes: int = 5 * 1024 * 1024
""" The minimum file size in bytes of the final generated pm tiles file.  If the file is not at least this size, 
don't upload to the GCP bucket as the file may be corrupted, e.g. a source vacant properties dataset was incomplete with not enough features."""


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
