# show services

## Description

display information about deployed app services

## Usage

```
1
Usage: forge show services [options]
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
-e, --environment [environment]  specify the environment (see your default
                                 environment by running forge settings list)
-s, --service [service]          specify the name of the service
-w, --watch                      watch for changes to selected services
--json                           output service information in JSON format
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

Use the `forge show services` command to display details about all services, or a specific service. This command provides the following service details:

| **Column** | **Type** | **Purpose** |
| --- | --- | --- |
| **Service** | string | Name of the service, as defined in the manifest. This column only appears if the `-s` option is *not* used. |
| **Service Status** | `Available` `Unavailable` | Whether the service is receiving production traffic. |
| **Running Count** | integer | Number of available service instances. |
| **Pending Count** | integer | Number of service instances being created but not yet `Healthy` (Status). |
| **Min** | integer | Minimum number of service instances. |
| **Max** | integer | Maximum number of service instances. |
| **Created At** | timestamp | When the service was created. |
| **Updated At** | timestamp | When the service definition was last updated. |
| **Version Status** | `Updating` `Up-to-date` | `Updating`: Indicated the service is in the process of being replaced with a new version. `Up-to-date`: Indicates the service is at the latest deployed version. |

When you use the `-s <service-name>` option, you'll only see details for that service. The `<service-name>` must map to the
same `service.key` value used in the [manifest](/platform/forge/containers-reference/ref-manifest/).

If you don't use this option, the command will display details about *all* services defined in the manifest.

## Further information
