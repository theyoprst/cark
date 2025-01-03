# cark

Noah's Ark for your configs.
A command-line tool to backup configuration files from your user directory.

## Installation

You can install `cark` using Poetry: `poetry install`.

## Usage

1. Create a dedicated git repository for configs, e.g. `git@github.com:theyoprst/configs.git`

2. Create a YAML config in `~/.config/cark.yaml`

```yaml
destination:
  path: ~/.cark-data
  git_remote: git@github.com:theyoprst/configs.git
  git_branch: personal-laptop

include:
- .config/cark.yaml # This file.
- .config/fish/config.fish
- .config/starship.toml
- .config/zed/settings.json
- .gitconfig
- .gitignore
- .golangci.yaml
```

3. Run backup

```sh
poetry run cark backup
```

It will backup all the files and push them to the specified git repository in the specified branch.

## TODO

- [ ] Remove not found files from the git repository (e.g. remove everything first)
- [ ] Run it periodically and store logs somewhere OR run it as a service
- [ ] Find files by mask recursively

