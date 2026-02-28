# show containers

## Description

display information about deployed app containers for a given service

## Usage

```
1
Usage: forge show containers [options]
```

## Options

```
1
2
3
4
5
6
7
8
--verbose                        enable verbose mode
-s, --service <service>          specify the name of a service
-c, --container [container]      specify the name of a container
-e, --environment [environment]  specify the environment (see your default
                                 environment by running forge settings list)
--json                           output container information in JSON format
                                 (default: false)
-h, --help                       display help for command
```

## Operation

This command is used with Forge Containers, which is currently available under
[Forge's Early Access Program (EAP)](/platform/forge/whats-coming/#eap).
EAPs are offered to selected users for testing and feedback purposes.

APIs and features under EAP are:

* Unsupported and subject to change without notice
* Not recommended for use in production environments

Use the `forge show containers` command to display details about all containers of a specific service, or a specific container defined for that service. This command provides the following container details:

| **Column** | **Type** | **Purpose** |
| --- | --- | --- |
| **Container** | string | Container name as defined in manifest. |
| **Health** | `Healthy` `Unhealthy` | The response from the configured `health` check for the container. |
| **Status** | `Provisioning` `Running`  `Removing` | The state of a given container instance. |
| **ImageURI** | string | ImageURI that that the container is running. |
| **Created At** | timestamp | When the most recent instance of the container was created. |

### Specify a service

To specify a service whose containers you want to inspect, use the `-s <service-name>` option. If you don't use this option, the
`forge show containers` command will ask you to choose from a list of all services defined in the
[manifest](/platform/forge/containers-reference/ref-manifest/).

### Specify a container

To specify which container of a specific service to inspect, use the `-s <service-name> -c <container-name>` option.

## Further information
