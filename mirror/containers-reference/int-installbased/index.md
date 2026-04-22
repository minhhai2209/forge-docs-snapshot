# Call a containerised service without an invocation ID (EAP)

Forge Containers are now available through Forge's Early Access Program (EAP). To start testing this feature,
submit your app's ID to our team [through this link](https://ecosystem.atlassian.net/servicedesk/customer/portal/1040/create/18884).

EAPs are offered to selected users for testing and feedback purposes. APIs and features under EAP
are unsupported and subject to change without notice. APIs and features under EAP are not recommended
for use in production environments.

For more details, see [Forge EAP, Preview, and GA](/platform/forge/whats-coming/#eap).

You can make "offline" API calls at any time from your container on behalf of an **installation** within your app environment.
This means that you no longer need to wait for an invocation to deliver you an `invocationId` to make API requests.

## Query app installations

To perform operations on behalf of an installation, you need its `installationId`.
The [Get app installations](/platform/forge/rest/v2/api-group-app-installations/#api-v1-installations-get) endpoint enumerates all available installations for the current app environment.

This endpoint uses cursor-based pagination with a default and maximum page size of 100 installations. If your app has over 100 installations in a specific environment, you'll need to make multiple requests to retrieve all the installations. Each response includes a `cursor` value, which you can pass as a parameter in your next request to fetch the subsequent page. When there are no more results to return, the `cursor` will be `null`.

You can pass `pageSize` and `cursor` as query parameters. For example:

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
# Returns up to the first 100 installations (default page size)
GET <FORGE_EGRESS_PROXY_URL>/v1/installations

# Returns up to the first 50 installations
GET <FORGE_EGRESS_PROXY_URL>/v1/installations?pageSize=50

# Returns up to the next 50 installations after the given cursor
GET <FORGE_EGRESS_PROXY_URL>/v1/installations?pageSize=50&cursor=eyJhbGciOi...

# Returns up to the next 100 installations after the given cursor (default page size)
GET <FORGE_EGRESS_PROXY_URL>/v1/installations?cursor=eyJhbGciOi...
```

Sample response:

```
```
1
2
```



```
{
  "installations": [
    {
      "id": "<installation-1-id-uuid>",
      "installationContext": "ari:cloud:confluence::site/<cloudId>",
      "version": "12.0.3",
      "secondaryInstallationContexts": ["<secondary-installation-context-1>", "<secondary-installation-context-2>"]
    },
    {
      "id": "<installation-2-id-uuid>",
      "installationContext": "ari:cloud:jira::site/<cloudId>",
      "version": "11.0.0",
      "secondaryInstallationContexts": []
    },
    {
      "id": "<installation-3-id-uuid>",
      "installationContext": "ari:cloud:jira::site/<cloudId>",
      "version": "11.0.0",
      "secondaryInstallationContexts": []
    }
  ],
  "cursor": null
}
```
```

## Query a single installation

The [Get details about a single installation](/platform/forge/rest/v2/api-group-app-installations/#api-v1-installation-installationid-get) endpoint lets you retrieve detailed information about an installation using its `installationId`. This allows you to implement custom logic based on installation details.

For example, you can use this endpoint the same way that Forge functions use [Permissions SDK](https://developer.atlassian.com/platform/forge/rolling-releases/#permissions-sdk) to implement [rolling releases](https://developer.atlassian.com/platform/forge/rolling-releases/) (that is, gate app capabilities behind admin consent).

In addition to the installation context, this endpoint returns the scopes and permissions associated with the app version (these were defined in the manifest when the app version was deployed).

Example request:

```
```
1
2
```



```
GET <FORGE_EGRESS_PROXY_URL>/v1/installation/<installationId>
```
```

Sample response:

```
```
1
2
```



```
{
  "id": "<installation-1-id-uuid>",
  "version": "12.0.3",
  "installationContext": "ari:cloud:confluence::site/<cloudId>",
  "secondaryInstallationContexts": ["<secondary-installation-context-1>"],
  "scopes": ["read:jira-user", "storage:app"],
  "external": {
    "fetch": {
      "backend": ["<backend-url>"],
      "client": ["<client-url>"]
    },
    "images": ["<image-url>"],
    "media": ["<media-url>"],
    "scripts": ["<script-url>"],
    "styles": ["<stylesheet-url>"],
    "fonts": ["<font-url>"],
    "frames": ["<frame-url>"]
  }
}
```
```

## Send an API request on behalf of an installation

Once you have an installation's `installationId`, you can make an API request on its behalf. To do this, pass the `installationId` as a part of the digest-based
`forge-proxy-authorization` header.

For example, to call the Jira REST API on an installation's behalf:

```
```
1
2
```



```
GET <FORGE_EGRESS_PROXY_URL>/jira/<path>
  -H forge-proxy-authorization: Forge as=app,installationId=<installationId>
```
```

## Test locally

Offline access leverages several components specific to running on the hosted Forge Container environment.
We replicated parts of the hosted environment locally to enable offline access while tunnelling.

This local environment is only accessible when Forge [manages the Docker Compose stack](/platform/forge/containers-reference/test-service-locally#setup-docker-compose). It won't work when you [start the Docker Compose stack manually](/platform/forge/containers-reference/test-service-locally#setup-docker-compose-manual).
