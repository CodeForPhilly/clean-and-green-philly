from typing import Optional, Set

from .schema_drift_validator import SchemaDriftValidator


class CrimeIncidentsValidator(SchemaDriftValidator):
    """Validator for Crime Incidents dataset schema drift"""

    def __init__(self):
        super().__init__(size_tolerance=0.20)  # 20% tolerance

    @property
    def expected_columns(self) -> Set[str]:
        return {
            "text_general_code",
            "dispatch_date",
            "point_x",
            "point_y",
        }

    @property
    def required_non_null(self) -> Set[str]:
        return {
            "text_general_code",  # 100% required
            "dispatch_date",  # 100% required
        }

    @property
    def expected_record_count(self) -> Optional[int]:
        return 3_387_139
