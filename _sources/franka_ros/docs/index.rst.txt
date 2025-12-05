franka_ros
==========

.. toctree::
   :maxdepth: 1

   ../franka_ros/doc/index
   ../franka_control/doc/index
   ../franka_description/doc/index
   ../franka_example_controllers/doc/index
   ../franka_gazebo/doc/index
   ../franka_gripper/doc/index
   ../franka_hw/doc/index
   ../franka_msgs/doc/index
   ../franka_visualization/doc/index

.. _write_own_controller:

Writing  your own controller
----------------------------
All example controllers from the :ref:`example controllers package<example_controllers>` are
derived from the ``controller_interface::MultiInterfaceController`` class, which allows to claim
up to four interfaces in one controller instance. The declaration of your class then looks like:

.. code-block:: c++

    class NameOfYourControllerClass : controller_interface::MultiInterfaceController <
                                  my_mandatory_first_interface,
                                  my_possible_second_interface,
                                  my_possible_third_interface,
                                  my_possible_fourth_interface> {
      bool init (hardware_interface::RobotHW* hw, ros::NodeHandle& nh);  // mandatory
      void update (const ros::Time& time, const ros::Duration& period);  // mandatory
      void starting (const ros::Time& time)   // optional
      void stopping (const ros::Time& time);  // optional
      ...
    }


The available interfaces are described in Section :ref:`franka_hw <franka_hw>`.

.. important::

    Note that the claimable combinations of commanding interfaces are restricted as it does not
    make sense to e.g. command joint positions and Cartesian poses simultaneously. Read-only
    interfaces like the *JointStateInterface*, the *FrankaStateInterface* or the
    *FrankaModelInterface* can always be claimed and are not subject to restrictions.


Possible claims to command interfaces are:

+-------------------------------------------------+----------------------------------------------+
|          ``franka_hw::FrankaHW``                | ``franka_combinable_hw::FrankaCombinableHW`` |
+=================================================+==============================================+
|     - all possible single interface claims      |     - ``EffortJointInterface``               |
|     - ``EffortJointInterface`` +                |     - ``EffortJointInterface`` +             |
|       ``PositionJointInterface``                |       ``FrankaCartesianPoseInterface``       |
|     - ``EffortJointInterface`` +                |     - ``EffortJointInterface`` +             |
|       ``VelocityJointInterface``                |       ``FrankaCartesianVelocityInterface``   |
|     - ``EffortJointInterface`` +                |                                              |
|       ``FrankaCartesianPoseInterface``          |                                              |
|     - ``EffortJointInterface`` +                |                                              |
|       ``FrankaCartesianVelocityInterface``      |                                              |
+-------------------------------------------------+----------------------------------------------+

The idea behind offering the *EffortJointInterface* in combination with a motion generator
interface is to expose the internal motion generators to the user. The calculated desired joint
pose corresponding to a motion generator command is available in the robot state one time step
later. One use case for this combination would be following a Cartesian trajectory using your own
joint-level torque controller. In this case you would claim the combination *EffortJointInterface*
+ *FrankaCartesianPoseInterface*, stream your trajectory into the *FrankaCartesianPoseInterface*,
and compute your joint-level torque commands based on the resulting desired joint pose (q_d) from
the robot state. This allows to use the robot's built-in inverse kinematics instead of having to
solve it on your own.

To implement a fully functional controller you have to implement at least the inherited virtual
functions ``init`` and ``update``. Initializing - e.g. start poses - should be done in the
``starting`` function as ``starting`` is called when restarting the controller, while ``init`` is
called only once when loading the controller. The ``stopping`` method should contain shutdown
related functionality (if needed).

.. important::

    Always command a gentle slowdown before shutting down the controller. When using velocity
    interfaces, do not simply command zero velocity in ``stopping``. Since it might be called
    while the robot is still moving, it would be equivalent to commanding a jump in velocity
    leading to very high resulting joint-level torques. In this case it would be better to keep the
    same velocity and stop the controller than sending zeros and let the robot handle
    the slowdown.

Your controller class must be exported correctly with ``pluginlib`` which requires adding:

.. code-block:: c++

    #include <pluginlib/class_list_macros.h>
    // Implementation ..
    PLUGINLIB_EXPORT_CLASS(name_of_your_controller_package::NameOfYourControllerClass,
                           controller_interface::ControllerBase)


at the end of the ``.cpp`` file. In addition you need to define a ``plugin.xml`` file with the
following content:

.. code-block:: xml

      <library path="lib/lib<name_of_your_controller_library>">
        <class name="name_of_your_controller_package/NameOfYourControllerClass"
               type="name_of_your_controller_package::NameOfYourControllerClass"
               base_class_type="controller_interface::ControllerBase">
          <description>
            Some text to describe what your controller is doing
          </description>
        </class>
      </library>


which is exported by adding:

.. code-block:: xml

    <export>
      <controller_interface plugin="${prefix}/plugin.xml"/>
    </export>


to your package.xml. Further, you need to load at least a controller name in combination with a
controller type to the ROS parameter server. Additionally, you can include other parameters you
need. An exemplary configuration.yaml file can look like:

.. code-block:: yaml

    your_custom_controller_name:
      type: name_of_your_controller_package/NameOfYourControllerClass
      additional_example_parameter: 0.0
      # ..

Now you can start your controller using the ``controller_spawner`` node from ROS control or via the
service calls offered by the ``hardware_manager``. Just make sure that both the
``controller_spawner`` and the ``franka_control_node`` run in the same namespace. For more details
have a look at the controllers from the
:ref:`franka_example_controllers package<example_controllers>` or the
`ROS control tutorials <http://wiki.ros.org/ros_control/Tutorials>`_.
