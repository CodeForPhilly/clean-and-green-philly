import functools
import logging
import time
from abc import ABC
from typing import Callable, List

import geopandas as gpd
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

    schema: pa.DataSchemaModel = None

    def __init_subclass__(cls):
        schema = getattr(cls, "schema", None)
        if schema is not None and (
            not isinstance(schema, type) or not isinstance(schema, pa.DataFrameModel)
        ):
            raise TypeError(
                f"{cls.__name__} must define a 'schema' class variable that is a subclass of pandera.SchemaModel."
            )
        return super().__init_subclass__()

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

        # Step 1: Get Philadelphia's bounding box
        phl_start = time.time()
        phl_bounds = PHL_GEOMETRY.bounds  # (minx, miny, maxx, maxy)
        time.time() - phl_start

        # Step 2: Get all geometry bounding boxes at once
        bbox_start = time.time()
        geometry_bounds = (
            gdf.geometry.bounds
        )  # DataFrame with minx, miny, maxx, maxy for each geometry
        time.time() - bbox_start

        # Step 3: Create three categories using coordinate logic
        category_start = time.time()

        # Category 1 - Definitely Outside: No overlap with Philadelphia's bounding box
        definitely_outside = (
            (geometry_bounds["maxx"] < phl_bounds[0])  # entirely to the left
            | (geometry_bounds["minx"] > phl_bounds[2])  # entirely to the right
            | (geometry_bounds["maxy"] < phl_bounds[1])  # entirely below
            | (geometry_bounds["miny"] > phl_bounds[3])  # entirely above
        )

        # Category 2 - Definitely Inside: Completely contained within Philadelphia's bounding box
        definitely_inside = (
            (
                geometry_bounds["minx"] >= phl_bounds[0]
            )  # left edge inside or on boundary
            & (
                geometry_bounds["maxx"] <= phl_bounds[2]
            )  # right edge inside or on boundary
            & (
                geometry_bounds["miny"] >= phl_bounds[1]
            )  # bottom edge inside or on boundary
            & (
                geometry_bounds["maxy"] <= phl_bounds[3]
            )  # top edge inside or on boundary
        )

        # Category 3 - Boundary Cases: Everything else (overlaps but extends beyond)
        boundary_cases = ~(definitely_outside | definitely_inside)

        time.time() - category_start

        # Print category statistics
        cat1_count = definitely_outside.sum()
        cat2_count = definitely_inside.sum()
        cat3_count = boundary_cases.sum()

        # Step 4: Apply validation logic
        validation_start = time.time()

        # Mark Category 1 as invalid (outside Philadelphia)
        if cat1_count > 0:
            outside_phl = True
        else:
            # Only run expensive intersection test on Category 3 geometries
            if cat3_count > 0:
                boundary_gdf = gdf[boundary_cases]
                boundary_outside = (
                    ~boundary_gdf.geometry.intersects(PHL_GEOMETRY)
                ).any()
                outside_phl = boundary_outside
            else:
                outside_phl = False

        time.time() - validation_start

        total_time = time.time() - phl_start
        print(
            f"    [GEOMETRY] {total_time:.3f}s ({cat1_count} outside, {cat2_count} inside, {cat3_count} boundary)"
        )

        if not correct_crs:
            self.errors.append(
                f"Geodataframe for {self.__class__.__name__} is not using the correct coordinate system pegged to Philadelphia"
            )

        if outside_phl:
            self.errors.append(
                f"Dataframe for {self.__class__.__name__} contains observations outside Philadelphia limits."
            )

    def opa_validation(self, gdf: gpd.GeoDataFrame):
        """
        Validate the opa_id column in a geodataframe if it exists, including checks for string types and uniqueness

        Args:
            gdf (GeoDataFrame): The GeoDataFrame input to validate.

        Appends errors to the class instance errors
        """
        if "opa_id" in gdf.columns:
            opa_validation_start = time.time()

            # Profile the expensive .apply() call
            opa_string_start = time.time()
            opa_string = gdf["opa_id"].apply(lambda x: isinstance(x, str)).all()
            opa_string_time = time.time() - opa_string_start

            if not opa_string:
                self.errors.append(
                    f"OPA ids are not all typed as strings for {self.__class__.__name__}"
                )

            # Profile the uniqueness check
            unique_start = time.time()
            unique_opa = gdf["opa_id"].is_unique
            unique_time = time.time() - unique_start

            if not unique_opa:
                self.errors.append(
                    f"OPA ids contain some duplicates for {self.__class__.__name__}"
                )

            total_opa_time = time.time() - opa_validation_start
            print(
                f"    [OPA] {total_opa_time:.3f}s (string check: {opa_string_time:.3f}s, uniqueness: {unique_time:.3f}s)"
            )

    def validate(self, gdf: gpd.GeoDataFrame) -> ValidationResult:
        """
        Validate the data after a service runs.

        Args:
            gdf: The GeoDataFrame to validate

        Returns:
            ValidationResult: A boolean success together with a list of collected errors from validation
        """
        validate_start = time.time()

        # Geometry validation
        geometry_start = time.time()
        self.geometry_validation(gdf)
        geometry_time = time.time() - geometry_start

        # OPA validation
        opa_start = time.time()
        self.opa_validation(gdf)
        opa_time = time.time() - opa_start

        # Schema validation
        schema_start = time.time()
        if self.schema:
            try:
                self.schema.validate(gdf, lazy_validation=True)
            except pa.errors.SchemaErrors as err:
                self.errors.append(err.failure_case)
        schema_time = time.time() - schema_start

        # Custom validation
        custom_start = time.time()
        self._custom_validation(gdf)
        custom_time = time.time() - custom_start

        total_validate_time = time.time() - validate_start
        print(
            f"  [VALIDATE] {total_validate_time:.3f}s (geometry: {geometry_time:.3f}s, opa: {opa_time:.3f}s, schema: {schema_time:.3f}s, custom: {custom_time:.3f}s)"
        )

        return ValidationResult(success=not self.errors, errors=self.errors)

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass


def validate_output(
    validator_cls: BaseValidator,
):
    def decorator(func: Callable[[gpd.GeoDataFrame], gpd.GeoDataFrame]):
        @functools.wraps(func)
        def wrapper(gdf: gpd.GeoDataFrame = None, *args, **kwargs):
            decorator_start = time.time()

            # Create validator
            validator_create_start = time.time()
            validator = validator_cls()
            time.time() - validator_create_start

            # Call the original function
            func_call_start = time.time()
            output_gdf, input_validation = func(gdf, *args, **kwargs)
            func_call_time = time.time() - func_call_start

            # Perform output validation
            output_validation_start = time.time()
            output_validation = validator.validate(output_gdf)
            output_validation_time = time.time() - output_validation_start

            # Create complete validation result
            validation_merge_start = time.time()
            complete_validation = {}
            complete_validation["input"] = input_validation
            complete_validation["output"] = output_validation
            time.time() - validation_merge_start

            decorator_total_time = time.time() - decorator_start
            print(
                f"[VALIDATOR] {decorator_total_time:.3f}s (function: {func_call_time:.3f}s, validation: {output_validation_time:.3f}s)"
            )

            return output_gdf, complete_validation

        return wrapper

    return decorator
