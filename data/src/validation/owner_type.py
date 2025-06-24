import geopandas as gpd
from pandera.pandas import DataFrameModel, Field, DataFrameSchema, Column, Check
from pandera.typing import Series

from .base import BaseValidator, no_na_check


# class OwnerTypeOutputSchema(DataFrameModel):
#     owner_type: Series[Literal["Individual", "Business (LLC)", "Public"]] = Field(
#         checks=[no_na_check]
#     )


output_schema = DataFrameSchema(
    {
        "owner_type": Column(
            str,
            checks=[
                Check.isin(["Individual", "Business (LLC)", "Public"]),
                no_na_check,
            ],
        )
    }
)


class OwnerTypeOutputValidator(BaseValidator):
    """Validator for owner type service output."""

    schema = output_schema

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass
