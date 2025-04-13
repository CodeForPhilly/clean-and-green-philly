import pandas as pd
from ..classes.featurelayer import FeatureLayer
from ..metadata.metadata_utils import provide_metadata
import requests
from datetime import datetime, timezone


@provide_metadata()
def recent_activity(primary_featurelayer: FeatureLayer) -> FeatureLayer:
    """
    Adds recent activity dates to the properties data by querying Carto directly.
    Returns the modified FeatureLayer with new date columns and days since activity.
    """
    # Access the GeoDataFrame from the FeatureLayer
    result_gdf = primary_featurelayer.gdf.copy()

    # Define our queries
    queries = {
        "latest_permit_date": """
        SELECT DISTINCT ON (opa_account_num)
        opa_account_num,
        permitissuedate AS latest_permit_date
        FROM permits
        WHERE opa_account_num IS NOT NULL
        ORDER BY opa_account_num, permitissuedate DESC
        """,
        "latest_business_license_date": """
        SELECT DISTINCT ON (opa_account_num)
        opa_account_num,
        mostrecentissuedate AS latest_business_license_date
        FROM business_licenses
        WHERE opa_account_num IS NOT NULL
        ORDER BY opa_account_num, mostrecentissuedate DESC
        """,
        "latest_appeal_date": """
        SELECT DISTINCT ON (opa_account_num)
        opa_account_num,
        scheduleddate AS latest_appeal_date
        FROM appeals
        WHERE opa_account_num IS NOT NULL
        ORDER BY opa_account_num, scheduleddate DESC
        """,
    }

    for col_name, query in queries.items():
        print(f"\n🔍 Querying Carto for {col_name}...")
        try:
            # Execute the query directly
            response = requests.get(
                "https://phl.carto.com/api/v2/sql", params={"q": query}
            )
            response.raise_for_status()

            # Convert to DataFrame
            data = response.json().get("rows", [])
            if not data:
                print("⚠️ No results found")
                result_gdf[col_name] = pd.NaT
                continue

            df = pd.DataFrame(data)
            print(f"✅ Retrieved {len(df)} rows")
            print("Sample results:")
            print(df.head(3))

            # Clean and merge
            result_gdf = result_gdf.merge(
                df, how="left", left_on="opa_id", right_on="opa_account_num"
            )

            # Clean up
            if "opa_account_num" in result_gdf.columns:
                result_gdf.drop(columns=["opa_account_num"], inplace=True)

            # Report nulls
            nulls = result_gdf[col_name].isna().sum()
            print(f"📊 {nulls} null values after merge")
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            result_gdf[col_name] = pd.NaT

    # Calculate days since each activity
    current_date = datetime.now(timezone.utc)

    # Create days_since columns and has_activity columns
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
            # Create has_record column (True if date exists, False otherwise)
            result_gdf[has_col] = ~result_gdf[date_col].isna()

            # Convert string dates to datetime if needed
            if result_gdf[date_col].dtype == "object":
                result_gdf[date_col] = pd.to_datetime(
                    result_gdf[date_col], errors="coerce"
                )

            # Calculate days since the date
            result_gdf[days_col] = (current_date - result_gdf[date_col]).dt.days

            # Replace NaN with sentinel value (e.g., 9999 days)
            result_gdf[days_col] = result_gdf[days_col].fillna(9999)

        # Update the gdf in the feature layer with our modified version
        primary_featurelayer.gdf = result_gdf

        # Print the first 10 rows of relevant columns
        relevant_columns = [
            "opa_id",
            "latest_permit_date",
            "days_since_permit",
            "has_permit_record",
            "latest_business_license_date",
            "days_since_business_license",
            "has_business_license_record",
            "latest_appeal_date",
            "days_since_appeal",
            "has_appeal_record",
        ]

    print("\n📊 First 10 rows of activity data:")
    print(result_gdf[relevant_columns].head(10))

    return primary_featurelayer

