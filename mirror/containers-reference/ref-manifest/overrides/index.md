# Manifest overrides for Forge Container services (Preview)

Forge Container services is now in Preview, and therefore fully supported. However, it remains under active development and may be subject to shorter deprecation windows. Preview features are suitable for early adopters in production environments.

We release preview features so partners and developers can study, test, and integrate them prior to General Availability (GA). For more details, see [Forge EAP, Preview, and GA](/platform/forge/whats-coming/#forge-preview).

Manifest overrides let you use the same `manifest.yml` file across deployments while adapting your
Forge Container services configuration to an environment type or placement. For example, you can
allocate fewer resources to a development environment or increase scaling for a particular data
residency realm.

Define overrides in the top-level `overrides` property. During deployment, Forge Container services
selects at most one matching override and replaces the top-level `services` property with the
override's `services` value. If no override matches, the base `services` configuration is used.

An override must contain the complete `services` array, including every service and all required
service and container properties. An override can't add, remove, or rename a service key.
Properties from the base `services` configuration aren't preserved when omitted from the override.

## Properties

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `overrides` | `Array` | No | A list of manifest overrides. At most one matching override is applied to a deployment. |
| `overrides[].applyTo` | `Object` | Yes | Defines when the override applies. Include at least one of `environmentTypes` or `placements`. If you include both properties, both must match. |
| `overrides[].applyTo.environmentTypes` | `Array<string>` | No | One or more Forge environment types. Supported values are `DEVELOPMENT`, `STAGING`, and `PRODUCTION`. Values are case-sensitive. |
| `overrides[].applyTo.placements` | `Array<string>` | No | One or more data residency realms or placement IDs. See [Supported placements](#supported-placements). |
| `overrides[].value` | `Object` | Yes | Contains the manifest properties to replace when the override is selected. |
| `overrides[].value.services` | `Array` | Yes | The complete replacement for the base `services` array. It supports the same properties as the [base services configuration](/platform/forge/containers-reference/ref-manifest/). |

Within an `environmentTypes` or `placements` array, matching any listed value satisfies that
property.

## Supported placements

The `placements` filter supports the following values:

| Placement type | Supported values |
| --- | --- |
| Data residency realm | `EU`, `US`, `AU`, `DE`, `SG`, `CA`, `IN`, `KR`, `JP`, `GB`, or `CH` |
| Isolated Cloud ID | An Isolated Cloud ID provided by Atlassian |

### EU and specific realms

`EU` is a broad realm that covers European placements. `DE`, `GB`, and `CH` are more specific realms
within `EU`. For a deployment in one of these specific realms, an override filtered by `EU` and an
override filtered by the specific realm can both match. The specific realm takes precedence.

For override selection, any supported realm other than `EU` is considered a specific realm. For
example, `US` and `AU` are specific realms even though they aren't sub-realms of `EU`.

## Override selection and precedence

Forge Container services first finds the overrides whose filters match the deployment. It then
selects the most specific match according to the following order:

| Order | `environmentTypes` | `placements` |
| --- | --- | --- |
| 1 (most specific) | Specified | A specific realm or Isolated Cloud ID |
| 2 | Not specified | A specific realm or Isolated Cloud ID |
| Specified | `EU` |
| 3 (least specific) | Specified | Not specified |
| Not specified | `EU` |

## Example

The following manifest uses a smaller container and fewer instances in development. For a production
deployment in the `DE` realm, it uses a larger container and additional instances.

```
```
1
2
```



```
# Used by default when no override matches.
services:
  - key: java-service
    containers:
      - key: java-service
        tag: "1.0.0"
        resources:
          cpu: "1"
          memory: "2Gi"
        health:
          type: http
          route:
            path: "/healthcheck"
    scaling:
      min: 1
      max: 3

overrides:
  - applyTo:
      environmentTypes:
        - DEVELOPMENT
    value:
      services:
        - key: java-service
          containers:
            - key: java-service
              tag: "1.0.0"
              resources:
                cpu: "500m"
                memory: "1Gi"
              health:
                type: http
                route:
                  path: "/healthcheck"
          scaling:
            min: 1
            max: 1

  - applyTo:
      environmentTypes:
        - PRODUCTION
      placements:
        - DE
    value:
      services:
        - key: java-service
          containers:
            - key: java-service
              tag: "1.0.0"
              resources:
                cpu: "2"
                memory: "4Gi"
              health:
                type: http
                route:
                  path: "/healthcheck"
          scaling:
            min: 2
            max: 5
```
```

## Preview the rendered manifest

Use the [manifest render](/platform/forge/cli-reference/manifest-render/) command to preview the
manifest after Forge Container services applies an override:

```
```
1
2
```



```
forge manifest render --environment production --placement DE
```
```

The `--environment` option accepts a Forge environment key. Include `--placement` when you want to
preview a placement-specific override. Omit `--placement` to preview environment-only selection.
The rendered output doesn't include the top-level `overrides` property.
