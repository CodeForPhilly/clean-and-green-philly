import argparse
import os
import zipfile

import geopandas as gpd
from sqlalchemy import create_engine


def fetch_data(connection_string, sql_query, geom_col):
    engine = create_engine(connection_string)
    gdf = gpd.read_postgis(sql=sql_query, con=engine, geom_col=geom_col)
    return gdf


def save_file(gdf, filename, zipped):
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    if filename.endswith(".parquet"):
        gdf.to_parquet(filename)
    else:
        temp_filename = filename
        gdf.to_file(temp_filename)

        if zipped:
            zip_filename = f"{os.path.splitext(filename)[0]}.zip"
            with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(temp_filename, os.path.basename(temp_filename))
            os.remove(temp_filename)


def main(output_filename, zipped):
    connection_string = os.getenv("VACANT_LOTS_DB")
    sql_query = "SELECT * FROM vacant_properties_end;"
    geom_col = "geometry"
    gdf = fetch_data(connection_string, sql_query, geom_col)
    save_file(gdf, output_filename, zipped)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Fetch data from PostGIS and save as a file."
    )
    parser.add_argument(
        "output_filename", type=str, help="The output filename for the data."
    )
    parser.add_argument(
        "--zipped", action="store_true", help="Whether to zip the output file."
    )
    args = parser.parse_args()
    main(args.output_filename, args.zipped)
