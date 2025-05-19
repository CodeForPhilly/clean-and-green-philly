from typing import Optional, Set

from .schema_drift_validator import SchemaDriftValidator


class CensusBGsValidator(SchemaDriftValidator):
    """Validator for Census Block Groups dataset schema drift"""

    def __init__(self):
        super().__init__(size_tolerance=0.01)  # 1% tolerance

    @property
    def expected_columns(self) -> Set[str]:
        return {
            "OBJECTID",
            "STATEFP10",
            "COUNTYFP10",
            "TRACTCE10",
            "BLKGRPCE10",
            "GEOID10",
            "NAMELSAD10",
            "MTFCC10",
            "FUNCSTAT10",
            "ALAND10",
            "AWATER10",
            "INTPTLAT10",
            "INTPTLON10",
            "Shape__Area",
            "Shape__Length",
            "geometry",
        }

    @property
    def required_non_null(self) -> Set[str]:
        return {
            "OBJECTID",
            "STATEFP10",
            "COUNTYFP10",
            "TRACTCE10",
            "BLKGRPCE10",
            "GEOID10",
            "NAMELSAD10",
            "MTFCC10",
            "FUNCSTAT10",
            "ALAND10",
            "AWATER10",
            "INTPTLAT10",
            "INTPTLON10",
            "Shape__Area",
            "Shape__Length",
            "geometry",
        }

    @property
    def expected_record_count(self) -> Optional[int]:
        return 1_500
