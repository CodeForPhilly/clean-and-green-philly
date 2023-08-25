import datetime

VACANT_PROPS_LAYERS_TO_LOAD = [
    "https://services.arcgis.com/fLeGjb7u4uXqeF9q/ArcGIS/rest/services/Vacant_Indicators_Land/FeatureServer/0/",
    "https://services.arcgis.com/fLeGjb7u4uXqeF9q/ArcGIS/rest/services/Vacant_Indicators_Bldg/FeatureServer/0/",
]

CITY_OWNED_PROPERTIES_TO_LOAD = [
    "https://services.arcgis.com/fLeGjb7u4uXqeF9q/ArcGIS/rest/services/LAMAAssets/FeatureServer/0/"
]

PHS_LAYERS_TO_LOAD = [
    "https://services.arcgis.com/fLeGjb7u4uXqeF9q/ArcGIS/rest/services/PHS_CommunityLandcare/FeatureServer/0/",
    "https://services.arcgis.com/fLeGjb7u4uXqeF9q/ArcGIS/rest/services/PHS_PhilaLandCare_Maintenance/FeatureServer/0/",
]

one_year_ago = (datetime.datetime.now() - datetime.timedelta(days=365)).strftime(
    "%Y-%m-%d"
)

# Load data for complaints from L&I
COMPLAINTS_SQL_QUERY = f"SELECT address, service_request_id, subject, status, service_name, service_code, lat AS y, lon AS x FROM public_cases_fc WHERE requested_datetime >= '{one_year_ago}' AND lat IS NOT NULL;"

VIOLATIONS_SQL_QUERY = f"SELECT parcel_id_num, casenumber, casecreateddate, casetype, casestatus, violationnumber, violationcodetitle, violationstatus, opa_account_num, address, opa_owner, geocode_x AS x, geocode_y AS y FROM violations WHERE violationdate >= '{one_year_ago}' AND geocode_x IS NOT NULL;"
