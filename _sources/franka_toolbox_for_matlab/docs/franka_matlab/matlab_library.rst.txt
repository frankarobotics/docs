.. _matlab-library:

Franka Library for MATLAB - Reference
=====================================

FrankaRobot Class
-----------------

The ``FrankaRobot`` constructor initializes a connection to the Franka robot. It can be configured for two primary scenarios: connecting to a robot on a local network (Host PC) or connecting to a robot via an external AI companion computer like a Jetson.

**Local Host PC as Target PC**

.. code-block:: matlab

    fr = FrankaRobot('RobotIP', '172.16.0.2');

**Connecting via AI Companion/NVIDIA Jetson**

When using an external Target PC to control the robot, you must provide connection details for that computer, including its IP address and a username.

.. warning::

    Before attempting to connect to the robot via an external AI companion or NVIDIA Jetson, 
    ensure that you have copied your SSH key to the target PC, e.g with ``ssh-copy-id`` for Linux. 
    This step is crucial for establishing an SSH connection without requiring a password each time.

.. code-block:: matlab

    fr = FrankaRobot('RobotIP', '172.16.0.2', ...
                     'Username', 'jetson_user', ...
                     'ServerIP', '192.168.1.100');

All constructor parameters are optional and have default values.

Parameters:
    - RobotIP: IP address of the Franka robot (default: '172.16.0.2')
    - Username: Username for the server on the AI companion (default: 'franka')
    - ServerIP: IP address of the server on the AI companion (default: '172.16.1.2')
    - SSHPort: SSH port for server connection (default: '22')
    - ServerPort: Server port for communication (default: '5001')

Automatic Error Recovery
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: matlab

    fr.automatic_error_recovery();

Attempts an automatic error recovery of the robot.

Get Joint Poses
^^^^^^^^^^^^^^^

.. code-block:: matlab

    jp = fr.joint_poses();

Returns a 7-element array with the current robot joint poses.

Get Robot State
^^^^^^^^^^^^^^^

.. code-block:: matlab

    rs = fr.robot_state();

Returns a struct with the current robot state.

Joint Point to Point Motion
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: matlab

    fr.joint_point_to_point_motion(joints_target_configuration, speed_factor);

Moves the robot into a desired joint configuration.

Parameters:
    - joints_target_configuration: 7-element double array with target configuration
    - speed_factor: Scalar between 0 and 1 (default: 0.5)

Joint Trajectory Motion
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: matlab

    fr.joint_trajectory_motion(positions);

Moves the robot based on the given desired joint trajectory.

Parameters:
    - positions: 7xN double array with desired joint trajectory

.. warning::
    Make sure that the current configuration of the robot matches the initial trajectory element `q(1:7,1)` that is passed in the function! Additionally make sure that
    the given trajectory is sufficiently smooth and continuous.

Collision Thresholds
^^^^^^^^^^^^^^^^^^^^

.. code-block:: matlab

    fr.setCollisionThresholds(thresholds);
    thresholds = fr.getCollisionThresholds();

Sets or gets the collision thresholds for the robot.

Parameters:
    - thresholds: Struct containing collision threshold parameters

Load Inertia
^^^^^^^^^^^^

.. code-block:: matlab

    fr.setLoadInertia(loadInertia);
    inertia = fr.getLoadInertia();

Sets or gets the load inertia parameters for the robot.

Parameters:
    - loadInertia: Struct containing mass, center of mass, and inertia matrix

Robot Homing
^^^^^^^^^^^^

.. code-block:: matlab

    result = fr.robot_homing();

Moves the robot to its home configuration using point-to-point motion.

Returns:
    - true if the motion was successful, false otherwise

Reset Settings
^^^^^^^^^^^^^^

.. code-block:: matlab

    fr.resetSettings();

Resets all robot settings to their default values.

Gripper Control
^^^^^^^^^^^^^^^

The FrankaRobot class provides access to both standard and vacuum grippers through the following properties:

.. code-block:: matlab

    fr.Gripper        % Standard gripper interface
    fr.VacuumGripper  % Vacuum gripper interface

See the respective gripper class documentation for available methods.

FrankaGripper Class
-------------------

The ``FrankaGripper`` class is accessed through the ``Gripper`` property of a ``FrankaRobot`` instance.

Get Gripper State
^^^^^^^^^^^^^^^^^

.. code-block:: matlab

    state = fr.Gripper.state();

Returns a struct with the current gripper state.

Gripper Homing
^^^^^^^^^^^^^^

.. code-block:: matlab

    result = fr.Gripper.homing();

Performs gripper homing. Returns true if successful.

Grasp Object
^^^^^^^^^^^^

.. code-block:: matlab

    result = fr.Gripper.grasp(width, speed, force, epsilon_inner, epsilon_outer);

Grasps an object with the specified width.

Parameters:
    - width: Target width in meters.
    - speed: Speed of the motion (default: 0.1).
    - force: Grasping force in N (default: 50).
    - epsilon_inner: Inner epsilon for grasping (default: 0.1).
    - epsilon_outer: Outer epsilon for grasping (default: 0.1).

Returns:
    - true if grasping was successful, false otherwise.

Move Gripper
^^^^^^^^^^^^

.. code-block:: matlab

    result = fr.Gripper.move(width, speed);

Moves the gripper to a specific width.

Parameters:
    - width: Target width in meters.
    - speed: Speed of the motion (default: 0.1).

Returns:
    - true if motion was successful, false otherwise.

Stop Gripper
^^^^^^^^^^^^

.. code-block:: matlab

    result = fr.Gripper.stop();

Stops the gripper motion. Returns true if successful.

FrankaVacuumGripper Class
-------------------------

The ``FrankaVacuumGripper`` class is accessed through the ``VacuumGripper`` property of a ``FrankaRobot`` instance.

Get Vacuum Gripper State
^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: matlab

    state = fr.VacuumGripper.state();

Returns a struct with the current vacuum gripper state, including vacuum level and part presence.

Apply Vacuum
^^^^^^^^^^^^

.. code-block:: matlab

    result = fr.VacuumGripper.vacuum(control_point, timeout, profile);

Applies vacuum to the gripper.

Parameters:
    - control_point: Vacuum control point (default: 0).
    - timeout: Timeout in milliseconds (default: 5000).
    - profile: Production setup profile (default: 0).

Returns:
    - true if vacuum was successfully applied, false otherwise.

Drop Off
^^^^^^^^

.. code-block:: matlab

    result = fr.VacuumGripper.dropOff(timeout);

Drops off the currently held object.

Parameters:
    - timeout: Timeout in milliseconds (default: 5000).

Returns:
    - true if drop off was successful, false otherwise.

Stop Vacuum Gripper
^^^^^^^^^^^^^^^^^^^

.. code-block:: matlab

    result = fr.VacuumGripper.stop();

Stops the vacuum gripper. Returns true if successful.