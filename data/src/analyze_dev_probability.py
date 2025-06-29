#!/usr/bin/env python3
"""
Simple script to analyze dev_probability data directly by running the service inline.
"""

import os
import sys

import pandas as pd

# Ensure the parent directory (data) is in sys.path so 'src' can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.classes.loaders import CartoLoader
from src.constants.services import OPA_PROPERTIES_QUERY
from src.data_utils.dev_probability import dev_probability


def analyze_dev_probability():
    print("=" * 80)
    print("DEV PROBABILITY DATA ANALYSIS (INLINE)")
    print("=" * 80)

    # Load OPA properties dataset
    loader = CartoLoader(
        name="OPA Properties",
        carto_queries=OPA_PROPERTIES_QUERY,
        opa_col="parcel_number",
        cols=[
            "market_value",
            "sale_date",
            "sale_price",
            "parcel_number",
            "owner_1",
            "owner_2",
            "mailing_address_1",
            "mailing_address_2",
            "mailing_care_of",
            "mailing_city_state",
            "mailing_street",
            "mailing_zip",
            "unit",
            "street_address",
            "building_code_description",
            "zip_code",
            "zoning",
        ],
    )
    opa_gdf, _ = loader.load_or_fetch()
    print(f"Loaded OPA properties: {len(opa_gdf):,} rows")
    print(f"OPA columns: {list(opa_gdf.columns)}")
    print("OPA head:")
    print(opa_gdf.head())

    # Run the dev_probability service
    result_gdf, _ = dev_probability(opa_gdf)
    print(f"Service output: {len(result_gdf):,} rows")
    print(f"Columns: {list(result_gdf.columns)}")

    # Analyze permit_count
    if "permit_count" in result_gdf.columns:
        print("\npermit_count analysis:")
        null_count = result_gdf["permit_count"].isnull().sum()
        print(f"  Null count: {null_count:,}")
        print(f"  Data type: {result_gdf['permit_count'].dtype}")
        numeric_data = pd.to_numeric(result_gdf["permit_count"], errors="coerce")
        non_null_data = numeric_data.dropna()
        if len(non_null_data) > 0:
            stats = non_null_data.describe()
            print(f"  Count: {len(non_null_data):,}")
            print(f"  Mean: {stats['mean']:.2f}")
            print(f"  Std:  {stats['std']:.2f}")
            print(f"  Min:  {stats['min']:.2f}")
            print(f"  Max:  {stats['max']:.2f}")
            print(f"  Q1:   {stats['25%']:.2f}")
            print(f"  Q3:   {stats['75%']:.2f}")
            value_counts = non_null_data.value_counts().head(10)
            print("  Top 10 values:")
            for value, count in value_counts.items():
                pct = (count / len(non_null_data)) * 100
                print(f"    {value}: {count:,} ({pct:.1f}%)")
            print(f"  Sample values: {non_null_data.head(10).tolist()}")
        else:
            print("  No valid numeric data found")

    # Analyze dev_rank
    if "dev_rank" in result_gdf.columns:
        print("\ndev_rank analysis:")
        null_count = result_gdf["dev_rank"].isnull().sum()
        print(f"  Null count: {null_count:,}")
        print(f"  Data type: {result_gdf['dev_rank'].dtype}")
        nan_strings = (result_gdf["dev_rank"] == "nan").sum()
        print(f"  'nan' strings: {nan_strings:,}")
        value_counts = result_gdf["dev_rank"].value_counts()
        print("  Value distribution:")
        for value, count in value_counts.items():
            pct = (count / len(result_gdf)) * 100
            print(f"    {value}: {count:,} ({pct:.1f}%)")
        print(f"  Sample values: {result_gdf['dev_rank'].head(10).tolist()}")
        valid_ranks = ["Low", "Medium", "High"]
        invalid_values = result_gdf["dev_rank"][
            ~result_gdf["dev_rank"].isin(valid_ranks)
        ]
        if len(invalid_values) > 0:
            print(f"  Invalid values found: {invalid_values.value_counts().to_dict()}")

    print("\n" + "=" * 80)


if __name__ == "__main__":
    analyze_dev_probability()
