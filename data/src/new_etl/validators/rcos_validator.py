from typing import Optional, Set

from .schema_drift_validator import SchemaDriftValidator


class RCOsValidator(SchemaDriftValidator):
    """Validator for Registered Community Organizations dataset schema drift"""

    def __init__(self):
        super().__init__(size_tolerance=0.05)  # 5% tolerance

    @property
    def expected_columns(self) -> Set[str]:
        return {
            "OBJECTID",
            "ORGANIZATION_NAME",
            "ORGANIZATION_ADDRESS",
            "MEETING_LOCATION_ADDRESS",
            "ORG_TYPE",
            "PREFFERED_CONTACT_METHOD",
            "PRIMARY_NAME",
            "PRIMARY_ADDRESS",
            "PRIMARY_EMAIL",
            "PRIMARY_PHONE",
            "P_PHONE_EXT",
            "ALTERNATE_NAME",
            "ALTERNATE_ADDRESS",
            "ALTERNATE_EMAIL",
            "ALTERNATE_PHONE",
            "A_PHONE_EXT",
            "EXPIRATIONYEAR",
            "EFFECTIVE_DATE",
            "LNI_ID",
            "Shape__Area",
            "Shape__Length",
        }

    @property
    def required_non_null(self) -> Set[str]:
        return {
            "OBJECTID",  # 100% required
            "ORGANIZATION_NAME",  # 100% required
            "ORGANIZATION_ADDRESS",  # 100% required
            "MEETING_LOCATION_ADDRESS",  # 100% required
            "ORG_TYPE",  # 100% required
            "PREFFERED_CONTACT_METHOD",  # 100% required
            "PRIMARY_NAME",  # 100% required
            "PRIMARY_ADDRESS",  # 100% required
            "PRIMARY_EMAIL",  # 100% required
            "ALTERNATE_NAME",  # 100% required
            "ALTERNATE_ADDRESS",  # 100% required
            "ALTERNATE_EMAIL",  # 100% required
            "EXPIRATIONYEAR",  # 100% required
            "EFFECTIVE_DATE",  # 100% required
            "LNI_ID",  # 100% required
            "Shape__Area",  # 100% required
            "Shape__Length",  # 100% required
        }

    @property
    def expected_record_count(self) -> Optional[int]:
        return 257
