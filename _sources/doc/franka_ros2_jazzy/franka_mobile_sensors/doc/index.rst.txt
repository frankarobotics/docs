franka_mobile_sensors
=====================

Package Overview
----------------

This package contains launch files and run-time configurations for using sensors on Franka Robotics mobile research robots.
It provides integration for:

* **RealSense Cameras** - Intel RealSense depth cameras (D455)
* **SICK Safety Scanners** - SICK nanoScan3 safety lidars
* **Olive Robotics IMU** - Olive Robotics olixSense X1 IMU

The package handles sensor configuration, driver launching, and RViz visualization for the complete sensor suite.

Usage
-----

Launch the complete sensor suite with::

    ros2 launch franka_mobile_sensors franka_mobile_sensors.launch.py \
      robot_type:=<robot_type> \
      config_file:=<config_name>

Launch Arguments
^^^^^^^^^^^^^^^^

* ``start_cameras`` (default: ``true``) - Start RealSense camera drivers
* ``start_lidars`` (default: ``true``) - Start SICK safety scanner drivers
* ``start_rviz`` (default: ``true``) - Start RViz visualization
* ``robot_type`` (default: ``tmrv0_2``) - ID of the robot type for visualization
* ``config_file`` (default: ``default_sensor_suite``) - Sensor suite configuration (without .yaml extension)

Configuration
-------------

Sensor Suite Configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^

The main sensor suite is configured in:

* ``config/default_sensor_suite.yaml`` - Defines which sensors are used

This file specifies:

* List of cameras with their device profiles
* List of lidars with their device profiles
* Network configurations
* Sensor placement and mounting parameters

Device-Specific Parameters
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Individual device parameters are configured in device profile files:

**Cameras:**

* ``config/cameras/franka_mobile_d455.yaml`` - RealSense D455 parameters

**Lidars:**

* ``config/lidars/sick_nanoscan3.yaml`` - SICK nanoScan3 parameters

Custom Configurations
^^^^^^^^^^^^^^^^^^^^^

To create a custom configuration:

1. Copy ``config/default_sensor_suite.yaml`` to ``config/my_custom_suite.yaml``
2. Modify camera/lidar lists and reference existing or new device profiles
3. Launch with: ``config_file:=my_custom_suite``

Example
-------

To launch only cameras without lidars and RViz::

    ros2 launch franka_mobile_sensors franka_mobile_sensors.launch.py \
      start_cameras:=true \
      start_lidars:=false \
      start_rviz:=false

To use a custom sensor configuration::

    ros2 launch franka_mobile_sensors franka_mobile_sensors.launch.py \
      config_file:=my_custom_suite \
      robot_type:=tmrv0_2
