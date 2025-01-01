from pathlib import Path
from typing import List
from dataclasses import dataclass

import yaml


@dataclass
class Config:
    """Configuration data object."""
    include: List[str]
    backup_dir: Path
    git_remote: str | None = None
    git_branch: str | None = None

    @classmethod
    def from_file(cls, path: str | Path) -> "Config":
        """
        Load configuration from a YAML file.

        Args:
            path: Path to the configuration file

        Returns:
            Config object with loaded data

        Raises:
            FileNotFoundError: If config file doesn't exist
            ValueError: If no paths are specified in config
        """
        config_file = Path(path).expanduser()
        if not config_file.exists():
            raise FileNotFoundError(f"Config file not found: {config_file}")

        with open(config_file) as f:
            config_data = yaml.safe_load(f)

        include_paths = config_data.get("include", [])
        if not include_paths:
            raise ValueError("No paths specified in config file")

        destination = config_data.get("destination", {})
        backup_dir = Path(destination.get("path", "~/.config-backup")).expanduser()
        git_remote = destination.get("git_remote")
        git_branch = destination.get("git_branch")

        return cls(
            include=include_paths,
            backup_dir=backup_dir,
            git_remote=git_remote,
            git_branch=git_branch
        )
