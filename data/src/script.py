import time
import traceback

from src.classes.backup_archive_database import BackupArchiveDatabase
from src.classes.diff_report import DiffReport
from src.classes.slack_error_reporter import send_error_to_slack
from src.config.config import BACKUP_SCHEMA, FORCE_RELOAD, tiles_file_id_prefix
from src.config.psql import conn
from src.data_utils.access_process import access_process
from src.data_utils.city_owned_properties import city_owned_properties
from src.data_utils.community_gardens import community_gardens
from src.data_utils.conservatorship import conservatorship
from src.data_utils.contig_neighbors import contig_neighbors
from src.data_utils.deliquencies import deliquencies
from src.data_utils.dev_probability import dev_probability
from src.data_utils.drug_crimes import drug_crimes
from src.data_utils.gun_crimes import gun_crimes
from src.data_utils.imm_dang_buildings import imm_dang_buildings
from src.data_utils.l_and_i import l_and_i
from src.data_utils.nbhoods import nbhoods
from src.data_utils.negligent_devs import negligent_devs
from src.data_utils.opa_properties import opa_properties
from src.data_utils.owner_type import owner_type
from src.data_utils.park_priority import park_priority
from src.data_utils.phs_properties import phs_properties
from src.data_utils.ppr_properties import ppr_properties
from src.data_utils.priority_level import priority_level
from src.data_utils.rco_geoms import rco_geoms
from src.data_utils.tactical_urbanism import tactical_urbanism
from src.data_utils.tree_canopy import tree_canopy
from src.data_utils.unsafe_buildings import unsafe_buildings
from src.data_utils.vacant_properties import vacant_properties

try:
    services = [
        city_owned_properties,
        phs_properties,
        l_and_i,
        rco_geoms,
        tree_canopy,
        nbhoods,
        gun_crimes,
        drug_crimes,
        deliquencies,
        opa_properties,
        unsafe_buildings,
        imm_dang_buildings,
        tactical_urbanism,
        conservatorship,
        owner_type,
        community_gardens,
        park_priority,
        ppr_properties,
        contig_neighbors,
        dev_probability,
        negligent_devs,
    ]

    # backup sql schema if we are reloading data
    backup: BackupArchiveDatabase = None
    if FORCE_RELOAD and BACKUP_SCHEMA:
        # first archive any remaining backup that may exist from a previous run that errored
        backup = BackupArchiveDatabase()
        if backup.is_backup_schema_exists():
            backup.archive_backup_schema()
            conn.commit()
            time.sleep(1)  # make sure we get a different timestamp
            backup = (
                BackupArchiveDatabase()
            )  # create a new one so we get a new timestamp

        backup.backup_schema()
        conn.commit()

    # Load Vacant Property Data
    dataset = vacant_properties()

    # Load and join other datasets
    for service in services:
        dataset = service(dataset)

    before_drop = dataset.gdf.shape[0]
    dataset.gdf = dataset.gdf.drop_duplicates(subset="opa_id")
    after_drop = dataset.gdf.shape[0]
    print(
        f"Duplicate dataset rows dropped after initial services: {before_drop - after_drop}"
    )

    # Add Priority Level
    dataset = priority_level(dataset)

    # Print the distribution of "priority_level"
    distribution = dataset.gdf["priority_level"].value_counts()
    print("Distribution of priority level:")
    print(distribution)

    # Add Access Process
    dataset = access_process(dataset)

    # Print the distribution of "access_process"
    distribution = dataset.gdf["access_process"].value_counts()
    print("Distribution of access process:")
    print(distribution)

    before_drop = dataset.gdf.shape[0]
    dataset.gdf = dataset.gdf.drop_duplicates(subset="opa_id")
    after_drop = dataset.gdf.shape[0]
    print(f"Duplicate final dataset rows droppeds: {before_drop - after_drop}")

    # back up old tiles file whether we are reloading data or not
    if backup is None:
        backup = BackupArchiveDatabase()
    backup.backup_tiles_file()

    # Finalize in Postgres
    dataset.gdf.to_postgis(
        "vacant_properties_end", conn, if_exists="replace", index=False
    )

    conn.commit()

    # Post to GCP
    dataset.build_and_publish(tiles_file_id_prefix)

    # if we are reloading, run the diff report, then archive the backup and finally prune old archives
    if FORCE_RELOAD:
        diff_report = DiffReport(timestamp_string=backup.timestamp_string)
        diff_report.run()
        backup.archive_backup_schema()
        conn.commit()
        backup.prune_old_archives()
        conn.commit()

    conn.close()

except Exception as e:
    error_message = f"Error in backend job: {str(e)}\n\n{traceback.format_exc()}"
    send_error_to_slack(error_message)
    raise  # Optionally re-raise the exception
