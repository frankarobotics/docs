Franka Toolbox for MATLAB
=========================

The Franka Toolbox for MATLAB provides libraries and tools that integrate Franka robots with the MathWorks® software ecosystem.

.. figure:: _static/hardware_config_options.png
    :align: center
    :figclass: align-center

    Hardware/Software configuration options for the Franka Toolbox for MATLAB.

The toolbox comprises two main components:

* ``Franka Library for Simulink``, a set of Simulink blocks for interfacing the Franka Robot through automatic C++ code gen with Simulink Coder. The library mainly aims at assisting with the rapid-development of advanced robot controllers.

.. figure:: _static/simulink_library_browser.png
    :align: center
    :figclass: align-center

    Simulink Library for rapid-prototyping of controllers for the Franka Robot.

* ``Franka Library for MATLAB``, which provides the `FrankaRobot()` MATLAB class for directly interfacing the Franka Robot.

.. figure:: _static/matlab_pick_and_place_with_RRT_demo.png
    :align: center
    :figclass: align-center

    Example of a pick-and-place operation using RRT (Rapidly-exploring Random Tree) implemented in MATLAB Live Script.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   compatibility
   system_requirements
   installation
   getting_started
   simulink_library
   matlab_library
   troubleshooting
