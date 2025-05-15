from functools import wraps

import pandas as pd
import pandera as pa
from pandera.typing import Series

from .base import BaseValidator


class VacantPropertiesValidator(BaseValidator):
    vacant: Series[bool] = pa.Field(nullable=False)
    opa_id: Series[str] = pa.Field(nullable=False, unique=True)
    owner_1: Series[str] = pa.Field(nullable=True)
    owner_2: Series[str] = pa.Field(nullable=True)

    @pa.check("opa_id")
    def check_duplicates(cls, series: Series) -> Series:
        return ~series.duplicated()

    @classmethod
    def validate_owner_nulls(cls, df: pd.DataFrame, threshold: float = 0.01) -> None:
        """
        Checks if more than the threshold of properties have both owner_1 and owner_2 as null.
        Having one owner null but not the other is acceptable.

        Args:
            df (pd.DataFrame): The DataFrame to check for owner nulls.
            threshold (float): The threshold for acceptable percentage of both owners being null (default is 1%).

        Raises:
            ValueError: If more than threshold of properties have both owners null.
        """
        both_owners_null = df["owner_1"].isnull() & df["owner_2"].isnull()
        pct_both_null = both_owners_null.mean()

        if pct_both_null > threshold:
            raise ValueError(
                f"More than {threshold * 100}% of properties ({pct_both_null * 100:.1f}%) "
                "have both owner_1 and owner_2 as null."
            )

    @classmethod
    def validate_output(cls, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            # Run schema validation
            cls.validate(result.gdf)
            # Run owner null validation
            cls.validate_owner_nulls(result.gdf)
            return result

        return wrapper
