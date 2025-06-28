#!/usr/bin/env python3
"""
Simple script to analyze delinquencies data directly from cache.
"""

import pandas as pd

from src.classes.file_manager import FileManager


def analyze_delinquencies():
    """Load and analyze delinquencies data from cache."""

    print("=" * 80)
    print("DELINQUENCIES DATA ANALYSIS")
    print("=" * 80)

    # Load the cached delinquencies data
    file_manager = FileManager()

    # Try to load the most recent cache
    try:
        gdf = file_manager.get_most_recent_cache("property_tax_delinquencies")
        if gdf is None:
            print("No cached delinquencies data found!")
            return
    except Exception as e:
        print(f"Error loading cached data: {e}")
        return

    print(f"\nTotal records: {len(gdf):,}")
    print(f"Columns: {list(gdf.columns)}")

    # Check for the specific columns we care about
    columns_to_check = [
        "num_years_owed",
        "total_due",
        "total_assessment",
        "is_actionable",
        "sheriff_sale",
        "payment_agreement",
        "most_recent_year_owed",
    ]

    print("\nData types:")
    for col in columns_to_check:
        if col in gdf.columns:
            print(f"  {col}: {gdf[col].dtype}")
        else:
            print(f"  {col}: NOT FOUND")

    print("\nColumn coverage:")
    for col in columns_to_check:
        if col in gdf.columns:
            # Check for "NA" strings vs actual nulls
            na_strings = (gdf[col] == "NA").sum()
            actual_nulls = gdf[col].isnull().sum()
            non_null_count = gdf[col].notna().sum()
            coverage_pct = (non_null_count / len(gdf)) * 100

            print(
                f"  {col}: {non_null_count:,} ({coverage_pct:.1f}%) - 'NA' strings: {na_strings:,}, actual nulls: {actual_nulls:,}"
            )

            # Show sample values
            print(f"    Sample values: {gdf[col].head(5).tolist()}")
        else:
            print(f"  {col}: NOT FOUND")

    # Analyze numeric columns
    numeric_columns = ["num_years_owed", "total_due", "total_assessment"]
    for col in numeric_columns:
        if col in gdf.columns:
            print(f"\n{col} analysis:")

            # Convert "NA" strings to nulls for analysis
            data = gdf[col].replace("NA", pd.NA)
            numeric_data = pd.to_numeric(data, errors="coerce")
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

                # Show some actual values
                print(f"  Sample values: {non_null_data.head(10).tolist()}")
            else:
                print("  No valid numeric data found")

    # Analyze boolean columns
    boolean_columns = ["is_actionable", "sheriff_sale", "payment_agreement"]
    for col in boolean_columns:
        if col in gdf.columns:
            print(f"\n{col} analysis:")
            value_counts = gdf[col].value_counts()
            for value, count in value_counts.items():
                pct = (count / len(gdf)) * 100
                print(f"  {value}: {count:,} ({pct:.1f}%)")

            # Show sample values
            print(f"  Sample values: {gdf[col].head(10).tolist()}")

    print("\n" + "=" * 80)


if __name__ == "__main__":
    analyze_delinquencies()
