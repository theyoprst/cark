import click

import conf_ark.backup as bk
import conf_ark.config as cfg


@click.group()
def main():
    """Config Backup - A tool to backup and restore configuration files."""
    pass


@main.command()
def backup():
    """Backup configuration files from user directory."""
    config = cfg.Config.from_file("~/.config/conf-arc.yaml")
    bk.backup_files(config)
    bk.git_init(config)
    bk.git_push(config)

    click.echo(f"Backup completed to {config.backup_dir}")

if __name__ == '__main__':
    main()
