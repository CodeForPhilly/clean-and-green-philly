from typing import Optional, Set

from .schema_drift_validator import SchemaDriftValidator


class PPRPropertiesValidator(SchemaDriftValidator):
    """Validator for PPR Properties dataset schema drift"""

    def __init__(self):
        super().__init__(size_tolerance=0.05)  # 5% tolerance

    @property
    def expected_columns(self) -> Set[str]:
        return {
            "OBJECTID",
            "PUBLIC_NAME",
            "PARENT_NAME",
            "NESTED",
            "OFFICIAL_NAME",
            "LABEL",
            "ALIAS",
            "DPP_ASSET_ID",
            "ADDRESS_911",
            "ZIP_CODE",
            "ADDRESS_BRT",
            "ALIAS_ADDRESS",
            "ACREAGE",
            "PROPERTY_CLASSIFICATION",
            "PPR_USE",
            "PPR_PROG_DISTRICT",
            "PPR_OPS_DISTRICT",
            "COUNCIL_DISTRICT",
            "POLICE_DISTRICT",
            "CITY_SCALE_MAPS",
            "LOCAL_SCALE_MAPS",
            "PROGRAM_SITES",
            "COMMENTS",
            "Shape__Area",
            "Shape__Length",
        }

    @property
    def required_non_null(self) -> Set[str]:
        return {
            "OBJECTID",  # 100% required
            "PUBLIC_NAME",  # 100% required
            "PARENT_NAME",  # 100% required
            "NESTED",  # 100% required
            "LABEL",  # 100% required
            "DPP_ASSET_ID",  # 100% required
            "ADDRESS_911",  # 100% required
            "ZIP_CODE",  # 100% required
            "ADDRESS_BRT",  # 100% required
            "ALIAS_ADDRESS",  # 100% required
            "ACREAGE",  # 100% required
            "PROPERTY_CLASSIFICATION",  # 100% required
            "PPR_USE",  # 100% required
            "PPR_PROG_DISTRICT",  # 100% required
            "PPR_OPS_DISTRICT",  # 100% required
            "COUNCIL_DISTRICT",  # 100% required
            "POLICE_DISTRICT",  # 100% required
            "CITY_SCALE_MAPS",  # 100% required
            "LOCAL_SCALE_MAPS",  # 100% required
            "PROGRAM_SITES",  # 100% required
            "Shape__Area",  # 100% required
            "Shape__Length",  # 100% required
        }

    @property
    def expected_record_count(self) -> Optional[int]:
        return 507
