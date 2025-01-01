import shutil
from pathlib import Path

from conf_ark.config import Config


def backup_configs(backup_dir: str, config: Config) -> None:
    """
    Backup configuration files from user directory.

    Args:
        backup_dir: Directory where backups will be stored
    """
    backup_dir = Path(backup_dir).expanduser()

    # Create backup directory
    backup_dir.mkdir(parents=True, exist_ok=True)

    home = Path.home()

    for relpath in config.include:
        src = home / relpath
        if src.exists():
            dst = backup_dir / relpath

            # Create parent directories if they don't exist
            dst.parent.mkdir(parents=True, exist_ok=True)

            if src.is_file():
                print(f"Copying file: {src}")
                shutil.copy2(src, dst)
            elif src.is_dir():
                print(f"Copying directory: {src}")
                shutil.copytree(src, dst, dirs_exist_ok=True)
        else:
            print(f"Config not found: {src}")
