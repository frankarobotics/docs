# Controller Manager

## Overview

This controller_manager is borrowed from the [ros2_control repository](https://github.com/ros-controls/ros2_control) with custom modifications to meet our specific requirements.

## Modifications

We have added the **disabling of the sleep with overrun feature** on top of [commit 45e548c](https://github.com/ros-controls/ros2_control/commit/45e548c8c48ca7f1e9678983cd5b52ff04da00de) from the ros2_control repository.

### Base Commit
- **Repository**: [ros-controls/ros2_control](https://github.com/ros-controls/ros2_control)
- **Commit**: [`45e548c8c48ca7f1e9678983cd5b52ff04da00de`](https://github.com/ros-controls/ros2_control/commit/45e548c8c48ca7f1e9678983cd5b52ff04da00de)
- **Modification**: Sleep feature disabled

## Future Plans

After resolving [issue #2529](https://github.com/ros-controls/ros2_control/issues/2529) in the upstream ros2_control repository, we plan to:

- Discontinue this custom fork
- Return to using the latest binary packages from the official ros2_control repository

## Related Links

- [Upstream ros2_control Repository](https://github.com/ros-controls/ros2_control)
- [Tracking Issue #2529](https://github.com/ros-controls/ros2_control/issues/2529)
- [Base Commit](https://github.com/ros-controls/ros2_control/commit/45e548c8c48ca7f1e9678983cd5b52ff04da00de)