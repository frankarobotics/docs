franka_robot_state_broadcaster
==============================

This package contains read-only franka_robot_state_broadcaster controller.

Functionality
-------------

The broadcaster publishes franka_robot_state topic to the topic named `/franka_robot_state_broadcaster/robot_state`.
This controller node is spawned by franka_launch.py in the franka_bringup.
Therefore, all the examples that include the franka_launch.py publishes the robot_state topic.

Usage
-----

The robot state broadcaster is automatically started when you launch the robot using:

.. code-block:: shell

    ros2 launch franka_bringup franka.launch.py robot_ip:=<fci-ip>

Published Topics
----------------

* `/franka_robot_state_broadcaster/robot_state` (franka_msgs/FrankaRobotState): Contains comprehensive robot state information including joint states, Cartesian pose, and other robot-specific data.

Integration
-----------

This broadcaster integrates with the :doc:`franka_semantic_components <../../franka_semantic_components/doc/index>` package to provide safe access to robot state information for controllers and other nodes.