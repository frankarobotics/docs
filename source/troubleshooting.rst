.. _troubleshooting:

Troubleshooting
===============

This section lists solutions to a set of possible errors that may occur when using the FCI.

.. hint::

   Further help is provided in the troubleshooting page of the manual shipped with your robot.


.. _troubleshooting_realtime_kernel:

Cannot boot realtime kernel because of "Invalid Signature"
----------------------------------------------------------

When you have successfully installed the real-time kernel and try to boot it, Linux may fail to boot. 
This can happen when Ubuntu is installed alongside Windows (e.g., dual-boot). In such cases, the UEFI 
bootloader often has *Secure Boot* enabled, which prevents the unsigned real-time kernel from loading.

The easiest solution is to **disable "Secure Boot"** in your bootloader. This depends on your system, 
but it is commonly accessed by pressing F2, F3, F12, or DEL during startup.


.. _troubleshooting_connection_timeout:

Running a libfranka executable fails with "Connection timeout"
--------------------------------------------------------------

This error occurs if ``libfranka`` cannot connect to the robot at all. Please check:

* Robots with system version 4.2.0+ require FCI mode to be enabled. To enable: open Desk → expand sidebar menu → click **Activate FCI**.
* Your workstation is directly connected to Control, **not** the Arm LAN port (see :ref:`requirement-network`).
* The robot is reachable from your workstation (see :ref:`troubleshooting_robot_not_reachable`).
* The FCI feature file is installed on the robot (“Settings → System → Installed Features”).  
  Contact ``support@franka.de`` with your robot’s serial number if you need access to the feature.


.. _motion-stopped-due-to-discontinuities:

Motion stopped due to discontinuities or ``communication_constraints_violation``
--------------------------------------------------------------------------------

If the difference between commanded values between cycles is too large, motion stops with errors such as 
``joint_motion_generator_velocity_discontinuity``. Ensure the command changes do not exceed the :ref:`Limits for during specific control modes <control_modes>`.

Discontinuities can result from:

* Actual command jumps in your code  
* Network packet losses  

Packet loss can also produce ``communication_constraints_violation``.  
If it happens even when running official examples, the issue is likely network-related.

Check:

* Source code is compiled with optimizations (``-DCMAKE_BUILD_TYPE=Release``)
* Direct PC → Control connection without switches (see :ref:`Network <requirement-network>`)
* Network performance using the `network bandwidth, delay and jitter test`_
* ``franka::Robot`` instantiated using ``RealtimeConfig::kEnforce`` (default)
* CPU power-saving features are disabled (see :ref:`disable_cpu_frequency_scaling`)


.. _disable_cpu_frequency_scaling:

Disabling CPU frequency scaling
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

CPUs often reduce frequency under low load, increasing latency in real-time systems.  
Install the ``cpufrequtils`` package:

.. code-block:: shell

   sudo apt install cpufrequtils

Run ``cpufreq-info`` to inspect frequency governors. Example output:

.. code-block:: shell

   $ cpufreq-info
   ...
   current CPU frequency is 500 MHz.
   ...

If the "powersave" governor is active, switch to ``performance`` using Ubuntu GUI (``indicator-cpufreq``)  
or via terminal:

.. code-block:: shell

   sudo systemctl disable ondemand
   sudo systemctl enable cpufrequtils
   sudo sh -c 'echo "GOVERNOR=performance" > /etc/default/cpufrequtils'
   sudo systemctl daemon-reload && sudo systemctl restart cpufrequtils

Afterward, ``cpufreq-info`` should show the CPU running near its maximum frequency.


.. _troubleshooting_robot_not_reachable:

Robot is not reachable
----------------------

Ping the robot:

.. code-block:: shell

   ping <fci-ip>

If unreachable, the network or assigned IP is incorrect.  
Please follow the official network setup instructions provided with your robot.


.. _troubleshooting_udp_timeout:

Running a libfranka executable fails with "UDP receive: Timeout"
----------------------------------------------------------------

This occurs when the robot state cannot be received.  
Check that your workstation firewall is not blocking UDP traffic:

.. code-block:: shell

   sudo iptables -L


.. _network-bandwidth-delay-test:

Network bandwidth, delay and jitter test
----------------------------------------

Two diagnostic tests are provided:

1. A basic ping test  
2. An advanced UDP performance test using ``communication_test``


.. _network-ping-test:

Simple ping tests
^^^^^^^^^^^^^^^^^

Simulate FCI-level network load:

.. code-block:: shell

   sudo ping <fci-ip> -i 0.001 -D -c 10000 -s 1200

Example output:

.. code-block:: shell

   --- <fci-ip> ping statistics ---
   rtt min/avg/max/mdev = 0.147/0.240/0.502/0.038 ms

As described in the :ref:`Network requirements <requirement-network>`,  
**round-trip time + control loop execution must remain below 1 ms**.


Advanced network performance analysis
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Run ``communication_test``:

.. code-block:: shell

   source /opt/ros/noetic/setup.sh   # if installed via ROS
   communication_test <fci-ip>

Or from a local build:

.. code-block:: shell

   ./examples/communication_test <fci-ip>


.. _troubleshooting_incompatible_library:

Running a libfranka executable fails with "Incompatible Library Version"
------------------------------------------------------------------------

Your ``libfranka`` version does not match the robot’s system version.  
Use the reported server version to select the correct version (see :ref:`Robot System Version Compatibility <libfranka_compatibility>`).


.. _troubleshooting_safety_function_active:

Running a libfranka executable fails with safety function errors
----------------------------------------------------------------

Errors such as:

* `"command rejected due to activated safety function!"`
* `"command preempted due to activated safety function!"`

occur when a safety rule in Watchman prevents robot motion (e.g., speed limits).  
Disable or remove the relevant safety rule to allow FCI motion commands.


.. _troubleshooting_realtime_control_loops:

Realtime Control Loop Best Practices
------------------------------------

When implementing a 1 kHz control loop, the interval between **read** and **write** must complete within **500 µs**.

Delays may increase if:

* A switch is used instead of a direct connection
* The Ethernet card is low-performance
* A real-time kernel is not used


.. _realtime_what_not_to_do:

What NOT to do in 1 kHz control loops
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**❌ Load the model inside the loop**

.. code-block:: cpp
   :emphasize-lines: 7

   // BAD
   while (!torques.motion_finished) {
     std::tie(robot_state, period) = rw_interface->readOnce();
     franka::Model model = robot.loadModel();  // NEVER do this!
     auto gravity = model.gravity(robot_state);
     rw_interface->writeOnce(torques);
   }

**Good practice: load once before loop**

.. code-block:: cpp

   franka::Model model = robot.loadModel();
   while (...) {
     // use model
   }


**❌ Sleep or block inside the loop**

.. code-block:: cpp

   std::this_thread::sleep_for(std::chrono::microseconds(100));  // BLOCKS RT!


**❌ Print every cycle**

.. code-block:: cpp

   std::cout << "State: " << robot_state.q << std::endl;  // TOO SLOW


**❌ Dynamic memory allocations**

.. code-block:: cpp

   std::vector<double> error(7);  // allocated every cycle → BAD


**Good alternatives: preallocate or use fixed-size arrays**

.. code-block:: cpp

   std::array<double, 7> tau_d{};
   while (...) {
     // deterministic
   }
