from typing import Dict, List, Set, Tuple

import geopandas as gpd

from .base import ServiceValidator


class CityOwnedPropertiesValidator(ServiceValidator):
    """
    Validator for city-owned properties data.
    Ensures proper data quality and consistency for city-owned property assignments.
    """

    KNOWN_AGENCIES = {
        "PHA",
        "PPR",
        "PWD",
        "RDA",
        "OHCD",
        "OPA",
        "DOR",
        "DHS",
        "DPH",
        "DOT",
        "L&I",
        "PFD",
        "PFR",
        "PFS",
        "PFT",
        "PHA",
        "PHS",
        "PIT",
        "PMA",
        "PRA",
        "PRD",
        "PRS",
        "PRT",
        "PSA",
        "PSD",
        "PSS",
        "PST",
        "PTA",
        "PTC",
        "PTD",
        "PTE",
        "PTF",
        "PTG",
        "PTH",
        "PTI",
        "PTJ",
        "PTK",
        "PTL",
        "PTM",
        "PTN",
        "PTO",
        "PTP",
        "PTQ",
        "PTR",
        "PTS",
        "PTT",
        "PTU",
        "PTV",
        "PTW",
        "PTX",
        "PTY",
        "PTZ",
        "Unknown",
    }

    def _validate_service_specific(self, data: gpd.GeoDataFrame) -> List[str]:
        """
        Validate service-specific aspects of the city-owned properties data.

        Args:
            data: The GeoDataFrame to validate

        Returns:
            List of error messages
        """
        errors = []

        # Check for required columns
        required_columns = ["opa_id", "city_owner_agency", "side_yard_eligible"]
        missing_columns = [col for col in required_columns if col not in data.columns]
        if missing_columns:
            errors.append(f"Missing required columns: {', '.join(missing_columns)}")

        # Check for null values in required columns
        for col in required_columns:
            if col in data.columns:
                null_count = data[data[col].isna()].shape[0]
                if null_count > 0:
                    errors.append(f"Found {null_count} null values in {col}")

        # Check for valid agency values
        if "city_owner_agency" in data.columns:
            invalid_agencies = data[
                ~data["city_owner_agency"].isin(self.KNOWN_AGENCIES)
            ]
            if not invalid_agencies.empty:
                errors.append(
                    f"Found {len(invalid_agencies)} properties with invalid city_owner_agency values. Valid agencies are: {', '.join(sorted(self.KNOWN_AGENCIES))}"
                )

        # Check for valid side_yard_eligible values
        if "side_yard_eligible" in data.columns:
            invalid_side_yard = data[~data["side_yard_eligible"].isin(["Yes", "No"])]
            if not invalid_side_yard.empty:
                errors.append(
                    f"Found {len(invalid_side_yard)} properties with invalid side_yard_eligible values. Valid values are: Yes, No"
                )

        # Log statistics about city-owned properties
        if "city_owner_agency" in data.columns:
            total_properties = len(data)
            print("\nCity-Owned Properties Statistics:")
            print(f"- Total properties: {total_properties}")

            # Agency distribution
            agency_counts = data["city_owner_agency"].value_counts()
            print("\nTop 10 agencies by property count:")
            for agency, count in agency_counts.head(10).items():
                percentage = (count / total_properties) * 100
                print(f"- {agency}: {count} properties ({percentage:.1f}%)")

            print("\nBottom 10 agencies by property count:")
            for agency, count in agency_counts.tail(10).items():
                percentage = (count / total_properties) * 100
                print(f"- {agency}: {count} properties ({percentage:.1f}%)")

        return errors

    def get_required_input_columns(self) -> List[str]:
        """
        Get the list of required input columns for this service.

        Returns:
            List of required input column names
        """
        return ["opa_id", "city_owner_agency", "side_yard_eligible"]

    def get_required_input_values(self) -> Dict[str, Set]:
        """
        Get the dictionary of required input values for this service.

        Returns:
            Dictionary mapping column names to sets of valid values
        """
        return {
            "city_owner_agency": self.KNOWN_AGENCIES,
            "side_yard_eligible": {"Yes", "No"},
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
