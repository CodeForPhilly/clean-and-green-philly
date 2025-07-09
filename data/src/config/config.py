import logging
import threading
from contextlib import contextmanager
from pathlib import Path

FORCE_RELOAD = True
""" During the data load, whether to query the various GIS API services for the data to load. If True, will query the
API services and report on data differences.  If false will read the cached data."""

USE_CRS = "EPSG:2272"
""" the standard geospatial code for Pennsylvania South (ftUS) """

ROOT_DIRECTORY = Path(__file__).resolve().parent.parent
""" the root directory of the project """

CACHE_FRACTION = 0.05
"""The fraction used to cache portions of the pipeline's transformed data in each step of the pipeline."""

log_level: int = logging.WARN
""" overall log level for the project """

# Centralized logger configuration
ENABLED_LOGGERS = {}
""" Set of enabled logger types. Add/remove logger types to control what logging is active.
Available types: "cache", "performance", "pipeline", "geometry_debug", "data_quality"
Examples:
- {"cache", "performance"} - Enable only cache and performance logging
- {"pipeline", "data_quality"} - Enable only pipeline and data quality logging  
- set() - Disable all specialized logging
- {"cache", "performance", "pipeline", "geometry_debug", "data_quality"} - Enable all logging
"""

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


def get_logger(logger_type: str) -> logging.Logger:
    """
    Get a logger for the specified logger type.
    Returns a logger that respects the ENABLED_LOGGERS configuration.

    Args:
        logger_type: The type of logger to get (e.g., "cache", "performance", "pipeline", etc.)

    Returns:
        A configured logger instance

    Example:
        logger = get_logger("cache")  # Gets cache logger if "cache" is in ENABLED_LOGGERS
    """
    logger = logging.getLogger(f"cagp.{logger_type}")

    # If this logger type is not enabled, set level to CRITICAL (effectively disables all messages)
    if logger_type not in ENABLED_LOGGERS:
        logger.setLevel(logging.CRITICAL)
    else:
        logger.setLevel(logging.INFO)

    # Only add handler if it doesn't already exist
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%H:%M:%S"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.propagate = False  # Prevent duplicate messages

    return logger


# Thread-local storage for statistical summary control
_stats_context = threading.local()


def is_statistical_summaries_enabled() -> bool:
    """
    Check if statistical summaries should be printed for the current thread.
    Returns True if enabled via context manager, False otherwise.
    """
    return getattr(_stats_context, "enabled", False)


@contextmanager
def enable_statistical_summaries():
    """
    Context manager to enable statistical summary printing for functions within the context.

    Usage:
        with enable_statistical_summaries():
            result = some_function(data)  # Will print statistical summaries
        # Outside context - no statistical summaries printed
    """
    # Store previous state
    previous_state = getattr(_stats_context, "enabled", False)

    # Enable statistical summaries for this context
    _stats_context.enabled = True

    try:
        yield
    finally:
        # Restore previous state
        _stats_context.enabled = previous_state
