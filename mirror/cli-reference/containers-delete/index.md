# containers delete

## Description

delete container definition along with the associated image repository and all
of its images

## Usage

```
1
Usage: forge containers delete [options]
```

## Options

```
1
2
3
4
--verbose        enable verbose mode
-k, --key <key>  specify the key of the container
-f, --force      force deletion without confirmation
-h, --help       display help for command
```

## Operation

This command is used with Forge Containers, which is currently available under
[Forge's Early Access Program (EAP)](/platform/forge/whats-coming/#eap).
EAPs are offered to selected users for testing and feedback purposes.

APIs and features under EAP are:

* Unsupported and subject to change without notice
* Not recommended for use in production environments

Use `forge containers delete` to delete an existing Forge Containers registry, along with its associated image repository (this includes all stored images). This command cannot be undone.

For a complete list of `forge containers` subcommands, refer to the command's [reference](/platform/forge/cli-reference/containers/#operation).

## Further information
