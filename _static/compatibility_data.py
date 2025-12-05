"""Compatibility data for different robot versions."""

import os
import csv
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


def load_compatibility_data():
    """Load compatibility data from CSV files."""
    data_dir = Path(__file__).parent / "compatibility_data"
    print(f"Looking for CSV files in: {data_dir}")
    compatibility_data = {}

    # Map of robot types to their CSV files
    robot_files = {"FR3": "FR3.csv", "FER": "FER.csv"}

    for robot, filename in robot_files.items():
        file_path = data_dir / filename
        print(f"Checking for file: {file_path}")
        if file_path.exists():
            print(f"Found file for {robot}")
            headers, data = read_csv_data(file_path)
            compatibility_data[robot] = {"headers": headers, "data": data}
        else:
            print(f"File not found for {robot}")

    print(f"Final compatibility data: {compatibility_data}")
    return compatibility_data


# Load the compatibility data when the module is imported
COMPATIBILITY_DATA = load_compatibility_data()
