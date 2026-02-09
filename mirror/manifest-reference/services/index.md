# Services (EAP)

Forge Containers are now available through Forge's Early Access Program (EAP). To start testing this feature,
submit your app's ID to our team [through this link](https://ecosystem.atlassian.net/servicedesk/customer/portal/1040/create/18884).

EAPs are offered to selected users for testing and feedback purposes. APIs and features under EAP
are unsupported and subject to change without notice. APIs and features under EAP are not recommended
for use in production environments.

For more details, see [Forge EAP, Preview, and GA](/platform/forge/whats-coming/#eap).

Forge features a top-level manifest property named `services` that lets you define a service and its corresponding container.
It supports the following properties:

| **Property** | **Required?** | **Description** |
| --- | --- | --- |
| `key` | Yes | A key for the service, which modules (like [endpoint](/platform/forge/manifest-reference/endpoint/)) can refer to. Each service in the manifest must have a unique key (regex: `^[a-zA-Z0-9_-]+$`) |
| `containers` | Yes | Defines a container (and its properties) within the service. The `containers` property supports its own set of properties to configure a container; see [Property: containers](/platform/forge/containers-reference/ref-manifest/#containers) for details. |
| `tunnel` | No | Defines the local port that invocations of the service should be made to whilst tunnelling. If undefined, requests will be made to port `7071`. See [Property: tunnel](/platform/forge/containers-reference/ref-manifest/#tunnel) for details. |
| `scaling` | No | Horizontal scaling configuration defining the min & max number of container instances to run. See [Property: scaling](/platform/forge/containers-reference/ref-manifest/#scaling) for details. |

The ability to configure multiple services and containers per app is available behind a feature flag. Contact us if your app requires multiple services. See [Roadmap](/platform/forge/containers-reference/roadmap) for details on upcoming updates.

## Containers

The `containers` property lets you configure a container’s resource, scaling, and health check settings:

| **Property** | **Required?** | **Description** |
| --- | --- | --- |
| `key` | Yes | A unique key that maps to the container’s image repository URI. This key is created with the `forge containers create` [command](http://platform/forge/containers-reference/ref-cli/#create); to view all container keys and their corresponding repository URIs, use the `forge repositories list` [command](/platform/forge/containers-reference/ref-cli/#list). |
| `tag` | Yes | The tag of the image that Forge should use to deploy the container. This image (and tag) must exist in the Forge Container Registry. |
| `resources` | Yes | Vertical scaling configuration defining CPU and memory available to your container, using the following settings:  * `cpu`: reserved amount of CPU units for the container in either *cpu* or *millicpu*, for example `"1"` or `"1000m"`. * `memory`: reserved amount of memory units for the container in either *mebibytes* or *gibibytes*, for example `"2048Mi"` or `"2Gi"`. |
| `health` | Yes | Configuration for an HTTP Health check that the Forge Platform will poll for a 2xx response before directing traffic to your container. |
| `tunnel` | No | Configuration to deploy the container locally and start it automatically with `forge tunnel`. These settings follow the same syntax as a standard docker compose file. See [Testing a containerised service locally](/platform/forge/containers-reference/test-service-locally/) for more information. |

## Scaling

The `scaling` property defines how the service should scale the number of instances.

| **Property** | **Required?** | **Description** |
| --- | --- | --- |
| `min` | Yes | The minimum number of instances that the service can scale down to. |
| `max` | Yes | The maximum number of instances that the service can scale up to. |
| `profile` | No | The scaling configuration used by this service. |

### Scaling profiles

For now, the only supported profile is `default`.
With this profile, scaling behaviors are triggered whenever the average CPU or memory usage reaches the following thresholds:

| **Resource** | **Average resource usage threshold** |
| --- | --- |
| CPU | 50% |
| Memory | 70% |

The following table describes the `default` profile’s scaling behavior:

| **Scaling behavior** | **Scale by** | **Trigger** |
| --- | --- | --- |
| Scale Up | 100% | Instances reached the average usage threshold. |
| Scale Down | 50% | Instances stay under the average usage threshold for a full 300 seconds. |

Forge Containers checks average resource usage every 15 seconds.

## Tunnel

The `tunnel` property lets you configure which port service invocations should be made to.

| **Property** | **Required?** | **Description** |
| --- | --- | --- |
| `port` | Yes | The port of the locally-deployed service. While tunnelling, any invocations of this service will be made to `localhost:${port}`. |

## Example

The following snippet shows a service named `java-service`, which is backed by a container of the same name. The service is accessible via the `/webtrigger` route on the `webtrigger-ep` [endpoint module](/platform/forge/manifest-reference/endpoint/#endpoint).

```
```
1
2
```



```
modules:
  webtrigger:
    - key: container-webtrigger
      endpoint: webtrigger-ep
  endpoint:
    - key: webtrigger-ep
      service: java-service
      route:
        path: /webtrigger

services:
  - key: java-service
    containers:
      - key: java-service
        tag: latest
        resources:
          cpu: "1"
          memory: "2Gi"
        health:
          type: http
          route:
            path: "/healthcheck"
    scaling: 
      min: 1
      max: 1
```
```
