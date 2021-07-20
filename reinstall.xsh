#!/usr/bin/env xonsh

# Rebuild wheels and reinstall with pipx to refresh the CLI with the latest code

# Bump patch version
poetry version patch

# Build wheel
build_str = $(poetry build -f wheel)
print(build_str)  # xonsh $() captures stdout

# Reinstall CLI apps from new wheel
wheel_file = build_str.split()[-1]
pipx install dist/@(wheel_file) --force
