from classes.featurelayer import FeatureLayer
from constants.services import VACANT_PROPS_LAYERS_TO_LOAD


def vacant_properties():
    vacant_properties = FeatureLayer(
        name="Vacant Properties",
        esri_rest_urls=VACANT_PROPS_LAYERS_TO_LOAD,
        cols=[
            "ADDRESS",
            "OWNER1",
            "OWNER2",
            "BLDG_DESC",
            "COUNCILDISTRICT",
            "ZONINGBASEDISTRICT",
            "ZIPCODE",
            "OPA_ID",
            "parcel_type",
        ]
    )

    vacant_properties.gdf.dropna(subset=["opa_id"], inplace=True)

    vacant_properties.gdf = vacant_properties.gdf.rename(
        columns={
            "owner1": "owner_1",
            "owner2": "owner_2",
            "bldg_desc": "building_description",
            "councildistrict": "council_district",
            "zoningbasedistrict": "zoning_base_district",
        }
    )

    return vacant_properties
