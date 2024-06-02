import logging as log
import os
import subprocess
from datetime import datetime, timedelta

import sqlalchemy as sa
from config.config import log_level, max_backup_schema_days, tiles_file_id_prefix, tile_file_backup_directory
from config.psql import conn, local_engine, url
from data_utils.utils import mask_password
from sqlalchemy import inspect
from classes.featurelayer import google_cloud_bucket

log.basicConfig(level=log_level)

backup_schema_name: str = "backup_"
""" the prefix for the backup schemas """

date_time_format: str = "%Y_%m_%dt%H_%M_%S"
""" the datetime format for the backup schema names """


class BackupArchiveDatabase:
    """
    Class to manage creating a backup of the public schema before the etl refresh is run.  After the etl job and data differences are reported, this class moves the current backup schema to a timestamped backup and prunes older backup schemas.
    """

    def __init__(self):
        self.timestamp_string = datetime.now().strftime(date_time_format)
        self.backup_schema_archive_name = backup_schema_name + self.timestamp_string

    def backup_schema(self):
        """
        backup the whole public schema to another schema in the same db.
        pgdump the public schema, replace public schema name with backup schema name, clean up the special column types, and import it with psql in one piped command
        """

        pgdump_command = (
            # first, dump the schema only where we can safely replace all 'public' strings with 'backup_'
            "pg_dump "
            + url
            + " -s --schema public | sed 's/public/"
            + backup_schema_name
            + "/g' | sed 's/"
            + backup_schema_name
            + ".geometry/public.geometry/' | sed 's/"
            + backup_schema_name
            + ".spatial_ref_sys/public.spatial_ref_sys/' | psql -v ON_ERROR_STOP=1 "
            + url
            + " > /dev/null "
            # then dump the data only and substitute the word public only where it is in DDL, not in the data
            + " && pg_dump "
            + url
            + " -a --schema public | sed 's/COPY public./COPY "
            + backup_schema_name
            + "./g' | sed 's/"
            + backup_schema_name
            + ".geometry/public.geometry/' | sed 's/"
            + backup_schema_name
            + ".spatial_ref_sys/public.spatial_ref_sys/' | psql -v ON_ERROR_STOP=1 "
            + url
            + " > /dev/null "
        )
        log.debug(mask_password(pgdump_command))
        complete_process = subprocess.run(pgdump_command, check=False, shell=True)

        if complete_process.returncode != 0 or complete_process.stderr:
            raise RuntimeError(
                "pg_dump command "
                + mask_password(pgdump_command)
                + " did not exit with success. "
                + complete_process.stderr.decode()
            )

    def archive_backup_schema(self):
        """
        mv backup_ schema to "backup_" + backup_timestamp
        """
        sql = (
            "ALTER SCHEMA "
            + backup_schema_name
            + " RENAME TO "
            + self.backup_schema_archive_name
        )
        log.debug(sql)
        conn.execute(sa.DDL(sql))

    def prune_old_archives(self):
        """
        drop backup schemas that are too old
        """
        # list all backup schemas
        schemas = inspect(local_engine).get_schema_names()
        cutoff = datetime.now() - timedelta(days=max_backup_schema_days)
        for schema in schemas:
            if schema.startswith(backup_schema_name):
                timestamp = schema.replace(backup_schema_name, "")
                backed_up_time = datetime.strptime(timestamp, date_time_format)
                if backed_up_time < cutoff:
                    sql = "drop schema " + schema + " cascade"
                    log.debug(sql)
                    conn.execute(sa.DDL(sql))

    def is_backup_schema_exists(self) -> bool:
        """ whether the backup schema exists

        Returns:
            bool: whether true
        """        
        return backup_schema_name in inspect(local_engine).get_schema_names()
    
    def backup_tiles_file(self):
        """backup the main tiles file to a timestamped copy in the backup/ folder in GCP
        """
        bucket = google_cloud_bucket()
        count: int = 0
        for blob in bucket.list_blobs(prefix=tiles_file_id_prefix):
            # there should only be one but in case there are more include the count in the backup file name
            suffix: str = '_' + self.timestamp_string + ('' if count == 0 else '_' + count )
            name, ext = os.path.splitext(blob.name)
            backup_file_name: str = tile_file_backup_directory + "/" + name + suffix + ext
            log.debug(backup_file_name)
            bucket.rename_blob(blob,new_name=backup_file_name)
            count += 1
        if count == 0:
            log.warning("No files were found to back up.")