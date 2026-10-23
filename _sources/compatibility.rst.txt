.. _compatibility-libfranka:

Software Versions Compatibility
===============================

This section provides an overview of the compatibility between different versions of the robot system version,
libfranka and the robot/gripper server version which are coupled to the robot system version. E.g. a
**robot system version** 5.7.2 needs a **robot** version 9 and **gripper** version 3.

Note: Often, people talk about *image version* while talking about the *robot system version*.

.. raw:: html

    <style>
        .compatibility-container {
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin: 20px 0;
        }
        .robot-select {
            padding: 8px 12px;
            font-size: 16px;
            margin-bottom: 20px;
            border: 1px solid #ddd;
            border-radius: 4px;
            width: 200px;
        }
        .compatibility-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        .compatibility-table th,
        .compatibility-table td {
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }
        .compatibility-table th {
            background-color: #f8f9fa;
            font-weight: bold;
        }
        .compatibility-table tr:nth-child(even) {
            background-color: #f8f9fa;
        }
        .matrix {
            display: none;
        }
        .matrix.active {
            display: block;
        }
        .robot-description {
            margin-bottom: 15px;
            font-style: italic;
            color: #666;
        }
    </style>

    <div class="compatibility-container">
        <select class="robot-select" id="robotSelector" onchange="showCompatibility()">
        </select>
        <div class="robot-description" id="robotDescription"></div>
        <div id="matrixContainer"></div>
    </div>

    <script src="_static/compatibility_data.js"></script>
    <script>
        // Populate the dropdown
        const selector = document.getElementById('robotSelector');

        // Sort robot names to ensure Franka Research 3 is first
        const robotNames = Object.keys(compatibilityData).sort((a, b) => {
            if (a === 'Franka Research 3') return -1;
            if (b === 'Franka Research 3') return 1;
            return a.localeCompare(b);
        });

        robotNames.forEach(robot => {
            const option = document.createElement('option');
            option.value = robot;
            option.textContent = robot;
            selector.appendChild(option);
        });

        // Set default selection to Franka Research 3
        selector.value = 'Franka Research 3';
        showCompatibility();  // Show the default selection immediately

        function createTable(robotData) {
            const table = document.createElement('table');
            table.className = 'compatibility-table';

            // Create header row
            const headerRow = document.createElement('tr');
            robotData.headers.forEach(header => {
                const th = document.createElement('th');
                th.textContent = header;
                headerRow.appendChild(th);
            });
            table.appendChild(headerRow);

            // Create data rows
            robotData.data.forEach(row => {
                const tr = document.createElement('tr');
                row.forEach(cell => {
                    const td = document.createElement('td');
                    td.textContent = cell;
                    tr.appendChild(td);
                });
                table.appendChild(tr);
            });

            return table;
        }

        function showCompatibility() {
            const selected = selector.value;
            const container = document.getElementById('matrixContainer');
            const descriptionElement = document.getElementById('robotDescription');

            // Clear previous content
            container.innerHTML = '';
            descriptionElement.textContent = '';

            if (selected && compatibilityData[selected]) {
                // Show robot description
                if (robotDescriptions[selected]) {
                    descriptionElement.innerHTML = robotDescriptions[selected];
                }

                // Create and show compatibility table
                const mainHeading = document.createElement('h4');
                mainHeading.textContent = selected;
                container.appendChild(mainHeading);
                const table = createTable(compatibilityData[selected]);
                container.appendChild(table);

                // Show additional tables if configured
                if (additionalTables[selected]) {
                    additionalTables[selected].forEach(entry => {
                        const heading = document.createElement('h4');
                        heading.textContent = entry.title;
                        heading.style.marginTop = '30px';
                        container.appendChild(heading);
                        if (entry.description) {
                            const desc = document.createElement('p');
                            desc.innerHTML = entry.description;
                            desc.style.fontStyle = 'italic';
                            desc.style.color = '#666';
                            container.appendChild(desc);
                        }
                        const extraTable = createTable(entry);
                        container.appendChild(extraTable);
                    });
                }
            }
        }

        // Initialize on page load
        document.addEventListener('DOMContentLoaded', function() {
            showCompatibility();
        });
    </script>

Further Compatibility Information
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For `franka_ros` compatibility information, please refer to :ref:`ros-compatibility` and for `franka_matlab`
compatibility information, please refer to :ref:`compatibility-franka-matlab`.

`Robot version
<https://github.com/frankarobotics/libfranka-common/blob/master/include/research_interface/robot/service_types.h>`_
and `Gripper version
<https://github.com/frankarobotics/libfranka-common/blob/master/include/research_interface/gripper/types.h>`_
are part of libfranka-common repository, a submodule of libfranka repository.

.. caution::
    Franka Robotics currently does not provide any support for Windows
