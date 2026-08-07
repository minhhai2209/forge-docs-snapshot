# containers create

## Description

create new container definition

## Usage

```
1
Usage: forge containers create [options]
```

## Options

```
1
2
3
--verbose        enable verbose mode
-k, --key <key>  specify the name of the container
-h, --help       display help for command
```

## Operation

This command is used with Forge Container services, which is now in [Preview](/platform/forge/whats-coming/#forge-preview). Preview features are fully supported but remain under active development and may be subject to shorter deprecation windows.

Use `forge containers create` to register a new container for your app, as well as a corresponding image repository (with its own repository URI). Each app can have a maximum of 10 container repositories.

The `key` you provide with this command will be the key used for the container's *image repository*. You'll also use this value as your
`container.key` value in the [manifest](/platform/forge/containers-reference/ref-manifest/#containers).

For a complete list of `forge containers` subcommands, refer to the command's [reference](/platform/forge/cli-reference/containers/#operation).

## Further information
