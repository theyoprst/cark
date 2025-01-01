import os
import shutil
from datetime import datetime
from pathlib import Path
import yaml


def backup_configs(backup_dir: str) -> None:
    """
    Backup configuration files from user directory.

    Args:
        backup_dir: Directory where backups will be stored
    """
    backup_dir = Path(backup_dir).expanduser()

    # Create backup directory
    backup_dir.mkdir(parents=True, exist_ok=True)

    # Read config paths from YAML file
    config_file = Path("~/.config-backup.yaml").expanduser()
    if not config_file.exists():
        raise FileNotFoundError(f"Config file not found: {config_file}")

    with open(config_file) as f:
        config_data = yaml.safe_load(f)

    config_paths = config_data.get("include", [])
    if not config_paths:
        raise ValueError("No paths specified in config file")

    home = Path.home()

    for relpath in config_paths:
        src = home / relpath
        if src.exists():
            dst = backup_dir / relpath

            # Create parent directories if they don't exist
            dst.parent.mkdir(parents=True, exist_ok=True)

            if src.is_file():
                shutil.copy2(src, dst)
            elif src.is_dir():
                shutil.copytree(src, dst, dirs_exist_ok=True)
        else:
            print(f"Config not found: {src}")
