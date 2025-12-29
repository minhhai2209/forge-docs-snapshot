# Forge Remote essentials

There are some key considerations and responsibilities when using Forge Remote.

# Increased responsibility

If you decide to integrate remote services with Forge you take on additional responsibilities under the Forge [Shared responsibility model](/platform/forge/shared-responsibility-model/).

## Remote contract

This section defines the contract used by remote requests including HTTPS protocol level details, request and response schema.

|  | UI modules | Events and scheduled triggers |
| --- | --- | --- |
|
| API Architecture | REST | REST |
| Protocol | HTTPS | HTTPS |
| Methods | GET, POST, PUT, PATCH, DELETE | POST |
| Timeout | 25s | 5s |
| Retries | None | 4 (See [Handling retries](/platform/forge/remote/sending-product-events/#handling-retries) for more details) |
| Response headers | `Content-Type: application/json`    Custom headers: You can also return custom headers in your API response. | |

### Method usage

When using invokeRemote in your Forge app's [frontend](/apis-reference/ui-api-bridge/invokeRemote) or [backend](/platform/forge/runtime-reference/invoke-remote-api), you specify the method and path for the endpoint in the invokeRemote call.

When using Forge Remote with events or a scheduled trigger, the request is automatically routed to the endpoint configured in the manifest using the `POST` method.

### IP address ranges used when invoking remote backends from Forge

When communicating with remote backends, Forge uses IP address ranges as indicated in the **Outgoing Connections** section of [IP addresses and domains for Atlassian cloud apps](https://support.atlassian.com/organization-administration/docs/ip-addresses-and-domains-for-atlassian-cloud-products/#Outgoing-Connections). This information may be important if your app's remote backend is behind a firewall or other network equipment that restricts access based on IP address.

The following headers are added to requests to your remote.

| Header | Required | Description |
| --- | --- | --- |
| `x-b3-traceid` | Yes | The TraceId is 64 or 128-bit in length and indicates the overall ID of the trace. Every span in a trace shares this ID. |
| `x-b3-spanid` | Yes | The SpanId is 64 or 128-bit in length and indicates the position of the current operation in the trace tree. The value should not be interpreted: it may or may not be derived from the value of the TraceId. |
| `authorization` | Yes | The [Forge Invocation Token (FIT)](#the-forge-invocation-token--fit-) is passed as a bearer token. |
| `x-forge-oauth-system` | No | The app system token. This is used to [call Atlassian app REST APIs](/platform/forge/apis-reference/product-rest-api-reference) from your remote backend. This header is included only if `endpoint.auth.appSystemToken` or `remote.auth.appSystemToken` is true in the app's manifest. |
| `x-forge-oauth-user` | No | The app's user token. This is used to [call Atlassian app REST APIs](/platform/forge/apis-reference/product-rest-api-reference) from your remote backend on behalf of a user. This header is included only if your app manifest has the following configured:  * `endpoint.auth.appUserToken` or `remote.auth.appSystemToken` is `true`. * At lease one user scope required by your app is defined (for example, `read:confluence-content.summary` for Confluence apps). |

# OAuth tokens must be treated as opaque

OAuth tokens provided for FRC (and JWT claims within) need to be treated as Opaque and do not form part of any Published API specification. If your remote requires access to properties such as the cloudId, it can retrieve them by parsing the [Forge Invocation Token (FIT)](#the-forge-invocation-token--fit-).

As an example:

```
```
1
2
```



```
x-b3-traceid: a523b7549f0b88c9
x-b3-spanid: 2a2436c64727923f
authorization: Bearer ${FIT}
x-forge-oauth-system: ${OAuth-System-Token}
x-forge-oauth-user: ${OAuth-User-Token}
header1: value ## Set customer headers when invoking your remote from a UI module
```
```

### Errors

Requests that exceed the timeout or do not return a 2xx HTTP Status Code, will be considered as a failure and will appear in the developer console metrics. See [Remote observability](/platform/forge/remote/observability) for more on metrics and logging.

| HTTP Status Code | Description |
| --- | --- |
| 2xx | The remote successfully processed the request. |
| 3xx | Redirects are not supported and are treated as an error status code. |
| 401 | The JWT token validation failed. |

### The Forge Invocation Token (FIT)

Requests to your remote backend will include a Forge Invocation Token (FIT) as a bearer token in the authorization header. The FIT includes important information about the invocation context and should be used to verify that the request came from Atlassian and is intended for your app.

The Forge Invocation Token contains a JSON object with the following properties:

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `app` | `object` | Yes | Information about the app and installation context. |
| `app.installationId` | `string` | Yes | Identifier for the specific installation of an app. This is the value that any remote storage should be keyed against. Example: `ari:cloud:ecosystem::installation/75969db9-dc7b-4798-9715-bd098ac0d9d1` |
| `app.apiBaseUrl` | `url` | Yes | API base URL where all Atlassian app API requests should be routed. Example: `https://api.atlassian.com/ex/confluence/4c822e2f-510f-48b9-b8d2-8419d0932949` |
| `app.id` | `string` | Yes | The Forge application ID. This should match the value in your Forge `manifest.yml` file. Example: `ari:cloud:ecosystem::app/77334c21-3dd0-474f-a53f-28b4eeee5a71` |
| `app.version` | `string` | Yes | [**\*DEPRECATED\***](https://developer.atlassian.com/changelog/#CHANGE-2433): The app `app.version` value used by some internal Atlassian services. To invoke your actual app version, use `app.appVersion` instead. The `app.version` field will be removed on September 24, 2025.  Example: `1` |
| `app.appVersion` | `string` | Yes | The Forge application version being invoked. Example: `2.0.0` |
| `app.environment` | `object` | Yes | Information about the environment the app is running in. |
| `app.environment.type` | `string` | Yes | The Forge environment type that this invocation was generated for. Examples: `DEVELOPMENT`, `STAGING`, `PRODUCTION` |
| `app.environment.id` | `string` | Yes | The Forge environment id that this invocation was generated for. Example: `ari:cloud:ecosystem::environment/3bb5deab-afcd-4140-9be4-f837b4b14b2c` |
| `app.module` | `object` | Yes | Information about the module that initiated this remote call. |
| `app.module.type` | `string` | Yes | The module type initiating the remote call. This will be the module type, such as `xen:macro` for front-end invocations. Otherwise, it will be `core:endpoint`. To determine the type of module that specified the remote resolver, see `payload.context.extension.type`. Example: `core:endpoint` |
| `app.module.key` | `string` | Yes | The Forge module key for this endpoint. Example: `forge-remote-app-boot` |
| `app.license` | `object` | No | Contains information about the license of the app. This field is only present for paid apps in the production environment.  `license` is `undefined` for free apps, apps in `DEVELOPMENT` and `STAGING` environments, and apps that are not listed on the Atlassian Marketplace. |
| `app.license.isActive` | `boolean` | No | Specifies if the license is active. |
| `app.license.billingPeriod` | `string` | No | Represents the app's billing period. |
| `app.license.ccpEntitlementId` | `string` | No | Represents entitlement id of license if billing system is Commerce Cloud Platform |
| `app.license.ccpEntitlementSlug` | `string` | No | Represents entitlement number of license if billing system is Commerce Cloud Platform |
| `app.license.isEvaluation` | `boolean` | No | A flag indicating whether the app is being used under an evaluation license. |
|
| `app.license.subscriptionEndDate` | `string` | No | Represents the expiration date of the application subscription. |
| `app.license.supportEntitlementNumber` | `string` | No | The Support Entitlement Number (SEN) identifying the license. |
| `app.license.trialEndDate` | `string` | No | Represents the termination date of the trial period. |
| `app.license.type` | `string` | No | Indicates the type of license. Possible values include, but are not limited to `COMMERCIAL`, `COMMUNITY`, `ACADEMIC`, and `DEVELOPER`. |
| `app.installation` | `object` | Yes | Information about app installations. |
| `app.installation.id` | `string` | Yes | Identifier for the specific installation of an app. This is the value that any remote storage should be keyed against. Example: `ari:cloud:ecosystem::installation/75969db9-dc7b-4798-9715-bd098ac0d9d1` |
| `app.installation.contexts` | `[object]` | Yes | The list of contexts where the app is installed. Each item in the list is an object as defined below. |
| `app.installation.contexts.name` | `string` | Yes | Name of the context where app is installed. |
| `app.installation.contexts.apiBaseUrl` | `url` | Yes | API base URL where all Atlassian app API requests should be routed. Example: `https://api.atlassian.com/ex/confluence/4c822e2f-510f-48b9-b8d2-8419d0932949` |
| `context` | `object` |  | The context depends on how the app is using Forge Remote. When invoked from a frontend function, it will contain context describing the module that invoked it. When invoked from a backend function, no context is currently provided. |
| `principal` | `string` |  | The identifier for the user who invoked the app. UI modules only. |

Example:

```
```
1
2
```



```
{
  "app": {
    "id": "ari:cloud:ecosystem::app/8db33809-1f32-48bb-8c52-5877dab48107",
    "version": "16",
    "appVersion": "16.0.1",
    "installationId": "ari:cloud:ecosystem::installation/0a3a7799-53ae-4a5b-9e7e-03338980abb5",
    "apiBaseUrl": "https://api.stg.atlassian.com/ex/confluence/d0d52620-3203-4cfa-8db5-f2587155f0dd",
    "environment": {
      "type": "DEVELOPMENT",
      "id": "ari:cloud:ecosystem::environment/8db33809-1f32-48bb-8c52-5877dab48107/aa911f10-c54b-4b93-9e27-dd2947840b9e"
    },
    "module": {
      "type": "xen:macro",
      "key": "forge-remote-app-boot"
    },
    "license": {
      "isActive": true,
      "billingPeriod": "MONTHLY",
      "ccpEntitlementId": "5e176cc2-6fa0-3c7b-8fc4-302443a16e86",
      "ccpEntitlementSlug": "X-3SH-1A6-33A-AS0",
      "isEvaluation": false,
      "subscriptionEndDate": "1689949707000",
      "supportEntitlementNumber": "SEN-###",
      "trialEndDate": "1989949707000",
      "type": "commercial"
    }
  },
  "context": {
    "localId": "4654fa12-4c7c-4792-95a9-6019edb27953",
    "cloudId": "d0d52620-3203-4cfa-8db5-f2587155f0dd",
    "moduleKey": "forge-remote-app-boot",
    "siteUrl": "https://pbray2.jira-dev.com",
    "extension": {
      "type": "macro",
      "content": {
        "id": "5341185"
      },
      "space": {
        "key": "~655362312d3308895442b0aa38771a10c88656",
        "id": "65538"
      },
      "isEditing": false,
      "references": []
    }
  },
  "principal": "655362:312d3308-8954-42b0-aa38-771a10c88656",
  "aud": "ari:cloud:ecosystem::app/8db33809-1f32-48bb-8c52-5877dab48107",
  "iss": "forge/invocation-token",
  "iat": 1700175149,
  "nbf": 1700175149,
  "exp": 1700175174,
  "jti": "d8a496253ec8c18a54631e4c82cbedd5d0ae8570"
}
```
```

## Verifying remote requests

If you implement a remote backend, you take on additional responsibilities under the Forge [Shared responsibility model](/platform/forge/shared-responsibility-model/).

You must ensure that you:

* Validate all JWT Forge Invocation Tokens provided to your remote endpoint in an authorization header against the following JWKS to ensure that they originated from Atlassian Forge and were intended for an audience of your Application ID.
* Never share or log any OAuth access tokens provided.

To help illustrate the requirements for the above, here is some sample code in both [Javascript](https://bitbucket.org/atlassian/forge-remote-nodejs/src/main/src/validateAuthHeader.js) and [Java](https://bitbucket.org/atlassian/forge-remote-spring-boot/src/main/src/main/java/com/atlassian/frc/FITValidator.java), which is available from the linked repos.

Example code in Java:

```
```
1
2
```



```
@Component
public class FITValidator {

    @Value("${jwks.endpoint:https://forge.cdn.prod.atlassian-dev.net/.well-known/jwks.json}")
    private String jwksUrl;

    @Value("${appId}")
    private String appId;

    public void validate(String invocationToken) throws InvalidJwtException {
        var httpsJwks = new HttpsJwks(jwksUrl);
        var httpsJwksKeyResolver = new HttpsJwksVerificationKeyResolver(httpsJwks);
        var jwtConsumer = new JwtConsumerBuilder()
                .setVerificationKeyResolver(httpsJwksKeyResolver)
                .setExpectedAudience(appId)
                .setExpectedIssuer("forge/invocation-token")
                .build();

        jwtConsumer.process(invocationToken);
    }
}
```
```

Example code in Javascript:

```
```
1
2
```



```
export const validateContextToken = async (invocationToken, appId) => {
  const jwksUrl = 'https://forge.cdn.prod.atlassian-dev.net/.well-known/jwks.json';
  const JWKS = jose.createRemoteJWKSet(new URL(jwksUrl));

  const payload = await jose.jwtVerify(invocationToken, JWKS, {audience: appId});
  return payload;
}
```
```

## Data residency eligibility

When an app contains a `remotes` declaration, Forge will (by default) assume the app is storing in-scope end-user data on a remote backend.

To qualify for the `PINNED` status, you must explicitly declare that your remote backend does not store in-scope End-User Data. Alternatively, apps can still achieve `PINNED` status if they store in-scope End-User Data on a remote backend configured with region-specific URLs. To meet data residency requirements, update the manifest file by defining region-specific `baseUrl` values and marking them with `inScopeEUD: true` to ensure compliance with data residency standards. See [Remotes](/platform/forge/manifest-reference/remotes/#data-residency) for specific instructions on how to do this in your manifest.

For more details about in-scope End-User Data and the `PINNED` status for apps, see [Data residency](/platform/forge/data-residency/).

## Reference materials

Forge Remote makes particular use of some `manifest.yml` sections and properties, runtime APIs, and data structures you might not have encountered before.
