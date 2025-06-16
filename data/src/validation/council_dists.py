import geopandas as gpd
import pandera.pandera as pa
from .base import BaseValidator


class CouncilDistrictsSchema(pa.DataFrameModel):
    OBJECTID_1: pa.typing.Series[int]
    OBJECTID: pa.typing.Series[int]
    DISTRICT: pa.typing.Series[str]
    SHAPE_LENG: pa.typing.Series[float]
    Shape__Area: pa.typing.Series[float]
    Shape__Length: pa.typing.Series[float]

    class Config:
        strict = True  # Columns must match exactly


class CouncilDistrictsInputValidator(BaseValidator):
    """Validator for council districts service input."""

    schema = None

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        pass


class CouncilDistrictsOutputValidator(BaseValidator):
    """Validator for council districts service output."""

    schema = CouncilDistrictsSchema

    def _custom_validation(self, gdf: gpd.GeoDataFrame):
        # Check there are exactly 10 rows
        if len(gdf) != 10:
            self.errors.append(f"Expected 10 council district records, got {len(gdf)}")

        # Check "district" values are exactly "1" through "10"
        expected = {str(i) for i in range(1, 11)}
        actual = list(gdf["district"])
        if actual != expected:
            self.errors.append(
                f"'district' column values must be strings '1' through '10', but got: {sorted(actual)}"
            )
