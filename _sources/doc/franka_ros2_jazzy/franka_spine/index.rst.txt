franka_spine
============

ROS 2 action/service server for the Franka Spine REST API.

Launch
------

.. code-block:: bash

   ros2 launch franka_spine_server spine.launch.py spine_ip:=172.16.16.10

With a namespace:

.. code-block:: bash

   ros2 launch franka_spine_server spine.launch.py spine_ip:=172.16.16.10 namespace:=my_robot

Topics
------

Subscribe to these for a continuous position or state stream. Do not call the
services in a loop to get the same thing: the spine REST API is served by a
single upstream behind nginx, and overlapping requests wedge it until the TMR
is rebooted.

Both topics are published at ``feedback_rate`` (default 10 Hz) and only while
someone is subscribed, so an idle node leaves the device alone. The ``valid``
field is false when the last read of the device failed; ``position`` then holds
the last known value.

.. code-block:: bash

   ros2 topic echo /franka_spine_node/position
   ros2 topic echo /franka_spine_node/state

Services
--------

The node reads position and state from the device at most ``feedback_rate``
times per second in total, and serves everything else from that sample, so
these services stay safe to call from several clients at once. A service call
can therefore return a value up to one period old.

Get spine state
^^^^^^^^^^^^^^^

.. code-block:: bash

   ros2 service call /franka_spine_node/get_state franka_spine_msgs/srv/GetSpineState

Get position
^^^^^^^^^^^^

.. code-block:: bash

   ros2 service call /franka_spine_node/get_position franka_spine_msgs/srv/GetPosition

Switch on
^^^^^^^^^

.. code-block:: bash

   ros2 service call /franka_spine_node/switch_on franka_spine_msgs/srv/SwitchOn

Switch off
^^^^^^^^^^

.. code-block:: bash

   ros2 service call /franka_spine_node/switch_off franka_spine_msgs/srv/SwitchOff

Fault reset
^^^^^^^^^^^

.. code-block:: bash

   ros2 service call /franka_spine_node/fault_reset franka_spine_msgs/srv/FaultReset

Halt motion
^^^^^^^^^^^

.. code-block:: bash

   ros2 service call /franka_spine_node/halt franka_spine_msgs/srv/Halt

Get parameters
^^^^^^^^^^^^^^

.. code-block:: bash

   ros2 service call /franka_spine_node/get_parameters_spine franka_spine_msgs/srv/GetParameters

Action
------

Move to absolute position
^^^^^^^^^^^^^^^^^^^^^^^^^

Send a goal:

.. code-block:: bash

   ros2 action send_goal /franka_spine_node/move_absolute franka_spine_msgs/action/MoveAbsolute \
     "{position: 0.4, velocity: 0.1, acceleration: 0.2, deceleration: 0.2}" --feedback

Python Client Example
---------------------

See the ``franka_spine_examples`` package for a runnable Python client:

.. code-block:: bash

   ros2 run franka_spine_examples spine_client_example.py
