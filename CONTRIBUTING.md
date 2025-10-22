# Contributing to this Project

## Getting Started

To start contributing, you can first build the documentation by following the instructions in the [README.md](README.md) file. This will help you understand the structure and content of the documentation.
After that, feel free to explore the codebase and identify areas where you can contribute.

## Structure of Documentation

The main source files are located in the `docs/` directory. Yet, we pull from various repositories via VCS such as `libfranka` or `franka_ros2` to create a comprehensive documentation set. If you want to contribute, it helps to work on the source repositories within this workspace to allow a verification that the documentation still builds **successfully** and the linter **checks pass**.

## Building and Validating

For building and validating the documentation, you need to install following dependencies:

```bash
sudo apt-get install nodejs npm
sudo npm install -g eclint
```

, you can use the following commands:

```bash
make html
find source -name "*.rst" | xargs eclint check
make linkcheck
```

Thank you for your contributions!
