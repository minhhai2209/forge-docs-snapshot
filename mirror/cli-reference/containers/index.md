# containers

## Description

manage containers and container images

## Usage

```
1
Usage: forge containers [options] [command]
```

## Options

```
1
2
--verbose               enable verbose mode
-h, --help              display help for command
```

## Commands

```
1
2
3
4
5
6
create [options]        create new container definition
delete [options]        delete container definition along with the associated
                        image repository and all of its images
docker-login [options]  authenticate to container registry
get-login [options]     get login password for the image repository
help [command]          display help for command
```

## Operation

This command is used with Forge Container services, which is now in [Preview](/platform/forge/whats-coming/#forge-preview). Preview features are fully supported but remain under active development and may be subject to shorter deprecation windows.

Use the `forge containers` command with any of the following subcommands to manage container instances and images for your service:

## Further information
