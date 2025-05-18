from typing import Optional, Set

from .schema_drift_validator import SchemaDriftValidator


class DORParcelsValidator(SchemaDriftValidator):
    """Validator for DOR Parcels dataset schema drift"""

    @property
    def expected_columns(self) -> Set[str]:
        return {
            "OBJECTID",
            "RECSUB",
            "BASEREG",
            "MAPREG",
            "PARCEL",
            "RECMAP",
            "STCOD",
            "HOUSE",
            "SUF",
            "UNIT",
            "STEX",
            "STDIR",
            "STNAM",
            "STDESSUF",
            "ELEV_FLAG",
            "TOPELEV",
            "BOTELEV",
            "CONDOFLAG",
            "MATCHFLAG",
            "INACTDATE",
            "ORIG_DATE",
            "STATUS",
            "GEOID",
            "STDES",
            "ADDR_SOURCE",
            "ADDR_STD",
            "PIN",
            "Shape__Area",
            "Shape__Length",
            "geometry",
        }

    @property
    def required_non_null(self) -> Set[str]:
        return {
            "OBJECTID",
            "BASEREG",
            "MAPREG",
            "PARCEL",
            "RECMAP",
            "STCOD",
            "STNAM",
            "ELEV_FLAG",
            "TOPELEV",
            "BOTELEV",
            "CONDOFLAG",
            "MATCHFLAG",
            "INACTDATE",
            "ORIG_DATE",
            "STATUS",
            "STDES",
            "ADDR_SOURCE",
            "ADDR_STD",
            "PIN",
            "Shape__Area",
            "Shape__Length",
            "geometry",
        }

    @property
    def expected_record_count(self) -> Optional[int]:
        return 600_000
