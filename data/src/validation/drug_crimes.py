import geopandas as gpd
from pandera.pandas import Column, DataFrameSchema

from .base import BaseValidator, DistributionParams, distribution_check

density_params = DistributionParams(
    max_value=2.775164283e-07,
    mean=6.379905688e-10,
    std=6.373370963e-09,
    q1=5.093356484e-11,
    q3=2.242882264e-10,
)
zscore_params = DistributionParams(
    max_value=43.50796563,
    mean=0.0002106629869,
    std=1.001490273,
    q1=-0.09203751817,
    q3=-0.06479714437,
)
percentile_params = DistributionParams(
    max_value=100, mean=50.49923297, std=28.93429096, q1=26, q3=76
)

output_schema = DataFrameSchema(
    {
        "drug_crimes_density": Column(
            float, checks=[*distribution_check(density_params)]
        ),
        "drug_crimes_density_zscore": Column(
            float, checks=[*distribution_check(zscore_params)]
        ),
        "drug_crimes_density_label": Column(str),
        "drug_crimes_density_percentile": Column(
            float, checks=[*distribution_check(percentile_params)]
        ),
    }
)


class DrugCrimesOutputValidator(BaseValidator):
    """Validator for drug crimes service output."""

    schema = output_schema

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass
