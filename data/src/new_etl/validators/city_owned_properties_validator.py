from typing import Optional, Set

from new_etl.validators.base_validator import BaseValidator
from new_etl.validators.geometry_validator import GeometryValidator
from new_etl.validators.schema_drift_validator import (
    SchemaDriftValidator,
    validate_schema_drift,
)


class CityOwnedPropertiesValidator(SchemaDriftValidator):
    """Validator for City Owned Properties dataset schema drift"""

    def __init__(self):
        super().__init__(size_tolerance=0.05)  # 5% tolerance

    @property
    def expected_columns(self) -> Set[str]:
        return {
            "pin",
            "mapreg_1",
            "agency",
            "opabrt",
            "location",
            "status_1",
            "councildistrict",
            "sideyardeligible",
            "zoning",
            "objectid",
            "Shape__Area",
            "Shape__Length",
        }

    @property
    def required_non_null(self) -> Set[str]:
        return {
            "mapreg_1",  # 100% required
            "agency",  # 100% required
            "location",  # 100% required
            "status_1",  # 100% required
            "councildistrict",  # 100% required
            "sideyardeligible",  # 100% required
            "zoning",  # 100% required
            "objectid",  # 100% required
            "Shape__Area",  # 100% required
            "Shape__Length",  # 100% required
        }

    @property
    def expected_record_count(self) -> Optional[int]:
        return 7_796


def validate_city_owned_properties(func):
    """Decorator to validate city owned properties data."""
    return GeometryValidator.validate(
        BaseValidator.validate(
            validate_schema_drift(CityOwnedPropertiesValidator())(func)
        )
    )
