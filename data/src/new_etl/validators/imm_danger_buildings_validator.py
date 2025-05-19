from typing import Optional, Set

from .schema_drift_validator import SchemaDriftValidator


class ImmDangerBuildingsValidator(SchemaDriftValidator):
    """Validator for Imminently Dangerous Buildings dataset schema drift"""

    def __init__(self):
        super().__init__(size_tolerance=0.10)  # 10% tolerance

    @property
    def expected_columns(self) -> Set[str]:
        return {
            "address",
            "violation_date",
            "opa_account_num",
            "owner",
            "the_geom",
        }

    @property
    def required_non_null(self) -> Set[str]:
        return {
            "address",  # 100% required
            "violation_date",  # 100% required
            "the_geom",  # 100% required
        }

    @property
    def expected_record_count(self) -> Optional[int]:
        return 186
