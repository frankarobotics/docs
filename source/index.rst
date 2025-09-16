Franka Control Interface Documentation
======================================

.. note::

  The software and its documentation support two different robots, the
  `Franka Research 3 (FR3) <https://franka.de/research>`_ and an older Franka Robotics Robot (FER or Panda).

.. todolist::

The Franka Control Interface (FCI) can be accessed via several open source components which we
provide on `GitHub <https://github.com/frankarobotics>`_. We welcome contributions and suggestions
for improvements.

These components are:

 * ``libfranka``, a C++ library that provides low-level control of Franka Robotics research robots.
   Its source code is available at https://github.com/frankarobotics/libfranka. API documentation is
   available at https://frankarobotics.github.io/libfranka.
 * ``franka_ros``, our `ROS integration <https://wiki.ros.org/franka_ros>`_, including support for
   ROS Control and MoveIt!. It also contains ``franka_description``, a collection of URDF models and
   3D meshes that can be useful outside of ROS.
   The repository is available at https://github.com/frankarobotics/franka_ros.
 * ``franka_ros2`` The repository is available at https://github.com/frankarobotics/franka_ros2.
 * ``Franka MATLAB®`` provides a Simulink and a Matlab API, together with helper functions and tools,
   for rapid-prototyping in Real-Time on the Franka Robot"
   Franka MATLAB® artifacts can be obtained at `Franka World <https://franka.world/>`_.

The source code of this documentation is also `available online
<https://github.com/frankarobotics/docs>`_.

.. important::
    Before you start using the FCI, please read through the documents shipped with the robot and
    the :doc:`requirements` chapter.

.. note::
    Using a robot with system version 4.2.0 or higher requires to enable the FCI mode. To do that
    open Desk -> expand the menu in the sidebar -> press `'Activate FCI'`. Further information
    about Single Point of Control (SPoC) can be found in the manual shipped with the robot.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   overview
   requirements
   compatibility
   installation_linux
   getting_started
   libfranka
   franka_ros
   franka_ros2/docs/index
   franka_matlab/index
   franka_matlab/franka_matlab_changelog
   control_parameters
   fr3-certification-remarks
   troubleshooting
   faq
