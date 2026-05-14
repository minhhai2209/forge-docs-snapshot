# Customer-managed egress and remotes (EAP)

Customer-managed egress and remotes are a way of defining egress in your app. They let customers and admins control which external services your app can talk to, and when those connections are enabled.

In other implementations, Forge apps must [declare all possible egress destinations up front](/platform/forge/add-content-security-and-egress-controls/), which limits
customer choice and can introduce unnecessary security risks.

Customer-managed egress enables apps to declare and manage their egress and remotes per installation,
instead of listing every destination in the manifest. This approach improves trust for
customers by giving them more visibility and control over data flows, and provides more flexible
integration options.

## When to use it

Consider using customer‑managed egress and remotes when:

* Your app integrates with external systems where the exact domains or endpoints differ per customer.
* You want admins to have the ability to enable or disable specific integrations without a new app deployment.
* You need to expose a “bring your own endpoint” or “bring your own domain” experience in your app’s configuration UI.
* You want to strengthen your app’s **trust posture** by giving admins clear visibility and explicit consent over where data can be sent.
* Your app doesn’t know in advance which domains a customer will need, but can offer a “permitted list of domains” experience.
* Your app integrates with external services hosted on customer‑specific or variable URLs.
* Different customers need to point the same app to different analytics, logging, or backend endpoints.

Customer‑managed egress and remotes **must not** be used to request pre‑defined, required egress.

If your app always needs to talk to specific external domains that are fixed or pre‑set, you must
declare those via static [external permissions](/platform/forge/manifest-reference/permissions/#external-permissions) and [remotes](/platform/forge/manifest-reference/remotes/), rather than prompting admins
to approve them immediately via customer‑managed egress.

If your app always talks to the same fixed set of external destinations, you can keep using static [external permissions](/platform/forge/manifest-reference/permissions/#external-permissions) and [remotes](/platform/forge/manifest-reference/remotes/).

## Key benefits

* **Per‑installation control**: Admins can define and manage which external domains an app can communicate with in the Forge app and in the Atlassian Administration Connected Apps page.
* **Feature gating by consent**: Apps can expose features that rely on external integrations only when customers explicitly enable and configure them.
* **Better trust posture**: Admins get clear visibility and explicit consent over where data can be sent, which helps with internal security reviews and compliance.

## How it works

Instead of declaring every external destination up front in `manifest.yml`, your app can:

* Ask an admin to approve new egress destinations and remote endpoints at runtime.
* Store those choices per installation.
* Use the configured values when making outbound calls.

### Relationship to runtime egress permissions

* **Runtime egress permissions** are the enforcement layer that decides, at invocation time, whether a call to an external domain is allowed.
* **Customer‑managed egress and remotes** are ways to manage that configuration per installation via the
  [Forge bridge APIs](#forge-bridge-apis), instead of only via static manifest entries.
* Both use the same underlying egress types and content security model; customer‑managed egress simply gives admins more control over the allowed destinations.

## Egress vs remotes

* **Egress groups** describe *which external domains* your app is allowed to talk to, and for which types of traffic (backend fetch, client fetch, images, styles, and so on). They are a customer‑managed layer on top of the existing `permissions.external.*` model.
* **Remotes** describe *a specific backend service* (with a key, base URL, purpose, and optional authentication configuration), which Forge can call via Forge Remote or use as a fetch backend. Customer‑managed remotes let admins supply or override the remote’s endpoint URL per installation.

In practice, you will usually:

* Use **customer-managed egress groups** when you want admins to manage a list of allowed domains for different resource types.
* Use **customer‑managed remotes** when you want admins to configure a single backend endpoint (by key) that your app or Forge Remote calls.

### Customer‑managed egress groups

The customer-managed egress data model is based on the idea of an **egress group**. A group may have one or more egress entries defined. Grouping makes it easier for an admin to understand what a particular egress is related to.

An example egress group looks like:

```
```
1
2
```



```
{
  "key": "egress-group",
  "description": "Access to example.com",
  "configured": [
    {
      "domain": "https://api.example.com",
      "type": ["FETCH_BACKEND_SIDE", "FETCH_CLIENT_SIDE"]
    },
    {
      "domain": "https://media.example.com",
      "type": ["IMAGES", "MEDIA"]
    },
    {
      "domain": "https://cdn.example.com",
      "type": ["FONTS", "SCRIPTS", "STYLES"]
    }
  ]
}
```
```

**Field details**

| Field | Type | Description |
| --- | --- | --- |
| `key` | `string` | A key for the egress group that is defined by the Forge app. |
| `description` | `string` | A user‑facing description for this egress group. |
| `configured[].domain` | `string` | A URL or wildcard that will be used to fetch resources from. |
| `configured[].type` | `EgressType[]` | The type(s) of allowed egress. These map to the existing manifest egress types documented in [Add content security and egress controls](/platform/forge/add-content-security-and-egress-controls/).  There is an enum `EgressType` for the accepted types exposed from the `@forge/egress` package if you wish to import this in your app. Otherwise the following string values are accepted:   * `'FETCH_BACKEND_SIDE'` * `'FETCH_CLIENT_SIDE'` * `'FONTS'` * `'FRAMES'` * `'IMAGES'` * `'MEDIA'` * `'SCRIPTS'` * `'STYLES'` |

### Customer‑managed remotes

The data model for a customer-managed remote looks like:

```
```
1
2
```



```
{
  "key": "external-api",
  "configured": {
    "endpoint": "https://api.external.com"
  }
}
```
```

**Field details**

| Field | Type | Description |
| --- | --- | --- |
| `key` | `string` | Must correlate to a remote key defined in the manifest. |
| `endpoint` | `string (URL)` | The absolute URL for the remote as defined by the admin of your app (inside `configured`). |

## Set up customer‑managed egress and remotes

### 1. Update the manifest to enable customer‑managed egress or remotes

#### For customer-managed egress

To enable customer‑managed egress, enable the feature in your app manifest:

```
```
1
2
```



```
permissions:
  external:
    configurable:
      enabled: true
```
```

If this property is not `true`, any calls to the egress APIs will fail.
This property is required for egress and remotes, but a customer-managed remote requires one additional
property to be set.

#### For customer-managed remotes

Customer-managed remotes are defined in the manifest similarly to existing remotes, but add a `configurable` object describing how admins can configure the endpoint URL. A customer-managed remote must be specified in the manifest, arbitrary remotes cannot be configured.

Basic example:

```
```
1
2
```



```
remotes:
  - key: my-site-1
    configurable:
      name: "My site"
      description: "This will be used to make connections to My Site"
      supportedPatterns:
        - "*.example.com"
```
```

Key points:

* `key` is still required; remotes are always keyed values.
* `baseUrl` becomes optional when `configurable` is defined. If you omit `baseUrl`, the remote is purely customer‑configured.
* The `configurable` object provides:
  * `name` and `description`: Used in the Atlassian Administration **Connected Apps** UI and in in‑app modals to explain what the remote is used for.
  * `supportedPatterns`: An optional array of patterns used to validate admin‑provided URLs. This accepts any string values, including a single `*` wildcard character. Validation for these will be performed in Admin Hub, and server-side. If a URL is provided that does not match a specified pattern, setting the remote will be rejected.
* Customer-managed remotes are compatible with [endpoints](/platform/forge/manifest-reference/endpoint).

For example, to provide a default `baseUrl` while still allowing customers to override it:

```
```
1
2
```



```
remotes:
  - key: my-site-1
    baseUrl: "https://default.example.com"
    configurable:
      name: "My site"
      description: "This will be used to make connections to My Site"
      supportedPatterns:
        - "*.example.com"
```
```

##### Interaction with data residency

Customer-managed remotes are not eligible for data residency. A remote must not have `configured` for it to be eligible.

### 2. Use the Forge bridge APIs

Once the manifest is configured, your app can interact with customer‑managed egress and remotes at runtime using the Forge bridge.

All customer-managed egress and remotes APIs:

* Are exposed from the `permissions` module in `@forge/bridge`.
* Require `permissions.external.configurable.enabled: true` in the manifest.
* Only allow admins to **set** or **delete** configuration (they show an admin consent modal).
* Can be used to **read** configuration from both app code and resolvers.

There are six async Forge bridge functions available in `@forge/bridge`:

* `permissions.egress.get`
* `permissions.egress.set`
* `permissions.egress.deleteDomain`
* `permissions.egress.deleteGroup`
* `permissions.remote.set`
* `permissions.remote.get`

For detailed arguments and TypeScript types, see [the API documentation](/platform/forge/apis-reference/customer-managed-egress-and-remotes-api).

## Admin experience

Customer‑managed egress and remotes are designed to be understandable and controllable for admins. An admin’s primary experience is usually within the context of your app, but some functionality is also available in **Connected Apps** in Atlassian Administration.

### In‑app experience

When a Forge app invokes the `set` operations for egress or remotes, an admin will see a modal asking them to confirm the addition or change. If the `permissions.external.configurable.enabled` is not `true`, this will be rejected.

* The description, domains, and remotes specified when calling these functions are shown in the modal.
* The modal is controlled by Atlassian and is used to obtain explicit consent for new egress or remote destinations.
* If the admin approves, the configuration is saved and the async function resolves.
* If the admin rejects, the async function rejects.

If egress has already been configured for a particular domain and that domain is reused for a different type, the modal is not shown again for the same domain.

### Connected Apps in Atlassian Administration

When viewing a specific app after navigating to **Connected Apps** in Atlassian Administration, and
selecting an app, the **Data management** tab provides:

* The ability to view and set a customer-managed remote:
  * Admins can update the customer-managed endpoint URL.
  * Admins can reset the remote back to the value defined in the manifest (or unset it if no default exists).
* The ability to view egress groups configured by your app, and delete individual domains or entire groups.

This gives admins a centralized place to review data flows across multiple apps in their organization.

### API access and admin control

The customer-managed egress and remotes APIs are designed so that admins must be in control of any changes:

* **Setting** egress or remotes, and **deleting** egress groups or domains, is only available via the Forge bridge functions and must be explicitly approved by an admin.
* These operations cannot be performed on behalf of an admin via Forge User Impersonation.
* **Reading** configuration (for example, to adjust your UI based on configured egress/remotes) can be done from resolvers.
* Changes to egress configuration and dynamic modules are also recorded in Atlassian Guard audit logs, giving admins centralized visibility into who modified what and when.

For detailed API behaviour and type definitions, see the [Forge bridge permissions reference](/platform/forge/apis-reference/ui-api-bridge/permissions/).

## Limitations and considerations

* **Runs on Atlassian eligibility**:
  * Any app that uses customer‑managed egress or customer‑managed remotes is not eligible for [Runs on Atlassian](/platform/forge/runs-on-atlassian/).
* **Maximum configuration limits**:
  * There is a limit of 10 customer-managed egress groups per installation. This is required for scaling limits and to ensure that the size of the CSPs generated on page load won't get too big.
* **Connect remotes**:
  * Connect remotes cannot be dynamically added using customer-managed remotes. Adding a `configurable` field to a Connect remote will be rejected.
* **App upgrade eligibility**:
  * Information about versioning changes for customer-managed egress and remotes are on the [versions page](/platform/forge/versions/).
