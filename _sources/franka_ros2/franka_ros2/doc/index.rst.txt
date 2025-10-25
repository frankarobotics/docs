franka_ros2
===========

.. note::

 ``franka_ros2`` is not supported on Windows.

You can access the changelog of franka_ros2 at `this link <https://github.com/frankarobotics/franka_ros2/blob/jazzy/CHANGELOG.rst>`_

The `franka_ros2 repo <https://github.com/frankarobotics/franka_ros2>`_ contains a ROS 2 integration of
libfranka.

.. caution::
    franka_ros2 is in rapid development. Anticipate breaking changes. Report bugs on
    `GitHub <https://github.com/frankarobotics/franka_ros2/issues>`_.


Installation
------------

Please refer to the `README.md <https://github.com/frankarobotics/franka_ros2/blob/humble/README.md>`_

MoveIt
------

To see if everything works, you can try to run the MoveIt example on the robot::

    ros2 launch franka_fr3_moveit_config moveit.launch.py robot_ip:=<fci-ip>

Then activate the ``MotionPlanning`` display in RViz.

If you do not have a robot you can still test your setup by running on a dummy hardware::

    ros2 launch franka_fr3_moveit_config moveit.launch.py robot_ip:=dont-care use_fake_hardware:=true


Wait until you can see the green ``You can start planning now!`` message from MoveIt inside the
terminal. Then turn off the ``PlanningScene`` and turn it on again. After that turn on the ``MotionPlanning``.

Namespace enabled launch files
------------------------------

To demonstrate how to launch the robot within a specified namespace, we provide an example launch file located at
``franka_bringup/launch/example.launch.py``.

By default ``example.launch.py`` file is configured to read essential robot configuration details from a YAML file, ``franka.ns-config.yaml``,
located in the franka_bringup/launch/ directory. You may provide a different YAML file by specifying the path to it in the command line.

For more details, see the franka_bringup documentation below.

Example Controllers
-------------------

This repo comes with a few example controllers located in the ``franka_example_controllers`` package.

For a comprehensive list of available controllers and their usage, see the franka_example_controllers documentation below.

Package Descriptions
--------------------

This section contains more detailed descriptions of what each package does. In general the package structure tries to
adhere to the structure that is proposed
`here <https://rtw.stoglrobotics.de/master/guidelines/robot_package_structure.html>`_.

.. toctree::
   :maxdepth: 1

   ../../franka_bringup/doc/index
   ../../franka_example_controllers/doc/index
   ../../franka_hardware/doc/index
   ../../franka_semantic_components/doc/index
   ../../franka_gripper/doc/index
   ../../franka_robot_state_broadcaster/doc/index
   ../../franka_fr3_moveit_config/doc/index
   ../../franka_gazebo/doc/index
   ../../franka_msgs/doc/index