import argparse

from constants import (
    ARCGIS_LAND_DATASET_PATH,
    ARCGIS_BUILDINGS_DATASET_PATH,
    ARCGIS_PHS_LANDCARE_DATASET_PATH,
    ARCGIS_PHS_MAINTENANCE_DATASET_PATH,
    ARCGIS_RCO_DATASET_PATH,
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
)


def orchestrate_processing(output_filename: str) -> bool:
    # fetch data
    land_gdf = get_arcgis_dataset(ARCGIS_LAND_DATASET_PATH)
    buildings_gdf = get_arcgis_dataset(ARCGIS_BUILDINGS_DATASET_PATH)
    phs_landcare_gdf = get_arcgis_dataset(ARCGIS_PHS_LANDCARE_DATASET_PATH)
    phs_maintenance_gdf = get_arcgis_dataset(ARCGIS_PHS_MAINTENANCE_DATASET_PATH)
    rco_gdf = get_arcgis_dataset(ARCGIS_RCO_DATASET_PATH)
    complaints_gdf = get_philadelphia_li_complaint_dataset()
    violations_gdf = get_philadelphia_li_violation_dataset()
    neighborhoods_gdf = get_shapefile_dataset(PHILADELPHIA_NEIGHBORHOODS_DATASET_URL)
    tree_canopy_gdf = get_shapefile_dataset(PHILADELPHIA_TREE_CANOPY_DATASET_URL)
    gun_crime_gdf = get_philadelphia_gun_crime_dataset()
    opa_df = get_property_assessment_dataset()
    delinquency_df = get_delinquency_dataset()

    # preprocess data

    # merge data
    return True


def main():
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Process various Philadelphia data into a GeoJSON file"
    )
    parser.add_argument("filename", help="the output file name")
    args = parser.parse_args()

    output_filename: str = args.filename

    if orchestrate_processing(output_filename):
        print(f"Successfully processed data. Results are saved in {output_filename}")
    else:
        print("An error occurred during data processing.")


if __name__ == "__main__":
    main()
