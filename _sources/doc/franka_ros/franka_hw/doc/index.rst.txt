.. _franka_hw:

franka_hw
---------
This package contains the hardware abstraction of the robot for the ROS control framework
based on the ``libfranka`` API. The hardware class ``franka_hw::FrankaHW`` is implemented in this
package offering the following interfaces to controllers:

+-------------------------------------------------+----------------------------------------------+
|                    Interface                    |                   Function                   |
+=================================================+==============================================+
| ``hardware_interface::JointStateInterface``     | Reads joint states.                          |
+-------------------------------------------------+----------------------------------------------+
| ``hardware_interface::VelocityJointInterface``  | Commands joint velocities and reads joint    |
|                                                 | states.                                      |
+-------------------------------------------------+----------------------------------------------+
| ``hardware_interface::PositionJointInterface``  | Commands joint positions and reads joint     |
|                                                 | states.                                      |
+-------------------------------------------------+----------------------------------------------+
| ``hardware_interface::EffortJointInterface``    | Commands joint-level torques and reads       |
|                                                 | joint states.                                |
+-------------------------------------------------+----------------------------------------------+
| ``franka_hw::FrankaStateInterface``             | Reads the full robot state.                  |
+-------------------------------------------------+----------------------------------------------+
| ``franka_hw::FrankaPoseCartesianInterface``     | Commands Cartesian poses and reads the full  |
|                                                 | robot state.                                 |
+-------------------------------------------------+----------------------------------------------+
| ``franka_hw::FrankaVelocityCartesianInterface`` | Commands Cartesian velocities and reads the  |
|                                                 | full robot state.                            |
+-------------------------------------------------+----------------------------------------------+
| ``franka_hw::FrankaModelInterface``             | Reads the dynamic and kinematic model of the |
|                                                 | robot.                                       |
+-------------------------------------------------+----------------------------------------------+

To use ROS control interfaces, you have to retrieve resource handles by name:

+-------------------------------------------------+----------------------------------------+
|                    Interface                    |          Resource handle name          |
+=================================================+========================================+
| ``hardware_interface::JointStateInterface``     | "<arm_id>_joint1" to "<arm_id>_joint7" |
+-------------------------------------------------+----------------------------------------+
| ``hardware_interface::VelocityJointInterface``  | "<arm_id>_joint1" to "<arm_id>_joint7" |
+-------------------------------------------------+----------------------------------------+
| ``hardware_interface::PositionJointInterface``  | "<arm_id>_joint1" to "<arm_id>_joint7" |
+-------------------------------------------------+----------------------------------------+
| ``hardware_interface::EffortJointInterface``    | "<arm_id>_joint1" to "<arm_id>_joint7" |
+-------------------------------------------------+----------------------------------------+
| ``franka_hw::FrankaStateInterface``             | "<arm_id>_robot"                       |
+-------------------------------------------------+----------------------------------------+
| ``franka_hw::FrankaPoseCartesianInterface``     | "<arm_id>_robot"                       |
+-------------------------------------------------+----------------------------------------+
| ``franka_hw::FrankaVelocityCartesianInterface`` | "<arm_id>_robot"                       |
+-------------------------------------------------+----------------------------------------+
| ``franka_hw::FrankaModelInterface``             | "<arm_id>_robot"                       |
+-------------------------------------------------+----------------------------------------+

.. hint::

    By default, <arm_id> is set to "panda".

The ``franka_hw::FrankaHW`` class also implements the starting, stopping and switching of
controllers.

The ``FrankaHW`` class also serves as base class for ``FrankaCombinableHW``, a hardware class that
can be combined with others to control multiple robots from a single controller. The combination of
an arbitrary number of Panda robots (number configured by parameters) based on ``FrankaCombinableHW``
for the ROS control framework `<https://github.com/ros-controls/ros_control>`_ is implemented
in ``FrankaCombinedHW``. The key-difference between ``FrankaHW`` and ``FrankaCombinedHW`` is
that the latter supports torque control only.

.. important::

  The ``FrankaCombinableHW`` class is available from version 0.7.0 and allows torque/effort control only.

The ROS parameter server is used to determine at runtime which robots are loaded in the combined
class. For an example on how to configure the ``FrankaCombinedHW`` in the according hardware node,
see :ref:`franka_control <franka_control>`.

.. note::

   The approach of ``FrankaHW`` is optimal for controlling single robots. Thus we recommend using
   the ``FrankaCombinableHW``/``FrankaCombinedHW`` classes only for controlling multiple robots.

The interfaces offered by the ``FrankaCombinableHW``/``FrankaCombinedHW`` classes are the following:

+-------------------------------------------------+----------------------------------------------+
|                    Interface                    |                   Function                   |
+=================================================+==============================================+
| ``hardware_interface::EffortJointInterface``    | Commands joint-level torques and reads       |
|                                                 | joint states.                                |
+-------------------------------------------------+----------------------------------------------+
| ``hardware_interface::JointStateInterface``     | Reads joint states.                          |
+-------------------------------------------------+----------------------------------------------+
| ``franka_hw::FrankaStateInterface``             | Reads the full robot state.                  |
+-------------------------------------------------+----------------------------------------------+
| ``franka_hw::FrankaModelInterface``             | Reads the dynamic and kinematic model of the |
|                                                 | robot.                                       |
+-------------------------------------------------+----------------------------------------------+

The only admissible command interface claim is the ``EffortJointInterface`` which can be combined
with any set of read-only-interfaces (``FrankaModelInterface``, ``JointStateInterface``,
``FrankaStateInterface``). The resource handles offered by all interfaces are claimed by name and
follow the same naming conventions as described for `FrankaHW`. Every instance of
``FrankaCombinableHW`` offers the complete set of service and action interfaces
(see :ref:`franka_control <franka_control>`).

.. note::

   The ``FrankaCombinedHW`` class offers an additional action server in the control node namespace
   to recover all robots. If a reflex or error occurs on any of the robots, the control loop of all
   robots stops until they are recovered.

.. important::

    ``FrankaHW`` makes use of the ROS `joint_limits_interface <http://wiki.ros.org/ros_control#Joint_limits_interface>`_
    to `enforce position, velocity and effort safety limits
    <http://wiki.ros.org/pr2_controller_manager/safety_limits>`_.
    The utilized interfaces are listed below:

     * joint_limits_interface::PositionJointSoftLimitsInterface
     * joint_limits_interface::VelocityJointSoftLimitsInterface
     * joint_limits_interface::EffortJointSoftLimitsInterface

    Approaching the limits will result in the (unannounced) modification of the commands.
