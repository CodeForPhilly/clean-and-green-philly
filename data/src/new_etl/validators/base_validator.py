from functools import wraps
from typing import Any, Callable, TypeVar

import geopandas as gpd
import pandera as pa
from pandera.typing import Series

# Define a type variable for the decorator
T = TypeVar("T")


class BaseValidator:
    """
    Base validator class that all feature layer validators should inherit from.
    Provides basic OPA ID validation that all feature layers must pass.
    """

    @staticmethod
    def validate(
        func: Callable[..., gpd.GeoDataFrame],
    ) -> Callable[..., gpd.GeoDataFrame]:
        """
        Base decorator to validate OPA ID constraints in GeoDataFrame output.

        This decorator ensures that:
        1. No OPA IDs are null
        2. No OPA IDs are duplicated

        Args:
            func: The function that returns a GeoDataFrame

        Returns:
            A wrapped function that validates the output GeoDataFrame
        """

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> gpd.GeoDataFrame:
            # Get the output GeoDataFrame
            result = func(*args, **kwargs)

            # Define the schema for validation
            class OpaIdSchema(pa.SchemaModel):
                opa_id: Series[str] = pa.Field(
                    nullable=False,
                    unique=True,
                    description="OPA ID must be present and unique",
                )

            # Validate the GeoDataFrame
            try:
                OpaIdSchema.validate(result)
                return result
            except pa.errors.SchemaError as e:
                raise ValueError(
                    f"Base validation failed for {func.__name__}: {str(e)}"
                )

        return wrapper
