from typing import Optional, Set

from .schema_drift_validator import SchemaDriftValidator


class CouncilDistrictsValidator(SchemaDriftValidator):
    """Validator for Council Districts dataset schema drift"""

    def __init__(self):
        super().__init__(size_tolerance=0.00)  # 0% tolerance - must be exact

    @property
    def expected_columns(self) -> Set[str]:
        return {
            "OBJECTID_1",
            "OBJECTID",
            "DISTRICT",
            "SHAPE_LENG",
            "Shape__Area",
            "Shape__Length",
        }

    @property
    def required_non_null(self) -> Set[str]:
        return {
            "OBJECTID_1",  # 100% required
            "OBJECTID",  # 100% required
            "DISTRICT",  # 100% required
            "SHAPE_LENG",  # 100% required
            "Shape__Area",  # 100% required
            "Shape__Length",  # 100% required
        }

    @property
    def expected_record_count(self) -> Optional[int]:
        return 10  # Must be exactly 10 districts
