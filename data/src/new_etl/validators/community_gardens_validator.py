from typing import Optional, Set

from new_etl.validators.base_validator import BaseValidator
from new_etl.validators.geometry_validator import GeometryValidator
from new_etl.validators.schema_drift_validator import (
    SchemaDriftValidator,
    validate_schema_drift,
)


class CommunityGardensValidator(SchemaDriftValidator):
    """Validator for Community Gardens dataset schema drift"""

    def __init__(self):
        super().__init__(size_tolerance=0.05)  # 5% tolerance

    @property
    def expected_columns(self) -> Set[str]:
        return {"OBJECTID", "Site_Name", "Supported", "Website"}

    @property
    def required_non_null(self) -> Set[str]:
        return {"OBJECTID", "Site_Name", "Supported"}

    @property
    def expected_record_count(self) -> Optional[int]:
        return 205


def validate_community_gardens(func):
    """Decorator to validate community gardens data."""
    return GeometryValidator.validate(
        BaseValidator.validate(validate_schema_drift(CommunityGardensValidator())(func))
    )
