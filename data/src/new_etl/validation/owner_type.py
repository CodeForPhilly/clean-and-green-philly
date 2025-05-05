from typing import List, Tuple

import geopandas as gpd

from .base_validator import BaseValidator


class OwnerTypeValidator(BaseValidator):
    """
    Validator for owner type categorization.
    Ensures properties are correctly categorized as Public, Business (LLC), or Individual.
    """

    # Valid owner types
    VALID_OWNER_TYPES = {"Public", "Business (LLC)", "Individual"}

    def validate(self, gdf: gpd.GeoDataFrame) -> Tuple[bool, List[str]]:
        """
        Validate the owner type categorization.

        Args:
            gdf (gpd.GeoDataFrame): The GeoDataFrame to validate.

        Returns:
            Tuple[bool, List[str]]: A tuple containing:
                - bool: Whether the validation passed
                - List[str]: List of error messages if validation failed
        """
        errors = []

        # Check required columns
        required_columns = ["owner_type", "owner_1", "owner_2", "city_owner_agency"]
        missing_columns = [col for col in required_columns if col not in gdf.columns]
        if missing_columns:
            errors.append(f"Missing required columns: {', '.join(missing_columns)}")

        # Check that owner_type column exists and has valid values
        if "owner_type" in gdf.columns:
            # Check for null values in owner_type
            null_owner_types = gdf["owner_type"].isna().sum()
            if null_owner_types > 0:
                errors.append(
                    f"Found {null_owner_types} properties with null owner_type"
                )

            # Check for invalid owner types
            invalid_types = (
                set(gdf["owner_type"].dropna().unique()) - self.VALID_OWNER_TYPES
            )
            if invalid_types:
                errors.append(f"Found invalid owner types: {sorted(invalid_types)}")

            # Validate categorization logic
            for owner_type in self.VALID_OWNER_TYPES:
                subset = gdf[gdf["owner_type"] == owner_type]

                if owner_type == "Public":
                    # Public properties should have a non-null city_owner_agency
                    invalid_public = subset[subset["city_owner_agency"].isna()]
                    if not invalid_public.empty:
                        errors.append(
                            f"Found {len(invalid_public)} properties marked as Public with null city_owner_agency"
                        )

                elif owner_type == "Business (LLC)":
                    # Business (LLC) properties should have "LLC" in owner_1 or owner_2
                    invalid_business = subset[
                        ~subset["owner_1"].str.lower().str.contains(" llc", na=False)
                        & ~subset["owner_2"].str.lower().str.contains(" llc", na=False)
                    ]
                    if not invalid_business.empty:
                        errors.append(
                            f"Found {len(invalid_business)} properties marked as Business (LLC) without 'LLC' in owner names"
                        )

                elif owner_type == "Individual":
                    # Individual properties should not have a city_owner_agency and should not have "LLC" in owner names
                    invalid_individual = subset[
                        subset["city_owner_agency"].notna()
                        | subset["owner_1"].str.lower().str.contains(" llc", na=False)
                        | subset["owner_2"].str.lower().str.contains(" llc", na=False)
                    ]
                    if not invalid_individual.empty:
                        errors.append(
                            f"Found {len(invalid_individual)} properties marked as Individual that should be Public or Business (LLC)"
                        )

        # Log statistics about owner types
        if "owner_type" in gdf.columns:
            total_properties = len(gdf)
            print("\nOwner Type Statistics:")
            print(f"- Total properties: {total_properties}")

            for owner_type in self.VALID_OWNER_TYPES:
                count = len(gdf[gdf["owner_type"] == owner_type])
                percentage = (count / total_properties) * 100
                print(f"- {owner_type}: {count} ({percentage:.1f}%)")

        return len(errors) == 0, errors
