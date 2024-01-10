from classes.featurelayer import FeatureLayer
from constants.services import VACANT_PROPS_LAYERS_TO_LOAD
from config.psql import conn


def vacant_properties():
    vacant_properties = FeatureLayer(
        name="Vacant Properties", esri_rest_urls=VACANT_PROPS_LAYERS_TO_LOAD, cols=["ADDRESS", "OWNER1", "OWNER2", "BLDG_DESC", "COUNCILDISTRICT", "ZONINGBASEDISTRICT", "ZIPCODE", "OPA_ID"]
    )

    vacant_properties.gdf.dropna(subset=["OPA_ID"], inplace=True)

    vacant_properties.gdf = vacant_properties.gdf.rename(
        columns={
            "ADDRESS": "address",
            "OWNER1": "owner_1",
            "OWNER2": "owner_2",
            "BLDG_DESC": "building_description",
            "COUNCILDISTRICT": "council_district",
            "ZONINGBASEDISTRICT": "zoning_base_district",
            "ZIPCODE": "zipcode",
        }
    )

    return vacant_properties
