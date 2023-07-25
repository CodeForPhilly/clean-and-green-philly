import argparse
import os

import geopandas as gpd
import pandas as pd
import logging

from constants import (
    ARCGIS_LAND_DATASET_PATH,
    ARCGIS_BUILDINGS_DATASET_PATH,
    ARCGIS_PHS_LANDCARE_DATASET_PATH,
    ARCGIS_PHS_MAINTENANCE_DATASET_PATH,
    ARCGIS_COMMUNITY_ORGANISATIONS_DATASET_PATH,
    PHILADELPHIA_TREE_CANOPY_DATASET_URL,
    PHILADELPHIA_NEIGHBORHOODS_DATASET_URL,
)
from data_utils import (
    get_arcgis_dataset,
    get_philadelphia_li_complaint_dataset,
    get_philadelphia_li_violation_dataset,
    get_shapefile_dataset,
    get_philadelphia_gun_crime_dataset,
    get_property_assessment_dataset,
    get_delinquency_dataset,
    clean_ownership_values,
)

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=os.environ.get("LOGLEVEL", "INFO"), format="%(asctime)s %(message)s"
)


def clean_and_merge_gdfs(
    land_gdf,
    buildings_gdf,
    phs_landcare_gdf,
    phs_maintenance_gdf,
    community_orgs_gdf,
    complaints_gdf,
    violations_gdf,
    neighborhoods_gdf,
    tree_canopy_gdf,
    gun_crime_gdf,
    property_assessment_df,
    delinquency_df,
) -> gpd.GeoDataFrame:
    """this method needs quite a bit of refactoring"""

    """ land & buildings """
    columns = [
        "geometry",
        "ADDRESS",
        "BLDG_DESC",
        "OPA_ID",
        "COUNCILDISTRICT",
        "ZIPCODE",
        "OWNER1",
        "OWNER2",
    ]

    land_gdf, buildings_gdf = land_gdf[columns], buildings_gdf[columns]
    land_gdf.insert(0, "type", "lot")
    buildings_gdf.insert(0, "type", "building")

    main_gdf = pd.concat([land_gdf, buildings_gdf], axis=0)
    main_gdf = clean_ownership_values(main_gdf)

    """ PHS """
    phs_landcare_gdf = phs_landcare_gdf[["geometry", "COMM_PARTN"]]
    phs_maintenance_gdf.insert(0, "COMM_PARTN", "PHS")
    phs_maintenance_gdf = phs_maintenance_gdf[["geometry", "COMM_PARTN"]]

    phs_gdf = gpd.GeoDataFrame(
        pd.concat([phs_landcare_gdf, phs_maintenance_gdf], ignore_index=True),
        crs=phs_landcare_gdf.crs,
    )

    main_gdf = gpd.sjoin(main_gdf, phs_gdf, how="left", predicate="intersects")
    main_gdf.drop(["index_right"], axis=1, inplace=True)

    main_gdf["COMM_PARTN"] = main_gdf["COMM_PARTN"].fillna("None", inplace=True)

    """ L&I """
    complaints_gdf.drop(["lat", "lon"], axis=1, inplace=True)

    complaints_gdf = complaints_gdf[complaints_gdf["status"] == "Open"]

    complaints_gdf = (
        complaints_gdf.groupby("address")["service_name"]
        .apply(lambda x: "; ".join([val for val in x if val is not None]))
        .reset_index()
    )

    complaints_gdf.rename(columns={"service_name": "li_complaints"}, inplace=True)

    all_violations_count_df = (
        violations_gdf.groupby("opa_account_num")
        .count()
        .reset_index()[["opa_account_num", "violationnumber"]]
    )
    all_violations_count_df = all_violations_count_df.rename(
        columns={"violationnumber": "all_violations_past_year"}
    )

    violations_gdf = violations_gdf[(violations_gdf["violationstatus"] == "OPEN")]
    open_violations_count_df = (
        violations_gdf.groupby("opa_account_num")
        .count()
        .reset_index()[["opa_account_num", "violationnumber"]]
    )
    open_violations_count_df = open_violations_count_df.rename(
        columns={"violationnumber": "open_violations_past_year"}
    )

    violations_count_gdf = all_violations_count_df.merge(
        open_violations_count_df, how="left", on="opa_account_num"
    )
    violations_count_gdf.fillna(0, inplace=True)

    violations_count_gdf["all_violations_past_year"] = violations_count_gdf[
        "all_violations_past_year"
    ].astype(int)
    violations_count_gdf["open_violations_past_year"] = violations_count_gdf[
        "open_violations_past_year"
    ].astype(int)

    violations_gdf = (
        violations_gdf.groupby("opa_account_num")["violationcodetitle"]
        .apply(lambda x: "; ".join([val for val in x if val is not None]))
        .reset_index()
    )
    violations_gdf.rename(
        columns={"violationcodetitle": "li_code_violations"}, inplace=True
    )

    main_gdf = main_gdf.merge(
        complaints_gdf, how="left", left_on="ADDRESS", right_on="address"
    )
    main_gdf = main_gdf.merge(
        violations_gdf, how="left", left_on="OPA_ID", right_on="opa_account_num"
    )

    main_gdf.drop(["address", "opa_account_num"], axis=1, inplace=True)

    """ Centroids """
    main_gdf["centroid"] = main_gdf["geometry"].centroid
    poly_gdf = main_gdf[["OPA_ID", "geometry"]]
    main_gdf.drop(["geometry"], axis=1, inplace=True)
    main_gdf.set_geometry("centroid", inplace=True)

    """ neighborhoods """
    main_gdf = gpd.sjoin(
        main_gdf, neighborhoods_gdf, how="left", predicate="intersects"
    )
    main_gdf = main_gdf.drop(
        ["index_right", "NAME", "LISTNAME", "Shape_Leng", "Shape_Area"], axis=1
    )
    main_gdf.rename(columns={"MAPNAME": "neighborhood"}, inplace=True)

    """ community orgs """
    community_orgs_gdf["PRIMARY_PHONE"] = community_orgs_gdf["PRIMARY_PHONE"].astype(
        str
    )
    community_orgs_gdf["EXPIRATIONYEAR"] = community_orgs_gdf["EXPIRATIONYEAR"].astype(
        str
    )
    rco_aggregate_cols = [
        "ORGANIZATION_NAME",
        "ORGANIZATION_ADDRESS",
        "PRIMARY_EMAIL",
        "PRIMARY_PHONE",
    ]
    community_orgs_gdf["rco_info"] = community_orgs_gdf[rco_aggregate_cols].agg(
        "; ".join, axis=1
    )
    rcos_final_cols = ["geometry", "rco_info"]
    community_orgs_gdf = community_orgs_gdf[rcos_final_cols]

    w_community_orgs_gdf = gpd.sjoin(
        main_gdf, community_orgs_gdf, how="left", predicate="within"
    )
    w_community_orgs_gdf.drop(["index_right"], axis=1, inplace=True)
    w_community_orgs_gdf.rename(columns={"rco_info": "rco_info"}, inplace=True)
    w_community_orgs_gdf.drop_duplicates(subset="OPA_ID", inplace=True)

    w_community_orgs_gdf["OPA_ID"] = w_community_orgs_gdf["OPA_ID"].astype(str)

    rcos_by_opa_id_gdf = (
        w_community_orgs_gdf.groupby("OPA_ID")["rco_info"]
        .apply(lambda x: "| ".join([str(val) for val in x if val is not None]))
        .reset_index()
    )

    rcos_by_opa_id_gdf.rename(columns={"rco_info": "relevant_rcos"}, inplace=True)

    main_gdf = main_gdf.merge(
        rcos_by_opa_id_gdf, how="left", left_on="OPA_ID", right_on="OPA_ID"
    )
    main_gdf.drop_duplicates(subset="OPA_ID", inplace=True)

    """ tree canopy """
    main_gdf = gpd.sjoin(main_gdf, tree_canopy_gdf, how="left", predicate="intersects")
    main_gdf.drop(["index_right"], axis=1, inplace=True)
    main_gdf.drop_duplicates(subset="OPA_ID", inplace=True)

    return main_gdf


def orchestrate_processing(output_filename: str) -> bool:
    logger.info("Fetching data sources")
    land_gdf = get_arcgis_dataset(ARCGIS_LAND_DATASET_PATH)
    buildings_gdf = get_arcgis_dataset(ARCGIS_BUILDINGS_DATASET_PATH)
    phs_landcare_gdf = get_arcgis_dataset(ARCGIS_PHS_LANDCARE_DATASET_PATH)
    phs_maintenance_gdf = get_arcgis_dataset(ARCGIS_PHS_MAINTENANCE_DATASET_PATH)
    community_orgs_gdf = get_arcgis_dataset(ARCGIS_COMMUNITY_ORGANISATIONS_DATASET_PATH)
    complaints_gdf = get_philadelphia_li_complaint_dataset()
    violations_gdf = get_philadelphia_li_violation_dataset()
    neighborhoods_gdf = get_shapefile_dataset(PHILADELPHIA_NEIGHBORHOODS_DATASET_URL)
    tree_canopy_gdf = get_shapefile_dataset(PHILADELPHIA_TREE_CANOPY_DATASET_URL)
    gun_crime_gdf = get_philadelphia_gun_crime_dataset()
    property_assessment_df = get_property_assessment_dataset()
    delinquency_df = get_delinquency_dataset()
    logger.info("Successfully fetched data")

    logger.info("Cleaning and merging the data")
    main_gdf = clean_and_merge_gdfs(
        land_gdf,
        buildings_gdf,
        phs_landcare_gdf,
        phs_maintenance_gdf,
        community_orgs_gdf,
        complaints_gdf,
        violations_gdf,
        neighborhoods_gdf,
        tree_canopy_gdf,
        gun_crime_gdf,
        property_assessment_df,
        delinquency_df,
    )
    logger.info("Successfully processed data")

    logger.info(f"Writing data to ./{output_filename}")
    main_gdf.to_file(f"./{output_filename}", driver="GeoJSON")

    return True


def main():
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Process various Philadelphia data into a GeoJSON file"
    )
    parser.add_argument("filename", help="the output file name")
    args = parser.parse_args()

    output_filename: str = args.filename

    if orchestrate_processing(output_filename):
        logger.info(
            f"Successfully processed data. Results are saved in {output_filename}"
        )
    else:
        logger.info("An error occurred during data processing.")


if __name__ == "__main__":
    main()
