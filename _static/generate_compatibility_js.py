#!/usr/bin/env python3
"""
Script to generate JavaScript compatibility data file from CSV files and RST tables.
This script reads CSV files and RST compatibility matrices and generates a JavaScript
file with the data structured for use in the documentation.
"""

import csv
import json
import os
import re
from pathlib import Path


def read_csv_file(file_path):
    """Read a CSV file and return headers and data."""
    with open(file_path, "r") as f:
        reader = csv.reader(f)
        headers = next(reader)  # First row contains headers
        data = [row for row in reader]
    return headers, data


def read_rst_list_table(file_path, start_marker, end_marker):
    """Read an RST list-table between markers and return description, headers and data."""
    with open(file_path, "r") as f:
        content = f.read()

    # Extract content between markers
    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)
    if start_idx == -1 or end_idx == -1:
        return None, None, None
    section = content[start_idx + len(start_marker):end_idx]

    # Extract description text before the list-table directive
    description_lines = []
    in_table = False
    for line in section.splitlines():
        if line.strip().startswith('.. list-table::'):
            in_table = True
        if not in_table:
            # Convert RST bold markers to HTML
            cleaned = line.strip()
            if cleaned:
                cleaned = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', cleaned)
                description_lines.append(cleaned)
    description = ' '.join(description_lines).strip()

    # Parse list-table rows: each row starts with "   * -" (header/first cell)
    # or "     -" (subsequent cells)
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
        return description, None, None

    headers = rows[0]
    data = rows[1:]
    return description, headers, data


def generate_js():
    """Generate JavaScript file with compatibility data."""
    # Directory containing CSV files
    csv_dir = Path("source/_static/compatibility_data")

    # Dictionary to store compatibility data
    compatibility_data = {}

    # Map of file names to display names
    robot_display_names = {"FER": "FER"}

    # Read each CSV file in the directory
    for csv_file in csv_dir.glob("*.csv"):
        robot_type = csv_file.stem  # Get filename without extension
        headers, data = read_csv_file(csv_file)
        display_name = robot_display_names.get(robot_type, robot_type)
        compatibility_data[display_name] = {"headers": headers, "data": data}

    # Read libfranka compatibility from RST
    libfranka_rst = Path("source/doc/libfranka/docs/compatibility_matrix.rst")
    libfranka_description = ""
    if libfranka_rst.exists():
        description, headers, data = read_rst_list_table(
            libfranka_rst, ".. table-start-libfranka", ".. table-end-libfranka"
        )
        if headers and data:
            compatibility_data["Franka Research 3"] = {"headers": headers, "data": data}
            if description:
                libfranka_description = description

    # Read RST compatibility matrices for franka_ros2
    rst_sources = {
        "franka_ros2 Humble": {
            "file": "source/doc/franka_ros2_humble/franka_ros2/doc/compatibility_matrix.rst",
            "start": ".. table-start-humble",
            "end": ".. table-end-humble",
        },
        "franka_ros2 Jazzy": {
            "file": "source/doc/franka_ros2_jazzy/franka_ros2/doc/compatibility_matrix.rst",
            "start": ".. table-start-jazzy",
            "end": ".. table-end-jazzy",
        },
    }

    # Additional tables shown alongside a dropdown entry
    additional_tables = {"Franka Research 3": []}

    for display_name, cfg in rst_sources.items():
        rst_path = Path(cfg["file"])
        if rst_path.exists():
            description, headers, data = read_rst_list_table(rst_path, cfg["start"], cfg["end"])
            if headers and data:
                entry = {"title": display_name, "headers": headers, "data": data}
                if description:
                    entry["description"] = description
                additional_tables["Franka Research 3"].append(entry)

    # Robot descriptions
    robot_descriptions = {
        "Franka Research 3": libfranka_description,
        "Franka Research 3 (FR3)": "Latest generation Franka Robot with ROS 2 support",
        "Franka Emika Robot (FER)": "First generation Franka Robot",
    }

    # Generate JavaScript content
    js_content = f"""// Generated compatibility data
const compatibilityData = {json.dumps(compatibility_data, indent=2)};

// Additional tables to show alongside a dropdown selection
const additionalTables = {json.dumps(additional_tables, indent=2)};

// Robot descriptions
const robotDescriptions = {json.dumps(robot_descriptions, indent=2)};
"""

    # Write to JavaScript file
    js_file_path = Path("source/_static/compatibility_data.js")
    with open(js_file_path, "w") as f:
        f.write(js_content)


if __name__ == "__main__":
    generate_js()
