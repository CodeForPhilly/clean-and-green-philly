import datetime

VACANT_PROPS_LAYERS_TO_LOAD = [
    "https://services.arcgis.com/fLeGjb7u4uXqeF9q/ArcGIS/rest/services/Vacant_Indicators_Land/FeatureServer/0/",
    "https://services.arcgis.com/fLeGjb7u4uXqeF9q/ArcGIS/rest/services/Vacant_Indicators_Bldg/FeatureServer/0/",
]

COUNCIL_DISTRICTS_TO_LOAD = [
    "https://services.arcgis.com/fLeGjb7u4uXqeF9q/arcgis/rest/services/Council_Districts_2024/FeatureServer/0/"
]

CITY_OWNED_PROPERTIES_TO_LOAD = [
    "https://services.arcgis.com/fLeGjb7u4uXqeF9q/ArcGIS/rest/services/LAMAAssets/FeatureServer/0/"
]

PHS_LAYERS_TO_LOAD = [
    "https://services.arcgis.com/fLeGjb7u4uXqeF9q/ArcGIS/rest/services/phs_landcare/FeatureServer/0",
]

RCOS_LAYERS_TO_LOAD = [
    "https://services.arcgis.com/fLeGjb7u4uXqeF9q/ArcGIS/rest/services/Zoning_RCO/FeatureServer/0/"
]

COMMUNITY_GARDENS_TO_LOAD = [
    "https://services2.arcgis.com/qjOOiLCYeUtwT7x7/arcgis/rest/services/PHS_NGT_Supported_Current_view/FeatureServer/0/"
]

PPR_PROPERTIES_TO_LOAD = [
    "https://services.arcgis.com/fLeGjb7u4uXqeF9q/ArcGIS/rest/services/PPR_Properties/FeatureServer/0"
]

one_year_ago = (datetime.datetime.now() - datetime.timedelta(days=365)).strftime(
    "%Y-%m-%d"
)

# Load data for complaints from L&I
COMPLAINTS_SQL_QUERY = f"""
SELECT address, service_request_id, subject, status, service_name, service_code, the_geom, lat AS y, lon AS x 
FROM public_cases_fc 
WHERE requested_datetime >= '{one_year_ago}' 
  AND lat IS NOT NULL
  AND (
    subject ILIKE '%dumping%'
    OR subject ILIKE '%blight%'
    OR subject ILIKE '%rubbish%'
    OR subject ILIKE '%weeds%'
    OR subject ILIKE '%graffiti%'
    OR subject ILIKE '%abandoned%'
    OR subject ILIKE '%sanitation%'
    OR subject ILIKE '%litter%'
    OR subject ILIKE '%vacant%'
    OR subject ILIKE '%trash%'
    OR subject ILIKE '%unsafe%'
  )
"""

VIOLATIONS_SQL_QUERY = f"SELECT parcel_id_num, casenumber, casecreateddate, casetype, casestatus, violationnumber, violationcodetitle, violationstatus, opa_account_num, address, opa_owner, the_geom, geocode_x AS x, geocode_y AS y FROM violations WHERE violationdate >= '{one_year_ago}' AND geocode_x IS NOT NULL"

GUNCRIME_SQL_QUERY = f"SELECT text_general_code, dispatch_date, the_geom, point_x AS x, point_y AS y FROM incidents_part1_part2 WHERE dispatch_date_time >= '{one_year_ago}' AND text_general_code IN ('Aggravated Assault Firearm', 'Robbery Firearm') AND point_x IS NOT NULL"

DRUGCRIME_SQL_QUERY = f"SELECT text_general_code, dispatch_date, the_geom, point_x AS x, point_y AS y FROM incidents_part1_part2 WHERE dispatch_date_time >= '{one_year_ago}' AND text_general_code IN ('Narcotic / Drug Law Violations') AND point_x IS NOT NULL"

DELINQUENCIES_QUERY = "SELECT * FROM real_estate_tax_delinquencies"

OPA_PROPERTIES_QUERY = "SELECT building_code_description, market_value, sale_date, sale_price, parcel_number, location as street_address,owner_1, owner_2, mailing_address_1, mailing_address_2, mailing_care_of, mailing_street, mailing_zip, mailing_city_state, unit, zip_code, zoning, the_geom FROM opa_properties_public"

PWD_PARCELS_QUERY = "SELECT *, the_geom FROM pwd_parcels"

UNSAFE_BUILDINGS_QUERY = "SELECT opa_account_num, the_geom FROM unsafe"

IMMINENT_DANGER_BUILDINGS_QUERY = "SELECT * FROM imm_dang"

PERMITS_QUERY = f"""
        SELECT
        address,
        addressobjectid,
        approvedscopeofwork,
        commercialorresidential,
        opa_account_num,
        permittype,
        status,
        unit_num,
        unit_type,
        permitissuedate,
        typeofwork,
        the_geom,
        ST_AsGeoJSON(the_geom)::json AS the_geom_geojson
        FROM permits
        WHERE permitissuedate >= '{one_year_ago}'
    """

NBHOODS_URL = "https://raw.githubusercontent.com/opendataphilly/open-geo-data/master/philadelphia-neighborhoods/philadelphia-neighborhoods.geojson"

CENSUS_BGS_URL = (
    "https://opendata.arcgis.com/datasets/2f982bada233478ea0100528227febce_0.geojson"
)

PARK_PRIORITY_AREAS_URBAN_PHL = [
    "https://server7.tplgis.org/arcgis7/rest/services/ParkServe/ParkServe_ProdNew/FeatureServer/6/"
]
