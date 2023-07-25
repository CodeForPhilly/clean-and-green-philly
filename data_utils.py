import datetime

import pandas as pd
import geopandas as gpd
import requests
from shapely import Polygon

from constants import DEFAULT_ARCGIS_QUERY_PARAMETERS, ARCGIS_BASE_URL, PHILADELPHIA_CARTO_BASE_URL


def get_arcgis_dataset(dataset_path: str) -> gpd.GeoDataFrame:
    dfs: list[pd.DataFrame] = []
    pagination_offset: int = 0

    while True:
        query_params = DEFAULT_ARCGIS_QUERY_PARAMETERS | {"resultOffset": pagination_offset}
        response = requests.get(url=ARCGIS_BASE_URL + dataset_path, params=query_params)
        if response.status_code != 200:
            print(f"Error calling ArcGIS API, request returned HTTP {response.status_code}")
            break

        df = pd.DataFrame(response.json()['features'])

        # separate the attributes column into one column per attribute
        df = pd.concat([df.drop(['attributes'], axis=1), df['attributes'].apply(pd.Series)], axis=1)

        # make the `geometry` column a shapely geometry object
        df['geometry'] = df['geometry'].apply(lambda x: Polygon(x['rings'][0]))

        land_gdf = gpd.GeoDataFrame(df, geometry='geometry', crs='EPSG:3857')
        dfs.append(land_gdf.to_crs(epsg=2272))

        pagination_offset += len(land_gdf)

        # we specify 2000 results in the query, <2000 indicates no further results
        if len(land_gdf) < 2000:
            break

    return gpd.GeoDataFrame(pd.concat(dfs, ignore_index=True), crs='EPSG:2272')


def get_philadelphia_li_complaint_dataset() -> gpd.GeoDataFrame:
    one_year_ago: str = (datetime.datetime.now() - datetime.timedelta(days=365)).strftime("%Y-%m-%d")

    query: str = f"SELECT address, service_request_id, subject, status, service_name, service_code, lat, lon" \
                 f" FROM public_cases_fc " \
                 f"WHERE requested_datetime >= '{one_year_ago}'"

    complaints_response = requests.get(url=PHILADELPHIA_CARTO_BASE_URL, params={"q": query})

    complaints_data = complaints_response.json()["rows"]
    df = pd.DataFrame(complaints_data)
    return gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.lon, df.lat), crs='EPSG:2272')


def get_philadelphia_li_violation_dataset() -> gpd.GeoDataFrame:
    one_year_ago: str = (datetime.datetime.now() - datetime.timedelta(days=365)).strftime("%Y-%m-%d")

    query: str = f"SELECT parcel_id_num, casenumber, casecreateddate, casetype, casestatus, violationnumber," \
                 f"       violationcodetitle, violationstatus, opa_account_num, address, opa_owner, " \
                 f"       geocode_x, geocode_y " \
                 f"FROM violations " \
                 f"WHERE violationdate >= '{one_year_ago}'"

    violations_response = requests.get(url=PHILADELPHIA_CARTO_BASE_URL, params={"q": query})

    violations_data = violations_response.json()["rows"]

    violations_df = pd.DataFrame(violations_data)

    return gpd.GeoDataFrame(violations_df,
                            geometry=gpd.points_from_xy(violations_df.geocode_x, violations_df.geocode_y),
                            crs='EPSG:2272')


