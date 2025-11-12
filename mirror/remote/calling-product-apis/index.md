# Calling Atlassian app APIs from a remote

Once your remote backend has received a request from Forge, you can call Atlassian app APIs.

## Prerequisites

When setting up your app to:

* Call a remote (from a Custom UI or UI Kit 2 frontend)
* Send Atlassian app and lifecycle events (to a remote)
* Configure scheduled triggers to invoke a remote backend

You'll need one of the following in your manifest.yml:

* `endpoint.auth.appSystemToken` set to `true`
* `endpoint.auth.appUserToken` set to `true`

Which one you need depends on whether you want to access Atlassian app APIs as a generic bot user (`appSystemToken`) or the current user's permission (`appUserToken`).

This ensures requests to your remote contain an `x-forge-oauth-system` or `x-forge-oauth-user` header, containing a token you can use to call Atlassian app and Forge storage APIs.

### Token Expiry

Both of these tokens are encoded in JWT. The [`exp`](https://datatracker.ietf.org/doc/html/rfc7519#section-4.1.4) claim in their payload represents the expiration time.

* We recommend adding a [lifecycle events](/platform/forge/events-reference/life-cycle/#installation)
  trigger for the installation and upgrade events to ensure that your app starts off with a token available.
* If your app needs to ensure the access token is periodically refreshed, consider utilizing a [scheduled trigger](/platform/forge/remote/scheduled-triggers/).
  There is no endpoint for proactively refreshing the access token.
* As there is no lifecycle event sent upon app uninstallation yet ([FRGE-1246](https://ecosystem.atlassian.net/browse/FRGE-1246)),
  Atlassian app APIs returning 4xx can indicate the app is no longer installed on the tenant.
  You can infer the app was uninstalled if it stopped receiving a scheduled trigger.

## Getting started

Once you've got your token, you can use it in backend requests to Atlassian app APIs.

### Node.js example

This example uses the `fetch` function from the `node-fetch` module to request data from the Confluence API:

```
```
1
2
```



```
'use strict'
import fetch from 'node-fetch';

export async function fetchFromConfluence(token, apiBaseUrl) {
  const headers = {
    Accept: 'application/json',
    Authorization: `Bearer ${token}`
  }
  return await fetch(`${apiBaseUrl}/wiki/rest/api/content`, { headers });
}
```
```

For more detail, see the [Confluence node client](https://bitbucket.org/atlassian/forge-remote-nodejs/src/main/src/requestConfluence.js) in Bitbucket.

For [Connect apps that have adopted Forge](https://developer.atlassian.com/platform/adopting-forge-from-connect/how-to-adopt/), the Atlassian Connect Express framework provides a method [`getForgeAppToken`](https://bitbucket.org/atlassian/atlassian-connect-express/src/f3ef1a18e9632f92beaeb5790cd6cc9ae0e27b58/lib/index.js#lines-229:231)
to retrieve an app token stored in a request from the Forge platform.

### Java example

This example uses a GET request to call from a Confluence Content API:

```
```
1
2
```



```
public ResponseEntity<String> getContent(final String token, String baseUrl) {

    final HttpHeaders headers = new HttpHeaders();
    headers.setBearerAuth(token);

    final HttpEntity<String> entity = new HttpEntity<>(null, headers);

    final ResponseEntity<String> response =
            restTemplate.exchange(baseUrl + "/wiki/rest/api/content",
                    HttpMethod.GET, entity, String.class);

    logger.info("Response statusCode={}", response.getStatusCode());

    return response;
}
```
```

For more detail, see the [Confluence java client](https://bitbucket.org/atlassian/forge-remote-spring-boot/src/main/src/main/java/com/atlassian/frc/ConfluenceRestClient.java) in Bitbucket.

For [Connect apps that have adopted Forge](https://developer.atlassian.com/platform/adopting-forge-from-connect/how-to-adopt/), the Atlassian Connect Spring Boot framework provides a method [`asApp(String installationId)`](https://bitbucket.org/atlassian/atlassian-connect-spring-boot/src/c23b9ae9b8a26729f42449890916679a2fc121bf/atlassian-connect-spring-boot-api/src/main/java/com/atlassian/connect/spring/AtlassianForgeRestClients.java#lines-23)
to send a request using a stored app access token. An example is available at [Forge Remote Sample](https://bitbucket.org/atlassian/atlassian-connect-spring-boot-samples/src/db2ef84e3111a71402091ac49ac1ff233647963e/atlassian-connect-spring-boot-sample-forge-remote/src/main/java/sample/connect/spring/frc/controllers/Controller.java#lines-80:85).

## Offline user impersonation

Apps have the ability to impersonate any user in their installation context, subject to a number of conditions. For more information, see:

On a Forge remote, impersonating a user that's not in session requires exchanging the app system token for an authorisation token for another
user. This can be done by calling a special mutation on [Atlassian's GraphQL Gateway](/platform/atlassian-graphql-api/graphql/). This mutation
is configured to allow being called from a Forge remote using a Forge app system token.

```
```
1
2
```



```
mutation forge_remote_offlineUserAuthToken($input: OfflineUserAuthTokenInput!) {
  offlineUserAuthToken(input: $input) {
    success
    errors {
      message
    }
    authToken {
      token
      ttl
    }
  }
}
```
```

Where `input` contains:

```
```
1
2
```



```
{
  contextIds: ["<context ARI of the installation>"],
  userId: "<account ID being impersonated>"
}
```
```

This can be called by calling the GraphQL gateway at `https://api.atlassian.com/graphql` and setting the `Authorization` header to
`Bearer ${appSystemToken}`. If `success` is set to `true` in the response, the corresponding `token` in `authToken` can be used in the same
way as the app system token or app user token in the examples above. This will make API calls authenticated as the given account ID,
subject to the constraints of offline user impersonation.

The `ttl` is the token lifetime in seconds. This can be used to cache a particular user token for a given installation and user ID, we
recommend doing this if your app will make multiple impersonation calls for the same user.

The rate limit for requesting user impersonation tokens using this mutation is 10,000 requests per minute, per app.

### Node.js example

```
```
1
2
```



```
const query = "<as above>";

async getTokenForUser(systemToken, contextAri, userAccountId) {
  const response = await fetch("https://api.atlassian.com/graphql", {
    method: "POST",
    headers: {
      accept: "application/json",
      "content-type": "application/json",
      authorization: `Bearer ${systemToken}`,
    },
    body: JSON.stringify({
      query,
      variables: {
        input: {
          contextIds: [contextAri],
          userId: userAccountId,
        },
      },
    }),
  });

  if (!response.ok) {
    throw new Error(`HTTP error: ${response.status}`);
  }

  const json = await response.json();

  if (!json.data.offlineUserAuthToken.success) {
    throw new Error(`GraphQL error: ${json.data.offlineUserAuthToken.errors}`);
  }

  // returns { token: "<token>", ttl: <token TTL> }
  return json.data.offlineUserAuthToken.authToken;
}
```
```

## Atlassian app APIs

For a complete list of Atlassian app APIs that you can call from your remote, see :

## Next steps

For further help, see how you can:
