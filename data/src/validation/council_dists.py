import geopandas as gpd
import pandera.pandas as pa
import pandas as pd
from .base import BaseValidator

CouncilDistrictsInputSchema = pa.DataFrameSchema(
    columns={
        "district": pa.Column(
            str,
            nullable=True,
        ),
        "geometry": pa.Column("geometry"),
    },
    # district should contain 10 records of strings 1-10
    checks=pa.Check(
        lambda df: set(df["district"].dropna().unique())
        == {str(i) for i in range(1, 11)}
    ),
    strict=True,
)

CouncilDistrictsOutputSchema = pa.DataFrameSchema(
    columns={
        "opa_id": pa.Column(pa.String),
        "street_address": pa.Column(pa.String, nullable=True),
        "market_value": pa.Column(pa.Int, nullable=True),
        "sale_date": pa.Column(pd.DatetimeTZDtype(tz="UTC"), nullable=True),
        "sale_price": pa.Column(pa.Float, nullable=True),
        "owner_1": pa.Column(pa.String, nullable=True),
        "owner_2": pa.Column(pa.String, nullable=True),
        "building_code_description": pa.Column(pa.String, nullable=True),
        "zip_code": pa.Column(pa.String, nullable=True),
        "zoning": pa.Column(pa.String, nullable=True),
        "parcel_type": pa.Column(pa.String, nullable=True),
        "vacant": pa.Column(pa.Bool, nullable=True),
        "district": pa.Column(
            str, nullable=True, checks=pa.Check.isin([str(i) for i in range(1, 11)])
        ),
        "geometry": pa.Column("geometry"),
    },
    strict=True,
)


class CouncilDistrictsInputValidator(BaseValidator):
    """Validator for council districts service input."""

    schema = CouncilDistrictsInputSchema

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass


class CouncilDistrictsOutputValidator(BaseValidator):
    """Validator for council districts service output."""

    schema = CouncilDistrictsOutputSchema

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass
