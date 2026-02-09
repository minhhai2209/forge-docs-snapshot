# Call a containerised service without an invocation ID (EAP)

Forge Containers are now available through Forge's Early Access Program (EAP). To start testing this feature,
submit your app's ID to our team [through this link](https://ecosystem.atlassian.net/servicedesk/customer/portal/1040/create/18884).

EAPs are offered to selected users for testing and feedback purposes. APIs and features under EAP
are unsupported and subject to change without notice. APIs and features under EAP are not recommended
for use in production environments.

For more details, see [Forge EAP, Preview, and GA](/platform/forge/whats-coming/#eap).

To invoke a container service or make calls from one, you'll need to first define its endpoint.
See [Define endpoints](/platform/forge/containers-reference/integrating-service/#define-endpoints) for details.

You can make "offline" API calls at any time from your container on behalf of an **installation** within your app environment.
This means that you no longer need to wait for an invocation to deliver you an `invocationId` to make API requests.

## Query app installations

To perform operations on behalf of an installation, you need its `installationId`.
The installations API allows apps to enumerate all available installations for the current app environment:

```
1
GET <FORGE_EGRESS_PROXY_URL>/v0/installations
```

Sample response:

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
[
    {
        "id": "<installation-1-id-uuid>",
        "installationContext": "ari:cloud:confluence::site/<cloudId>",
        "version": "<installation-1-version-uuid>"
    },
    {
        "id": "<installation-2-id-uuid>",
        "installationContext": "ari:cloud:jira::site/<cloudId>",
        "version": "<installation-2-version-uuid>"
    }
]
```

## Send an install-based API request

Once you have an installation's `installationId`, you can make an API request on its behalf. To do this, pass the `installationId` as a part of the digest-based
`forge-proxy-authorization` header.

For example, to call the Jira REST API on behalf on an installation:

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

## Testing locally

Offline access leverages several components specific to running on the hosted Forge Container environment.
We replicated parts of the hosted environment locally, so offline access works while tunnelling.

This local environment is only accessible when Forge [manages the Docker Compose stack](/platform/forge/containers-reference/test-service-locally#setup-docker-compose). It won't work when you [start the Docker Compose stack manually.](/platform/forge/containers-reference/test-service-locally#setup-docker-compose-manual).
