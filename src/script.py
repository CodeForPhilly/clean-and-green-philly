from classes.featurelayer import FeatureLayer
from config.psql import conn
from constants.services import VACANT_PROPS_LAYERS_TO_LOAD
from data_utils.city_owned_properties import city_owned_properties
from data_utils.phs_properties import phs_properties
from data_utils.l_and_i import l_and_i


"""
Load Vacant Properties Datasets
"""


vacant_properties = FeatureLayer(
    name="Vacant Properties", esri_rest_urls=VACANT_PROPS_LAYERS_TO_LOAD
)


"""
Load City Owned Properties
"""
vacant_properties = city_owned_properties(vacant_properties)


"""
Load PHS Data
"""
vacant_properties = phs_properties(vacant_properties)


"""
Load L&I Data
"""
vacant_properties = l_and_i(vacant_properties)

vacant_properties.gdf.to_postgis(
    "vacant_properties_end", conn, if_exists="replace", index=False
)

# Clean up

conn.close()
