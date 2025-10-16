Installation
============

Installation Methods
--------------------

Option 1: Drag and drop the franka.mltbx file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Drag and drop the ``franka.mltbx`` file into your MATLAB Command Window or

Option 2: Programmatically
^^^^^^^^^^^^^^^^^^^^^^^^^^
.. code-block:: matlab

    uiopen('<path to your franka.mltbx file>', 1);

License Management & Activation
-------------------------------

1. Generate System Identifier
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Execute the following command in MATLAB to generate your system's unique identifier:

.. code-block:: matlab

    franka_toolbox_uid_gen()

2. Obtain License
^^^^^^^^^^^^^^^^^
Contact Franka Robotics with your generated identifier to receive your license number.

3. Activate License
^^^^^^^^^^^^^^^^^^^
For Franka Research 3 robots:

.. code-block:: matlab

    franka_toolbox_install('<your_license_number>');

Uninstall
---------

1. Clean-up local permanent installation artifacts:

.. code-block:: matlab

    franka_toolbox_uninstall();

2. Remove the toolbox using MATLAB Add-Ons Manager.

.. figure:: _static/franka_toolbox_uninstall.png
    :align: center
    :figclass: align-center
    :scale: 60%

    Uninstalling the Franka Toolbox.

.. _libfranka_handling_options:

Switching to system-wide libfranka installation (optional)
----------------------------------------------------------

As mentioned in the :ref:`system_dependencies_precompiled_ai_companion` section, the Toolbox ships with a precompiled libfranka and all its 3d party dependencies for the Target PC.

In case of any potential issues with the Toolbox prebuilt dependencies, you can always manually build and install libfranka from source for your system.

In that case, please inform the Toolbox so it will opt for building against the system-wide libfranka installation by executing:

.. code-block:: matlab

    franka_toolbox_libfranka_system_installation_set(true);

This will trigger the Toolbox to build against the system-wide libfranka installation.

For reverting back to the local installation in the scope of the Toolbox, you can execute:

.. code-block:: matlab

    franka_toolbox_libfranka_system_installation_set(false);
