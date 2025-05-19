import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, Set

import geopandas as gpd

logger = logging.getLogger(__name__)


@dataclass
class SchemaDriftCheck:
    """Results of a schema drift check"""

    missing_columns: Set[str]
    incomplete_columns: Set[str]
    record_count: int
    expected_count: Optional[int]
    size_drift: bool
    size_drift_percentage: Optional[float]


class SchemaDriftValidator(ABC):
    """Abstract base class for schema drift validation"""

    def __init__(self, size_tolerance: float = 0.1):
        """
        Initialize the validator with a size tolerance.

        Args:
            size_tolerance: Acceptable deviation from expected size (default 10%)
        """
        self.size_tolerance = size_tolerance

    @property
    @abstractmethod
    def expected_columns(self) -> Set[str]:
        """Columns that must be present in the dataset"""
        pass

    @property
    @abstractmethod
    def required_non_null(self) -> Set[str]:
        """Columns that must not contain null values"""
        pass

    @property
    @abstractmethod
    def expected_record_count(self) -> Optional[int]:
        """Expected number of records in the dataset"""
        pass

    def validate(self, gdf: gpd.GeoDataFrame) -> SchemaDriftCheck:
        """
        Check for schema drift in the dataset.

        Args:
            gdf: GeoDataFrame to validate

        Returns:
            SchemaDriftCheck with validation results
        """
        # Check for missing columns
        missing_cols = self.expected_columns - set(gdf.columns)

        # Check for incomplete required columns
        incomplete_cols = {
            col
            for col in self.required_non_null
            if col in gdf.columns and gdf[col].isnull().any()
        }

        # Check record count
        record_count = len(gdf)
        expected_count = self.expected_record_count

        # Calculate size drift if we have an expected count
        size_drift = False
        size_drift_percentage = None

        if expected_count is not None:
            size_drift_percentage = abs(record_count - expected_count) / expected_count
            size_drift = size_drift_percentage > self.size_tolerance

        return SchemaDriftCheck(
            missing_columns=missing_cols,
            incomplete_columns=incomplete_cols,
            record_count=record_count,
            expected_count=expected_count,
            size_drift=size_drift,
            size_drift_percentage=size_drift_percentage,
        )

    def validate_and_raise(self, gdf: gpd.GeoDataFrame) -> None:
        """
        Validate the dataset and raise an exception if schema drift is detected.

        Args:
            gdf: GeoDataFrame to validate

        Raises:
            ValueError: If schema drift is detected
        """
        check = self.validate(gdf)

        # Build error message if any drift is detected
        error_parts = []

        if check.missing_columns:
            error_parts.append(
                f"Missing columns: {', '.join(sorted(check.missing_columns))}"
            )

        if check.incomplete_columns:
            error_parts.append(
                f"Incomplete (null values present) columns: {', '.join(sorted(check.incomplete_columns))}"
            )

        if check.size_drift:
            error_parts.append(
                f"Size drift detected: got {check.record_count} records, "
                f"expected {check.expected_count} (±{check.size_drift_percentage:.1%})"
            )

        if error_parts:
            error_msg = "Schema drift detected:\n" + "\n".join(
                f"- {part}" for part in error_parts
            )
            logger.error(error_msg)
            raise ValueError(error_msg)

        logger.info(
            f"Schema validation passed: {check.record_count} records, "
            f"all expected columns present and complete"
        )
