from typing import Optional, Set

from .schema_drift_validator import SchemaDriftValidator


class PWDParcelsValidator(SchemaDriftValidator):
    """Validator for PWD Parcels dataset schema drift"""

    def __init__(self):
        super().__init__(size_tolerance=0.05)  # 5% tolerance

    @property
    def expected_columns(self) -> Set[str]:
        return {
            "address",
            "owner",
            "building_code",
            "building_description",
            "gross_area",
            "the_geom",
        }

    @property
    def required_non_null(self) -> Set[str]:
        return {
            "gross_area",  # 100% required
            "the_geom",  # 100% required
        }

    @property
    def expected_record_count(self) -> Optional[int]:
        return 547_351
