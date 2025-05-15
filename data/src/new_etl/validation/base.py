import logging
from abc import ABC
from functools import wraps
from typing import Dict, List, Optional, Set, Tuple

import geopandas as gpd
import pandera as pa
from pandera.typing import Series
from shapely import is_valid

from ..classes.featurelayer import FeatureLayer
from ..constants.services import CITY_LIMITS_URL


class ServiceValidator(ABC):
    """Base class for service-specific data validation."""

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def validate(self, data: gpd.GeoDataFrame) -> Tuple[bool, List[str]]:
        """
        Validate the data after a service runs.
        This method runs common validation checks and then calls service-specific validation.

        Args:
            data: The GeoDataFrame to validate

        Returns:
            Tuple of (is_valid, list of error messages)
        """
        errors = []

        # Run common validation checks
        errors.extend(self._run_common_validation(data))

        # Run service-specific validation
        errors.extend(self._validate_service_specific(data))

        return len(errors) == 0, errors

    def _run_common_validation(self, data: gpd.GeoDataFrame) -> List[str]:
        """
        Run common validation checks that should be performed for all services.
        Currently checks for:
        - Required fields present (opa_id)
        - No duplicate OPA IDs
        - Valid geometries
        - Minimum record count (500,000)
        - Required input columns present
        - Required input values present

        Args:
            data: The GeoDataFrame to validate

        Returns:
            List of error messages
        """
        errors = []

        # Check required columns
        errors.extend(self.check_required_columns(data, ["opa_id"]))

        # Check for duplicate OPA IDs
        errors.extend(self.check_duplicates(data, "opa_id"))

        # Check data types
        if "opa_id" in data.columns and not data["opa_id"].dtype == "object":
            errors.append("opa_id must be string type")

        # Check null values in critical fields
        errors.extend(
            self.check_null_percentage(data, "opa_id", threshold=0.0)
        )  # No nulls allowed

        # Check geometry validity
        if not data.geometry.is_valid.all():
            errors.append("Found invalid geometries")

        # Check record counts
        errors.extend(self.check_count_threshold(data, min_count=500000))

        # Check required input columns
        required_inputs = self.get_required_input_columns()
        if required_inputs:
            missing_inputs = [col for col in required_inputs if col not in data.columns]
            if missing_inputs:
                errors.append(
                    f"Missing required input columns: {', '.join(missing_inputs)}"
                )

        # Check required input values
        required_values = self.get_required_input_values()
        if required_values:
            for column, valid_values in required_values.items():
                if column in data.columns:
                    invalid_values = set(data[column].unique()) - valid_values
                    if invalid_values:
                        errors.append(
                            f"Found invalid values in {column}: {', '.join(map(str, invalid_values))}"
                        )

        return errors

    def _validate_service_specific(self, data: gpd.GeoDataFrame) -> List[str]:
        """
        Run service-specific validation checks.
        This method can be overridden by service validators to add custom validation.

        Args:
            data: The GeoDataFrame to validate

        Returns:
            List of error messages
        """
        return []

    def get_required_input_columns(self) -> List[str]:
        """
        Get the list of required input columns for this service.
        This method can be overridden by service validators to specify required columns.

        Returns:
            List of required input column names
        """
        return []

    def get_required_input_values(self) -> Dict[str, Set]:
        """
        Get the dictionary of required input values for this service.
        This method can be overridden by service validators to specify valid values.

        Returns:
            Dictionary mapping column names to sets of valid values
        """
        return {}

    def check_required_columns(
        self, data: gpd.GeoDataFrame, required_columns: List[str]
    ) -> List[str]:
        """Check if all required columns are present."""
        missing_columns = [col for col in required_columns if col not in data.columns]
        if missing_columns:
            return [f"Missing required columns: {', '.join(missing_columns)}"]
        return []

    def check_null_percentage(
        self, data: gpd.GeoDataFrame, column: str, threshold: float = 0.1
    ) -> List[str]:
        """Check if null percentage in a column exceeds threshold."""
        null_pct = data[column].isna().mean()
        if null_pct > threshold:
            return [
                f"Column {column} has {null_pct:.1%} null values (threshold: {threshold:.1%})"
            ]
        return []

    def check_duplicates(self, data: gpd.GeoDataFrame, column: str) -> List[str]:
        """Check for duplicate values in a column."""
        duplicates = data[data[column].duplicated()]
        if not duplicates.empty:
            return [f"Found {len(duplicates)} duplicate values in column {column}"]
        return []

    def check_count_threshold(
        self, data: gpd.GeoDataFrame, min_count: int, max_count: Optional[int] = None
    ) -> List[str]:
        """
        Check if row count is within expected range.
        This is a utility method intended for use by validator subclasses.

        Args:
            data: The GeoDataFrame to check
            min_count: Minimum number of rows required
            max_count: Optional maximum number of rows allowed

        Returns:
            List of error messages if thresholds are exceeded
        """
        count = len(data)
        errors = []
        if count < min_count:
            errors.append(
                f"Row count ({count}) is below minimum threshold ({min_count})"
            )
        if max_count and count > max_count:
            errors.append(
                f"Row count ({count}) exceeds maximum threshold ({max_count})"
            )
        return errors


class BaseValidator(pa.DataFrameModel):
    # These checks should run on EVERY DataFrame
    opa_id: Series[str] = pa.Field(nullable=False, unique=True)

    @pa.check("opa_id")
    def check_duplicates(cls, series: Series) -> Series:
        return ~series.duplicated()

    @classmethod
    def validate_input(cls, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Get the DataFrame from the first argument
            first_arg = args[0]
            if isinstance(first_arg, FeatureLayer):
                df = first_arg.gdf
            else:
                df = first_arg
            # Run all validations
            cls.validate(df)
            return func(*args, **kwargs)

        return wrapper

    @classmethod
    def validate_output(cls, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            # Run all validations on the result
            if isinstance(result, FeatureLayer):
                df = result.gdf
            else:
                df = result
            cls.validate(df)
            return result

        return wrapper


class GeoValidator(BaseValidator):
    # These checks only run on GeoDataFrames
    geometry: Series = pa.Field()

    @pa.check("geometry")
    def validate_geometry(cls, series: Series) -> Series:
        return series.apply(lambda x: is_valid(x))

    @classmethod
    def validate_city_limits(cls, gdf: gpd.GeoDataFrame) -> bool:
        """
        Validate that all geometries are within Philadelphia city limits.

        Args:
            gdf: GeoDataFrame to validate

        Returns:
            bool: True if all geometries are within city limits, False otherwise
        """
        # Load city limits using FeatureLayer
        city_limits = FeatureLayer(
            name="City Limits",
            esri_rest_urls=[CITY_LIMITS_URL],
            skip_save=True,  # Don't save to PostgreSQL
        )

        if city_limits.gdf is None or len(city_limits.gdf) == 0:
            raise Exception("Failed to load city limits data")

        # Get the city limits geometry
        city_limits_geom = city_limits.gdf.geometry.iloc[0]

        # Check if all geometries are within city limits
        return all(city_limits_geom.contains(geom) for geom in gdf.geometry)
