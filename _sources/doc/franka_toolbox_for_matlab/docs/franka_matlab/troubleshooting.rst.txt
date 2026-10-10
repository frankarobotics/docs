Troubleshooting
===============

.. hint::
    Checkout the `Franka Community <https://www.franka-community.de>`_  and the
    `franka_matlab category <https://www.franka-community.de/c/franka-matlab/15>`_ for relevant posts or for creating new ones!

control_modes.h: No such file or directory error.
-------------------------------------------------

.. figure:: _static/simulink_model_apply_control_only_build_error.png
    :align: center
    :figclass: align-center

    The build error message in simulink when only the "apply control is present".

This is a known current limitation of the system, as the build process will fail if only
the "apply control" block is present in a simulink model.

.. figure:: _static/simulink_model_apply_control_only.png
    :align: center
    :figclass: align-center

    Example of a Simulink model with only "apply control". The build will fail.

For fixing the issue just include any other block from the Franka Simulink Library, e.g
with the terminal if it will be left unused.

.. figure:: _static/simulink_model_apply_control_only_fix.png
    :align: center
    :figclass: align-center

    Fixing the "control_modes.h: No such file or directory error." by including any other
    block from the Franka Simulink Library.

missing "MW_custom_RTOS_header.h"
---------------------------------

When working with the AI Companion or a NVIDIA Jetson platform, if you encounter an error
releated to missing "MW_custom_RTOS_header.h", you can try forcing the NVIDIA Simulink Code Generation settings to reset:

.. figure:: _static/ai_companion_jetson_trouble.png
    :align: center
    :figclass: align-center

    Fixing the "missing MW_custom_RTOS_header.h" error by forcing the Simulink Jetson related
    settings to reset.

libfranka reference
-------------------
.. hint::
    Same error messages and advised troubleshooting applies as `libfranka <https://frankarobotics.github.io/docs/troubleshooting.html>`_.

Issues with the graphics driver in Linux
----------------------------------------

NVIDIA's graphics driver's are not officially supported in Linux with Real-Time Kernel. This could cause issues in graphics renderings in Matlab
and Simulink, e.g with figures and scopes respectively. We would then recommend starting matlab with the `-softwareopengl` for avoiding these issues:

.. code-block:: shell

    $ matlab -softwareopengl

Issues with libstdc++.so and other system dynamic libraries
-----------------------------------------------------------

Make sure that you have installed the `matlab-support package <https://packages.ubuntu.com/search?keywords=matlab-support>`_ for your system, in order for Matlab to reference the system dynamic libraries
instead of the precompiled ones that it ships with:

.. code-block:: shell

    sudo apt install matlab-support

Franka Simulink library number of block instances
-------------------------------------------------

.. important::
    The Simulink library has been designed for rapid-prototyping of robot controllers with one-robot
    in mind. Multiple instances for the Apply Control block are not encouraged as this has not been tested.
    Multiple instances of all the other Simulink blocks, as long as they point to the same robot ip, can be
    utilized.
