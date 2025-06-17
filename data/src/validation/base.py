from dataclasses import dataclass
import functools
import logging
from abc import ABC
from typing import Callable, List, Optional

import geopandas as gpd
from pandera import Check
import pandera.pandas as pa

from src.config.config import USE_CRS
from src.constants.city_limits import PHL_GEOMETRY


class ValidationResult:
    def __init__(self, success: bool, errors: List[str] = []):
        self.success = success
        self.errors = errors

    def __bool__(self):
        return self.success


class BaseValidator(ABC):
    """Base class for service-specific data validation."""

    schema: pa.DataFrameModel = None

    def __init_subclass__(cls):
        return super().__init_subclass__()
        if not isinstance(getattr(cls, "schema", None), type) or not isinstance(
            cls.schema, pa.DataFrameModel
        ):
            raise TypeError(
                f"{cls.__name__} must define a 'schema' class variable that is a subclass of pandera.SchemaModel."
            )

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.errors = []

    def geometry_validation(self, gdf: gpd.GeoDataFrame):
        """
        Validate the geometry column in a geodataframe if it exists, including checks for coordinate system and
        location being with Philadelphi city bounds.

        Args:
            gdf (GeoDataFrame): The GeoDataFrame input to validate.

        Appends errors to the class instance errors
        """
        correct_crs = gdf.crs == USE_CRS
        within_phl = gdf.geometry.within(PHL_GEOMETRY).all()

        if not correct_crs:
            self.errors.append(
                f"Geodataframe for {self.__class__.__name__} is not using the correct coordinate system pegged to Philadelphia"
            )

        if not within_phl:
            self.errors.append(
                f"Dataframe for {self.__class__.__name__} not contained within Philadelphia limits."
            )

    def opa_validation(self, gdf: gpd.GeoDataFrame):
        """
        Validate the opa_id column in a geodataframe if it exists, including checks for string types and uniqueness

        Args:
            gdf (GeoDataFrame): The GeoDataFrame input to validate.

        Appends errors to the class instance errors
        """
        if "opa_id" in gdf.columns:
            opa_string = gdf["opa_id"].apply(lambda x: isinstance(x, str)).all()
            if not opa_string:
                self.errors.append(
                    f"OPA ids are not all typed as strings for {self.__class__.__name__}"
                )

            unique_opa = gdf["opa_id"].is_unique
            if not unique_opa:
                self.errors.append(
                    f"OPA ids contain some duplicates for {self.__class__.__name__}"
                )

    def validate(self, gdf: gpd.GeoDataFrame) -> ValidationResult:
        """
        Validate the data after a service runs.

        Args:
            gdf: The GeoDataFrame to validate

        Returns:
            ValidationResult: A boolean success together with a list of collected errors from validation
        """
        self.geometry_validation(gdf)
        self.opa_validation(gdf)
        if self.schema:
            try:
                self.schema.validate(gdf, lazy_validation=True)
            except pa.errors.SchemaErrors as err:
                self.errors.append(err.failure_case)
        self._custom_validation(gdf)

        return ValidationResult(success=not self.errors, errors=self.errors)

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass


def validate_output(
    validator_cls: BaseValidator,
):
    def decorator(func: Callable[[gpd.GeoDataFrame], gpd.GeoDataFrame]):
        @functools.wraps(func)
        def wrapper(gdf: gpd.GeoDataFrame = None, *args, **kwargs):
            validator = validator_cls()
            output_gdf, input_validation = func(gdf, *args, **kwargs)
            output_validation = validator.validate(output_gdf)

            complete_validation = {}
            complete_validation["input"] = input_validation
            complete_validation["output"] = output_validation

            return output_gdf, complete_validation

        return wrapper

    return decorator


no_na_check = Check.ne("NA", error="Value cannot be NA")

unique_check = Check(lambda s: s.is_unique, error="Should have all unique values")


def unique_value_check(lower: int, upper: int) -> Check:
    return Check(
        lambda s: s.nunique() >= lower and s.unique < upper,
        f"Number of unique values is roughly between {lower} and {upper}",
    )


def null_percentage_check(null_percent: float) -> Check:
    return Check(
        lambda s: s.isnull().mean() >= 0.8 * null_percent
        and s.isnull().mean() <= 1.2 * null_percent,
        error=f"Percentage of nulls in column should be roughly {null_percent}",
    )


@dataclass
class DistributionParams:
    min_value: Optional[int | float]
    max_value: Optional[int | float]
    mean: Optional[int | float]
    median: Optional[int | float]
    std: Optional[int | float]
    q1: Optional[int | float]
    q3: Optional[int | float]


def distribution_check(params: DistributionParams) -> List[Check]:
    res = []

    if params.min_value:
        res.append(Check.ge(params.min_value))
    if params.max_value:
        res.append(Check.le(params.max_value))
    if params.mean:
        res.append(
            Check(
                lambda s: s.mean() >= 0.8 * params.mean
                and s.mean() <= 1.2 * params.mean,
                error=f"Column mean should be roughly {params.mean}",
            )
        )
    if params.median:
        res.append(
            Check(
                lambda s: s.quantile(0.5) >= 0.8 * params.median
                and s.quantile(0.5) <= 1.2 * params.median,
                error=f"Column median should be roughly {params.median}",
            )
        )
    if params.std:
        res.append(
            Check(
                lambda s: s.std() >= 0.8 * params.std and s.std() <= 1.2 * params.std,
                error=f"Column standard deviation should be roughly {params.std}",
            )
        )
    if params.q1:
        res.append(
            Check(
                lambda s: s.quantile(0.25) >= 0.8 * params.q1
                and s.quantile(0.25) <= 1.2 * params.q1,
                error=f"Column first quantile should be roughly {params.q1}",
            )
        )
    if params.q3:
        res.append(
            Check(
                lambda s: s.quantile(0.75) >= 0.8 * params.q3
                and s.quantile(0.75) <= 1.2 * params.q3,
                error=f"Column third quantile should be roughly {params.q3}",
            )
        )

    return res
