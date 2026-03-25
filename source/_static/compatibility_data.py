"""Compatibility data for different robot versions."""

import csv
import os
import re
from pathlib import Path


def read_csv_data(file_path):
    """Read CSV file and return headers and data."""
    print(f"Reading CSV file: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        headers = next(reader)  # First row contains headers
        data = [row for row in reader]
    print(f"Headers: {headers}")
    print(f"Data: {data}")
    return headers, data


def read_rst_list_table(file_path, start_marker, end_marker):
    """Read an RST list-table between markers and return headers and data."""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)
    if start_idx == -1 or end_idx == -1:
        return None, None
    section = content[start_idx + len(start_marker):end_idx]

    rows = []
    current_row = None
    for line in section.splitlines():
        match_first = re.match(r'^\s+\* - (.+)', line)
        match_next = re.match(r'^\s+- (.+)', line)
        if match_first:
            if current_row is not None:
                rows.append(current_row)
            current_row = [match_first.group(1).strip()]
        elif match_next and current_row is not None:
            current_row.append(match_next.group(1).strip())
    if current_row is not None:
        rows.append(current_row)

    if not rows:
        return None, None

    return rows[0], rows[1:]


def load_compatibility_data():
    """Load compatibility data from CSV files and RST tables."""
    data_dir = Path(__file__).parent / "compatibility_data"
    print(f"Looking for CSV files in: {data_dir}")
    compatibility_data = {}

    # Load FER data from CSV
    fer_file = data_dir / "FER.csv"
    print(f"Checking for file: {fer_file}")
    if fer_file.exists():
        print(f"Found file for FER")
        headers, data = read_csv_data(fer_file)
        compatibility_data["FER"] = {"headers": headers, "data": data}

    # Load FR3 data from libfranka RST compatibility matrix
    rst_path = Path(__file__).parent.parent / "doc" / "libfranka" / "docs" / "compatibility_matrix.rst"
    print(f"Checking for RST file: {rst_path}")
    if rst_path.exists():
        print(f"Found RST file for FR3")
        headers, data = read_rst_list_table(rst_path, ".. table-start-libfranka", ".. table-end-libfranka")
        if headers and data:
            compatibility_data["FR3"] = {"headers": headers, "data": data}
    else:
        print(f"RST file not found for FR3")

    print(f"Final compatibility data: {compatibility_data}")
    return compatibility_data


# Load the compatibility data when the module is imported
COMPATIBILITY_DATA = load_compatibility_data()
