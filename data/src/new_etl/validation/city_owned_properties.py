from typing import List, Tuple

import geopandas as gpd

from .base import ServiceValidator


class CityOwnedPropertiesValidator(ServiceValidator):
    """Validator for city-owned properties service."""

    # Known valid city agencies
    KNOWN_AGENCIES = {
        "Land Bank (PHDC)",
        "PRA",
        "DPP",
        "PHA",
        "City of Philadelphia",
    }

    def validate(self, data: gpd.GeoDataFrame) -> Tuple[bool, List[str]]:
        """
        Validate city-owned properties data.

        Critical checks:
        - Required fields present (city_owner_agency, side_yard_eligible)
        - city_owner_agency is string or NA
        - side_yard_eligible is "Yes" or "No" (no NAs)
        - city_owner_agency values match known agencies
        - Valid geometries

        Returns:
            Tuple of (is_valid, list of error messages)
        """
        errors = []

        # Check required columns
        errors.extend(
            self.check_required_columns(
                data, ["city_owner_agency", "side_yard_eligible"]
            )
        )

        # Check data types and values
        if "city_owner_agency" in data.columns:
            # Check type for non-null values
            non_null_agencies = data[data["city_owner_agency"].notna()]
            if (
                len(non_null_agencies) > 0
                and non_null_agencies["city_owner_agency"].dtype != "object"
            ):
                errors.append("city_owner_agency must be string type")

            # Check for unknown agency values
            unknown_agencies = (
                set(
                    data[data["city_owner_agency"].notna()][
                        "city_owner_agency"
                    ].unique()
                )
                - self.KNOWN_AGENCIES
            )
            if unknown_agencies:
                errors.append(
                    f"Found unknown city_owner_agency values: {sorted(unknown_agencies)}"
                )

        # Check side_yard_eligible values
        if "side_yard_eligible" in data.columns:
            invalid_values = data[~data["side_yard_eligible"].isin(["Yes", "No"])][
                "side_yard_eligible"
            ].unique()
            if len(invalid_values) > 0:
                errors.append(
                    f"side_yard_eligible must be 'Yes' or 'No', found: {sorted(invalid_values)}"
                )

        # Check geometry validity
        if not data.geometry.is_valid.all():
            errors.append("Found invalid geometries")

        # Log statistics about city ownership and side yard eligibility
        if all(
            col in data.columns for col in ["city_owner_agency", "side_yard_eligible"]
        ):
            total_properties = len(data)
            city_owned = len(data[data["city_owner_agency"].notna()])
            side_yard_eligible = len(data[data["side_yard_eligible"] == "Yes"])

            print("\nCity Ownership Statistics:")
            print(f"- Total properties: {total_properties}")
            print(
                f"- City-owned properties: {city_owned} ({city_owned / total_properties:.1%})"
            )
            print(
                f"- Side yard eligible: {side_yard_eligible} ({side_yard_eligible / total_properties:.1%})"
            )

            if city_owned > 0:
                print("\nCity Owner Agency Distribution:")
                agency_counts = (
                    data[data["city_owner_agency"].notna()]["city_owner_agency"]
                    .value_counts()
                    .to_dict()
                )
                for agency, count in agency_counts.items():
                    print(f"  - {agency}: {count} ({count / city_owned:.1%})")

        return len(errors) == 0, errors
