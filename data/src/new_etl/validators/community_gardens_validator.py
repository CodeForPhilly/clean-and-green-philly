from typing import Optional, Set

from .schema_drift_validator import SchemaDriftValidator


class CommunityGardensValidator(SchemaDriftValidator):
    """Validator for Community Gardens dataset schema drift"""

    def __init__(self):
        super().__init__(size_tolerance=0.05)  # 5% tolerance

    @property
    def expected_columns(self) -> Set[str]:
        return {
            "OBJECTID",
            "Site_Name",
            "Supported",
            "Website",
        }

    @property
    def required_non_null(self) -> Set[str]:
        return {
            "OBJECTID",  # 100% required
            "Site_Name",  # 100% required
            "Supported",  # 100% required
        }

    @property
    def expected_record_count(self) -> Optional[int]:
        return 205
