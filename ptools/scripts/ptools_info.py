import shutil
from pathlib import Path

import pkg_resources

from ptools.base import Script
from ptools.config import (
    SECRETS_FILE_PATH,
    SECRETS_TEMPLATE_PATH,
    SETTINGS_FILE_PATH,
    SETTINGS_TEMPLATE_PATH,
    ptools_dirs,
)
from ptools.utils import open_file_with_default


class PTools(Script):
    """Script providing information about the package."""

    @classmethod
    def info(cls) -> None:
        """Output basic info."""
        print(f"ptools version {cls.version()}")
        print(f"Settings files location: {ptools_dirs.user_config_dir}")

    @classmethod
    def version(cls) -> str:
        """Return the version of the current ptools build."""
        version = pkg_resources.get_distribution("ptools").version
        assert isinstance(version, str)
        return version

    @staticmethod
    def _open_for_editing(to_open: Path, template: Path) -> None:
        """Opens a file for editing, creating it from a template if it does not
        exist.
        """
        if not to_open.exists():
            if not to_open.parent.exists():
                to_open.parent.mkdir()
            shutil.copy(template, to_open)
        open_file_with_default(to_open)

    @classmethod
    def config(cls) -> None:
        """Open an editor for editing settings."""
        cls._open_for_editing(SETTINGS_FILE_PATH, SETTINGS_TEMPLATE_PATH)

    @classmethod
    def config_secrets(cls) -> None:
        """Open an editor for editing secrets."""
        cls._open_for_editing(SECRETS_FILE_PATH, SECRETS_TEMPLATE_PATH)
