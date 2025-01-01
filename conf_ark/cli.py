import click
from conf_ark.backup import backup_configs


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
    backup_configs(backup_dir)
    click.echo(f"Backup completed to {backup_dir}")


if __name__ == '__main__':
    main()
