.. _franka_gripper:

franka_gripper
--------------
This package implements the ``franka_gripper_node`` for interfacing a gripper from ROS.
The node publishes the state of the gripper and offers the following `actions servers`:

 * ``franka_gripper::MoveAction(width, speed)``: moves to a target ``width`` with the defined
   ``speed``.
 * ``franka_gripper::GraspAction(width, epsilon_inner, epsilon_outer, speed, force)``: tries to
   grasp at the desired ``width`` with a desired ``force`` while closing with the given ``speed``. The
   operation is successful if the distance :math:`d` between the gripper fingers is:
   :math:`\text{width} - \epsilon_\text{inner} < d < \text{width} + \epsilon_\text{outer}`.
 * ``franka_gripper::HomingAction()``: homes the gripper and updates the maximum width given the
   mounted fingers.
 * ``franka_gripper::StopAction()``: aborts a running action. This can be used to stop applying
   forces after grasping.
 * ``control_msgs::GripperCommandAction(width, max_effort)``: A standard gripper action
   recognized by MoveIt!. If the argument ``max_effort`` is greater than zero, the gripper
   will try to grasp an object of the desired ``width``. On the other hand, if ``max_effort`` is
   zero (:math:`\text{max_effort} < 1^{-4}`), the gripper will move to the desired ``width``.

  .. note::

      Use the argument ``max_effort`` only when grasping an object, otherwise, the gripper will
      close ignoring the ``width`` argument.


You can launch the ``franka_gripper_node`` with:

.. code-block:: shell

    roslaunch franka_gripper franka_gripper.launch robot_ip:=<fci-ip>

.. hint::

    Starting with ``franka_ros`` 0.6.0, specifying ``load_gripper:=true`` for
    ``roslaunch franka_control franka_control.launch`` will start a ``franka_gripper_node`` as well.

