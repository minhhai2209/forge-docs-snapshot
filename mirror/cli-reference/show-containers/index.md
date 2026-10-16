# show containers

## Description

display information about deployed app containers for a given service

## Usage

```
1Usage: forge show containers [options]
2
```

## Options

```
1--verbose                        enable verbose mode
2-s, --service <service>          specify the name of a service
3-c, --container [container]      specify the name of a container
4-e, --environment [environment]  specify the environment (see your default
5                                 environment by running forge settings list)
6--json                           output results in JSON format (default:
7                                 false)
8--placement <placement>          placement where the app is deployed
9-h, --help                       display help for command
10
```

## Operation

This command is used with Forge Container services, which is now in [Preview](/platform/forge/whats-coming/#forge-preview). Preview features are fully supported but remain under active development and may be subject to shorter deprecation windows.

Run `forge show containers` from your app's root directory to inspect the deployed containers for a service. Use `-e <environment>` to select an environment. If you omit it, the command uses your default environment, which you can check with `forge settings list`.

The command shows the container name and image repository above a table with these columns:

| **Column** | **Type** | **Purpose** |
| --- | --- | --- |
| **Image Tag** | string | Tag of the image running in the reported instance. |
| **Health** | `Healthy` `Unhealthy` `Unknown` | The reported health of the container. |
| **Status** | `Provisioning` `Running` `Removing` `Unknown` | The state of the reported container instance. |
| **CPU** | string | Reported CPU value in millicores (`m`). |
| **Memory** | string | Reported memory value in mebibytes (`MiB`). |
| **Created at** | timestamp | Creation timestamp of the reported instance. |
| **Instance** | string | Identifier of the reported instance. |

CPU and memory show usage metrics when available. If usage metrics are unavailable, the command may show configured resource allocations instead. These fallback values do not represent current usage. A `Not Available` means a resource value is unavailable; it does not mean zero usage. To view configured resource limits, check the container's [`resources` definition](/platform/forge/containers-reference/ref-manifest/#resources) in the manifest.

### Example

```
```
1
2
```



```
forge show containers -e development -s java-service
```
```

Example output may look like:

```
```
1
2
3
4
5
6
7
8
```



```
Container: java-service
Image repository: forge-registry.services.atlassian.com/forge/5175c066-7f18-474e-9137-19e6718a8c99/java-service
┌───────────┬─────────┬─────────┬──────┬────────┬──────────────────────────┬───────────────────────────────┐
│ Image Tag │ Health  │ Status  │ CPU  │ Memory │ Created at               │ Instance                      │
├───────────┼─────────┼─────────┼──────┼────────┼──────────────────────────┼───────────────────────────────┤
│ 1.0.0     │ Healthy │ Running │ 125m │ 256MiB │ 2026-10-15T01:00:00.000Z │ java-service-7d8f6c9b5f-abcde │
└───────────┴─────────┴─────────┴──────┴────────┴──────────────────────────┴───────────────────────────────┘
```
```

### Specify a service

To specify a service whose containers you want to inspect, use the `-s <service-name>` option. If you don't use this option, the
`forge show containers` command will ask you to choose from a list of all services defined in the
[manifest](/platform/forge/containers-reference/ref-manifest/).

### Specify a container

To specify which container of a specific service to inspect, use the `-s <service-name> -c <container-name>` option.

## Further information
