# Permissions

The `permissions` section of the `manifest.yml` file controls your app's access to
remote resources.

## Scopes

The `scopes` list declares which OAuth 2.0 scopes are required by your app
when using the authenticated Atlassian app [Fetch APIs](/platform/forge/runtime-reference/product-fetch-api/),
and [events](/platform/forge/events-reference/).

The `scopes` list also declares which OAuth 2.0 scopes are required by an app
that uses [Forge Remote](/platform/forge/remote) to pass auth tokens to a remote back end.

[Connect apps that have adopted Forge modules](/platform/adopting-forge-from-connect) may declare legacy Connect scopes
here - these will be inserted by the `@atlassian/connect-to-forge` tool as part of a descriptor conversion. These can
be listed alongside OAuth 2.0 scopes (e.g. when incrementally adopting Forge OAuth 2.0).

Define each scope on a new line. Your app should use the minimum set of scopes required. For example:

```
1
2
3
4
permissions:
  scopes:
    - "read:confluence-content.summary"
    - "write:jira-work"
```

If your app requires no OAuth 2.0 permissions, you must provide an empty `scopes` list as in the example below.

```
1
2
permissions:
  scopes: []
```

If your app needs to use offline user impersonation (e.g. to impersonate a user from a scheduled trigger), you will need to specify the scopes as a map instead, and specify `allowImpersonation: true` on scopes your app will use for offline user impersonation. Other scopes can either be an empty map or a map with `allowImpersonation: false`, for example:

```
```
1
2
```



```
permissions:
  scopes:
    read:confluence-content.summary:
      allowImpersonation: true
    write:confluence-content:
      allowImpersonation: false
    write:jira-work: {}
```
```

### Platform and Atlassian app scopes

Certain platform features, such as the [App storage API](/platform/forge/runtime-reference/storage-api/),
are authenticated using OAuth 2.0.
For a list of scopes required by these features, refer to [Forge scopes](/platform/forge/manifest-reference/scopes-forge/).

Atlassian app scopes enable a Forge app to request a level of access to an Atlassian app. You can find details about each Atlassian app operation's required scopes through the
[REST API](/platform/forge/apis-reference/product-rest-api-reference/) documentation (specifically, in the
operation's *Oauth scopes required* field). For information about each Atlassian app event's
required scopes, see our [events](/platform/forge/events-reference/product_events/)
documentation.

For more details about each Atlassian app's OAuth 2.0 (3LO) and Forge scopes,
refer to the pages below:

## Content permissions

The `content` section declares which Content Security Policy (CSP) options are required by your app
when using Custom UI.

### Scripts

The `scripts` list declares which sources are allowed for an app's `script-src` policy.

#### Example

In the example below, `script-src 'unsafe-hashes'` is included in the CSP header for all modules
using Custom UI:

```
```
1
2
```



```
permissions:
  content:
    scripts:
      - "unsafe-hashes"
```
```

| Source | Description |
| --- | --- |
| `unsafe-inline` | Allows the use of inline resources, such as inline `<script>` elements, `javascript:` URLs, and inline event handlers. |
| `unsafe-hashes` | Allows the use of specific inline event handlers. |
| `unsafe-eval` | Allows the use of `eval()` and similar methods for creating code from strings. |
| `blob:` | Allows `blob:` URIs to be used as a content source. |
| `<sha-algorithm>-<base64-value>` | Allows a specific script to be executed, provided it matches the hash declared here. The only valid hash algorithms are: `sha256`, `sha384`, and `sha512`. |

### Styles

The `styles` list declares which sources are allowed for an app's `style-src` policy.

#### Example

In the example below, `style-src 'unsafe-inline'` is included in the CSP header for all modules
using Custom UI:

```
```
1
2
```



```
permissions:
  content:
    styles:
      - "unsafe-inline"
```
```

| Source | Description |
| --- | --- |
| `unsafe-inline` | Allows the use of inline resources, such as inline `<script>` elements, `javascript:` URLs, and inline event handlers. |

## External permissions

Using the capabilities discussed in this section may make your app *not* eligible for **Runs on Atlassian**.

Go to [this page](/platform/forge/runs-on-atlassian/) to know more about the Runs on Atlassian program. To know how to check if your app is eligible for Runs on Atlassian, go to the
[Forge CLI documentation](/platform/forge/cli-reference/eligibility/).

The `external` section declares the external resources that your Forge UI app is allowed to access.
This section also covers external website your Forge function is allowed to communicate with.
This covers both Custom UI resolvers and any other Forge functions.

In each section, you can add a list of external domains, which end up as a source in an
equivalent CSP directive.

External permissions support the following types for each entry in the list of domains:
`String | EgressPermission | Remote`

### Egress permissions

You can use the `EgressPermission` type to define egress permission as an object, as well as
to include a `category` for egress permissions for your app.

The `EgressPermission` type has the following properties:

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `address` | `string` | Yes | The address to which egress is allowed.  [Valid domain formats](/platform/forge/manifest-reference/permissions/#valid-domain-formats) are listed below. |
| `category` | `enum` | No | The category in which egress falls under. Only `analytics` is supported, but only for pre-approved domains (refer to [Analytics tools policy for Forge apps](/platform/forge/analytics-tool-policy) for more information).  If set to `analytics`, the property `inScopeEUD` (below) defaults to `true`, unless specified otherwise. |
| `inScopeEUD` | `boolean` | No | Defines whether any [in-scope End-User Data](/platform/forge/data-residency/#in-scope-end-user-data) is egressing from the app for the purpose of analytics.  Defaults to `true` if not specified in the configuration.  If `inScopeEUD` is set to `true`, then the app is ineligible for Runs on Atlassian. Refer to [eligibility requirements](/platform/forge/runs-on-atlassian/#eligibilty-requirements) for further details. |

Apps use analytics data to identify trends and insights, which can be used to improve
app performance. These trends and insights can fall under different categories, such as
web analytics and Atlassian app analytics. In the context of [Runs on Atlassian](/platform/forge/runs-on-atlassian),
you must not mark tools that don't capture analytics data as *analytics egress*.

We enforce a policy in order to prevent abuse. Refer to [Analytics tools policy for Forge apps](/platform/forge/analytics-tool-policy) for more information.

While egress permissions can be categorized as analytics,
[app admins](https://support.atlassian.com/organization-administration/docs/installing-and-managing-app-access/#Manage-access-to-analytics-and-logs-for-all-apps)
can still choose to disable access
to analytics. You must ensure that your app can efficiently handle the scenario when analytics access
is disabled. Otherwise, this may lead to poor user experience, in the form of failing
app invocations or elements not rendering properly in the UI, and more.

### Remote

The `remote` property is only allowed for `fetch.backend` and `fetch.client`. See
[this example](/platform/forge/manifest-reference/permissions/#as-a-remote-back-end) that shows
the `remote` property defined as a `fetch.backend`.

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `remote` | `string` | Yes | The remote element that describes the purpose of egress. See [Fetch](/platform/forge/manifest-reference/permissions/#fetch) for more details.  [Valid domain formats](/platform/forge/manifest-reference/permissions/#valid-domain-formats) are listed below. |

### Valid domain formats

External domains follow
[CSP protocols](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/script-src#sources)
and must be in one of the following formats:

* An `https` or `wss` URL, such as `https://www.example-dev.com`.

  Adding a site URL means
  that all resources to this site are allowed – you don't need to add `*` at the end.
* A [valid domain name](https://developer.mozilla.org/en-US/docs/Learn/Common_questions/What_is_a_domain_name),
  such as `www.example-dev.com`
* A wildcard domain name starting with `*`, for example `*.example.com`. This includes all
  nested subdomains below the specified domain name. Wildcards can be used with subdomains,
  for example `*.static.example.com` to limit to just the static subdomain.
* A generic wildcard to support every domain: `*`

External domains must not contain any invalid special characters. You can check your domain with
the following regex pattern:

```
```
1
2
```



```
^(\*\.)?[.a-zA-Z0-9_\-\/:~#%]+$
```
```

### Fetch

The `fetch` section has the following configurations:

| Configuration | Description |
| --- | --- |
| `backend` | The `fetch.backend` list declares which external domains your Forge functions can talk to. This applies to both Custom UI resolvers and any other Forge functions. |
| `client` | The `fetch.client` list declares which external sources are allowed for an app's `connect-src` policy. Additionally, links included in the `fetch.client` list do not display the external link warning popup when opened with [router.navigate](/platform/forge/custom-ui-bridge/router/#navigate). |

There are two ways to declare an external URL for your fetch back end:

#### Direct listing

This involves listing the domains directly in the `fetch.backend` or `fetch.client` section.
You can define these directly as as `string` or as an `EgressPermission` object.
You don't need to specify individual URL paths, such as `example-dev.com/path`. Adding one domain
allows access to any URL on that domain.

###### EXAMPLE AS A STRING

```
```
1
2
```



```
permissions:
  external:
    fetch:
      backend:
        - "*.example-dev.com"
```
```

```
```
1
2
```



```
permissions:
  external:
    fetch:
      client:
        - "*.example-dev.com"
```
```

###### EXAMPLE AS AN OBJECT

```
```
1
2
```



```
permissions:
  external:
    fetch:
      backend:
        - address: "*.example-dev.com"
          category: analytics
          inScopeEUD: false
```
```

```
```
1
2
```



```
permissions:
  external:
    fetch:
      client:
        - address: "*.example-dev.com"
          category: analytics
          inScopeEUD: false
```
```

Using a wildcard for a `backend` or `client` (for example, `*.example-dev`) does not include
the parent domain. If you need to support both, you need to explicitly add the parent domain
as a second entry.

**Data residency eligibility for PINNED status:** If you want your app to be eligible for `PINNED` status for data residency purposes, any address declared in `fetch.backend` or `fetch.client` must match an address in a remote declaration. The match must be an exact string match (wildcards are not evaluated). Alternatively, you can set `inScopeEUD: false` on the fetch entry to maintain eligibility. See [Data residency eligibility](/platform/forge/data-residency/#eligibility) for more information.

###### Example: Direct listing with matching remote for PINNED status

To maintain eligibility for `PINNED` status when using direct listing, ensure the address in your fetch declaration exactly matches a `baseUrl` in your remotes section:

```
```
1
2
```



```
permissions:
  external:
    fetch:
      backend:
        - "https://api.example.com"
remotes:
  - key: api-backend
    baseUrl: "https://api.example.com"
    operations:
      - fetch
```
```

In this example, `"https://api.example.com"` in `fetch.backend` exactly matches the `baseUrl` in the remote declaration, which helps maintain eligibility for `PINNED` status.

#### As a remote back end

This involves declaring the URLs in a separate `remotes` section, where you can explicitly define
its purpose (in this case, as a fetch back end). Upon declaring the remote back end, you can refer
to its *key* in your `fetch.backend` or `fetch.client` list.

```
```
1
2
```



```
permissions:
  external:
    fetch:
      backend:
        - remote: remote-backend
remotes:
  - key: remote-backend
    baseUrl: "https://example-dev.io"
    operations:
      - fetch
```
```

The `fetch` setting in the operations property defines the purpose of the remote back end.
Since the fetch entry references a remote by key, the address automatically matches a remote declaration,
which helps maintain eligibility for `PINNED` status for data residency purposes. See [Data residency eligibility](/platform/forge/data-residency/#eligibility)
for more information.

Calls made to any domain that is not defined in the `manifest.yml` file of your app will be
rejected. See [runtime egress permissions](/platform/forge/runtime-egress-permissions/) to know more.

### Fonts

The `fonts` list declares which external sources are allowed for an app's `font-src` policy.

#### Example

In the example below, `font-src https://www.example-dev.com/fonts.css` is included in the CSP
header for all modules using Custom UI:

```
```
1
2
```



```
permissions:
  external:
    fonts:
      - "https://www.example-dev.com/fonts.css"
```
```

### Styles

The `styles` list declares which external styles are allowed for an app's `style-src` policy.

#### Example

In the example below, `style-src https://www.example-dev.com/stylesheet.css` is included in the CSP
header for all modules using Custom UI:

```
```
1
2
```



```
permissions:
  external:
    styles:
      - "https://www.example-dev.com/stylesheet.css"
```
```

If you are using specific styles and fonts together in your application, you must include both of them as permissions in your app's manifest file. This is because the styles and fonts are external resources that the app needs to access in order to display correctly. By including these permissions, you are granting your app the ability to access and utilize these resources, ensuring that the text and design elements appear as intended.

### Frames

The `frames` list declares which external sources are allowed for an app's `frame-src` policy.

#### Example

In the example below, `frame-src https://www.example-dev.com/embed/page` is included in the CSP
header for all modules using Custom UI:

```
```
1
2
```



```
permissions:
  external:
    frames:
      - "https://www.example-dev.com/embed/page"
```
```

Popups from embedded iframes are blocked by default for security reasons. To allow for them, the following permissions must be applied to your app:

```
```
1
2
```



```
permissions:
  external:
    fetch:
      client:
        - address: '*'
```
```

This will automatically add the `allow-popups` and `allow-popups-to-escape-sandbox` directives to the iframe sandbox attribute. This enables external links to be clickable and open in new tabs using anchor tags `<a>` or `window.open(your_url)`.

### Images

The `images` list declares which external sources are allowed for an app's `img-src` policy.

#### Example

In the example below, `img-src https://www.example-dev.com/image.png` is included in the CSP
header for all modules using Custom UI:

```
```
1
2
```



```
permissions:
  external:
    images:
      - address: https://www.example-dev.com/image.png
```
```

The `media` list declares which external sources are allowed for an app's `media-src` policy.

#### Example

In the example below, `media-src https://www.example-dev.com/video.mp4` is included in the CSP
header for all modules using Custom UI:

```
```
1
2
```



```
permissions:
  external:
    media:
      - "https://www.example-dev.com/video.mp4"
```
```

### Scripts

The `scripts` list declares which external sources are allowed for an app's `script-src` policy.

#### Example

In the example below, `script-src https://www.example-dev.com/script.js` is included in the CSP
header for all modules using Custom UI:

```
```
1
2
```



```
permissions:
  external:
    scripts:
      - "https://www.example-dev.com/script.js"
```
```

```
```
1
2
```



```
permissions:
  external:
    scripts:
      - address: "https://www.example-dev.com/script.js"
        category: analytics
        inScopeEUD: false
```
```
