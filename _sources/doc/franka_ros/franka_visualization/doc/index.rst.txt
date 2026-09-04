.. _franka_visualization:
.. _ros_visualization:

franka_visualization
--------------------
This package contains publishers that connect to a robot and publish the robot and
gripper joint states for visualization in RViz. To run this package launch:

.. code-block:: shell

    roslaunch franka_visualization franka_visualization.launch robot_ip:=<fci-ip> \
      load_gripper:=<true|false> robot:=<panda|fr3>


This is purely for visualization - no commands are sent to the robot. It can be useful to check the
connection to the robot.

.. important::

    Only one instance of a ``franka::Robot`` can connect to the robot. This means, that for example
    the ``franka_joint_state_publisher`` cannot run in parallel to the ``franka_control_node``.
    This also implies that you cannot execute the visualization example alongside a separate
    program running a controller.
