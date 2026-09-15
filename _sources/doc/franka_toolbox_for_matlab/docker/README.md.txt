# Docker Build System

This directory contains Docker infrastructure for building Franka Toolbox server binaries.

## Quick Start

```bash
cd docker
./build.sh              # Build for both x86_64 and ARM64
./build.sh amd64        # x86_64 only
./build.sh arm64        # ARM64 only (cross-compiled)
```

## Output

| File | Description |
|------|-------------|
| `common/bin.zip` | x86_64 common library |
| `common/bin_arm.zip` | ARM64 common library |
| `franka_robot_server/bin.tar.gz` | x86_64 server |
| `franka_robot_server/bin_arm.tar.gz` | ARM64 server |
| `dependencies/libfranka.zip` | x86_64 libfranka |
| `dependencies/libfranka_arm.zip` | ARM64 libfranka |

## Options

```bash
./build.sh [arch] [options]

  amd64 | arm64 | all     Architecture (default: all)
  --no-cache              Rebuild without Docker cache
  --libfranka <version>   Override libfranka version
  --build-type <type>     Release or Debug (default: Release)
```

## Documentation

For complete build instructions including MEX files and distribution packaging, see the [Custom Build Guide](https://frankarobotics.github.io/docs/franka_toolbox_for_matlab/docs/franka_matlab/custom_build.html).
