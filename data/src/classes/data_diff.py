import os
import re
from datetime import datetime

from src.classes.file_manager import FileManager, FileType, LoadType

file_manager = FileManager()


def extract_date(filename: str) -> datetime:
    """Parse the ``YYYY_MM_DD`` date embedded in a pipeline cache filename."""
    match = re.search(r"\d{4}_\d{1,2}_\d{1,2}", filename)
    if match is None:
        raise ValueError(f"Unable to find a date string within '{filename}'")
    return datetime.strptime(match.group(), "%Y_%m_%d")


class DiffReport:
    def __init__(self, table_name="all_properties_end", unique_id_col="opa_id"):
        """
        Initialize the DiffReport.

        Args:
            table_name (str): The name of the table to analyze.
            unique_id_col (str): Column used as a unique identifier.
        """
        self.table_name = table_name
        self.unique_id_col = unique_id_col
        self.latest_timestamp = None
        self.previous_timestamp = None
        self.summary_text = ""

    def generate_diff(self):
        """
        Generate the data diff and summarize changes.
        """
        cache_directory = file_manager.pipeline_cache_directory
        cached_files = [
            file for file in os.listdir(cache_directory) if self.table_name in file
        ]

        if len(cached_files) < 2:
            print(
                f"Table {self.table_name} has less than two separate files with different timestamps. Cannot perform comparison"
            )
            self.summary_text = f"Table {self.table_name} has less than two separate files with different timestamps. Cannot perform comparison"
            return self

        # Sort newest first so index 0 is the latest file, 1 the previous one.
        cached_files.sort(key=extract_date, reverse=True)

        latest_file, previous_file = cached_files[0], cached_files[1]
        self.latest_timestamp = extract_date(latest_file)
        self.previous_timestamp = extract_date(previous_file)

        gdf_latest = file_manager.load_gdf(
            latest_file, LoadType.PIPELINE_CACHE, FileType.PARQUET
        )
        gdf_previous = file_manager.load_gdf(
            previous_file, LoadType.PIPELINE_CACHE, FileType.PARQUET
        )

        common_columns = [
            col for col in gdf_latest.columns if col in gdf_previous.columns
        ]
        gdf_latest = gdf_latest[common_columns]
        gdf_previous = gdf_previous[common_columns]

        # Align indexes to include all rows from both DataFrames
        gdf_latest = gdf_latest.set_index(self.unique_id_col).reindex(
            gdf_previous.index.union(gdf_latest.index)
        )
        gdf_previous = gdf_previous.set_index(self.unique_id_col).reindex(
            gdf_previous.index.union(gdf_latest.index)
        )

        # Ensure columns are in the same order
        gdf_latest = gdf_latest[sorted(gdf_latest.columns)]
        gdf_previous = gdf_previous[sorted(gdf_previous.columns)]

        # Step 4: Perform the comparison
        diff = gdf_latest.compare(
            gdf_previous, align_axis=1, keep_shape=False, keep_equal=False
        )

        if diff.empty:
            print("No changes detected between the two timestamps.")
            self.summary_text = "No changes detected between the two timestamps."
            return

        # Step 5: Calculate percentage changes
        print("Calculating percentages...")
        total_rows = len(gdf_latest)
        changes_by_column = {
            col: (diff.xs(col, level=0, axis=1).notna().sum().sum() / total_rows) * 100
            for col in diff.columns.get_level_values(0).unique()
        }

        # Step 6: Create plain text summary
        summary_lines = [
            f"Diff Report for {self.table_name}",
            f"Latest timestamp: {self.latest_timestamp}",
            f"Previous timestamp: {self.previous_timestamp}",
            "",
            "Comparison Summary (% of rows with changes per column):",
        ]

        for col, pct_change in sorted(
            changes_by_column.items(), key=lambda x: x[1], reverse=True
        ):
            summary_lines.append(f"  - {col}: {pct_change:.2f}%")

        self.summary_text = "\n".join(summary_lines)
