#!/usr/bin/env python3
"""
Script to generate JavaScript compatibility data file from CSV files.
This script reads CSV files containing compatibility information for different robot types
and generates a JavaScript file with the data structured for use in the documentation.
"""

import csv
import json
import os
from pathlib import Path


def read_csv_file(file_path):
    """Read a CSV file and return headers and data."""
    with open(file_path, "r") as f:
        reader = csv.reader(f)
        headers = next(reader)  # First row contains headers
        data = [row for row in reader]
    return headers, data


def generate_js():
    """Generate JavaScript file with compatibility data."""
    # Directory containing CSV files
    csv_dir = Path("source/_static/compatibility_data")

    # Dictionary to store compatibility data
    compatibility_data = {}

    # Map of file names to display names
    robot_display_names = {"FR3": "Franka Research 3", "FER": "FER"}

    # Read each CSV file in the directory
    for csv_file in csv_dir.glob("*.csv"):
        robot_type = csv_file.stem  # Get filename without extension
        headers, data = read_csv_file(csv_file)
        display_name = robot_display_names.get(robot_type, robot_type)
        compatibility_data[display_name] = {"headers": headers, "data": data}

    # Robot descriptions
    robot_descriptions = {
        "Franka Research 3 (FR3)": "Latest generation Franka Robot with ROS 2 support",
        "Franka Emika Robot (FER)": "First generation Franka Robot",
    }

    # Generate JavaScript content
    js_content = f"""// Generated compatibility data
const compatibilityData = {json.dumps(compatibility_data, indent=2)};

// Robot descriptions
const robotDescriptions = {json.dumps(robot_descriptions, indent=2)};
"""

    # Write to JavaScript file
    js_file_path = Path("source/_static/compatibility_data.js")
    with open(js_file_path, "w") as f:
        f.write(js_content)


if __name__ == "__main__":
    generate_js()
