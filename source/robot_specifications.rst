.. _control_interface_specifications:

=============================================
Control Interface Specification and Robot Limits
=============================================

.. _overview:

Overview
--------

Realtime control commands sent to the robot must satisfy a set of *recommended* and
*necessary* conditions. Recommended conditions ensure optimal and stable behavior,
while necessary conditions are strict safety and feasibility requirements. Violating
any necessary condition results in an immediate motion abort.

The executed robot trajectory is based on the user-defined trajectory but adjusted
to ensure that recommended conditions are respected. As long as all necessary
conditions are satisfied, the robot will follow the commanded trajectory; however,
it will only match it exactly if the recommended conditions are also fulfilled.

If a necessary condition is violated, the system raises an error and stops the
motion. For example, if the first point of a user-provided joint trajectory differs
too much from the robot's actual start configuration
(:math:`q(t=0) \neq q_c(t=0)`), a ``start_pose_invalid`` error is triggered.

All constants referenced in the equations below are provided in the
`Limits for Franka Emika Robot (FER)`_ and `Limits for Franka Research 3 (FR3)`_
sections.

.. _control_modes:

Control Modes
-------------

.. _joint_space_control:

Joint Space Control Requirements
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. _joint_space_necessary:

Necessary Conditions
""""""""""""""""""""

- :math:`q_{min} < q_c < q_{max}`
- :math:`-\dot{q}_{max} < \dot{q}_c < \dot{q}_{max}`
- :math:`-\ddot{q}_{max} < \ddot{q}_c < \ddot{q}_{max}`
- :math:`-\dddot{q}_{max} < \dddot{q}_c < \dddot{q}_{max}`

.. _joint_space_recommended:

Recommended Conditions
""""""""""""""""""""""

- :math:`-{\tau_j}_{max} < {\tau_j}_d < {\tau_j}_{max}`
- :math:`-\dot{\tau_j}_{max} < \dot{\tau_j}_d < \dot{\tau_j}_{max}`

.. _joint_space_initial:

Initial trajectory requirements:

- :math:`q = q_c`
- :math:`\dot{q}_c = 0`
- :math:`\ddot{q}_c = 0`

.. _joint_space_final:

Final trajectory requirements:

- :math:`\dot{q}_c = 0`
- :math:`\ddot{q}_c = 0`

.. _torque_control:

Torque Control Requirements
""""""""""""""""""""""""""""

.. _torque_necessary:

Necessary Conditions
''''''''''''''''''''

- :math:`-\dot{\tau_j}_{max} < \dot{{\tau_j}_d} < \dot{\tau_j}_{max}`

.. _torque_recommended:

Recommended Conditions
''''''''''''''''''''''

- :math:`-{\tau_j}_{max} < {\tau_j}_d < {\tau_j}_{max}`

.. _torque_initial:

Initial controller requirements:

- :math:`{\tau_j}_d = 0`

.. _cartesian_space_control:

Cartesian Space Control Requirements
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. _cartesian_space_necessary:

Necessary Conditions
""""""""""""""""""""

- :math:`T` is a proper transformation matrix.
- :math:`-\dot{p}_{max} < \dot{p}_c < \dot{p}_{max}` (Cartesian velocity)
- :math:`-\ddot{p}_{max} < \ddot{p}_c < \ddot{p}_{max}` (Cartesian acceleration)
- :math:`-\dddot{p}_{max} < \dddot{p}_c < \dddot{p}_{max}` (Cartesian jerk)

Conditions derived from inverse kinematics:

- :math:`q_{min} < q_c < q_{max}`
- :math:`-\dot{q}_{max} < \dot{q}_c < \dot{q}_{max}`
- :math:`-\ddot{q}_{max} < \ddot{q}_c < \ddot{q}_{max}`

.. _cartesian_space_recommended:

Recommended Conditions
""""""""""""""""""""""

Conditions derived from inverse kinematics:

- :math:`-{\tau_j}_{max} < {\tau_j}_d < {\tau_j}_{max}`
- :math:`-\dot{\tau_j}_{max} < \dot{{\tau_j}_d} < \dot{\tau_j}_{max}`

.. _cartesian_space_initial:

Initial trajectory requirements:

- :math:`{}^OT_{EE} = {{}^OT_{EE}}_c`
- :math:`\dot{p}_c = 0`
- :math:`\ddot{p}_c = 0`

.. _cartesian_space_final:

Final trajectory requirements:

- :math:`\dot{p}_c = 0`
- :math:`\ddot{p}_c = 0`

.. _robot_models:

System Limits for Supported Robot Models
----------------------------------------

.. _limits_fr3:

Limits for Franka Research 3 (FR3)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. _fr3_cartesian_limits:

Cartesian-space limits:

+------------------------+-----------------------------------------------+----------------------------------------------+--------------------------------------------+
|          Name          |                 Translation                   |                   Rotation                   |                  Elbow                     |
+========================+===============================================+==============================================+============================================+
| :math:`\dot{p}_{max}`  | 3.0 :math:`\frac{\text{m}}{\text{s}}`         | 2.5 :math:`\frac{\text{rad}}{\text{s}}`      | 2.620 :math:`\frac{rad}{\text{s}}`         |
+------------------------+-----------------------------------------------+----------------------------------------------+--------------------------------------------+
| :math:`\ddot{p}_{max}` | 9.0 :math:`\frac{\text{m}}{\text{s}^2}`       | 17.0 :math:`\frac{\text{rad}}{\text{s}^2}`   | 10.0 :math:`\frac{rad}{\text{s}^2}`        |
+------------------------+-----------------------------------------------+----------------------------------------------+--------------------------------------------+
| :math:`\dddot{p}_{max}`| 4500.0 :math:`\frac{\text{m}}{\text{s}^3}`    | 8500.0 :math:`\frac{\text{rad}}{\text{s}^3}` | 5000.0 :math:`\frac{rad}{\text{s}^3}`      |
+------------------------+-----------------------------------------------+----------------------------------------------+--------------------------------------------+

.. _fr3_joint_limits:

Joint-space limits:

.. csv-table::
   :header-rows: 1
   :file: control-parameters-joint-fr3.csv

The arm reaches its maximum extension when joint 4 is at
:math:`q_{elbow-flip} = -0.467002423653011\:rad`.

.. _fr3_position_based_velocity:

Position-Based Velocity Limits
"""""""""""""""""""""""""""""""

.. important::

    The maximum joint velocity depends on both the joint position and the direction
    of motion. The position-dependent velocity limits can be queried via:

    .. code-block:: c++

        Robot::getUpperJointVelocityLimits(
            const std::array<double, 7UL>& joint_positions
        );
        Robot::getLowerJointVelocityLimits(
            const std::array<double, 7UL>& joint_positions
        );

    Position-based limits are computed as:

    .. math::

        \dot{q_i}(q_i)_{max} =
        \min(
            \dot{q}_{max,i},
            \max(
                0,
                -\dot{q}_{offset,i} +
                \sqrt{\max(0, 2 \cdot \ddot{q}_{dec,i} (q_{max,i} - q_i))}
            )
        )

    .. math::

        \dot{q_i}(q_i)_{min} =
        \max(
            \dot{q}_{min,i},
            \min(
                0,
                \dot{q}_{offset,i} -
                \sqrt{\max(0, 2 \cdot \ddot{q}_{dec,i} (-q_{min,i} + q_i))}
            )
        )

    These limits ensure safety and may be more restrictive than the nominal
    hardware capabilities.

Users may choose their own joint ranges and velocity limits depending on the
requirements of their motion generator.

.. figure:: _static/pbv_limits_generic.svg
   :align: center
   :figclass: align-center

   Position-based velocity limits.

Suggested rectangular position–velocity limits:

.. csv-table::
   :header-rows: 1
   :file: control-parameters-joint-fr3-rectangular.csv

.. _limits_fer:

Limits for Franka Emika Robot (FER)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. _fer_cartesian_limits:

Cartesian-space limits:

+------------------------+-----------------------------------------------+----------------------------------------------+--------------------------------------------+
|          Name          |                 Translation                   |                   Rotation                   |                  Elbow                     |
+========================+===============================================+==============================================+============================================+
| :math:`\dot{p}_{max}`  | 1.7 :math:`\frac{\text{m}}{\text{s}}`         | 2.5 :math:`\frac{\text{rad}}{\text{s}}`      | 2.1750 :math:`\frac{rad}{\text{s}}`        |
+------------------------+-----------------------------------------------+----------------------------------------------+--------------------------------------------+
| :math:`\ddot{p}_{max}` | 13.0 :math:`\frac{\text{m}}{\text{s}^2}`      | 25.0 :math:`\frac{\text{rad}}{\text{s}^2}`   | 10.0 :math:`\frac{rad}{\text{s}^2}`        |
+------------------------+-----------------------------------------------+----------------------------------------------+--------------------------------------------+
| :math:`\dddot{p}_{max}`| 6500.0 :math:`\frac{\text{m}}{\text{s}^3}`    | 12500.0 :math:`\frac{\text{rad}}{\text{s}^3}`| 5000.0 :math:`\frac{rad}{\text{s}^3}`      |
+------------------------+-----------------------------------------------+----------------------------------------------+--------------------------------------------+

.. _fer_joint_limits:

Joint-space limits:

.. csv-table::
   :header-rows: 1
   :file: control-parameters-joint-Franka Emika Robot (FER).csv

The arm reaches its maximum extension when joint 4 is at
:math:`q_{elbow-flip} = -0.467002423653011\:rad`. This parameter determines the elbow
flip direction.

.. _kinematic_configuration:

Kinematic Configuration
-----------------------

.. _dh_parameters:

Denavit–Hartenberg Parameters
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The Denavit–Hartenberg parameters for the Franka Research 3 kinematic chain
(following Craig's convention) are shown below:

.. figure:: _static/dh-diagram-frankarobotics.png
    :align: center
    :figclass: align-center

    Franka Research 3 kinematic chain.

.. _dh_table:

+-------------+-----------------------+-----------------------+------------------------------+------------------------------+
|    Joint    | :math:`a\;(\text{m})` | :math:`d\;(\text{m})` | :math:`\alpha\;(\text{rad})` | :math:`\theta\;(\text{rad})` |
+=============+=======================+=======================+==============================+==============================+
| Joint 1     | 0                     | 0.333                 | 0                            | :math:`\theta_1`             |
+-------------+-----------------------+-----------------------+------------------------------+------------------------------+
| Joint 2     | 0                     | 0                     | :math:`-\frac{\pi}{2}`       | :math:`\theta_2`             |
+-------------+-----------------------+-----------------------+------------------------------+------------------------------+
| Joint 3     | 0                     | 0.316                 | :math:`\frac{\pi}{2}`        | :math:`\theta_3`             |
+-------------+-----------------------+-----------------------+------------------------------+------------------------------+
| Joint 4     | 0.0825                | 0                     | :math:`\frac{\pi}{2}`        | :math:`\theta_4`             |
+-------------+-----------------------+-----------------------+------------------------------+------------------------------+
| Joint 5     | -0.0825               | 0.384                 | :math:`-\frac{\pi}{2}`       | :math:`\theta_5`             |
+-------------+-----------------------+-----------------------+------------------------------+------------------------------+
| Joint 6     | 0                     | 0                     | :math:`\frac{\pi}{2}`        | :math:`\theta_6`             |
+-------------+-----------------------+-----------------------+------------------------------+------------------------------+
| Joint 7     | 0.088                 | 0                     | :math:`\frac{\pi}{2}`        | :math:`\theta_7`             |
+-------------+-----------------------+-----------------------+------------------------------+------------------------------+
| Flange      | 0                     | 0.107                 | 0                            | 0                            |
+-------------+-----------------------+-----------------------+------------------------------+------------------------------+

.. note::

    :math:`{}^0T_{1}` describes the pose of frame 1 in frame 0.

    The full kinematic chain is computed as:

    :math:`{}^0T_{2} = {}^0T_{1} \cdot {}^1T_{2} \cdot {}^2T_{n}`
