import geopandas as gpd
import pandera.pandas as pa
import pandas as pd
from .base import BaseValidator

# Expecting ~7,796 records returned (within ±20% tolerance).
# This is checked in CityOwnedPropertiesInputSchema
expected = 7796
lower = int(expected * 0.8)
upper = int(expected * 1.2)

CityOwnedPropertiesInputSchema = pa.DataFrameSchema(
    columns={
        "opa_id": pa.Column(pa.Int, checks=pa.Check(lambda s: s.dropna() != "")),
        "agency": pa.Column(pa.String, nullable=True),
        "sideyardeligible": pa.Column(
            pa.Category, nullable=True, checks=pa.Check.isin(["Yes", "No"])
        ),
        "geometry": pa.Column("geometry"),
    },
    checks=pa.Check(lambda df: lower <= df.shape[0] <= upper),
    strict=True,
)

CityOwnedPropertiesOutputSchema = pa.DataFrameSchema(
    columns={
        "opa_id": pa.Column(pa.Int, checks=pa.Check(lambda s: s.dropna() != "")),
        "market_value": pa.Column(pa.Int, nullable=True),
        "sale_date": pa.Column(pd.DatetimeTZDtype(tz="UTC"), nullable=True),
        "sale_price": pa.Column(pa.Float, nullable=True),
        "owner_1": pa.Column(pa.String, nullable=True),
        "owner_2": pa.Column(pa.String, nullable=True),
        "building_code_description": pa.Column(pa.String, nullable=True),
        "zip_code": pa.Column(pa.String, nullable=True),
        "zoning": pa.Column(pa.String, nullable=True),
        "parcel_type": pa.Column(pa.String, nullable=True),
        "standardized_address": pa.Column(pa.String, nullable=True),
        "vacant": pa.Column(pa.Bool, nullable=True),
        "district": pa.Column(pa.String, nullable=True),
        "neighborhood": pa.Column(pa.String, nullable=True),
        "rco_info": pa.Column(pa.String, nullable=True),
        "rco_names": pa.Column(pa.String, nullable=True),
        "city_owner_agency": pa.Column(pa.String, nullable=True),
        "side_yard_eligible": pa.Column(
            pa.Category, nullable=True, checks=pa.Check.isin(["Yes", "No"])
        ),
        "geometry": pa.Column("geometry"),
    },
    strict=True,
)


class CityOwnedPropertiesInputValidator(BaseValidator):
    """
    Validator for the city-owned properties dataset input.
    schema and _custom_validation() are used by validate() in the parent class.
    """

    schema = CityOwnedPropertiesInputSchema

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass


class CityOwnedPropertiesOutputValidator(BaseValidator):
    """
    Validator for the city-owned properties dataset output.
    schema and _custom_validation() are used by validate() in the parent class.
    """

    schema = CityOwnedPropertiesOutputSchema

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass
