from datetime import datetime

import pytest

from src.classes.data_diff import extract_date


def test_extract_date_parses_cache_filename():
    # File labels are "<table>_<YYYY_MM_DD>_new.parquet" (FileManager.generate_file_label)
    assert extract_date("all_properties_end_2024_06_24_new.parquet") == datetime(
        2024, 6, 24
    )


def test_extract_date_raises_when_no_date():
    with pytest.raises(ValueError):
        extract_date("all_properties_end_new.parquet")
