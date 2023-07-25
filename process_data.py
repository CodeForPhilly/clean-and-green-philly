from data_utils import *


def main():

    # fetch data
    land_gdf = get_arcgis_dataset(ARCGIS_LAND_DATASET_PATH)
    buildings_gdf = get_arcgis_dataset(ARCGIS_BUILDINGS_DATASET_PATH)
    phs_landcare_gdf = get_arcgis_dataset(ARCGIS_PHS_LANDCARE_DATASET_PATH)
    phs_maintenance_gdf = get_arcgis_dataset(ARCGIS_PHS_MAINTENANCE_DATASET_PATH)
    rco_gdf = get_arcgis_dataset(ARCGIS_RCO_DATASET_PATH)
    complaints_gdf = get_philadelphia_li_complaint_dataset()
    violations_gdf = get_philadelphia_li_complaint_dataset()

    # preprocess data

    # merge data


if __name__ == "__main__":
    main()
