import os
import platform
import subprocess
from pathlib import Path


def open_file_with_default(filepath: Path) -> None:

    # From https://stackoverflow.com/a/435669/5686598.
    # Only tested on Linux.

    if platform.system() == "Darwin":
        # macOS
        subprocess.call(("open", filepath))
    elif platform.system() == "Windows":
        # Windows
        os.startfile(filepath)
    else:
        # Linux
        subprocess.call(("xdg-open", filepath))
