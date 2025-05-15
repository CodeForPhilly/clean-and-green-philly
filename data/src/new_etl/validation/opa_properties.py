from functools import wraps

import pandas as pd
import pandera as pa
from pandera.typing import Series

from .base import BaseValidator


class OPAPropertiesValidator(BaseValidator):
    """Validator for OPA properties data."""

    class Schema(pa.DataFrameModel):
        """Schema for OPA properties data."""

        opa_id: Series[str] = pa.Field(nullable=False)
        market_value: Series[float] = pa.Field(nullable=False)
        sale_date: Series[str] = pa.Field(nullable=False)
        sale_price: Series[float] = pa.Field(nullable=False)
        parcel_type: Series[str] = pa.Field(nullable=False)
        zip_code: Series[str] = pa.Field(nullable=False)
        zoning: Series[str] = pa.Field(nullable=False)
        owner_1: Series[str] = pa.Field(nullable=False)
        owner_2: Series[str] = pa.Field(nullable=False)
        building_code_description: Series[str] = pa.Field(nullable=False)
        standardized_mailing_address: Series[str] = pa.Field(nullable=False)

    @classmethod
    def validate_output(cls, func):
        """Validate the output of a function that returns a GeoDataFrame."""

        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if result is None:
                return None

            # Convert to DataFrame for validation
            df = pd.DataFrame(result.gdf)

            # Validate schema
            cls.Schema.validate(df)

            # Check minimum record count
            if len(df) < 580000:
                raise ValueError(
                    f"OPA properties data has fewer than 580,000 records: {len(df)}"
                )

            return result

        return wrapper
