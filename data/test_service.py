#!/usr/bin/env python3
"""
Test script for individual pipeline services.
Usage: uv run python test_service.py <service_name>
Example: uv run python test_service.py phs_properties
"""

import sys

from src.classes.loaders import BaseLoader
from src.config.config import enable_statistical_summaries

# Import all services
from src.data_utils import (
    access_process,
    city_owned_properties,
    community_gardens,
    conservatorship,
    contig_neighbors,
    council_dists,
    delinquencies,
    dev_probability,
    drug_crimes,
    gun_crimes,
    imm_dang_buildings,
    li_complaints,
    li_violations,
    nbhoods,
    negligent_devs,
    opa_properties,
    owner_type,
    park_priority,
    phs_properties,
    ppr_properties,
    priority_level,
    pwd_parcels,
    rco_geoms,
    tactical_urbanism,
    tree_canopy,
    unsafe_buildings,
    vacant_properties,
)

# Service mapping
SERVICES = {
    "phs_properties": phs_properties,
    "vacant_properties": vacant_properties,
    "pwd_parcels": pwd_parcels,
    "council_dists": council_dists,
    "nbhoods": nbhoods,
    "rco_geoms": rco_geoms,
    "city_owned_properties": city_owned_properties,
    "community_gardens": community_gardens,
    "ppr_properties": ppr_properties,
    "owner_type": owner_type,
    "li_violations": li_violations,
    "li_complaints": li_complaints,
    "tree_canopy": tree_canopy,
    "gun_crimes": gun_crimes,
    "drug_crimes": drug_crimes,
    "delinquencies": delinquencies,
    "unsafe_buildings": unsafe_buildings,
    "imm_dang_buildings": imm_dang_buildings,
    "contig_neighbors": contig_neighbors,
    "dev_probability": dev_probability,
    "negligent_devs": negligent_devs,
    "tactical_urbanism": tactical_urbanism,
    "conservatorship": conservatorship,
    "park_priority": park_priority,
    "priority_level": priority_level,
    "access_process": access_process,
}

# Service dependencies - defines which services need to be run before each target service
SERVICE_DEPENDENCIES = {
    "conservatorship": [
        "opa_properties",
        "vacant_properties",
        "city_owned_properties",
        "delinquencies",
        "li_violations",
    ],
    "contig_neighbors": ["opa_properties", "vacant_properties", "pwd_parcels"],
    "negligent_devs": ["opa_properties", "vacant_properties", "li_violations"],
    "priority_level": [
        "opa_properties",
        "vacant_properties",
        "phs_properties",
        "li_violations",
        "li_complaints",
        "gun_crimes",
        "tree_canopy",
    ],
    "tactical_urbanism": [
        "opa_properties",
        "vacant_properties",
        "unsafe_buildings",
        "imm_dang_buildings",
    ],
    # Keep existing special cases
    "community_gardens": ["opa_properties", "vacant_properties"],
    "access_process": ["opa_properties", "vacant_properties", "city_owned_properties"],
}


def disable_caching():
    """Temporarily disable caching for testing"""
    original_cache_data = BaseLoader.cache_data

    def no_cache_data(self, gdf):
        print("Caching disabled for testing")
        return

    BaseLoader.cache_data = no_cache_data
    return original_cache_data


def restore_caching(original_method):
    """Restore the original caching method"""
    BaseLoader.cache_data = original_method


def run_dependencies(dataset, dependencies):
    """Run all required dependencies for a service."""
    if not dependencies:
        return dataset

    print(f"\nRunning dependencies: {', '.join(dependencies)}")
    print("-" * 30)

    for dep in dependencies:
        if dep == "opa_properties":
            # opa_properties is the base dataset, already loaded
            continue

        print(f"Running {dep}...")
        service_func = SERVICES[dep]

        # Run dependencies without statistical summaries
        dataset, validation = service_func(dataset)

        print(f"  Dataset shape after {dep}: {dataset.shape}")
        print(f"  Validation: {validation}")

        if not validation["input"] or not validation["output"]:
            print(f"  Warning: {dep} validation failed: {validation}")

    return dataset


def test_service(service_name: str):
    """Test a specific service with the base OPA properties dataset."""

    if service_name not in SERVICES:
        print(f"Error: Service '{service_name}' not found.")
        print(f"Available services: {', '.join(SERVICES.keys())}")
        return

    print(f"Testing service: {service_name}")
    print("=" * 50)

    # Disable caching for testing
    original_cache_method = disable_caching()

    try:
        # Load base dataset
        print("Loading OPA properties dataset...")
        dataset, opa_validation = opa_properties()
        print(f"Base dataset shape: {dataset.shape}")
        print(f"Base dataset columns: {list(dataset.columns)}")

        # Check validation
        if not opa_validation["input"] or not opa_validation["output"]:
            print(f"Warning: OPA properties validation failed: {opa_validation}")

        # Run dependencies if any
        dependencies = SERVICE_DEPENDENCIES.get(service_name, [])
        if dependencies:
            dataset = run_dependencies(dataset, dependencies)
            print(
                f"\nFinal dataset shape before running {service_name}: {dataset.shape}"
            )
            print(f"Final dataset columns: {list(dataset.columns)}")

        # Run the service
        service_func = SERVICES[service_name]
        print(f"\nRunning {service_name}...")

        # Enable statistical summaries only for the service being tested
        with enable_statistical_summaries():
            result_dataset, validation = service_func(dataset)

        # Show results
        print("\nResults:")
        print(f"Output dataset shape: {result_dataset.shape}")
        print(f"Output dataset columns: {list(result_dataset.columns)}")
        print(f"Validation: {validation}")

        # Show sample data
        print("\nSample data (first 3 rows):")
        print(result_dataset.head(3))

        # Show what columns were added
        original_cols = set(dataset.columns)
        new_cols = set(result_dataset.columns)
        added_cols = new_cols - original_cols
        if added_cols:
            print(f"\nAdded columns: {list(added_cols)}")
        else:
            print("\nNo new columns added")

    finally:
        # Always restore caching
        restore_caching(original_cache_method)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: uv run python test_service.py <service_name>")
        print(f"Available services: {', '.join(SERVICES.keys())}")
        sys.exit(1)

    service_name = sys.argv[1]
    test_service(service_name)
