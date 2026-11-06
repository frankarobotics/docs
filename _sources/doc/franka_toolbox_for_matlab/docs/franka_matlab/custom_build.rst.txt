Custom Build
============

This guide covers building the Franka Toolbox from source. For most users, we recommend downloading the pre-built toolbox from the `GitHub Releases <https://github.com/frankarobotics/franka_toolbox_for_matlab/releases>`_ page.

Overview
--------

The toolbox consists of two parts:

1. **Server binaries** — Run on the target Linux PC connected to the robot
2. **MEX files** — Run on your MATLAB host (Windows or Linux)

Building Server Binaries (Docker)
---------------------------------

Server binaries are built using Docker, which handles all dependencies automatically.
If you need a specific ``libfranka`` version instead of the one used for the pre-built release packages, build with ``./build.sh --libfranka <version>`` from the ``docker/`` directory.
You can also build only ``amd64`` for a local host target or only ``arm64`` when targeting Jetson, instead of building both architectures.

**Requirements:** Docker installed and running

.. code-block:: bash

    cd docker
    ./build.sh              # Build for both x86_64 and ARM64
    # Or:
    ./build.sh amd64        # x86_64 only
    ./build.sh arm64        # ARM64 only (cross-compiled)

**Output files:**

- ``common/bin.zip``, ``common/bin_arm.zip`` — Common library
- ``franka_robot_server/bin.tar.gz``, ``franka_robot_server/bin_arm.tar.gz`` — Server executable
- ``dependencies/libfranka.zip``, ``dependencies/libfranka_arm.zip`` — libfranka with dependencies

For implementation details, see the ``Dockerfile.amd64`` and ``Dockerfile.arm64`` files in the ``docker/`` directory.

Building MEX Files
------------------

MEX files must be built on each platform where you want to use the toolbox.

Linux
^^^^^

**Install dependencies:**

.. code-block:: bash

    sudo apt-get update
    sudo apt-get install -y cmake build-essential libeigen3-dev

    # Build Cap'n Proto (static libraries with PIC)
    CAPNP_VERSION="1.0.2"
    curl -O https://capnproto.org/capnproto-c++-${CAPNP_VERSION}.tar.gz
    tar zxf capnproto-c++-${CAPNP_VERSION}.tar.gz
    cd capnproto-c++-${CAPNP_VERSION}
    mkdir build && cd build
    cmake -DBUILD_TESTING=OFF -DBUILD_SHARED_LIBS=OFF -DCMAKE_POSITION_INDEPENDENT_CODE=ON ..
    make -j$(nproc)
    sudo make install
    sudo ldconfig

**Build MEX files (in MATLAB):**

.. code-block:: matlab

    franka_simulink_library_mex();
    franka_robot_mex();

Windows
^^^^^^^

**Requirements:**

- Visual Studio 2022
- CMake 3.15+

**Install Cap'n Proto:**

Build Cap'n Proto from source as static libraries. See the CI workflow in ``.github/workflows/build-and-release.yml`` for the exact steps.

**Build MEX files (in MATLAB):**

.. code-block:: matlab

    franka_simulink_library_mex();
    franka_robot_mex();

Creating the Distribution Package
---------------------------------

After building both server binaries and MEX files:

.. code-block:: matlab

    franka_toolbox_dist_make();

By default, ``franka_toolbox_dist_make()`` now uses the CI-safe packaging behavior and preserves the generated server and MEX archives in your working tree.
This creates ``dist/franka.mltbx`` by default. You can also specify the output name:

.. code-block:: matlab

    franka_toolbox_dist_make('OutputName', 'franka-fr3'); % For FR3
    franka_toolbox_dist_make('OutputName', 'franka-fer'); % For FER

If you explicitly want the old local cleanup behavior, you can run:

.. code-block:: matlab

    franka_toolbox_dist_make('Mode', 'local');

``Mode='local'`` runs ``git clean -ffxd`` before packaging. This removes untracked generated artifacts from the repository checkout, including locally built archives that have not been committed.

CI/CD Reference
---------------

For a complete automated build example, see ``.github/workflows/build-and-release.yml`` which builds for all platforms and creates release packages.

