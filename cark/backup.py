import shutil
import subprocess
from pathlib import Path

from cark.config import Config


def backup_files(config: Config) -> None:
    """
    Backup (just copy) configuration files from user directory.
    """
    backup_dir = Path(config.backup_dir).expanduser()

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


def git_init(config: Config) -> None:
    """
    Initializes git repository if it was not initialized yet.
    It used branch name from the config.

    If the git repository was initialized, it asserts that git branch and git remote are the same as in config
    """
    repo_path = Path(config.backup_dir).expanduser()

    if not (repo_path / '.git').exists():
        # Initialize new repo
        subprocess.run(['git', 'init', '--initial-branch='+config.git_branch], cwd=repo_path, check=True)

        subprocess.run(['git', 'remote', 'add', 'origin', config.git_remote],
                        cwd=repo_path, check=True)

    else:
        # Verify existing repo matches config
        result = subprocess.run(['git', 'remote', 'get-url', 'origin'],
                                cwd=repo_path, capture_output=True, text=True)
        remote = result.stdout.strip()
        assert remote == config.git_remote, \
            f"Git remote mismatch. Expected {config.git_remote}, got {remote}"

        result = subprocess.run(['git', 'branch', '--show-current'],
                                cwd=repo_path, capture_output=True, text=True)
        branch = result.stdout.strip()
        assert branch == config.git_branch, \
            f"Git branch mismatch. Expected {config.git_branch}, got {branch}"


def git_push(config: Config) -> None:
    """
    Adds all files and pushes to the repository.
    """
    repo_path = Path(config.backup_dir).expanduser()
    subprocess.run(['git', 'add', '-A'], cwd=repo_path, check=True)

    # Check if there are changes to commit
    status = subprocess.run(['git', 'status', '--porcelain'],
                          cwd=repo_path, capture_output=True, text=True)
    if not status.stdout.strip():
        print("No changes to commit")
        return
    # Changes exist, commit and push
    subprocess.run(['git', '-c', 'user.name=Config Backup Bot',
                    '-c', 'user.email=bot@config-backup.local',
                    'commit', '-m', 'Update config backup'],
                    cwd=repo_path, check=True)
    subprocess.run(['git', 'push', 'origin', 'HEAD'], cwd=repo_path, check=True)
