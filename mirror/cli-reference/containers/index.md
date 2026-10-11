# containers

## Description

manage containers and container images

## Usage

```
1Usage: forge containers [options] [command]
2
```

## Options

```
1--verbose               enable verbose mode
2-h, --help              display help for command
3
```

## Commands

```
1create [options]        create new container definition
2get-login [options]     get login password for the image repository
3delete [options]        delete container definition along with the associated
4                        image repository and all of its images
5docker-login [options]  authenticate to container registry
6
```

## Operation

This command is used with Forge Container services, which is now in [Preview](/platform/forge/whats-coming/#forge-preview). Preview features are fully supported but remain under active development and may be subject to shorter deprecation windows.

Use the `forge containers` command with any of the following subcommands to manage container instances and images for your service:

## Further information
