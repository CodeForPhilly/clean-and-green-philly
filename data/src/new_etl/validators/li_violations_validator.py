from typing import Optional, Set

from .schema_drift_validator import SchemaDriftValidator


class LIViolationsValidator(SchemaDriftValidator):
    """Validator for L&I Violations dataset schema drift"""

    def __init__(self):
        super().__init__(size_tolerance=0.20)  # 20% tolerance

    @property
    def expected_columns(self) -> Set[str]:
        return {
            "parcel_id_num",
            "casenumber",
            "casecreateddate",
            "casetype",
            "casestatus",
            "violationnumber",
            "violationcodetitle",
            "violationstatus",
            "opa_account_num",
            "address",
            "opa_owner",
            "geocode_x",
            "geocode_y",
        }

    @property
    def required_non_null(self) -> Set[str]:
        return {
            "casenumber",  # 100% required
            "casecreateddate",  # 100% required
            "casetype",  # 100% required
            "casestatus",  # 100% required
            "violationnumber",  # 100% required
            "violationcodetitle",  # 100% required
            "violationstatus",  # 100% required
            "opa_account_num",  # 100% required
            "address",  # 99.98% required
            "opa_owner",  # 100% required
        }

    @property
    def expected_record_count(self) -> Optional[int]:
        return 54_401
