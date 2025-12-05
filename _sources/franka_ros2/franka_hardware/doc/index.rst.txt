franka_hardware
===============

.. important::
    Breaking changes as of 0.1.14 release: ``franka_hardware`` robot_state and robot_model will be prefixed by the ``arm_id``.

        - ``panda/robot_model  -> ${arm_id}/robot_model``
        - ``panda/robot_state  -> ${arm_id}/robot_state``

    There is no change with the state and command interfaces naming. They are prefixed with the joint names in the URDF.

Package Overview
----------------

This package contains the ``franka_hardware`` plugin needed for `ros2_control <https://control.ros.org/jazzy/index.html>`_.
The plugin is loaded from the URDF of the robot and passed to the controller manager via the robot description.

Hardware Interfaces
--------------------

The hardware plugin provides for each joint:

* a ``position state interface`` that contains the measured joint position.
* a ``velocity state interface`` that contains the measured joint velocity.
* an ``effort state interface`` that contains the measured link-side joint torques.
* an ``initial_position state interface`` that contains the initial joint position of the robot.
* an ``effort command interface`` that contains the desired joint torques without gravity.
* a  ``position command interface`` that contains the desired joint position.
* a  ``velocity command interface`` that contains the desired joint velocity.

Additional State Interfaces
---------------------------

In addition to joint interfaces, the hardware plugin provides:

* a ``franka_robot_state`` that contains the robot state information, `franka_robot_state <https://shorturl.at/wajZV>`_.
* a ``franka_robot_model_interface`` that contains the pointer to the model object.

.. important::
    ``franka_robot_state`` and ``franka_robot_model_interface`` state interfaces should not be used directly from hardware state interface.
    Rather, they should be utilized by the :doc:`franka_semantic_components <../../franka_semantic_components/doc/index>` interface.

Configuration
-------------

The IP of the robot is read over a parameter from the URDF.

Usage with Controllers
----------------------

Controllers can access these interfaces through the standard ros2_control framework. For examples of how to use these interfaces in practice, see the :doc:`franka_example_controllers <../../franka_example_controllers/doc/index>` package.