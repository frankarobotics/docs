# Franka Toolbox for MATLAB: Matlab & Simulink library for Franka Robotics research robots

A Simulink & Matlab library and tools for the Franka Robotics Robots based on the [Franka Control Interface (FCI)](https://frankarobotics.github.io/docs/). See the [documentation page](https://frankarobotics.github.io/docs/franka_toolbox_for_matlab/docs/franka_matlab/index.html) for more information.

The repository includes a complete franka.mtlbx distribution (including pre-built binaries) which you can find either under the `dist` folder or in the github release page.

You can alternatively build the project for your own machine configuration following the instructions bellow.

## Generating a franka.mtlbx distribution

1. Requirements: 

- Host PC: Windows
    - MATLAB R2022a or newer
    - Microsoft Visual Studio 2019 or newer
    - CMake 3.15 or newer
    - Git
    - Cap'n Proto: check https://capnproto.org/install.html#installation-windows

- Host PC: Linux
    - MATLAB R2022a or newer
    - Build essentials (gcc, g++, make)
    - CMake 3.15 or newer
    - Git
    - Cap'n Proto (build static library):
        ```bash
        # Install build dependencies
        sudo apt-get update
        sudo apt-get install -y build-essential cmake autoconf pkg-config libtool

        # Download and build Cap'n Proto from source
        curl -O https://capnproto.org/capnproto-c++-1.1.0.tar.gz
        tar zxf capnproto-c++-1.1.0.tar.gz
        cd capnproto-c++-1.1.0
        mkdir build && 
        cd build && 
        cmake -DBUILD_TESTING=OFF -DCMAKE_POSITION_INDEPENDENT_CODE=ON .. && 
        make -j10 && 
        sudo make install && 
        cd ../.. && 
        rm -rf capnproto-c++-1.1.0* && 
        sudo ldconfig
        ```

- Target PC: Host PC Linux or Jetson platform connected
    - libfranka's 3d party dependencies (based on libfranka's version). Refer to the [Documentation](https://github.com/frankarobotics/libfranka/blob/main/README.md) for more information. The dependencies in the local Linux native target PC (not AI Companion) should be installed in the native system and not in a container. For the AI compantion a running container can be targeted as well.
    - ssh keys setup for connection without password request.
    - Cap'n Proto (build static library):
        ```bash
        # Install build dependencies
        sudo apt-get update
        sudo apt-get install -y build-essential cmake autoconf pkg-config libtool

        # Install capnproto
        curl -O https://capnproto.org/capnproto-c++-1.1.0.tar.gz && 
        tar zxf capnproto-c++-1.1.0.tar.gz && 
        cd capnproto-c++-1.1.0 && 
        mkdir build && 
        cd build && 
        cmake -DBUILD_TESTING=OFF .. && 
        make -j3 && 
        sudo make install && 
        cd ../.. && 
        rm -rf capnproto-c++-1.1.0* && 
        sudo ldconfig
        ```

2. Set the desired libfranka version in the `libfranka_ver.csv` file under the `configs` folder

3. Build the binaries:


    1. If executed in windows: franka_toolbox_binaries_all_build(); will generate the necessary binaries for windows host (no libfranka related).

    2. If executed in Linux: franka_toolbox_binaries_all_build(); will generate the necessary binaries for linux host (no libfranka related) + the necessary binaries for linux as target (libfranka dependent).

    3. If executed with AI Companion connected as well from Linux host: franka_toolbox_binaries_all_build(user,ip,port); will generate the necessary binaries for linux host (no libfranka related) + the necessary binaries for linux as target (libfranka dependent) + the necessary binaries for the AI Companion (libfranka dependent).

    For generating all the necessary binaries for the final project packaging & distribution --> Steps 1. & 3. MUST be performed!

    a. First from a Ubuntu Host PC with AI companion PC connected with user, ip, port provided

    ```
    >> franka_toolbox_binaries_all_build(user, ip, port);
    ```

    b. Then from a Windows Host PC (no Jetson connected)

    ```
    >> franka_toolbox_binaries_all_build();
    ```

    For Windows only the Simulink sfunctions and the Matlab Franka Robot client will be built.

4. Generate the distribution (Tested in Linux Host PC):

    ```
    >> franka_toolbox_dist_make();
    ```