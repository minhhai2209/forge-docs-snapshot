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

This command is used with Forge Containers, which is currently available under
[Forge's Early Access Program (EAP)](/platform/forge/whats-coming/#eap).
EAPs are offered to selected users for testing and feedback purposes.

APIs and features under EAP are:

* Unsupported and subject to change without notice
* Not recommended for use in production environments

Use the `forge containers` command with any of the following subcommands to manage container instances and images for your service:

## Further information
