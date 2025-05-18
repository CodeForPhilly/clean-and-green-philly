from typing import Optional, Set

from .schema_drift_validator import SchemaDriftValidator


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
