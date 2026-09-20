# containers delete

## Description

delete container definition along with the associated image repository and all
of its images

## Usage

```
1Usage: forge containers delete [options]
2
```

## Options

```
1--verbose        enable verbose mode
2-k, --key <key>  specify the key of the container
3-f, --force      force deletion without confirmation
4-h, --help       display help for command
5
```

## Operation

This command is used with Forge Container services, which is now in [Preview](/platform/forge/whats-coming/#forge-preview). Preview features are fully supported but remain under active development and may be subject to shorter deprecation windows.

Use `forge containers delete` to delete an existing Forge Container services registry, along with its associated image repository (this includes all stored images). This command cannot be undone.

For a complete list of `forge containers` subcommands, refer to the command's [reference](/platform/forge/cli-reference/containers/#operation).

## Further information
