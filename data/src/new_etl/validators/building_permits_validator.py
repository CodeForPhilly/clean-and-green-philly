from typing import Optional, Set

from .schema_drift_validator import SchemaDriftValidator


class BuildingPermitsValidator(SchemaDriftValidator):
    """Validator for Building Permits dataset schema drift"""

    def __init__(self):
        super().__init__(size_tolerance=0.20)  # 20% tolerance

    @property
    def expected_columns(self) -> Set[str]:
        return {
            "address",
            "addressobjectid",
            "approvedscopeofwork",
            "commercialorresidential",
            "opa_account_num",
            "permittype",
            "status",
            "unit_num",
            "unit_type",
            "permitissuedate",
            "typeofwork",
            "the_geom",
            "the_geom_geojson",
        }

    @property
    def required_non_null(self) -> Set[str]:
        return {
            "permittype",  # 100% required
            "status",  # 100% required
            "permitissuedate",  # 100% required
            "the_geom",  # 100% required
            "the_geom_geojson",  # 100% required
        }

    @property
    def expected_record_count(self) -> Optional[int]:
        return 870_199
