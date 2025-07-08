import functools
import logging as log
import re
import sys
import time
from datetime import datetime, timezone
from typing import Any, List

import geopandas as gpd

from src.config.config import log_level

log.basicConfig(level=log_level)

DESCRIPTION_REGEX = r"^(?P<description>.*?)(?=\n\s*\w+:\s|$)"
SECTION_REGEX = r"^\s*(?P<key>[\w\s]+):\s*(?P<value>.*?)(?=^\s*[\w\s]+:\s|\Z)"
METADATA_FIELDS = [
    "description",
    "returns",
    "tagline",
    "columns added",
    "columns updated",
    "source",
    "known issues",
    "columns referenced",
]
METADATA_FIELD_TYPES = {
    "columns added": "columns",  # with types
    "columns updated": "columns",  # without types
    "columns referenced": "column_names",
}


def normalize_whitespace(text):
    """Convert newlines to spaces and collapse multiple spaces into one."""
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def get_description_from_docstring(docstring):
    """
    Extract the description from the docstring.

    Extracts all text before the first section header (e.g. Args:, Returns:).

    """

    # Regex to capture the "description": everything until a section header
    description_pattern = re.compile(DESCRIPTION_REGEX, re.DOTALL)
    description_match = description_pattern.search(docstring)
    description = (
        description_match.group("description").strip() if description_match else ""
    )
    return description


def get_sections_from_docstring(docstring):
    section_pattern = re.compile(
        SECTION_REGEX,
        re.DOTALL | re.MULTILINE,
    )
    sections = {
        m.group("key").lower(): m.group("value").strip()
        for m in section_pattern.finditer(docstring)
    }
    return sections


def get_column_details(text):
    """
    Parse the column details from the text in the format:
    "column_name (data_type): description"
    """
    pattern = r"(\w+)(?:\s+\((\w+)\))?:\s+(.+)"

    matches = re.findall(pattern, text)

    # Convert to structured data with default type as "unknown"
    parsed_columns = []
    for name, dtype, desc in matches:
        column = {
            "name": name.strip(),
            "description": desc.strip(),
        }
        if dtype:  # Only add 'type' if dtype is not empty
            column["type"] = dtype.strip()

        parsed_columns.append(column)

    return parsed_columns


def clean_docstring(docstring):
    """
    trim function from PEP-257

    Ensures that the docstring is clean, uniformly indented, and free of extraneous whitespace.
    """
    if not docstring:
        return ""

    # Convert tabs to spaces (following the normal Python rules)
    # and split into a list of lines:
    lines = docstring.expandtabs().splitlines()
    # Determine minimum indentation (first line doesn't count):
    indent = sys.maxsize
    for line in lines[1:]:
        stripped = line.lstrip()
        if stripped:
            indent = min(indent, len(line) - len(stripped))
    # Remove indentation (first line is special):
    trimmed = [lines[0].strip()]
    if indent < sys.maxsize:
        for line in lines[1:]:
            trimmed.append(line[indent:].rstrip())
    # Strip off trailing and leading blank lines:
    while trimmed and not trimmed[-1]:
        trimmed.pop()
    while trimmed and not trimmed[0]:
        trimmed.pop(0)

    # Current code/unittests expects a line return at
    # end of multiline docstrings
    # workaround expected behavior from unittests
    if "\n" in docstring:
        trimmed.append("")

    # Return a single string:
    return "\n".join(trimmed)


def parse_docstring(docstring):
    """Parse the docstring into its components."""
    # Capture the "description" which is everything before the first header
    if not docstring:
        return {}
    docstring = clean_docstring(docstring.lstrip("\n"))
    description = get_description_from_docstring(docstring)
    sections = get_sections_from_docstring(docstring)
    sections["description"] = description

    # "columns added" and "columns updated" require special handling
    # to breakdown the columns listed in the docstring

    result = {}
    for field in METADATA_FIELDS:
        if METADATA_FIELD_TYPES.get(field, "text") == "columns":
            result[field] = get_column_details(sections.get(field, ""))
        elif METADATA_FIELD_TYPES.get(field, "text") == "column_names":
            result[field] = [
                col.strip() for col in sections.get(field, "").split(",") if col.strip()
            ]
        else:
            result[field] = (
                normalize_whitespace(sections[field]) if sections.get(field) else ""
            )

    return result


def detect_added_columns(
    df_before: gpd.GeoDataFrame, df_after: gpd.GeoDataFrame
) -> set[str]:
    """
    Detects columns that have been added in df_after compared to df_before.
    Handles cases where df_before is None or empty.
    """
    if df_before is None or df_before.empty:
        return set(df_after.columns)
    return set(df_after.columns) - set(df_before.columns)


def provide_metadata(current_metadata: List[dict[str, Any]]):
    """
    Decorator to collect metadata from ETL functions.

    The collected metadata is stored in the an inputted `current_metadata` object that is passed into
    each decorator attached to a data service.

    Apply this decorator by adding `@provide_metadata(current_metadata)` above the function definition.

    The metadata collects info from the docstring in the following format:

    '''
    Description of what the function does.

    Args:
        param1 (Type): Description of parameter 1.
        param2 (Type): Description of parameter 2.

    Returns:
        ReturnType: Description of the return value.

    Tagline:
        A very short summary of the function for use in DAG graphs.

    Columns added:
        column_name (data_type): Description of what this new column represents.

    Columns updated:
        column_name: Description of how this column was changed.

    Columns referenced:
        column_name (data_type): Description of how this column is referenced.

    Source:
        URL or reference for additional context.

    Known issues:
        Any known issues or limitations with this function.

    '''
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(gdf: gpd.GeoDataFrame):
            # Run the function and collect metadata
            # including start time, end time, and duration

            start_gdf = gdf if not gdf.empty else gpd.GeoDataFrame()

            start_time_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
            start_time = time.time()

            end_gdf, validation = func(gdf)

            end_time = time.time()
            end_time_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
            try:
                detected_columns_added = detect_added_columns(start_gdf, end_gdf)

                func_name = func.__name__
                doc_meta = parse_docstring(func.__doc__)

                metadata = {
                    "name": func_name,
                    "start_time": start_time_str,
                    "end_time": end_time_str,
                    "duration_in_seconds": round(end_time - start_time, 2),
                }

                for field in METADATA_FIELDS:
                    metadata[field.replace(" ", "_")] = doc_meta.get(field, "")

                names_of_columns_added = set(
                    [col["name"] for col in metadata.get("columns_added", [])]
                )
                if detected_columns_added != names_of_columns_added:
                    log.debug(
                        "Columns added doesn't match columns listed as added in the docstring:"
                        f"Detected: {detected_columns_added}"
                        f"Listed in docstring: {names_of_columns_added}"
                    )

                current_metadata.append(metadata)

            except Exception as e:
                print("Failed to collect metadata for", func.__name__)
                print(type(e), e)
                log.error(e, exc_info=True)
                metadata = {
                    "name": func.__name__,
                    "description": "Failed to collect metadata",
                }

                current_metadata.append(metadata)

            return end_gdf, validation

        return wrapper

    return decorator
