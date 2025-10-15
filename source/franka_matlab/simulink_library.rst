Fanka Library for Simulink - Reference
======================================

.. hint::
    Regarding the input/output signal nomenclature, datatypes, and sizes, the libfranka definitions
    have been fully adopted. You can find the complete list of signals
    `here <https://frankarobotics.github.io/libfranka/0.15.0/structfranka_1_1RobotState.html>`_.
    The column-major format for signals has been adopted as well.

Robot Control
-------------

.. figure:: _static/robot_control.png
    :align: center
    :figclass: align-center

    Robot Control Simulink Block.

This is the main block of the Franka Simulink Library. It is responsible for applying the desired robot parameters and control signals to the robot.

The robot settings can be applied through the block parameters.

.. figure:: _static/block_parameters_robot_control.png
    :align: center
    :figclass: align-center
    :width: 530px

    Robot Control Simulink Block Settings.

.. hint::
    If desired, an initial robot configuration can be applied **before** the main execution of the control loop.
    Namely, the robot will move to the desired configuration and only then the main execution of the Simulink model
    will take place. You can define that in the `Initial Configuration` section of the block settings.

Robot State
-----------

.. figure:: _static/get_robot_state.png
    :align: center
    :figclass: align-center

    Robot State Simulink Block.

For reading the desired set of signals stemming from the current robot state,
you can free-type the names of the signals in the `Parameters` pane of the block parameters.
For the set of available signals and their namings --> `Robot State Attributes <https://frankarobotics.github.io/libfranka/0.15.0/structfranka_1_1RobotState.html>`_

.. figure:: _static/get_robot_state_settings.png
    :align: center
    :figclass: align-center

    Get initial robot state Simulink Block Settings.

Duration Period
---------------

.. figure:: _static/duration.png
    :align: center
    :figclass: align-center

    Get duration from last main callback(Sample Time) Simulink Block.

This Simulink block outputs the duration from the last execution step in seconds. Ideally this should be always
0.001 seconds but due to lost packages during communication errors 0.002 secs or 0.003 secs could be seen.

.. warning::
    The step count of the Simulink model **does not change** during these communication mishaps. It continues to increment even though an execution step has been lost in reality. Therefore, special design considerations are necessary, especially for sensitive position motion generators. For example, refer to the `generate_cartesian_pose_motion.slx` demo to see how the main "clock" of the application has been designed.

Gripper State
-------------

.. figure:: _static/gripper_state.png
    :align: center
    :figclass: align-center

    Get current gripper state Simulink Block.

The gripper state block will inform the application about the current gripper state.

Vacuum Gripper State
--------------------

.. figure:: _static/vacuum_gripper_state.png
    :align: center
    :figclass: align-center
    :width: 300px

    Get current vacuum gripper state Simulink Block.

The vacuum gripper state block will inform the application about the current vacuum gripper state.

Mass Matrix
-----------

.. figure:: _static/mass_matrix.png
    :align: center
    :figclass: align-center

    Get the Mass Matrix of the Robot Model.

Coriolis
--------

.. figure:: _static/coriolis.png
    :align: center
    :figclass: align-center

    Get the Coriolis Matrix of the Robot Model.

Gravity
-------

.. figure:: _static/gravity.png
    :align: center
    :figclass: align-center

    Get the Gravity Vector of the Robot Model.


Jacobian
--------

.. figure:: _static/jacobian.png
    :align: center
    :figclass: align-center

    Get the Jabobian Matrix of the Robot.

You can select between "zero" or "body" Jacobian as well as the desired
frame inside the block parameters.

Pose
----

.. figure:: _static/pose.png
    :align: center
    :figclass: align-center

    Get the Robot Pose.

You can select the desired pose frame inside the block parameters.
