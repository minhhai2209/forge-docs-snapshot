# Manifest overrides for Forge Container services (Preview)

Forge Container services is now in Preview, and therefore fully supported. However, it remains under active development and may be subject to shorter deprecation windows. Preview features are suitable for early adopters in production environments.

We release preview features so partners and developers can study, test, and integrate them prior to General Availability (GA). For more details, see [Forge EAP, Preview, and GA](/platform/forge/whats-coming/#forge-preview).

Manifest overrides let you use the same `manifest.yml` file across deployments while adapting your
Forge Container services configuration to an environment type or placement. For example, you can
allocate fewer resources to a development environment or increase scaling for a particular region.

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
| `overrides[].applyTo.placements` | `Array<string>` | No | One or more Forge regions or placement IDs. See [Supported placements](#supported-placements). |
| `overrides[].value` | `Object` | Yes | Contains the manifest properties to replace when the override is selected. |
| `overrides[].value.services` | `Array` | Yes | The complete replacement for the base `services` array. It supports the same properties as the [base services configuration](/platform/forge/containers-reference/ref-manifest/). |

Within an `environmentTypes` or `placements` array, matching any listed value satisfies that
property.

## Supported placements

The `placements` filter supports the following values:

| Placement type | Supported values |
| --- | --- |
| Region | `ap-southeast-2`, `ap-southeast-1`, `us-west-2`, `us-east-1`, `eu-west-1`, or `eu-central-1` |
| Isolated Cloud ID | An Isolated Cloud ID provided by Atlassian |

## Override selection and precedence

Forge Container services first finds the overrides whose filters match the deployment. It then
selects the most specific match according to the following order. A deployment's placement is
always a region or an Isolated Cloud ID, never both, so the order doesn't rank those two placement
values against each other.

| Order | `environmentTypes` | `placements` |
| --- | --- | --- |
| 1 (most specific) | Specified | Specified |
| 2 | Not specified | Specified |
| 3 (least specific) | Specified | Not specified |

## Example

The following manifest uses a smaller container and fewer instances in development. For a production
deployment in the `eu-central-1` region, it uses a larger container and additional instances.

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
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
38
39
40
41
42
43
44
45
46
47
48
49
50
51
52
53
54
55
56
57
58
59
60
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
        - eu-central-1
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
forge manifest render --environment production --placement eu-central-1
```
```

The `--environment` option accepts a Forge environment key. Include `--placement` when you want to
preview a placement-specific override. Omit `--placement` to preview environment-only selection.
The rendered output doesn't include the top-level `overrides` property.
