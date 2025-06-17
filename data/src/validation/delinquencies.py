from typing import Literal
import geopandas as gpd
from pandas import Series
from pandera import DataFrameModel, Field

from .base import BaseValidator


class DelinquenciesInputValidator(BaseValidator):
    """Validator for delinquencies service input."""

    schema = None

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass


class DelinquenciesOutputSchema(DataFrameModel):
    total_due: Series[float | Literal["NA"]] = Field()
    most_recent_year_owed: Series[str] = Field()
    num_years_owed: Series[int] = Field()
    payment_agreement: Series[str] = Field()
    is_actionable: Series[str] = Field()
    sheriff_sale: Series[str] = Field()
    total_assessment: Series[float] = Field()


class DelinquenciesOutputValidator(BaseValidator):
    """Validator for delinquencies service output."""

    schema = DelinquenciesOutputSchema

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass
