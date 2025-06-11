import functools
import logging
from abc import ABC
from typing import Callable, List

import geopandas as gpd
import pandera as pa

from src.config.config import USE_CRS

CITY_LIMITS = gpd.read_file("./constants/city_limits.geojson")
CITY_LIMITS.to_crs(USE_CRS)
PHL_GEOMETRY = CITY_LIMITS.geometry.iloc[0]


class ValidationResult:
    def __init__(self, success: bool, errors: List[str] = []):
        self.success = success
        self.errors = errors

    def __bool__(self):
        return self.success


class BaseValidator(ABC):
    """Base class for service-specific data validation."""

    schema: pa.SchemaModel = None

    def __init_subclass__(cls):
        return super().__init_subclass__()
        if not isinstance(getattr(cls, "schema", None), type) or not isinstance(
            cls.schema, pa.SchemaModel
        ):
            raise TypeError(
                f"{cls.__name__} must define a 'schema' class variable that is a subclass of pandera.SchemaModel."
            )

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.errors = []

    def geometry_validation(self, gdf: gpd.GeoDataFrame):
        correct_crs = gdf.crs == USE_CRS
        within_phl = gdf.geometry.within(PHL_GEOMETRY).all()

        if not correct_crs:
            self.errors.append(
                f"Geodataframe for {self.__name__} is not using the correct coordinate system pegged to Philadelphia"
            )

        if not within_phl:
            self.errors.append(
                f"Dataframe for {self.__name__} not contained within Philadelphia limits."
            )

    def opa_validation(self, gdf: gpd.GeoDataFrame):
        if "opa_id" in gdf.columns:
            opa_string = gdf["opa_id"].apply(lambda x: isinstance(x, str)).all()
            if not opa_string:
                self.errors.append(
                    f"OPA ids are not all typed as strings for {self.__name__}"
                )

            unique_opa = gdf["opa_id"].is_unique
            if not unique_opa:
                self.errors.append(
                    f"OPA ids contain some duplicates for {self.__name__}"
                )

    def validate(self, gdf: gpd.GeoDataFrame) -> ValidationResult:
        """
        Validate the data after a service runs.

        Args:
            data: The GeoDataFrame to validate

        Returns:
            Tuple of (is_valid, list of error messages)
        """
        self.geometry_validation(gdf)
        self.opa_validation(gdf)

        self._custom_validation(gdf)
        self.schema.validate(gdf)

        return ValidationResult(success=not self.errors, errors=self.errors)

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass

    # Validations
    # Duplicate opa_ids
    # Duplicate geometries
    # Invalid geometries
    # Required columns
    # Null percentage
    # Duplicate count
    # Row count


def validate_output(
    validator_cls: BaseValidator,
):
    def decorator(func: Callable[[gpd.GeoDataFrame], gpd.GeoDataFrame]):
        @functools.wraps(func)
        def wrapper(gdf: gpd.GeoDataFrame, *args, **kwargs):
            validator = validator_cls()
            output_gdf = func(gdf, *args, **kwargs)
            validation_result = validator.validate(output_gdf)
            return output_gdf, validation_result

        return wrapper

    return decorator
