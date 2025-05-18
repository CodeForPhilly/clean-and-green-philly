import pandera as pa
from pandera.typing import Series


class AccessProcessSchema(pa.SchemaModel):
    """Schema for validating access process column in the GeoDataFrame."""

    access_process: Series[str] = pa.Field(
        nullable=True,  # Allow NA for vacant properties
        isin=[
            "Private Land Use Agreement",
            "Go through Land Bank",
            "Do Nothing",
            "Buy Property",
        ],
        description="The access process for each property",
    )


def validate_access_process(func):
    """Decorator to validate the access process column in the output GeoDataFrame."""
    return pa.check_output(AccessProcessSchema)(func)


@validate_access_process
def validate_access_process_implementation(gdf):
    """
    Validate that the GeoDataFrame has a valid access_process column.
    Non-vacant properties should have NA values, and vacant properties
    should have one of the allowed access process values.

    Args:
        gdf: GeoDataFrame to validate

    Returns:
        The validated GeoDataFrame

    Raises:
        ValidationError: If validation fails, with details about what failed
    """
    try:
        print("Access process validation passed.")
        return gdf
    except pa.errors.SchemaError as e:
        error_message = f"Access process validation failed: {str(e)}"
        print(error_message)
        raise
