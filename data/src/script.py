from classes.featurelayer import FeatureLayer
from config.psql import conn
from constants.services import VACANT_PROPS_LAYERS_TO_LOAD
from data_utils import *
import sys

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
    deliquencies,
    opa_properties,
]


# Load Vacant Property Data
dataset = vacant_properties()

# Load and join other datasets
for service in services:
    dataset = service(dataset)

# Add Priority Level
dataset = priority_level(dataset)

# Add Access Process
dataset = access_process(dataset)


# Post to Mapbox
dataset.upload_to_mapbox("vacant_properties")

dataset.gdf.to_postgis(
    "vacant_properties_end", conn, if_exists="replace", index=False
)
print("Vacant Properties End Uploaded to Postgres")
conn.commit()
conn.close()
