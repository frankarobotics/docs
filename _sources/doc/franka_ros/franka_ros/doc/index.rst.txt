franka_ros
==========
.. note::

 ``franka_ros`` is not supported on Windows.

Before continuing with this chapter, please install or compile franka_ros following the installation instructions.

You can access the changelog of franka_ros at `this link <https://github.com/frankarobotics/franka_ros/blob/develop/CHANGELOG.md>`_

.. figure:: _static/ros-architecture.png
    :align: center
    :figclass: align-center

    Schematic overview of the ``franka_ros`` packages.

The ``franka_ros`` metapackage integrates ``libfranka`` into ROS and ROS control.
Here, we introduce its packages and
we also give a short how-to for :ref:`writing controllers <write_own_controller>`.

All parameters passed to launch files in this section come with default values, so they
can be omitted if using the default network addresses and ROS namespaces.
Make sure the ``source`` command was called with the setup script from your workspace:

.. code-block:: shell

   source /path/to/catkin_ws/devel/setup.sh
