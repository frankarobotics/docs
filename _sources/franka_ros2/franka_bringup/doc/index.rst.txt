franka_bringup
==============

.. note::

 ``franka_ros2`` is not supported on Windows.

The `franka_ros2 repo <https://github.com/frankarobotics/franka_ros2>`_ contains a ROS 2 integration of
`libfranka <https://frankarobotics.github.io/libfranka/>`_.

.. caution::
    franka_ros2 is in rapid development. Anticipate breaking changes. Report bugs on
    `GitHub <https://github.com/frankarobotics/franka_ros2/issues>`_.

Installation
------------

Please refer to the `README.md <https://github.com/frankarobotics/franka_ros2/blob/jazzy/README.md>`_

Package Overview
----------------

This package contains the launch files for the examples as well as the basic ``franka.launch.py`` launch file, that
can be used to start the robot without any controllers.

When you start the robot with::

    ros2 launch franka_bringup franka.launch.py arm_id:=fr3 robot_ip:=<fci-ip> use_rviz:=true

There is no controller running apart from the ``joint_state_broadcaster``. However, a connection with the robot is still
established and the current robot pose is visualized in RViz. In this mode the robot can be guided when the user stop
button is pressed. However, once a controller that uses the ``effort_command_interface`` is started, the robot will be
using the torque interface from libfranka. For example it is possible to launch the
``gravity_compensation_example_controller`` by running::

    ros2 control load_controller --set-state active  gravity_compensation_example_controller

This is the equivalent of running the ``gravity_compensation_example_controller`` example mentioned in
:doc:`Gravity Compensation <../../franka_example_controllers/doc/index>`.

When the controller is stopped with::

    ros2 control set_controller_state gravity_compensation_example_controller inactive

the robot will stop the torque control and will only send its current state over the FCI.

You can now choose to start the same controller again with::

    ros2 control set_controller_state gravity_compensation_example_controller active

or load and start a different one::

    ros2 control load_controller --set-state active joint_impedance_example_controller


Namespace enabled launch files
------------------------------

To demonstrate how to launch the robot within a specified namespace, we provide an example launch file located at
``franka_bringup/launch/example.launch.py``.

By default ``example.launch.py`` file is configured to read essential robot configuration details from a YAML file, ``franka.ns-config.yaml``,
located in the franka_bringup/launch/ directory. You may provide a different YAML file by specifying the path to it in the command line.

``franka.ns-config.yaml`` file specifies critical parameters, including:

* The path to the robot's URDF file.
* The namespace to be used for the robot instance.
* Additional configuration details specific to the robot instance.

example.launch.py "includes" ``franka.ns-launch.py`` which defines the core nodes typically required for robot operation..

The franka.ns-launch.py file, in turn, relies on ``ns-controllers.yaml`` to configure the ros2_controller framework.
This configuration ensures that controllers are loaded in a namespace-agnostic manner, supporting consistent behavior across multiple namespaces.

The ns-controllers.yaml file is designed to accommodate zero or more namespaces, provided all namespaces share the same node configuration parameters.

Each of the configuration and launch files (franka.ns-config.yaml, example.launch.py, franka.ns-launch.py, and ns-controllers.yaml)
contains detailed inline documentation to guide users through their structure and usage.  Further information about namespaces in ROS 2 can be found in the
`ROS 2 documentation <https://docs.ros.org/en/jazzy/Tutorials/Intermediate/Launch/Using-ROS2-Launch-For-Large-Projects.html#namespaces>`_.

To execute any of the example controllers defined in ns-controllers.yaml, you can use the example.launch.py launch file and specify
the desired controller name as a command-line argument.

First - modify ``franka.ns-config.yaml`` as appropriate for your setup.

Then, for example, to run the *move_to_start_example_controller*, use the following command:

.. code-block:: shell

    ros2 launch franka_bringup example.launch.py controller_name:=move_to_start_example_controller

Non-realtime robot parameter setting
------------------------------------

Non-realtime robot parameter setting can be done via ROS 2 services. They are advertised after the robot hardware is initialized.

Service names are given below::

 * /service_server/set_cartesian_stiffness
 * /service_server/set_force_torque_collision_behavior
 * /service_server/set_full_collision_behavior
 * /service_server/set_joint_stiffness
 * /service_server/set_load
 * /service_server/set_parameters
 * /service_server/set_parameters_atomically
 * /service_server/set_stiffness_frame
 * /service_server/set_tcp_frame

Service message descriptions are given below.

 * ``franka_msgs::srv::SetJointStiffness`` specifies joint stiffness for the internal controller
   (damping is automatically derived from the stiffness).
 * ``franka_msgs::srv::SetCartesianStiffness`` specifies Cartesian stiffness for the internal
   controller (damping is automatically derived from the stiffness).
 * ``franka_msgs::srv::SetTCPFrame`` specifies the transformation from <arm_id>_EE (end effector) to
   <arm_id>_NE (nominal end effector) frame. The transformation from flange to end effector frame
   is split into two transformations: <arm_id>_EE to <arm_id>_NE frame and <arm_id>_NE to
   <arm_id>_link8 frame. The transformation from <arm_id>_NE to <arm_id>_link8 frame can only be
   set through the administrator's interface.
 * ``franka_msgs::srv::SetStiffnessFrame`` specifies the transformation from <arm_id>_K to <arm_id>_EE frame.
 * ``franka_msgs::srv::SetForceTorqueCollisionBehavior`` sets thresholds for external Cartesian
   wrenches to configure the collision reflex.
 * ``franka_msgs::srv::SetFullCollisionBehavior`` sets thresholds for external forces on Cartesian
   and joint level to configure the collision reflex.
 * ``franka_msgs::srv::SetLoad`` sets an external load to compensate (e.g. of a grasped object).

Launch franka_bringup/franka.launch.py file to initialize robot hardware::

    ros2 launch franka_bringup franka.launch.py robot_ip:=<fci-ip>

Here is a minimal example:

.. code-block:: shell

    ros2 service call /service_server/set_joint_stif
    fness franka_msgs/srv/SetJointStiffness "{joint_stiffness: [1000.0, 1000.0, 10
    00.0, 1000.0, 1000.0, 1000.0, 1000.0]}"

.. important::

    Non-realtime parameter setting can only be done when the robot hardware is in `idle` mode.
    If a controller is active and claims command interface this will put the robot in the `move` mode.
    In `move` mode non-realtime param setting is not possible.

.. important::

    The <arm_id>_EE frame denotes the part of the
    configurable end effector frame which can be adjusted during run time through `franka_ros`. The
    <arm_id>_K frame marks the center of the internal
    Cartesian impedance. It also serves as a reference frame for external wrenches. *Neither the
    <arm_id>_EE nor the <arm_id>_K are contained in the URDF as they can be changed at run time*.
    By default, <arm_id> is set to "panda".

    .. figure:: ../../docs/assets/frames.svg
        :align: center
        :figclass: align-center

        Overview of the end-effector frames.

Non-realtime ROS 2 actions
--------------------------

Non-realtime ROS 2 actions can be done via the `ActionServer`. Following actions are available:

* ``/action_server/error_recovery`` - Recovers automatically from a robot error.

The used messages are:

* ``franka_msgs::action::ErrorRecovery`` - no parameters.

Example usage:::

    ros2 action send_goal /action_server/error_recovery franka_msgs/action/ErrorRecovery {}

Known Issues
------------

* When using the ``fake_hardware`` with MoveIt, it takes some time until the default position is applied.