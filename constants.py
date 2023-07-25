ARCGIS_BASE_URL: str = "https://services.arcgis.com"

ARCGIS_LAND_DATASET_PATH: str = "/fLeGjb7u4uXqeF9q/ArcGIS/rest/services/Vacant_Indicators_Land/FeatureServer/0/query"
ARCGIS_BUILDINGS_DATASET_PATH: str = "/fLeGjb7u4uXqeF9q/ArcGIS/rest/services/Vacant_Indicators_Bldg/FeatureServer/0/query"
ARCGIS_PHS_LANDCARE_DATASET_PATH: str = (
    "/fLeGjb7u4uXqeF9q/ArcGIS/rest/services/PHS_CommunityLandcare/FeatureServer/0/query"
)
ARCGIS_PHS_MAINTENANCE_DATASET_PATH: str = "/fLeGjb7u4uXqeF9q/ArcGIS/rest/services/PHS_PhilaLandCare_Maintenance/FeatureServer/0/query"
ARCGIS_RCO_DATASET_PATH: str = (
    "/fLeGjb7u4uXqeF9q/ArcGIS/rest/services/Zoning_RCO/FeatureServer/0/query"
)

PHILADELPHIA_CARTO_BASE_URL: str = "https://phl.carto.com/api/v2/sql"

PHILADELPHIA_NEIGHBORHOODS_DATASET_URL: str = "https://github.com/azavea/geo-data/raw/master/Neighborhoods_Philadelphia/Neighborhoods_Philadelphia.zip"

PHILADELPHIA_TREE_CANOPY_DATASET_URL: str = (
    "https://national-tes-data-share.s3.amazonaws.com/national_tes_share/pa.zip.zip"
)

DEFAULT_ARCGIS_QUERY_PARAMETERS: dict = {
    "where": "1=1",
    "outFields": "*",
    "returnGeometry": "true",
    "f": "json",
    "resultRecordCount": 2000,
}
