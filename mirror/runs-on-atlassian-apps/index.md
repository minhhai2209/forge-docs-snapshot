# Build Runs on Atlassian apps

The **Runs on Atlassian** program helps customers identify Forge apps that can benefit
enterprise customers with strict data privacy requirements. The **Runs on Atlassian** badge
is automatically applied to eligible apps on the Atlassian Marketplace.

Runs on Atlassian addresses the following requirements from customers:

1. Apps exclusively use Atlassian-hosted compute and storage.
2. Apps support data residency that matches data residency provided by the host Atlassian app.
3. Customers can control external data egress (for example, analytics and logs) via admin controls.

The Forge CLI provides a programmatic way to verify the above requirements.

While controls that limit external data egress are in place, these controls do not prevent misuse of access granted to the app during installation or abuse of the app runtime. The boundaries of tenant safety and data handling are defined in the [Shared responsibility model](/platform/forge/shared-responsibility-model/#tenant-safety).

![Runs on Atlassian page on app listing page](https://dac-static.atlassian.com/platform/forge/images/app-listing.svg?_v=1.5800.1840)

See [Runs on Atlassian](/platform/forge/runs-on-atlassian/) for more details.

## Eligibility of apps

Eligible apps do *not* list any of the following in the manifest:

Eligible apps can use [web triggers](/platform/forge/manifest-reference/modules/web-trigger/),
*only if* the apps use
[static](/platform/forge/manifest-reference/modules/web-trigger/#web-trigger-types)
web triggers.

Eligible apps must also do either of the following:

As new Forge storage capabilities are introduced,
in [EAP or Preview stages](/platform/forge/whats-coming/#eap--preview--and-ga),
these features may not support data residency until they reach general availability.

## Sample manifest structure

The following are examples of how the manifest file may look, depending on the eligibility
of an app for Runs on Atlassian.

### Runs on Atlassian

```
```
1
2
```



```
permissions:
  scopes:
    - read:content-details:confluence
    - read:content.property:confluence
    - write:content.property:confluence
  external:
    fetch:
      backend:
        - address: '*.example-dev.com'
          category: analytics
          inScopeEUD: false
```
```

### Not Runs on Atlassian

The example below shows ineligibility due to egress.

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
        - 'https://backend.example.com.com'
    images:
      - address: *.atlassian.com' # non-analytics egress
```
```

The example below shows ineligibility due to analytics with in-scope End-User Data.

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
        - address: 'baconipsum.com'
          category: ANALYTICS
          inScopeEUD: true # in-scope end user data egress
```
```

The example below shows ineligibility due to remotes.

```
```
1
2
```



```
remotes:
  - key: remote-backend
    baseUrl: "https://backend.example.com"
    operations:
      - compute
      - fetch
      - other
```
```

## Eligibility check of apps

You can check the eligibility for Runs on Atlassian for any app at any time, including during
app deployment, where the Forge CLI automatically checks for eligibility. You can also check
the eligibility for a previous major version of an app.

Go to the [Forge CLI documentation](/platform/forge/cli-reference/eligibility/) to know more about
checking app eligibility.

Apps that have adopted the [EAP](/platform/forge/changelog/#CHANGE-2044)
and [Preview](/platform/forge/changelog/#CHANGE-2307) releases of Forge SQL may return inaccurate results when checking eligibility. You must redeploy your app to ensure accurate results.

### Eligibility check at any time

Navigate to the app's top-level directory and check its eligibility by running:

If your app is eligible, you should see output similar to:

```
```
1
2
```



```
The version of your app [2.14.0] that's deployed to [development] is eligible
for the Runs on Atlassian program.
```
```

If your app is not eligible, you should see output similar to:

```
```
1
2
```



```
The version of your app [2.16.0] that's deployed to [development] is not eligible
for the Runs on Atlassian program.
- App is using remote services
- App has Connect modules
```
```

The output lists all applicable reasons for ineligibility, which helps narrow down the necessary
changes to the app.

### Eligibility check at app deployment

When deploying your app to any environment, the Forge CLI automatically detects any changes that
may impact the app's eligibility for Runs on Atlassian.

If your app is eligible, you should see output similar to:

```
```
1
2
```



```
The version of your app [2.14.0] that was just deployed to [development] is eligible
for the Runs on Atlassian program.
```
```

If your app is not eligible, you should see output similar to:

```
```
1
2
```



```
The version of your app [2.16.0] that was just deployed to [development]
is not eligible for the Runs on Atlassian program. Run forge eligibility to know more.
To know more about Runs on Atlassian, go to: https://go.atlassian.com/runs-on-atlassian
```
```

By running `forge eligibility`, you should see output similar to:

```
```
1
2
```



```
App [2.16.0] in [development] is not eligible for Runs on Atlassian.
- App is using remote services
- App has Connect modules
```
```

The output lists all applicable reasons for ineligibility, which helps narrow down the necessary
changes to the app.

### Eligibility check for previous major versions

You can check the eligibility for a previous major version of an app at any time. This helps narrow
down at which major version the app has either lost or gained its eligibility for Runs on Atlassian.

Navigate to the app's top-level directory and check the eligibility of a major version by running:

```
```
1
2
```



```
forge eligibility --major-version [version]
```
```

If the app was eligible for Runs on Atlassian at the specified major version, you should see output
similar to:

```
```
1
2
```



```
The version of your app [1.18.0] that's deployed to [development] is eligible
for the Runs on Atlassian program.
```
```

## Removal of egress

Consider doing the following as necessary:

### Remove egress URLs that are allowed by default

Note that for UI specific egresses, the following rules apply:

1. Custom UI apps allow-list the host Atlassian app.
2. Atlassian-hosted avatars load by default.

For the Forge platform in general, the following rules apply:

| Egress type | Applies to | Details |
| --- | --- | --- |
| `images` | Custom UI and UI Kit | * `hostname` (For example, `my-tenant.atlassian.net`. [Custom domains](https://support.atlassian.com/organization-administration/docs/add-a-custom-domain/) are also allowed.) * `*.wp.com` * `secure.gravatar.com` * `images.unsplash.com` * `api.media.atlassian.com` * `api.atlassian.com` * `pf-emoji-service--cdn.us-east-1.prod.public.atl-paas.net` (for emojis) * `avatar-management--avatars.us-west-2.prod.public.atl-paas.net` |
| `media` | Custom UI | * `hostname` (For example, `my-tenant.atlassian.net`. [Custom domains](https://support.atlassian.com/organization-administration/docs/add-a-custom-domain/) are also allowed.) * `api.media.atlassian.com` |
| `frames` | Custom UI | * `hostname` (For example, `my-tenant.atlassian.net`. [Custom domains](https://support.atlassian.com/organization-administration/docs/add-a-custom-domain/) are also allowed.) |
| `fetch.client` | Custom UI and UI Kit | * `api.media.atlassian.com` * `api.atlassian.com/gateway/api/emoji/` (to fetch list of emojis) |
| `fetch.backend` | Backend functions | * `api.media.atlassian.com` |

We're currently not able to allow-list Atlassian domains (for example, `*.atlassian.net`, `api.atlassian.com`,
`bitbucket.org`) for other types of egress (for example, fetch and script) because this can lead to
cross-tenant access to data.

The default allow-list is only for the types mentioned above, and only include the domains mentioned
above. If your apps need to access domains not specified above, you must explicitly allow-list
them in your app manifest.

### Ensure your app is only egressing data for the purpose of analytics

Your app should not be egressing data. If your app must egress data, then the egress should only be
for the purpose of analytics, and the app should not egress any
[in-scope End-User Data](/platform/forge/data-residency/#in-scope-end-user-data).
See [External permissions](/platform/forge/manifest-reference/permissions/#external-permissions)
to know more.

Apps use analytics data to identify trends and insights, which can be used to improve
app performance. These trends and insights can fall under different categories, such as
web analytics and Atlassian app analytics. In the context of Runs on Atlassian,
you must not mark tools that don't capture analytics data as *analytics egress*.

We enforce a policy in order to prevent abuse. Refer to [Analytics tools policy for Forge apps](/platform/forge/analytics-tool-policy) for more information.

### Migrate from dynamic to static web trigger modules

Web triggers are eligible for Runs on Atlassian if they are defined as `static`. The following web triggers are not
eligible for Runs on Atlassian:

* Existing web triggers without a type defined
* Web triggers explicitly defined as `dynamic`

However, these web triggers can be migrated to `static` web triggers. Consider your use case for your web trrigger
module and whether it can be defined as `static`. Find out more about web trigger types in the
[web trigger manifest reference](/platform/forge/manifest-reference/modules/web-trigger/#web-trigger-types).

## Known issues

When avatars, attachment thumbnails, and other media are fetched from Jira APIs and passed to
`<img>` tags in Custom UI apps, the images may not load in some cases. This is because Jira expects
the requests to the APIs to be authenticated, which doesn't happen when URLs are passed to `<img>` tags.

Here are some workarounds to ensure images load correctly:

**Option 1**

Make the requests to the APIs from backend to fetch content as a blob. Then, convert it to base64
and pass it to the `img-src`. Since the requests are made from the backend, these will be authenticated
as expected, and the images will load correctly.

**Option 2**

Replace the base path of the URLs with the base path of your host.

If the URL returned from Jira APIs is in the format: `https://api.atlassian.com/ex/jira/tenant-id/rest/api/3/attachment/thumbnail/content-id`,
replace it with: `https://my-tenant.atlassian.net/rest/api/3/attachment/thumbnail/content-id`.

This option only works for users who are authenticated to the host Atlassian app. If the user isn’t
authenticated, the images will not load because the requests will remain unauthenticated.

### Issues when fetching list of emojis

To render emojis in your app, internal APIs are used to access the list of emojis available.
We’ve allow-listed the following:

* `api.atlassian.com/gateway/api/emoji/` for `fetch.client` to list emojis
* `pf-emoji-service--cdn.us-east-1.prod.public.atl-paas.net` to fetch emojis

However, if the API for getting the list of emojis is accessed using tenant-host
(for example, `https://my-tenant.atlassian.net/gateway/api/emoji/`), this may be blocked by the
[CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS) policy. As a workaround,
we recommend using the allow-listed domain `api.atlassian.com/gateway/api/emoji/` to fetch
the list of emojis.

### Issues when running the app using Forge tunnel

When running the app using Forge tunnel, some of the
[default allow-listed domains](#remove-egress-urls-that-are-allowed-by-default) might not work. This means that
some CSP policies are breaking during the tunnel experience because the hostname doesn't match
the allowed value. Though we don’t have a fix for this at the moment, the team is aware of
this particular limitation.

We also release updates to the Forge tunnel along with the Forge CLI release. This means that
there may be delays in any behavior updates between deployed Custom UI apps (which gets platform
code changes instantly) and the tunnel experience (which requires a new version of the CLI to be released).
