import datetime
import io
import warnings

import fiona
import geopandas as gpd
import pandas as pd
import requests
from shapely import Polygon

from constants import (
    DEFAULT_ARCGIS_QUERY_PARAMETERS,
    ARCGIS_BASE_URL,
    PHILADELPHIA_CARTO_BASE_URL,
    REDEVELOPMENT_OWNER_VALUES,
    DEPARTMENT_OF_PUBLIC_PROPERTY_OWNER_VALUES,
    PUBLIC_PROPERTY_OWNER_VALUES,
)

warnings.filterwarnings("ignore", "GeoSeries.notna", UserWarning)


def get_arcgis_dataset(dataset_path: str) -> gpd.GeoDataFrame:
    dfs: list[pd.DataFrame] = []
    pagination_offset: int = 0

    while True:
        query_params = DEFAULT_ARCGIS_QUERY_PARAMETERS | {
            "resultOffset": pagination_offset
        }
        response = requests.get(url=ARCGIS_BASE_URL + dataset_path, params=query_params)
        if response.status_code != 200:
            print(
                f"Error calling ArcGIS API, request returned HTTP {response.status_code}"
            )
            break

        df = pd.DataFrame(response.json()["features"])

        # separate the attributes column into one column per attribute
        df = pd.concat(
            [df.drop(["attributes"], axis=1), df["attributes"].apply(pd.Series)], axis=1
        )

        # make the `geometry` column a shapely geometry object
        df["geometry"] = df["geometry"].apply(lambda x: Polygon(x["rings"][0]))

        land_gdf = gpd.GeoDataFrame(df, geometry="geometry", crs="EPSG:3857")
        dfs.append(land_gdf.to_crs(epsg=2272))

        pagination_offset += len(land_gdf)

        # we specify 2000 results in the query, <2000 indicates no further results
        if len(land_gdf) < 2000:
            break

    return gpd.GeoDataFrame(pd.concat(dfs, ignore_index=True), crs="EPSG:2272")


def get_philadelphia_li_complaint_dataset() -> gpd.GeoDataFrame:
    one_year_ago: str = (
        datetime.datetime.now() - datetime.timedelta(days=365)
    ).strftime("%Y-%m-%d")

    query: str = (
        f"SELECT address, service_request_id, subject, status, service_name, service_code, lat, lon"
        f" FROM public_cases_fc "
        f"WHERE requested_datetime >= '{one_year_ago}'"
    )

    response = requests.get(url=PHILADELPHIA_CARTO_BASE_URL, params={"q": query})

    df = pd.DataFrame(response.json()["rows"])
    return gpd.GeoDataFrame(
        df, geometry=gpd.points_from_xy(df.lon, df.lat), crs="EPSG:2272"
    )


def get_philadelphia_li_violation_dataset() -> gpd.GeoDataFrame:
    one_year_ago: str = (
        datetime.datetime.now() - datetime.timedelta(days=365)
    ).strftime("%Y-%m-%d")

    query: str = (
        f"SELECT parcel_id_num, casenumber, casecreateddate, casetype, casestatus, violationnumber,"
        f"       violationcodetitle, violationstatus, opa_account_num, address, opa_owner, "
        f"       geocode_x, geocode_y "
        f"FROM violations "
        f"WHERE violationdate >= '{one_year_ago}'"
    )

    response = requests.get(url=PHILADELPHIA_CARTO_BASE_URL, params={"q": query})

    df = pd.DataFrame(response.json()["rows"])

    return gpd.GeoDataFrame(
        df,
        geometry=gpd.points_from_xy(df.geocode_x, df.geocode_y),
        crs="EPSG:2272",
    )


def get_philadelphia_gun_crime_dataset() -> gpd.GeoDataFrame:
    one_year_ago: str = (
        datetime.datetime.now() - datetime.timedelta(days=365)
    ).strftime("%Y-%m-%d")

    query = (
        f"SELECT text_general_code, dispatch_date, point_x, point_y "
        f"FROM incidents_part1_part2 "
        f"WHERE dispatch_date_time >= '{one_year_ago}' "
        f"AND text_general_code IN ('Aggravated Assault Firearm', 'Robbery Firearm')"
    )

    response = requests.get(url=PHILADELPHIA_CARTO_BASE_URL, params={"q": query})

    df = pd.DataFrame(response.json()["rows"])

    gdf = gpd.GeoDataFrame(
        df, geometry=gpd.points_from_xy(df.point_x, df.point_y), crs="EPSG:4326"
    )

    gdf.drop(["point_x", "point_y"], axis=1, inplace=True)

    gdf.to_crs(epsg=2272, inplace=True)

    return gdf[gdf["geometry"].notnull()]


def get_property_assessment_dataset() -> pd.DataFrame:
    query = "SELECT parcel_number, market_value " "FROM opa_properties_public"

    response = requests.get(url=PHILADELPHIA_CARTO_BASE_URL, params={"q": query})

    return pd.DataFrame(response.json()["rows"])


def get_delinquency_dataset() -> pd.DataFrame:
    query = "SELECT * FROM real_estate_tax_delinquencies"

    response = requests.get(url=PHILADELPHIA_CARTO_BASE_URL, params={"q": query})

    return pd.DataFrame(response.json()["rows"])


def get_shapefile_dataset(dataset_url: str) -> gpd.GeoDataFrame:
    response = requests.get(url=dataset_url)

    bytes_array = io.BytesIO(response.content).read()

    with fiona.BytesCollection(bytes_array) as src:
        crs = src.crs
        gdf = gpd.GeoDataFrame.from_features(src, crs=crs)

    return gdf


def starts_with_preposition(string):
    return string.split(" ")[0].lower() in [
        "a",
        "an",
        "and",
        "as",
        "at",
        "but",
        "by",
        "for",
        "from",
        "in",
        "into",
        "nor",
        "of",
        "on",
        "or",
        "so",
        "the",
        "to",
        "up",
        "yet",
    ]


def combine_owners(row):
    if pd.isnull(row["OWNER1"]) and pd.isnull(row["OWNER2"]):
        return None
    elif pd.isnull(row["OWNER1"]) and not pd.isnull(row["OWNER2"]):
        return row["OWNER2"]
    elif not pd.isnull(row["OWNER1"]) and pd.isnull(row["OWNER2"]):
        return row["OWNER1"]
    elif starts_with_preposition(row["OWNER2"]):
        return row["OWNER1"] + " " + row["OWNER2"]
    else:
        return row["OWNER2"] + "; " + row["OWNER1"]


def clean_ownership_values(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """
    correct misspellings, and identify public vs. private ownership
    """
    gdf["OWNER"] = gdf.apply(combine_owners, axis=1)

    gdf.loc[
        gdf["OWNER"] == "PHILADELPHIA HOUSING AUTH", "OWNER"
    ] = "PHILADELPHIA HOUSING AUTHORITY"
    gdf.loc[
        gdf["OWNER"] == "PHILA HOUSING AUTHORITY", "OWNER"
    ] = "PHILADELPHIA HOUSING AUTHORITY"

    for val in REDEVELOPMENT_OWNER_VALUES:
        gdf.loc[
            gdf["OWNER"] == val, "OWNER"
        ] = "REDEVELOPMENT AUTHORITY OF PHILADELPHIA"

    for var in DEPARTMENT_OF_PUBLIC_PROPERTY_OWNER_VALUES:
        gdf.loc[
            gdf["OWNER"] == var, "OWNER"
        ] = "CITY OF PHILADELPHIA DEPARTMENT OF PUBLIC PROPERTY"

    gdf.loc[
        gdf["OWNER"] == "URBAN DEVELOPMENT; SECRETARY OF HOUSING", "OWNER"
    ] = "SECRETARY OF HOUSING AND URBAN DEVELOPMENT"
    gdf.loc[
        gdf["OWNER"] == "URBAN DEVELOPMENT; SECRETARY OF HOUSING AND", "OWNER"
    ] = "SECRETARY OF HOUSING AND URBAN DEVELOPMENT"

    gdf.loc[
        gdf["OWNER"] == "COMMONWEALTH OF PA", "OWNER"
    ] = "COMMONWEALTH OF PENNSYLVANIA"
    gdf.loc[
        gdf["OWNER"] == "COMMONWEALTH OF PENNA", "OWNER"
    ] = "COMMONWEALTH OF PENNSYLVANIA"

    gdf.loc[
        gdf["OWNER"] == "DEVELOPMENT CORPORATION; PHILADELPHIA HOUSING", "OWNER"
    ] = "PHILADELPHIA HOUSING DEVELOPMENT CORPORATION"
    gdf.loc[
        gdf["OWNER"] == "PHILA HOUSING DEV CORP", "OWNER"
    ] = "PHILADELPHIA HOUSING DEVELOPMENT CORPORATION"

    gdf.loc[
        gdf["OWNER"] == "DEPARTMENT OF TRANSPORTAT; COMMONWEALTH OF PENNSYLVA", "OWNER"
    ] = "PENNDOT"

    gdf.loc[gdf["OWNER"] == "CITY OF PHILADELPHIA", "OWNER"] = "CITY OF PHILA"

    gdf["public_owner"] = gdf["OWNER"].isin(PUBLIC_PROPERTY_OWNER_VALUES)

    return gdf.drop(["OWNER1", "OWNER2"], axis=1)
