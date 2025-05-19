from typing import Optional, Set

from .schema_drift_validator import SchemaDriftValidator


class NeighborhoodsValidator(SchemaDriftValidator):
    """Validator for Philadelphia Neighborhoods dataset schema drift"""

    def __init__(self):
        super().__init__(size_tolerance=0.01)  # 1% tolerance

    @property
    def expected_columns(self) -> Set[str]:
        return {
            "NAME",
            "LISTNAME",
            "MAPNAME",
            "Shape_Leng",
            "Shape_Area",
            "geometry",
        }

    @property
    def required_non_null(self) -> Set[str]:
        return {
            "NAME",
            "LISTNAME",
            "MAPNAME",
            "Shape_Leng",
            "Shape_Area",
            "geometry",
        }

    @property
    def expected_record_count(self) -> Optional[int]:
        return 158
