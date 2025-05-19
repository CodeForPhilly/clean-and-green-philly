import pandas as pd
import requests
from datetime import datetime, timezone

from ..classes.featurelayer import FeatureLayer
from ..metadata.metadata_utils import provide_metadata
from ..constants.services import ACTIVITY_QUERIES


def fetch_recent_activity(query: str) -> pd.DataFrame:
    response = requests.get("https://phl.carto.com/api/v2/sql", params={"q": query})
    response.raise_for_status()
    data = response.json().get("rows", [])
    return pd.DataFrame(data)


@provide_metadata()
def recent_activity(primary_featurelayer: FeatureLayer) -> FeatureLayer:
    result_gdf = primary_featurelayer.gdf.copy()

    for col_name, query in ACTIVITY_QUERIES.items():
        try:
            df = fetch_recent_activity(query)
            if df.empty:
                print("⚠️ No results found")
                result_gdf[col_name] = pd.NaT
                continue

            result_gdf = result_gdf.merge(
                df, how="left", left_on="opa_id", right_on="opa_account_num"
            )
            result_gdf.drop(columns=["opa_account_num"], inplace=True, errors="ignore")
            print(f"📊 {result_gdf[col_name].isna().sum()} null values after merge")
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            result_gdf[col_name] = pd.NaT

    current_date = datetime.now(timezone.utc)
    date_columns = [
        "latest_permit_date",
        "latest_business_license_date",
        "latest_appeal_date",
    ]

    for date_col in date_columns:
        activity_type = date_col.replace("latest_", "").replace("_date", "")
        days_col = f"days_since_{activity_type}"
        has_col = f"has_{activity_type}_record"

        if date_col in result_gdf.columns:
            result_gdf[has_col] = ~result_gdf[date_col].isna()
            if result_gdf[date_col].dtype == "object":
                result_gdf[date_col] = pd.to_datetime(
                    result_gdf[date_col], errors="coerce"
                )
            result_gdf[days_col] = (current_date - result_gdf[date_col]).dt.days.fillna(
                9999
            )

    primary_featurelayer.gdf = result_gdf

    return primary_featurelayer
