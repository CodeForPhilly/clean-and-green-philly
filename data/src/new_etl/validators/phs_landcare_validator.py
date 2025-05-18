from typing import Optional, Set

from .schema_drift_validator import SchemaDriftValidator


class PHSLandcareValidator(SchemaDriftValidator):
    """Validator for PHS Landcare dataset schema drift"""

    def __init__(self):
        super().__init__(size_tolerance=0.05)  # 5% tolerance

    @property
    def expected_columns(self) -> Set[str]:
        return {
            "address",
            "addr_range",
            "zipcode",
            "district",
            "year",
            "season",
            "program",
            "comm_ptnr",
            "fmr_prgm",
            "stabilized",
            "numparcels",
            "parcelarea",
            "objectid",
            "Shape__Area",
            "Shape__Length",
        }

    @property
    def required_non_null(self) -> Set[str]:
        return {
            "address",  # 100% required
            "addr_range",  # 100% required
            "zipcode",  # 100% required
            "district",  # 100% required
            "year",  # 100% required
            "season",  # 100% required
            "program",  # 100% required
            "comm_ptnr",  # 100% required
            "fmr_prgm",  # 100% required
            "stabilized",  # 100% required
            "numparcels",  # 100% required
            "parcelarea",  # 100% required
            "objectid",  # 100% required
            "Shape__Area",  # 100% required
            "Shape__Length",  # 100% required
        }

    @property
    def expected_record_count(self) -> Optional[int]:
        return 9_442
