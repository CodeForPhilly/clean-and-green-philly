import logging
from abc import ABC, abstractmethod
from typing import List, Optional, Tuple

import geopandas as gpd


class ServiceValidator(ABC):
    """Base class for service-specific data validation."""

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def validate(self, data: gpd.GeoDataFrame) -> Tuple[bool, List[str]]:
        """
        Validate the data after a service runs.

        Args:
            data: The GeoDataFrame to validate

        Returns:
            Tuple of (is_valid, list of error messages)
        """
        pass

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
