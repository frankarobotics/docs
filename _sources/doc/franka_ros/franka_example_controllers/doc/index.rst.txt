.. _example_controllers:

franka_example_controllers
--------------------------
In this package a set of example controllers for controlling the robot via ROS are implemented.
The controllers depict the variety of interfaces offered by the ``franka_hw::FrankaHW`` class and
the according usage. Each example comes with a separate stand-alone launch file that starts the
controller on the robot and visualizes it.

To launch the joint impedance example, execute the following command:

.. code-block:: shell

    roslaunch franka_example_controllers joint_impedance_example_controller.launch \
      robot_ip:=<fci-ip> load_gripper:=<true|false> robot:=<panda|fr3>

Other single Panda examples are started in the same way.

The ``dual_arm_cartesian_impedance_example_controller`` showcases the control of two Panda robots
based on ``FrankaCombinedHW`` using one realtime controller for fulfilling Cartesian tasks with
an impedance-based control approach. The example controller can be launched with

.. code-block:: shell

  roslaunch franka_example_controllers \
      dual_arm_cartesian_impedance_example_controller.launch \
      robot_id:=<name_of_the_2_arm_setup> \
      robot_ips:=<your_robot_ips_as_a_map> \
      rviz:=<true/false> rqt:=<true/false>

The example assumes a robot configuration according to `dual_panda_example.urdf.xacro` where two
Pandas are mounted at 1 meter distance on top of a box. Feel free to replace this robot description
with one that matches your setup.
The option `rviz` allows to choose whether a visualization should be launched. With `rqt` the user
can choose to launch an rqt-gui which allows an online adaption of the rendered end-effector
impedances at runtime via dynamic reconfigure.
