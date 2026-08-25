# show services

## Description

display information about deployed app services

## Usage

```
1Usage: forge show services [options]
2
```

## Options

```
1--verbose                        enable verbose mode
2-e, --environment [environment]  specify the environment (see your default
3                                 environment by running forge settings list)
4-s, --service [service]          specify the name of the service
5-w, --watch                      watch for changes to selected services
6--json                           output service information in JSON format
7                                 (default: false)
8-h, --help                       display help for command
9
```

## Operation

This command is used with Forge Container services, which is now in [Preview](/platform/forge/whats-coming/#forge-preview). Preview features are fully supported but remain under active development and may be subject to shorter deprecation windows.

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
