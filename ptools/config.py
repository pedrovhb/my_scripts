from pathlib import Path

from appdirs import AppDirs
from dynaconf import Dynaconf

ptools_dirs = AppDirs("ptools")

# Settings and secrets paths.
# On Linux, results in e.g. /home/pedro/.config/ptools/settings.toml
SETTINGS_DIR = Path(ptools_dirs.user_config_dir)

SETTINGS_FILE_NAME = "settings.toml"
SECRETS_FILE_NAME = ".secrets.toml"
SETTINGS_FILE_PATH = SETTINGS_DIR / SETTINGS_FILE_NAME
SECRETS_FILE_PATH = SETTINGS_DIR / SECRETS_FILE_NAME

# Settings and secrets template paths
SETTINGS_TEMPLATES_DIR = Path(__file__).parent / "settings_templates"
SETTINGS_TEMPLATE_PATH = SETTINGS_TEMPLATES_DIR / SETTINGS_FILE_NAME
SECRETS_TEMPLATE_PATH = SETTINGS_TEMPLATES_DIR / SECRETS_FILE_NAME

# Define settings objects that is imported and used throughout code
settings = Dynaconf(
    root_path=SETTINGS_DIR,
    envvar_prefix="DYNACONF",
    settings_files=[SETTINGS_FILE_NAME, SECRETS_FILE_NAME],
)
