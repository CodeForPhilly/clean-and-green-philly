from typing import Optional, Set

from .schema_drift_validator import SchemaDriftValidator


class OPAPropertiesValidator(SchemaDriftValidator):
    """Validator for OPA Properties dataset schema drift"""

    def __init__(self):
        super().__init__(size_tolerance=0.05)  # 5% tolerance

    @property
    def expected_columns(self) -> Set[str]:
        return {
            "building_code_description",
            "market_value",
            "sale_date",
            "sale_price",
            "parcel_number",
            "owner_1",
            "owner_2",
            "mailing_address_1",
            "mailing_address_2",
            "mailing_care_of",
            "mailing_street",
            "mailing_zip",
            "mailing_city_state",
            "zip_code",
            "zoning",
            "the_geom",
        }

    @property
    def required_non_null(self) -> Set[str]:
        return {
            "market_value",  # 100% required
            "parcel_number",  # 100% required
            "owner_1",  # 100% required
            "zip_code",  # 100% required
            "the_geom",  # 100% required
        }

    @property
    def expected_record_count(self) -> Optional[int]:
        return 582_781
