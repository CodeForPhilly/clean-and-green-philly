#!/usr/bin/env python3
"""
Simple analysis script for contig_neighbors data.
"""

from src.data_utils import opa_properties, pwd_parcels, vacant_properties
from src.data_utils.contig_neighbors import contig_neighbors


def analyze_contig_neighbors():
    """Analyze the contig_neighbors data to see actual statistics."""

    print("Loading base dataset...")
    dataset, _ = opa_properties()

    print("Running vacant_properties...")
    dataset, _ = vacant_properties(dataset)

    print("Running pwd_parcels...")
    dataset, _ = pwd_parcels(dataset)

    print("Running contig_neighbors (bypassing validation)...")
    # Call the undecorated function directly
    result_dataset, _ = contig_neighbors.__wrapped__(dataset)

    print("\n" + "=" * 60)
    print("CONTIG NEIGHBORS ANALYSIS")
    print("=" * 60)

    if "n_contiguous" in result_dataset.columns:
        # Get non-null values
        non_null_data = result_dataset["n_contiguous"].dropna()

        print(f"\nTotal records: {len(result_dataset):,}")
        print(f"Non-null n_contiguous values: {len(non_null_data):,}")
        print(
            f"Null n_contiguous values: {result_dataset['n_contiguous'].isna().sum():,}"
        )

        if len(non_null_data) > 0:
            print("\nActual Statistics:")
            print(f"  Min: {non_null_data.min()}")
            print(f"  Max: {non_null_data.max()}")
            print(f"  Mean: {non_null_data.mean():.3f}")
            print(f"  Std: {non_null_data.std():.3f}")
            print(f"  Q1: {non_null_data.quantile(0.25):.3f}")
            print(f"  Q3: {non_null_data.quantile(0.75):.3f}")

            print("\nExpected Ranges:")
            print(f"  Max: <= 49 (actual: {non_null_data.max()})")
            print(f"  Mean: [2.05, 3.08] (actual: {non_null_data.mean():.3f})")
            print(f"  Std: [3.90, 5.85] (actual: {non_null_data.std():.3f})")
            print(f"  Q1: [0.00, 0.00] (actual: {non_null_data.quantile(0.25):.3f})")
            print(f"  Q3: [2.40, 3.60] (actual: {non_null_data.quantile(0.75):.3f})")

            print("\nValue Distribution:")
            value_counts = non_null_data.value_counts().sort_index()
            for value, count in value_counts.head(20).items():
                pct = (count / len(non_null_data)) * 100
                print(f"  {value}: {count:,} ({pct:.1f}%)")

            if len(value_counts) > 20:
                print(f"  ... and {len(value_counts) - 20} more unique values")
        else:
            print("\nNo non-null n_contiguous values found!")
    else:
        print("\nNo n_contiguous column found!")


if __name__ == "__main__":
    analyze_contig_neighbors()
