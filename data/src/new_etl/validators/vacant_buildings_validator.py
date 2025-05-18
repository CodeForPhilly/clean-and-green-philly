from typing import Optional, Set

from .schema_drift_validator import SchemaDriftValidator


class VacantBuildingsValidator(SchemaDriftValidator):
    """Validator for Vacant Buildings dataset schema drift.

    Note: This validator is optional as the underlying data is known to be incorrect
    and is being fixed. Use with caution.
    """

    def __init__(self):
        super().__init__(size_tolerance=0.05)  # 5% tolerance
        self.is_optional = True  # Mark as optional due to known data issues

    @property
    def expected_columns(self) -> Set[str]:
        return {
            "OBJECTID",
            "ADDRESS",
            "OWNER1",
            "OWNER2",
            "BLDG_DESC",
            "OPA_ID",
            "LNIADDRESSKEY",
            "COUNCILDISTRICT",
            "ZONINGBASEDISTRICT",
            "ZIPCODE",
            "BUILD_RANK",
            "DATE_UPDATE",
            "Shape__Area",
            "Shape__Length",
        }

    @property
    def required_non_null(self) -> Set[str]:
        return {
            "OBJECTID",  # 100% required
            "ADDRESS",  # 100% required
            "OWNER1",  # 100% required
            "BLDG_DESC",  # 100% required
            "OPA_ID",  # 100% required
            "LNIADDRESSKEY",  # 100% required
            "COUNCILDISTRICT",  # 100% required
            "ZONINGBASEDISTRICT",  # 100% required
            "ZIPCODE",  # 100% required
            "BUILD_RANK",  # 100% required
            "DATE_UPDATE",  # 100% required
            "Shape__Area",  # 100% required
            "Shape__Length",  # 100% required
        }

    @property
    def expected_record_count(self) -> Optional[int]:
        return 7_577
