Compatible versions
===================

.. _compatibility-libfranka:

Compatibility with libfranka
----------------------------

Various versions of compatible components are available.
The table below offers an overview, with a recommendation to utilize up-to-date versions whenever possible.
The symbol '>= ' indicates that compatibility with newer robot system versions has not been tested,
implying that compatibility is not guaranteed (e.g., libfranka 0.2.0 may not be compatible with robot system version 4.0.0).

The Robot system versions 2.x.x are not listed in the table below, but they are included as compatible with Robot system version >= 1.3.0.
Therefore, they are compatible with libfranka versions 0.4.0 and 0.5.0.

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
                    descriptionElement.textContent = robotDescriptions[selected];
                }

                // Create and show compatibility table
                const table = createTable(compatibilityData[selected]);
                container.appendChild(table);
            }
        }

        // Initialize on page load
        document.addEventListener('DOMContentLoaded', function() {
            showCompatibility();
        });
    </script>

`Robot version line 19
<https://github.com/frankarobotics/libfranka-common/blob/master/include/research_interface/robot/service_types.h#L21>`_
and `Gripper version line 17
<https://github.com/frankarobotics/libfranka-common/blob/master/include/research_interface/gripper/types.h#L17>`_
are part of libfranka-common repository, a submodule of libfranka repository.

Franka MATLAB® compatible versions are located :ref:`here<compatibility-franka-matlab>`.

.. caution::
    Franka Robotics currently does not provide any support for Windows or Arm

Compatibility with the kernel
-----------------------------

There are different kernels, which are compatible with different Ubuntu system versions.
The following table gives an overview of recommended Kernels.

+----------------+-------------------------+
| Kernel version | Ubuntu                  |
+================+=========================+
| Pro Kernel     | 22.04 (Jammy Jellyfish) |
+----------------+-------------------------+
| 5.9.1          | 20.04 (Focal Fossa)     |
+----------------+-------------------------+
| 5.4.19         | 18.04 (Bionic)          |
+----------------+-------------------------+
| 4.14.12        | 16.04 (Xenial Xerus)    |
+----------------+-------------------------+
