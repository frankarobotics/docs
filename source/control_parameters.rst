.. _control_parameters_specifications:

Robot and interface specifications
===================================
Realtime control commands sent to the robot should fulfill *recommended* and *necessary*
conditions. Recommended conditions should be fulfilled to ensure optimal operation of the
robot. If necessary conditions are not met then the motion will be aborted.

The final robot trajectory is the result of processing the user-specified trajectory ensuring
that recommended conditions are fulfilled. As long as necessary conditions are met, the robot
will try to follow the user-provided trajectory but it will only match the final trajectory
if it also fulfills recommended conditions. If the necessary conditions are violated, an error
will abort the motion: if, for instance, the first point of the user defined joint trajectory
is very different from robot start position (:math:`q(t=0) \neq q_c(t=0)`) a ``start_pose_invalid`` error
will abort the motion.

Values for the constants used in the equations below are shown in the `Limits for Panda`_  and `Limits for Franka Research 3`_ section.

Joint trajectory requirements
-----------------------------

Necessary conditions
********************

- :math:`q_{min} < q_c < q_{max}`
- :math:`-\dot{q}_{max} < \dot{q}_c < \dot{q}_{max}`
- :math:`-\ddot{q}_{max} < \ddot{q}_c < \ddot{q}_{max}`
- :math:`-\dddot{q}_{max} < \dddot{q}_c < \dddot{q}_{max}`

Recommended conditions
**********************

- :math:`-{\tau_j}_{max} < {\tau_j}_d < {\tau_j}_{max}`
- :math:`-\dot{\tau_j}_{max} < \dot{\tau_j}_d < \dot{\tau_j}_{max}`

At the beginning of the trajectory, the following conditions should be fulfilled:

- :math:`q = q_c`
- :math:`\dot{q}_{c} = 0`
- :math:`\ddot{q}_{c} = 0`

At the end of the trajectory, the following conditions should be fulfilled:

- :math:`\dot{q}_{c} = 0`
- :math:`\ddot{q}_{c} = 0`

Cartesian trajectory requirements
---------------------------------

Necessary conditions
********************

- :math:`T` is proper transformation matrix
- :math:`-\dot{p}_{max} < \dot{p_c} < \dot{p}_{max}` (Cartesian velocity)
- :math:`-\ddot{p}_{max} < \ddot{p_c} < \ddot{p}_{max}` (Cartesian acceleration)
- :math:`-\dddot{p}_{max} < \dddot{p_c} < \dddot{p}_{max}` (Cartesian jerk)

Conditions derived from inverse kinematics:

- :math:`q_{min} < q_c < q_{max}`
- :math:`-\dot{q}_{max} < \dot{q_c} < \dot{q}_{max}`
- :math:`-\ddot{q}_{max} < \ddot{q_c} < \ddot{q}_{max}`

Recommended conditions
**********************

Conditions derived from inverse kinematics:

- :math:`-{\tau_j}_{max} < {\tau_j}_d < {\tau_j}_{max}`
- :math:`-\dot{\tau_j}_{max} < \dot{{\tau_j}_d} < \dot{\tau_j}_{max}`

At the beginning of the trajectory, the following conditions should be fulfilled:

- :math:`{}^OT_{EE} = {{}^OT_{EE}}_c`
- :math:`\dot{p}_{c} = 0` (Cartesian velocity)
- :math:`\ddot{p}_{c} = 0` (Cartesian acceleration)

At the end of the trajectory, the following conditions should be fulfilled:

- :math:`\dot{p}_{c} = 0` (Cartesian velocity)
- :math:`\ddot{p}_{c} = 0` (Cartesian acceleration)

Controller requirements
-----------------------

Necessary conditions
********************

- :math:`-\dot{\tau_j}_{max} < \dot{{\tau_j}_d} < \dot{\tau_j}_{max}`

Recommended conditions
**********************

- :math:`-{\tau_j}_{max} < {\tau_j}_d < {\tau_j}_{max}`

At the beginning of the trajectory, the following conditions should be fulfilled:

- :math:`{\tau_j}_{d} = 0`

.. _limit_table:

Limits for Panda
----------------

Limits in the Cartesian space are as follows:\

+------------------------+-----------------------------------------------+--------------------------------------------------+--------------------------------------------+
|          Name          |                 Translation                   |                   Rotation                       |                  Elbow                     |
+========================+===============================================+==================================================+============================================+
| :math:`\dot{p}_{max}`  | 1.7 :math:`\frac{\text{m}}{\text{s}}`         | 2.5 :math:`\frac{\text{rad}}{\text{s}}`          | 2.1750 :math:`\frac{rad}{\text{s}}`        |
+------------------------+-----------------------------------------------+--------------------------------------------------+--------------------------------------------+
| :math:`\ddot{p}_{max}` | 13.0 :math:`\frac{\text{m}}{\text{s}^2}`      | 25.0 :math:`\frac{\text{rad}}{\text{s}^2}`       | 10.0 :math:`\;\frac{rad}{\text{s}^2}`      |
+------------------------+-----------------------------------------------+--------------------------------------------------+--------------------------------------------+
| :math:`\dddot{p}_{max}`| 6500.0 :math:`\frac{\text{m}}{\text{s}^3}`    | 12500.0 :math:`\frac{\text{rad}}{\text{s}^3}`    | 5000.0 :math:`\;\frac{rad}{\text{s}^3}`    |
+------------------------+-----------------------------------------------+--------------------------------------------------+--------------------------------------------+

Joint space limits are:

.. csv-table::
   :header-rows: 1
   :file: control-parameters-joint-panda.csv

The arm can reach its maximum extension when joint 4 has angle :math:`q_{elbow-flip}`, where :math:`q_{elbow-flip} = -0.467002423653011\:rad`.
This parameter is used to determine the flip direction of the elbow.

Limits for Franka Research 3
----------------------------

Limits in the Cartesian space are as follows:\

+------------------------+-----------------------------------------------+--------------------------------------------------+--------------------------------------------+
|          Name          |                 Translation                   |                   Rotation                       |                  Elbow                     |
+========================+===============================================+==================================================+============================================+
| :math:`\dot{p}_{max}`  | 3.0 :math:`\frac{\text{m}}{\text{s}}`         | 2.5 :math:`\frac{\text{rad}}{\text{s}}`          | 2.620 :math:`\frac{rad}{\text{s}}`         |
+------------------------+-----------------------------------------------+--------------------------------------------------+--------------------------------------------+
| :math:`\ddot{p}_{max}` | 9.0 :math:`\frac{\text{m}}{\text{s}^2}`       | 17.0 :math:`\frac{\text{rad}}{\text{s}^2}`       | 10.0 :math:`\;\frac{rad}{\text{s}^2}`      |
+------------------------+-----------------------------------------------+--------------------------------------------------+--------------------------------------------+
| :math:`\dddot{p}_{max}`| 4500.0 :math:`\frac{\text{m}}{\text{s}^3}`    | 8500.0 :math:`\frac{\text{rad}}{\text{s}^3}`     | 5000.0 :math:`\;\frac{rad}{\text{s}^3}`    |
+------------------------+-----------------------------------------------+--------------------------------------------------+--------------------------------------------+

Joint space limits are:

.. csv-table::
   :header-rows: 1
   :file: control-parameters-joint-fr3.csv

The arm can reach its maximum extension when joint 4 has angle :math:`q_{elbow-flip}`, where :math:`q_{elbow-flip} = -0.467002423653011\:rad`.
This parameter is used to determine the flip direction of the elbow.


.. important::

    Note that the maximum joint velocity depends on both the joint position and the direction of motion. The maximum
    and minimum joint velocities for a given joint position can be obtained from the following functions:

    .. code-block:: c++

          Robot::getUpperJointVelocityLimits(const std::array<double, 7UL> &joint_positions);
          Robot::getLowerJointVelocityLimits(const std::array<double, 7UL> &joint_positions);

    The position based joint velocity limits are computed by:

    .. math::

      \dot{q_i} (q_i)_{max} = \min(\dot{q}_{max,i}, \max(0, \; -\dot{q}_{offset,i} + \sqrt{\max(0, \; 2 \cdot \ddot{q}_{dec,i} \cdot (q_{max,i} - q_i))}))

      \dot{q_i} (q_i)_{min} = \max(\dot{q}_{min,i}, \min(0, \; \dot{q}_{offset,i} - \sqrt{\max(0, \; 2 \cdot \ddot{q}_{dec,i} \cdot (-q_{min,i} + q_i))}))

    where:
      - :math:`\dot{q_i} (q_i)_{max}` is the maximum joint velocity for joint :math:`i` at position :math:`q_i`.
      - :math:`\dot{q_i} (q_i)_{min}` is the minimum joint velocity for joint :math:`i` at position :math:`q_i`.
      - :math:`\dot{q}_{max,i}` is the maximum joint velocity for joint :math:`i` from the table above.
      - :math:`\dot{q}_{min,i}` is the minimum joint velocity for joint :math:`i` from the table above.
      - :math:`\dot{q}_{offset,i}` is the velocity offset for joint :math:`i` from the table above.
      - :math:`\ddot{q}_{dec,i}` is the maximum deceleration limits for joint :math:`i` from the table above.
      - :math:`q_{max,i}` is the maximum joint position for joint :math:`i` from the table above.
      - :math:`q_{min,i}` is the minimum joint position for joint :math:`i` from the table above.
      - :math:`q_i` is the current joint position of joint :math:`i`.

    In order to avoid violating the safety joint velocity limits, the Max/Min Joint velocity limits for FCI are more restrictive than those provided in the Datasheet.

Since most motion planners cannot represent variable velocity limits and instead rely on constant limits, users are free to choose the joint range and velocity
limits within which they wish to operate.

In the figure below, the system velocity limits are shown in red and blue, and the position–velocity rectangular limits are depicted in black.

.. figure:: _static/pbv_limits_generic.svg
   :align: center
   :figclass: align-center

   Position based velocity limits


Below are suggested position-velocity rectangular limits:

.. csv-table::
   :header-rows: 1
   :file: control-parameters-joint-fr3-rectangular.csv

.. important::

   These limits are only a suggestion. Since FR3 does not inherently implement any restriction to the system limits (red and blue line in the plots above), you are free
   to implement your own motion generator to exploit the HW capabilities of FR3 beyond the rectangular limits imposed by existing motion generators.


Denavit–Hartenberg parameters
-----------------------------

The Denavit–Hartenberg parameters for the Franka Research 3 kinematic chain are derived following Craig's convention and are as follows:

.. figure:: _static/dh-diagram-frankarobotics.png
    :align: center
    :figclass: align-center

    Franka Research 3 kinematic chain.

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

    :math:`{}^0T_{1}` is the transformation matrix which describes the position and orientation of
    `frame 1` in `frame 0`. A kinematic chain can be calculated like the following:
    :math:`{}^0T_{2} = {}^0T_{1} * {}^1T_{2}`
