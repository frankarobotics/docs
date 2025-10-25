System Requirements
===================

Host PC Requirements
--------------------

MATLAB Toolbox Dependencies
^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following Mathworks products are required for the Host PC: 

* `MATLAB <https://www.mathworks.com/products/matlab.html>`_
* `Simulink <https://www.mathworks.com/products/simulink.html>`_
* `Simulink Coder <https://www.mathworks.com/products/simulink-coder.html>`_
* `Matlab Coder <https://www.mathworks.com/products/matlab-coder.html>`_

Some of demos provided with the franka_matlab need the following toolboxes:

* `Stateflow <https://www.mathworks.com/products/stateflow.html>`_ (required for the Simulink Example grasp_object.slx)
* `Matlab Robotics Toolbox <https://www.mathworks.com/products/robotics.html>`_ (required for the MATLAB example pick_and_place_with_RRT.mlx)

MATLAB Coder Support Package for NVIDIA Jetson
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
**For working with the Franka AI Companion & NVIDIA Jetson platforms** please download and install the `MATLAB Coder Support Package for NVIDIA Jetson and NVIDIA DRIVE Platforms <https://www.mathworks.com/matlabcentral/fileexchange/68644-matlab-coder-support-package-for-nvidia-jetson-and-nvidia-drive-platforms>`_.

MATLAB Support Package for Linux
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
In case of Ubuntu Target PC, it is highly recommended to install the `matlab-support package <https://packages.ubuntu.com/search?keywords=matlab-support>`_ 
in order for Matlab to reference the system dynamic libraries instead of the precompiled ones that it ships with:

.. code-block:: shell

    sudo apt install matlab-support

Target PC Requirements
----------------------

The Target PC is responsible for maintaing the real-time 1kHz control loop,
all the same system requirements for running libfranka apply.

.. _system_dependencies_precompiled_ai_companion:

Precompiled libfranka and 3d party dependencies for the Target PC
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The Franka Toolbox for MATLAB ships with a precompiled libfranka and all its 3d party dependencies for the Target PC and it should be able to execute out-of-the-box without additional installations,
given that the Target PC is running a supported version of Ubuntu as defined below.

+-------------------------+---------------------------------------------+----------------------------------------------+
| Franka Toolbox Version  | AI Companion/Jetson Orin Platform           |  Real-Time kernel Linux Host PC as Target PC |
+=========================+=============================================+==============================================+
| 3.0.0                   | Ubuntu 22.04 LTS                            |  Ubuntu 22.04 LTS                            |
+-------------------------+---------------------------------------------+----------------------------------------------+

.. warning::

    In case of an alternative Target PC OS version, or in case of any issue with the Toolbox prebuilt dependencies, you can always manually build and install libfranka from source for your system.
    Check the section :ref:`libfranka handling options for Target PC<libfranka_handling_options>` for more details, after the Toolbox installation steps.
