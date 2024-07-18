import sys
import time

from classes.backup_archive_database import BackupArchiveDatabase
from classes.diff_report import DiffReport
from config.psql import conn
from data_utils.access_process import access_process
from data_utils.city_owned_properties import city_owned_properties
from data_utils.community_gardens import community_gardens
from data_utils.conservatorship import conservatorship
from data_utils.contig_neighbors import contig_neighbors
from data_utils.deliquencies import deliquencies
from data_utils.dev_probability import dev_probability
from data_utils.drug_crimes import drug_crimes
from data_utils.gun_crimes import gun_crimes
from data_utils.imm_dang_buildings import imm_dang_buildings
from data_utils.l_and_i import l_and_i
from data_utils.llc_owner import llc_owner
from data_utils.nbhoods import nbhoods
from data_utils.negligent_devs import negligent_devs
from data_utils.opa_properties import opa_properties
from data_utils.park_priority import park_priority
from data_utils.phs_properties import phs_properties
from data_utils.ppr_properties import ppr_properties
from data_utils.priority_level import priority_level
from data_utils.rco_geoms import rco_geoms
from data_utils.tactical_urbanism import tactical_urbanism
from data_utils.tree_canopy import tree_canopy
from data_utils.unsafe_buildings import unsafe_buildings
from data_utils.vacant_properties import vacant_properties

from config.config import FORCE_RELOAD, tiles_file_id_prefix

# Ensure the directory containing awkde is in the Python path
awkde_path = "/usr/src/app"
if awkde_path not in sys.path:
    sys.path.append(awkde_path)

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
    llc_owner,
    community_gardens,
    park_priority,
    ppr_properties,
    contig_neighbors,
    dev_probability,
    negligent_devs,
]

# backup sql schema if we are reloading data
backup: BackupArchiveDatabase = None
if FORCE_RELOAD:
    # first archive any remaining backup that may exist from a previous run that errored
    backup = BackupArchiveDatabase()
    if backup.is_backup_schema_exists():
        backup.archive_backup_schema()
        conn.commit()
        time.sleep(1) # make sure we get a different timestamp
        backup = BackupArchiveDatabase() # create a new one so we get a new timestamp
    
    backup.backup_schema()
    conn.commit()

# Load Vacant Property Data
dataset = vacant_properties()

# Load and join other datasets
for service in services:
   dataset = service(dataset)

# Add Priority Level
dataset = priority_level(dataset)

# Add Access Process
dataset = access_process(dataset)

# back up old tiles file whether we are reloading data or not
if backup is None:
    backup = BackupArchiveDatabase()
backup.backup_tiles_file()

# Finalize in Postgres
dataset.gdf.to_postgis("vacant_properties_end", conn, if_exists="replace", index=False)

conn.commit()

# Post to Mapbox
dataset.build_and_publish_pmtiles(tiles_file_id_prefix)

# if we are reloading, run the diff report, then archive the backup and finally prune old archives
if FORCE_RELOAD:
    diff_report = DiffReport(timestamp_string=backup.timestamp_string)
    diff_report.run()
    backup.archive_backup_schema()
    conn.commit()
    backup.prune_old_archives()
    conn.commit()

conn.close()
