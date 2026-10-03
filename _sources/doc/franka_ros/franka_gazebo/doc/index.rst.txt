.. _franka_gazebo:

franka_gazebo
-------------
This package allows you to simulate our robot in `Gazebo <https://gazebosim.org/>`_. This is possible
because Gazebo is able to integrate into the ROS control framework with the
`gazebo_ros <https://classic.gazebosim.org/tutorials?tut=ros_control&cat=connect_ros>`_ package.

.. important:: This package is available from 0.8.0

Pick & Place Example
""""""""""""""""""""""
Let's dive in and simulate transporting a stone from A to B. Run the following command to start Gazebo with a Panda
and an example world.

.. code-block:: shell

  roslaunch franka_gazebo panda.launch x:=-0.5 \
      world:=$(rospack find franka_gazebo)/world/stone.sdf \
      controller:=cartesian_impedance_example_controller \
      rviz:=true

This will bring up the Gazebo GUI where you see the environment with the stone and RViz with which you can control
the end-effector pose of the robot.


.. figure:: _static/franka-gazebo-example.png
    :align: center
    :figclass: align-center

    Gazebo GUI (left) and RViz (right) of the pick and place example

To open the gripper, simply send a goal to the ``move`` action, similar to how the real ``franka_gripper``
works. Let's move the gripper to a width of :math:`8\:cm` between the fingers with :math:`10\:\frac{cm}{s}`:

.. code-block:: shell

  rostopic pub --once /franka_gripper/move/goal franka_gripper/MoveActionGoal "goal: { width: 0.08, speed: 0.1 }"


Since we launched our robot with the Cartesian Impedance controller from
:ref:`franka_example_controllers<example_controllers>`, we can move the end-effector around, just like in reality,
with the interactive marker gizmo in RViz. Move the robot such that the white stone is between the fingers of the
gripper ready to be picked up.

.. note::

  If the robot moves strangely with the elbow, this is because the default nullspace stiffness of the cartesian
  impedance example controller is set to low. Launch `Dynamic Reconfigure <http://wiki.ros.org/rqt_reconfigure>`_
  and adjust ``panda`` > ``cartesian_impedance_example_controller`` > ``nullspace_stiffness`` if necessary.

To pick up the object, we use the ``grasp`` action this time, since we want to excerpt a force after
the grasp to not drop the object. The stone is around :math:`3\:cm` wide and :math:`50\:g` heavy.
Let's grasp it with :math:`5\:N`:

.. code-block:: shell

   rostopic pub --once /franka_gripper/grasp/goal \
                franka_gripper/GraspActionGoal \
                "goal: { width: 0.03, epsilon:{ inner: 0.005, outer: 0.005 }, speed: 0.1, force: 5.0}"
.. note::

   In top menu of Gazebo go to **View** > **Contacts** to visualize contact points and forces

If the grasp succeeded, the fingers will now hold the stone in place. If not, probably the goal tolerances (inner
and outer epsilon) were too small and the action failed. Now move the object gently over to the red dropoff area.

.. figure:: _static/franka-gazebo-example-grasp.png
   :align: center
   :figclass: align-center

   Transport the stone from blue to red

After you placed it gently on the red pad, stop the grasp with the ``stop`` action from the gripper:

.. code-block:: shell

   rostopic pub --once /franka_gripper/stop/goal franka_gripper/StopActionGoal {}

Note that the contact forces disappear now, since no force is applied anymore. Alternatively you can also use
the ``move`` action.

Customization
""""""""""""""

The launch file from ``franka_gazebo`` takes a lot of arguments with which you can customize the behavior
of the simulation. For example to spawn two pandas in one simulation you can use the following:

.. code-block:: xml

  <?xml version="1.0"?>
  <launch>

    <include file="$(find gazebo_ros)/launch/empty_world.launch" >
      <!-- Start paused, simulation will be started, when Pandas were loaded -->
      <arg name="paused" value="true"/>
      <arg name="use_sim_time" value="true"/>
    </include>

    <group ns="panda_1">
      <include file="$(find franka_gazebo)/launch/panda.launch">
        <arg name="arm_id"     value="panda_1" />
        <arg name="y"          value="-0.5" />
        <arg name="controller" value="cartesian_impedance_example_controller" />
        <arg name="rviz"       value="false" />
        <arg name="gazebo"     value="false" />
        <arg name="paused"     value="true" />
      </include>
    </group>

    <group ns="panda_2">
      <include file="$(find franka_gazebo)/launch/panda.launch">
        <arg name="arm_id"     value="panda_2" />
        <arg name="y"          value="0.5" />
        <arg name="controller" value="force_example_controller" />
        <arg name="rviz"       value="false" />
        <arg name="gazebo"     value="false" />
        <arg name="paused"     value="false" />
      </include>
    </group>

  </launch>

.. note::

  To see which arguments are supported use: ``roslaunch franka_gazebo panda.launch --ros-args``

FrankaHWSim
"""""""""""

By default Gazebo ROS can only simulate joints with "standard" hardware interfaces like `Joint State Interfaces`
and `Joint Command Interfaces`. However our robot is quite different from this architecture! Next to
these joint-specific interfaces it also supports **robot-specific** interfaces like the ``FrankaModelInterface`` (see
:ref:`franka_hw <franka_hw>`). Naturally gazebo does not understand these custom hardware interfaces by default.
This is where the ``FrankaHWSim`` plugin comes in.

To make your robot capable of supporting Franka interfaces, simply declare a custom ``robotSimType`` in your URDF:

.. code-block:: xml

  <gazebo>
    <plugin name="gazebo_ros_control" filename="libgazebo_ros_control.so">
      <robotNamespace>${arm_id}</robotNamespace>
      <controlPeriod>0.001</controlPeriod>
      <robotSimType>franka_gazebo/FrankaHWSim</robotSimType>
    </plugin>
    <self_collide>true</self_collide>
  </gazebo>


When you spawn this robot with the `model spawner
<http://wiki.ros.org/simulator_gazebo/Tutorials/SpawningObjectInSimulation#Spawn_Model_in_Simulation>`_ this plugin
will be loaded into the gazebo node. It will scan your URDF and try to find supported hardware interfaces. Up to now
only some of the interfaces provided by :ref:`franka_hw <franka_hw>` are supported:


+---+-------------------------------------------------+----------------------------------------------+
|   |                    Interface                    |                   Function                   |
+===+=================================================+==============================================+
| ✔ | ``hardware_interface::JointStateInterface``     | Reads joint states.                          |
+---+-------------------------------------------------+----------------------------------------------+
| ✔ | ``hardware_interface::EffortJointInterface``    | Commands joint-level torques and reads       |
|   |                                                 | joint states.                                |
+---+-------------------------------------------------+----------------------------------------------+
| ✔ | ``hardware_interface::VelocityJointInterface``  | Commands joint velocities and reads joint    |
|   |                                                 | states.                                      |
+---+-------------------------------------------------+----------------------------------------------+
| ✔ | ``hardware_interface::PositionJointInterface``  | Commands joint positions and reads joint     |
|   |                                                 | states.                                      |
+---+-------------------------------------------------+----------------------------------------------+
| ✔ | ``franka_hw::FrankaStateInterface``             | Reads the full robot state.                  |
+---+-------------------------------------------------+----------------------------------------------+
| ✔ | ``franka_hw::FrankaModelInterface``             | Reads the dynamic and kinematic model of the |
|   |                                                 | robot.                                       |
+---+-------------------------------------------------+----------------------------------------------+
| ✘ | ``franka_hw::FrankaPoseCartesianInterface``     | Commands Cartesian poses and reads the full  |
|   |                                                 | robot state.                                 |
+---+-------------------------------------------------+----------------------------------------------+
| ✘ | ``franka_hw::FrankaVelocityCartesianInterface`` | Commands Cartesian velocities and reads the  |
|   |                                                 | full robot state.                            |
+---+-------------------------------------------------+----------------------------------------------+

.. important::

  This implies that you can only simulate controllers, that claim these supported interfaces and none other!
  For example the Cartesian Impedance Example Controller can be simulated, because it only requires the
  ``EffortJoint``-, ``FrankaState``- and ``FrankaModelInterface``. However the Joint Impedance Example Controller
  can't be simulated, because it requires the ``FrankaPoseCartesianInterface`` which is not supported yet.

Next to the realtime hardware interfaces the ``FrankaHWSim`` plugin supports some of the non-realtime commands
that :ref:`franka_control <franka_control>` supports:


+---+-------------------------------------------+--------------------------------------------------------------+
|   |         Service / Type                    |              Explanation                                     |
+===+===========================================+==============================================================+
| ✘ | ``set_joint_impedance`` /                 | Gazebo does not simulate an internal impedance               |
|   | `SetJointImpedance`_                      | controller, but sets commanded torques directly              |
+---+-------------------------------------------+--------------------------------------------------------------+
| ✘ | ``set_cartesian_impedance`` /             | Gazebo does not simulate an internal impedance               |
|   | `SetCartesianImpedance`_                  | controller, but sets commanded torques directly              |
+---+-------------------------------------------+--------------------------------------------------------------+
| ✔ | ``set_EE_frame`` /                        | Sets the :math:`{}^{\mathrm{NE}}\mathbf{T}_{\mathrm{EE}}`    |
|   | `SetEEFrame`_                             | i.e. the homogenous transformation from nominal end-effector |
|   |                                           | to end-effector. You can also initialize this by setting the |
|   |                                           | ROS parameter ``/<arm_id>/NE_T_EE``. Normally you would set  |
|   |                                           | :math:`{}^{\mathrm{F}}\mathbf{T}_{\mathrm{NE}}` in Desk, but |
|   |                                           | in ``franka_gazebo`` it's assumed as identity if no gripper  |
|   |                                           | was specified or defines a rotation around Z by :math:`45\:°`|
|   |                                           | and an offset by :math:`10.34\:cm` (same as Desk for the     |
|   |                                           | hand). You can always overwrite this value by setting the ROS|
|   |                                           | parameter ``/<arm_id>/NE_T_EE`` manually.                    |
+---+-------------------------------------------+--------------------------------------------------------------+
| ✔ | ``set_K_frame`` /                         | Sets the :math:`{}^{\mathrm{EE}}\mathbf{T}_{\mathrm{K}}` i.e.|
|   | `SetKFrame`_                              | the homogenous transformation from end-effector to stiffness |
|   |                                           | frame.                                                       |
+---+-------------------------------------------+--------------------------------------------------------------+
| ✔ | ``set_force_torque_collision_behavior`` / | Sets thresholds above which external wrenches are treated as |
|   | `SetForceTorqueCollisionBehavior`_        | contacts and collisions.                                     |
+---+-------------------------------------------+--------------------------------------------------------------+
| ✘ | ``set_full_collision_behavior`` /         | Not yet implemented                                          |
|   | `SetFullCollisionBehavior`_               |                                                              |
+---+-------------------------------------------+--------------------------------------------------------------+
| ✔ | ``set_load`` /                            | Sets an external load to compensate its gravity for, e.g. of |
|   | `SetLoad`_                                | a grasped object. You can also initialize this by setting    |
|   |                                           | the ROS parameters ``/<arm_id>/{m_load,I_load,F_x_load}``    |
|   |                                           | for mass, inertia tensor and center of mass for the load,    |
|   |                                           | respectively.                                                |
+---+-------------------------------------------+--------------------------------------------------------------+
| ✔ | ``set_user_stop`` /                       | This is a special service only available in ``franka_gazebo``|
|   | `std_srvs::SetBool`_                      | to simulate the user stop. Pressing the user stop (a.k.a     |
|   | (since 0.9.1)                             | publishing a ``true`` via this service) will *disconnect*    |
|   |                                           | all command signals from ROS controllers to be fed to the    |
|   |                                           | joints. To connect them again call the ``error_recovery``    |
|   |                                           | action.                                                      |
+---+-------------------------------------------+--------------------------------------------------------------+

.. _SetJointImpedance:               http://docs.ros.org/en/noetic/api/franka_msgs/html/srv/SetJointImpedance.html
.. _SetCartesianImpedance:           http://docs.ros.org/en/noetic/api/franka_msgs/html/srv/SetCartesianImpedance.html
.. _SetEEFrame:                      http://docs.ros.org/en/noetic/api/franka_msgs/html/srv/SetEEFrame.html
.. _SetKFrame:                       http://docs.ros.org/en/noetic/api/franka_msgs/html/srv/SetKFrame.html
.. _SetForceTorqueCollisionBehavior:
        http://docs.ros.org/en/noetic/api/franka_msgs/html/srv/SetForceTorqueCollisionBehavior.html
.. _SetFullCollisionBehavior:
        http://docs.ros.org/en/noetic/api/franka_msgs/html/srv/SetFullCollisionBehavior.html
.. _SetLoad:                         http://docs.ros.org/en/noetic/api/franka_msgs/html/srv/SetLoad.html
.. _std_srvs::SetBool:               http://docs.ros.org/en/noetic/api/std_srvs/html/srv/SetBool.html

FrankaGripperSim
""""""""""""""""

This plugin simulates the :ref:`franka_gripper_node <franka_gripper>` in Gazebo. This is done as a ROS controller for
the two finger joints with a position & force controller. It offers the same five actions like the real gripper node:

* ``/<arm_id>/franka_gripper/homing``
* ``/<arm_id>/franka_gripper/stop``
* ``/<arm_id>/franka_gripper/move``
* ``/<arm_id>/franka_gripper/grasp``
* ``/<arm_id>/franka_gripper/gripper_action``

.. important::
  The ``grasp`` action has a bug, that it will not succeed nor abort if the target width
  lets the fingers **open**. This is because of missing the joint limits interface which
  lets the finger oscillate at their limits. For now only use the ``grasp`` action to *close*
  the fingers!


It is assumed that the URDF contains two finger joints which can be force controlled, i.e. have a corresponding
``EffortJointInterface`` transmission declared. This controller expects the following parameters in its namespace:

* ``type``          (string, required): Should be ``franka_gazebo/FrankaGripperSim``
* ``arm_id``        (string, required): The arm id of the panda, to infer the name of the finger joints
* ``finger1/gains/p`` (double, required): The proportional gain for the position-force controller of the first finger
* ``finger1/gains/i`` (double, default: 0): The integral gain for the position-force controller of the first finger
* ``finger1/gains/d`` (double, default: 0): The differential gain for the position-force controller of the first finger
* ``finger2/gains/p`` (double, required): The proportional gain for the position-force controller of the second finger
* ``finger2/gains/i`` (double, default: 0): The integral gain for the position-force controller of the second finger
* ``finger2/gains/d`` (double, default: 0): The differential gain for the position-force controller of the second finger
* ``move/width_tolerance`` (double, default :math:`5\:mm`): The move action succeeds, when the finger width becomes
  below this threshold
* ``grasp/resting_threshold`` (double, default :math:`1\:\frac{mm}{s}`):  Below which speed the target width should
  be checked to abort or succeed the grasp action
* ``grasp/consecutive_samples`` (double, default: 3): How many times the speed has to be consecutively below
  ``resting_threshold`` before the grasping will be evaluated
* ``gripper_action/width_tolerance`` (double, default :math:`5\:mm`): The gripper action succeeds, when the finger
  width becomes below this threshold
* ``gripper_action/speed`` (double, default :math:`10\:\frac{cm}{s}`): The speed to use during the gripper action





JointStateInterface
"""""""""""""""""""""

To be able to access the joint state interface from a ROS controller you only have to declare the corresponding
joint in any transmission tag in the URDF. Then a joint state interface will be automatically available. Usually
you declare transmission tags for command interfaces like the :ref:`EffortJointInterface <effort_joint_interface>`.

.. note::
  For any joint named ``<arm_id>_jointN`` (with N as integer) FrankaHWSim will automatically compensate its gravity
  to mimic the behavior of libfranka.

.. _effort_joint_interface:

EffortJointInterface
""""""""""""""""""""""

To be able to send effort commands from your controller to a joint, you simply declare a transmission tag for the
joint in your URDF with the corresponding hardware interface type:

.. code-block:: xml

    <transmission name="${joint}_transmission">
     <type>transmission_interface/SimpleTransmission</type>
     <joint name="${joint}">
       <hardwareInterface>hardware_interface/EffortJointInterface</hardwareInterface>
     </joint>
     <actuator name="${joint}_motor">
       <hardwareInterface>${transmission}</hardwareInterface>
     </actuator>
    </transmission>

    <gazebo reference="${joint}">
      <!-- Needed for ODE to output external wrenches on joints -->
      <provideFeedback>true</provideFeedback>
    </gazebo>


.. note::

  If you want to be able to read external forces or torques, which come e.g. from collisions, make sure to set the
  ``<provideFeedback>`` tag to ``true``.

FrankaStateInterface
""""""""""""""""""""""

This is a **robot-specific** interface and thus a bit different from the normal hardware interfaces.
To be able to access the franka state interface from your controller declare the following transmission tag with
all seven joints in your URDF:

.. code-block:: xml

    <transmission name="${arm_id}_franka_state">
      <type>franka_hw/FrankaStateInterface</type>
      <joint name="${arm_id}_joint1"><hardwareInterface>franka_hw/FrankaStateInterface</hardwareInterface></joint>
      <joint name="${arm_id}_joint2"><hardwareInterface>franka_hw/FrankaStateInterface</hardwareInterface></joint>
      <joint name="${arm_id}_joint3"><hardwareInterface>franka_hw/FrankaStateInterface</hardwareInterface></joint>
      <joint name="${arm_id}_joint4"><hardwareInterface>franka_hw/FrankaStateInterface</hardwareInterface></joint>
      <joint name="${arm_id}_joint5"><hardwareInterface>franka_hw/FrankaStateInterface</hardwareInterface></joint>
      <joint name="${arm_id}_joint6"><hardwareInterface>franka_hw/FrankaStateInterface</hardwareInterface></joint>
      <joint name="${arm_id}_joint7"><hardwareInterface>franka_hw/FrankaStateInterface</hardwareInterface></joint>

      <actuator name="${arm_id}_motor1"><hardwareInterface>franka_hw/FrankaStateInterface</hardwareInterface></actuator>
      <actuator name="${arm_id}_motor2"><hardwareInterface>franka_hw/FrankaStateInterface</hardwareInterface></actuator>
      <actuator name="${arm_id}_motor3"><hardwareInterface>franka_hw/FrankaStateInterface</hardwareInterface></actuator>
      <actuator name="${arm_id}_motor4"><hardwareInterface>franka_hw/FrankaStateInterface</hardwareInterface></actuator>
      <actuator name="${arm_id}_motor5"><hardwareInterface>franka_hw/FrankaStateInterface</hardwareInterface></actuator>
      <actuator name="${arm_id}_motor6"><hardwareInterface>franka_hw/FrankaStateInterface</hardwareInterface></actuator>
      <actuator name="${arm_id}_motor7"><hardwareInterface>franka_hw/FrankaStateInterface</hardwareInterface></actuator>
    </transmission>

When your controller accesses the :api:`RobotState|structfranka_1_1RobotState.html` via the ``FrankaStateInterface`` it can
expect the following values to be simulated:

+---+----------------------------------+------------------------------------------------------------------------+
|   |   Field                          |                Comment                                                 |
+===+==================================+========================================================================+
| ✔ | ``O_T_EE``                       |                                                                        |
+---+----------------------------------+------------------------------------------------------------------------+
| ✘ | ``O_T_EE_d``                     | Motion generation not yet supported, field will contain only zeros     |
+---+----------------------------------+------------------------------------------------------------------------+
| ✔ | ``F_T_EE``                       | Can be configured via parameters ``F_T_NE``, ``NE_T_EE`` and/or        |
|   |                                  | service calls to ``set_EE_frame``                                      |
+---+----------------------------------+------------------------------------------------------------------------+
| ✔ | ``NE_T_EE``                      | Can be configured via parameter ``NE_T_EE`` and/or service calls       |
|   |                                  | to ``set_EE_frame``                                                    |
+---+----------------------------------+------------------------------------------------------------------------+
| ✔ | ``EE_T_K``                       | Can be configured via parameter ``EE_T_K`` and/or service calls        |
|   |                                  | to ``set_K_frame``                                                     |
+---+----------------------------------+------------------------------------------------------------------------+
| ✔ | ``m_ee``                         | Will be set from the mass in the inertial tag of URDF, if a hand can   |
|   |                                  | be found, otherwise zero. Can be overwritten by parameter ``m_ee``     |
+---+----------------------------------+------------------------------------------------------------------------+
| ✔ | ``I_ee``                         | Will be set from the inertia in the inertial tag of URDF, if a hand    |
|   |                                  | be found, otherwise zero. Can be overwritten by parameter ``I_ee``     |
+---+----------------------------------+------------------------------------------------------------------------+
| ✔ | ``F_x_Cee``                      | Will be set from the origin in the inertial tag of URDF, if a hand can |
|   |                                  | be found, otherwise zero. Can be overwritten by parameter ``F_x_Cee``  |
+---+----------------------------------+------------------------------------------------------------------------+
| ✔ | ``m_load``                       | Can be configured via parameter ``m_load`` and/or service calls to     |
|   |                                  | ``set_load``                                                           |
+---+----------------------------------+------------------------------------------------------------------------+
| ✔ | ``I_load``                       | Can be configured via parameter ``I_load`` and/or service calls to     |
|   |                                  | ``set_load``                                                           |
+---+----------------------------------+------------------------------------------------------------------------+
| ✔ | ``F_x_Cload``                    | Can be configured via parameter ``F_x_Cload`` and/or service calls to  |
|   |                                  | ``set_load``                                                           |
+---+----------------------------------+------------------------------------------------------------------------+
| ✔ | ``m_total``                      |                                                                        |
+---+----------------------------------+------------------------------------------------------------------------+
| ✔ | ``I_total``                      |                                                                        |
+---+----------------------------------+------------------------------------------------------------------------+
| ✔ | ``F_x_Ctotal``                   |                                                                        |
+---+----------------------------------+------------------------------------------------------------------------+
| ✘ | ``elbow``                        |                                                                        |
+---+----------------------------------+------------------------------------------------------------------------+
| ✘ | ``elbow_d``                      |                                                                        |
+---+----------------------------------+------------------------------------------------------------------------+
| ✘ | ``elbow_c``                      |                                                                        |
+---+----------------------------------+------------------------------------------------------------------------+
| ✘ | ``delbow_d``                     |                                                                        |
+---+----------------------------------+------------------------------------------------------------------------+
| ✘ | ``delbow_c``                     |                                                                        |
+---+----------------------------------+------------------------------------------------------------------------+
| ✔ | ``tau_J``                        | Comes directly from Gazebo                                             |
+---+----------------------------------+------------------------------------------------------------------------+
| ✔ | ``tau_J_d``                      | The values send by your effort controller. Zero otherwise.             |
+---+----------------------------------+------------------------------------------------------------------------+
| ✔ | ``dtau_J``                       | Numerical derivative of ``tau_J``                                      |
+---+----------------------------------+------------------------------------------------------------------------+
| ✔ | ``q``                            | Comes directly from Gazebo                                             |
+---+----------------------------------+------------------------------------------------------------------------+
| ✔ | ``q_d``                          | The last commanded joint position when using the position interface.   |
|   |                                  | Same as ``q`` when using the velocity interface. However,              |
|   |                                  | the value will not be updated when using the effort interface.         |
+---+----------------------------------+------------------------------------------------------------------------+
| ✔ | ``dq``                           | Comes directly from Gazebo                                             |
+---+----------------------------------+------------------------------------------------------------------------+
| ✔ | ``dq_d``                         | The last commanded joint velocity when using the velocity interface.   |
|   |                                  | Same as ``dq`` when using the position interface. However,             |
|   |                                  | the value will be zero when using the effort interface.                |
+---+----------------------------------+------------------------------------------------------------------------+
| ✔ | ``ddq_d``                        | Current acceleration when using the position or velocity interface.    |
|   |                                  | However, the value will be zero when using the effort interface.       |
+---+----------------------------------+------------------------------------------------------------------------+
| ✔ | ``joint_contact``                | :math:`\mid \hat{\tau}_{ext} \mid > \mathrm{thresh}_{lower}` where the |
|   |                                  | threshold can be set by calling ``set_force_torque_collision_behavior``|
+---+----------------------------------+------------------------------------------------------------------------+
| ✔ | ``joint_collision``              | :math:`\mid \hat{\tau}_{ext} \mid > \mathrm{thresh}_{upper}` where the |
|   |                                  | threshold can be set by calling ``set_force_torque_collision_behavior``|
+---+----------------------------------+------------------------------------------------------------------------+
| ✔ | ``cartesian_contact``            | :math:`\mid {}^K \hat{F}_{K,ext} \mid > \mathrm{thresh}_{lower}` where |
|   |                                  | threshold can be set by calling ``set_force_torque_collision_behavior``|
+---+----------------------------------+------------------------------------------------------------------------+
| ✔ | ``cartesian_collision``          | :math:`\mid {}^K \hat{F}_{K,ext} \mid > \mathrm{thresh}_{upper}` where |
|   |                                  | threshold can be set by calling ``set_force_torque_collision_behavior``|
+---+----------------------------------+------------------------------------------------------------------------+
| ✔ | ``tau_ext_hat_filtered``         | :math:`\hat{\tau}_{ext}` i.e. estimated external torques and forces at |
|   |                                  | the end-effector, filtered with a exponential moving average filter    |
|   |                                  | (EMA). This filtering :math:`\alpha` can be configured via a ROS       |
|   |                                  | parameter. This field does not contain any gravity, i.e.               |
|   |                                  | :math:`\tau_{ext} = \tau_J - \tau_{J_d} - \tau_{gravity}`              |
+---+----------------------------------+------------------------------------------------------------------------+
| ✔ | ``O_F_ext_hat_K``                | :math:`{}^O\hat{F}_{K,ext} = J_O^{\top +} \cdot \hat{\tau}_{ext}`      |
+---+----------------------------------+------------------------------------------------------------------------+
| ✔ | ``K_F_ext_hat_K``                | :math:`{}^K\hat{F}_{K,ext} = J_K^{\top +} \cdot \hat{\tau}_{ext}`      |
+---+----------------------------------+------------------------------------------------------------------------+
| ✘ | ``O_dP_EE_d``                    |                                                                        |
+---+----------------------------------+------------------------------------------------------------------------+
| ✔ | ``O_ddP_0``                      | Will be the same as the ``gravity_vector`` ROS parameter.              |
|   |                                  | By  default it is {0,0,-9.8}                                           |
+---+----------------------------------+------------------------------------------------------------------------+
| ✘ | ``O_T_EE_c``                     |                                                                        |
+---+----------------------------------+------------------------------------------------------------------------+
| ✘ | ``O_dP_EE_c``                    |                                                                        |
+---+----------------------------------+------------------------------------------------------------------------+
| ✘ | ``O_ddP_EE_c``                   |                                                                        |
+---+----------------------------------+------------------------------------------------------------------------+
| ✔ | ``theta``                        | Same as ``q``, since we don't simulate soft joints in Gazebo           |
+---+----------------------------------+------------------------------------------------------------------------+
| ✔ | ``dtheta``                       | Same as ``dq``, since we don't simulate soft joints in Gazebo          |
+---+----------------------------------+------------------------------------------------------------------------+
| ✘ | ``current_errors``               | Will entirely be false, reflex system not yet implemented              |
+---+----------------------------------+------------------------------------------------------------------------+
| ✘ | ``last_motion_errors``           | Will entirely be false, reflex system not yet implemented              |
+---+----------------------------------+------------------------------------------------------------------------+
| ✔ | ``control_command_success_rate`` | Always 1.0                                                             |
+---+----------------------------------+------------------------------------------------------------------------+
| ✘ | ``robot_mode``                   | Robot mode switches and reflex system not yet implemented              |
+---+----------------------------------+------------------------------------------------------------------------+
| ✔ | ``time``                         | Current ROS time in simulation, comes from Gazebo                      |
+---+----------------------------------+------------------------------------------------------------------------+


FrankaModelInterface
""""""""""""""""""""""

This is a **robot-specific** interface and thus a bit different from the normal hardware interfaces.
To be able to access the franka model interface from your controller declare the following transmission tag with
the root (e.g. ``panda_joint1``) and the tip (e.g. ``panda_joint8``) of your kinematic chain in your URDF:

.. code-block:: xml

  <transmission name="${arm_id}_franka_model">
    <type>franka_hw/FrankaModelInterface</type>
    <joint name="${root}">
      <role>root</role>
      <hardwareInterface>franka_hw/FrankaModelInterface</hardwareInterface>
    </joint>
    <joint name="${tip}">
      <role>tip</role>
      <hardwareInterface>franka_hw/FrankaModelInterface</hardwareInterface>
    </joint>

    <actuator name="${root}_motor_root"><hardwareInterface>franka_hw/FrankaModelInterface</hardwareInterface></actuator>
    <actuator name="${tip}_motor_tip"  ><hardwareInterface>franka_hw/FrankaModelInterface</hardwareInterface></actuator>
  </transmission>

The model functions themselve are implemented with `KDL <https://www.orocos.org/kdl.html>`_. This takes the kinematic
structure and the inertial properties from the URDF to calculate model properties like the Jacobian or the mass matrix.

Friction
"""""""""

For objects to have proper friction between each other (like fingers and objects) you need to tune
some Gazebo parameters in your URDF. For the links ``panda_finger_joint1`` and ``panda_finger_joint2`` we recommend to
set the following parameters:

.. code-block:: xml

    <gazebo reference="${link}">
      <collision>
        <max_contacts>10</max_contacts>
        <surface>
          <contact>
            <ode>
              <!-- These two parameter need application specific tuning. -->
              <!-- Usually you want no "snap out" velocity and a generous -->
              <!-- penetration depth to keep the grasping stable -->
              <max_vel>0</max_vel>
              <min_depth>0.003</min_depth>
            </ode>
          </contact>
          <friction>
            <ode>
              <!-- Rubber/Rubber contact -->
              <mu>1.16</mu>
              <mu2>1.16</mu2>
            </ode>
          </friction>
          <bounce/>
        </surface>
      </collision>
    </gazebo>

.. note::

  Refer to `Gazebo Friction Documentation <https://classic.gazebosim.org/tutorials?tut=friction>`_
