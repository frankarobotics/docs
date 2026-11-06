# Test Suite Architecture

This directory contains the integration and structural tests for the
`franka_bringup` package. Tests are organized by what they verify and
what hardware they require.

> Note: TMR fake-hardware is not covered because its `cartesian_velocity` GPIO
> command interfaces are not satisfiable under `mock_components/GenericSystem`.

## Test Categories

| Category | Requires Hardware | Framework | Purpose |
|----------|:-:|---|---|
| Fake-hardware integration | ❌ | launch_testing | Verify controller lifecycle with `mock_components/GenericSystem` |
| Interface validation | ❌ | pytest | Assert URDF xacro expands to correct ros2_control interfaces |
| Launch file parsing | ❌ | pytest | Verify all launch files import and generate valid descriptions |
| Teleop plumbing | ❌ | launch_testing | Verify Joy→cmd_vel pipeline works |
| Hardware smoke tests | ✅ | launch_testing | Run controllers on real robot for fixed duration |

## File Layout

```
test/
├── config/                                # YAML configs for test scenarios
│   ├── test_use_fake_hardware.config.yaml   # FR3 single-arm (use_fake_hardware=false)
│   ├── test_fake_hardware_fr3.config.yaml   # FR3 single-arm (fake hw)
│   ├── test_0.config.yaml ... test_1.config.yaml  # Real-hardware configs
│   └── ...
├── test_fake_hardware_controllers.py      # FR3 controller lifecycle (fake hw)
├── test_franka_arm_interfaces.py          # Single-arm URDF interface validation
├── test_xacro_path_resolution.py          # xacro path resolution validation
├── test_teleop_plumbing.py                # Joy → cmd_vel pipeline validation
├── test_launch_file_parsing.py            # Launch file structural validation
├── test_hardware_example_controllers.py   # Real-hardware controller tests
├── test_hardware_generic_controller.py    # Real-hardware generic test framework
├── test_gazebo_wrapper_expansion.py       # Gazebo URDF expansion test
└── ros2_control_test_helpers.py           # Shared URDF parsing utilities
```

## Shared Testing Utilities

Located in `franka_bringup/franka_bringup/testing/`:

- **`fake_hardware_test_base.py`** — `FakeHardwareTestBase` class providing
  ROS lifecycle management, joint_state waiting, and error assertion for all
  fake-hardware tests.
- **`controller_service_client.py`** — Service client wrapper for
  controller_manager operations (load, configure, switch, unload).
- **`controller_test_utils.py`** — Higher-level utilities for hardware tests
  (move_to_start workflow, smoke test runner).

## Fake-Hardware Test Design

All fake-hardware tests inherit from `FakeHardwareTestBase` and share:

1. **ROS lifecycle** — `rclpy.init()` in `setUpClass`, shutdown in
   `tearDownClass`, per-test node creation in `setUp`/`tearDown`.
2. **Stack readiness check** — `wait_for_stack_ready()` waits for
   controller_manager services and joint_state_broadcaster activation.
3. **Joint state verification** — `wait_for_joint_states(min_joints=N)`
   subscribes to `/joint_states` and waits for messages with enough joints.
4. **Error output assertion** — `assert_no_errors_in_output(proc_output)`
   with optional `ignore_patterns` for expected errors.

### Known Limitations

- **Franka GPIO controllers** (cartesian_pose, cartesian_velocity, etc.)
  cannot activate because `GenericSystem` doesn't provide GPIO interfaces.
  These are tested at load-only level.
- **`franka_fr3_moveit_config`** cannot be declared as a `test_depend` in
  `franka_bringup/package.xml` because it would create a circular dependency.
  The launch parsing test for MoveIt files works in full-workspace builds (CI),
  where a missing package is a failure. For isolated
  `--packages-up-to franka_bringup` builds, export
  `FRANKA_LAUNCH_TEST_ALLOW_MISSING_PACKAGES=1` to turn those cases into skips.

## Running Tests

```bash
# All no-hardware tests (CI default)
colcon test --packages-select franka_bringup \
  --ctest-args --exclude-regex 'test_hardware'

# Only fake-hardware integration tests
colcon test --packages-select franka_bringup \
  --ctest-args --tests-regex 'test_fake_hardware'

# Only interface/structural tests
colcon test --packages-select franka_bringup \
  --ctest-args --tests-regex 'test_franka_arm|test_launch|test_xacro'

# Hardware tests (requires robot_ip)
colcon test --packages-select franka_bringup \
  --ctest-args --tests-regex 'test_hardware' -- --robot_ip <ip>
```

## Adding New Tests

1. For a new fake-hardware test: inherit from `FakeHardwareTestBase`,
   define test methods, and provide `generate_test_description()`.
2. For a new interface test: use `ros2_control_test_helpers.py` utilities
   to expand xacro and assert on the parsed hardware components.
3. Register in `CMakeLists.txt` using `add_ros_isolated_launch_test()` or
   `ament_add_pytest_test()`.
