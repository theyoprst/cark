import click

import conf_ark.backup as bk
import conf_ark.config as cfg


@click.group()
def main():
    """Config Backup - A tool to backup and restore configuration files."""
    pass


@main.command()
@click.option(
    '--backup-dir',
    default='~/.config-backup',
    help='Directory to store backups'
)
def backup(backup_dir):
    """Backup configuration files from user directory."""

    config = cfg.Config.from_file("~/.config-backup.yaml")
    bk.backup_configs(backup_dir, config)
    click.echo(f"Backup completed to {backup_dir}")


if __name__ == '__main__':
    main()
