franka_fr3_moveit_config
========================

This package contains the configuration for MoveIt2.

Move Groups
-----------

There is a new move group called ``panda_manipulator`` that has its tip between the fingers of the gripper and has its Z-axis rotated by -45 degrees, so
that the X-axis is now facing forward, making it easier to use. The ``panda_arm`` move group is still available
for backward compatibility. New applications should use the new ``panda_manipulator`` move group instead.

.. figure:: ../../docs/assets/move-groups.png
    :align: center
    :figclass: align-center

    Visualization of the old and the new move group

Usage
-----

To see if everything works, you can try to run the MoveIt example on the robot::

    ros2 launch franka_fr3_moveit_config moveit.launch.py robot_ip:=<fci-ip>

Then activate the ``MotionPlanning`` display in RViz.

If you do not have a robot you can still test your setup by running on a dummy hardware::

    ros2 launch franka_fr3_moveit_config moveit.launch.py robot_ip:=dont-care use_fake_hardware:=true

Wait until you can see the green ``You can start planning now!`` message from MoveIt inside the
terminal. Then turn off the ``PlanningScene`` and turn it on again. After that turn on the ``MotionPlanning``.

Configuration Files
-------------------

This package includes:

* Motion planning configuration for the FR3 robot
* Joint limits and safety settings
* Planning groups and link configurations
* Kinematics solver configuration (kinematics.yaml)

For the Joint Impedance With IK Example controller, you can change the kinematic solver
in this package's kinematics.yaml file.