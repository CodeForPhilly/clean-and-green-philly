import geopandas as gpd
import pandera.pandas as pa
from typing import Optional, Literal
from .base import BaseValidator


class CityOwnedPropertiesSchema(pa.DataFrameModel):
    '''
    Used for schema checks to ensure expected columns
    are present with the correct types.

    `Optional` typing means null values are allowed.
    '''
    pin: Optional[pa.typing.Series[int]]
    mapreg_1: pa.typing.Series[str]
    agency: pa.typing.Series[str]
    opabrt: Optional[pa.typing.Series[str]]
    location: pa.typing.Series[str]
    status_1: pa.typing.Series[str]
    councildistrict: pa.typing.Series[int]
    sideyardeligible: pa.typing.Series[Literal["Yes", "No"]]
    zoning: pa.typing.Series[str]
    objectid: pa.typing.Series[int]
    Shape__Area: pa.typing.Series[float]
    Shape__Length: pa.typing.Series[float]

    class Config:
        strict = True   # Columns must match exactly


class CityOwnedPropertiesInputValidator(BaseValidator):
    """Validator for access city owned properties service input."""

    schema = None

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass


class CityOwnedPropertiesOutputValidator(BaseValidator):
    '''
    Validator for the city-owned properties dataset output.
    _custom_validation() is called by validate() in the parent class.
    '''

    schema = CityOwnedPropertiesSchema

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        # Row count check: expect approx. 7,796 plus/minus 20%
        expected = 7796
        lower = int(expected * 0.8)
        upper = int(expected * 1.2)
        if not lower <= len(gdf) <= upper:
            self.errors.append(
                f"Expected ~7,796 records ±20%, but got {len(gdf)}"
            )

        # Check status_1 and agency are strings
        if not gdf["status_1"].apply(lambda x: isinstance(x, str)).all():
            self.errors.append("Some values in 'status_1' are not strings.")

        if not gdf["agency"].apply(lambda x: isinstance(x, str)).all():
            self.errors.append("Some values in 'agency' are not strings.")

        # Check sideyardeligible values are "Yes" or "No"
        allowed = {"Yes", "No"}
        actual = set(gdf["sideyardeligible"].dropna().unique())
        if not actual.issubset(allowed):
            self.errors.append(
                f"'sideyardeligible' column must contain only 'Yes' or 'No', but got: {actual}"
            )

        # Check that non-null opabrt values are non-empty strings
        if not gdf["opabrt"].dropna().apply(lambda x: isinstance(x, str) and x.strip() != "").all():
            self.errors.append(
                "Some non-null values in 'opabrt' are not valid non-empty strings."
            )
