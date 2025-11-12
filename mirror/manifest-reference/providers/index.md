# Providers

Forge supports authentication with external applications using OAuth 2.0. An app may authenticate
with multiple different providers. See the following [step-by-step tutorial](/platform/forge/use-an-external-oauth-2.0-api-with-fetch/) to call an external OAuth 2.0 API.

## Properties

The `providers` section of the `manifest.yml` file enables integration with external providers.

## Authentication

To use OAuth2 providers via external authentication, you must specify the integration details of the
identity provider in the `auth` section.

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `key` | `string` | Yes | A key for the provider, used to refer to it from the [runtime API](/platform/forge/runtime-reference/external-fetch-api/#withprovider), and from the [function definition](/platform/forge/manifest-reference/modules/function/#provider-reference).  Must be unique within this list and have a maximum of 23 characters.  *Regex:* `^[a-z0-9_-]+$` |
| `name` | `string` | Yes | The display name of the provider that's shown to the user during the consent flow and on the connected apps page. |
| `type` | `string` | Yes | Must be `oauth2`. |
| `scopes` | `Array<string>` |  | A list of scopes needed to access the provider.  **Note,** scopes cannot be removed. To remove a provider scope, you must create a new integration by changing the provider `key` in the `manifest.yml` file. |
| `clientId` | `string` |  | The OAuth2 `client_id` for your app from the identity provider. |
| `remotes` | `Array<string>` | Yes | A list of [remote](/platform/forge/manifest-reference/remotes) keys that you wish to use this provider with. Do not use uppercase letters for this field.  This applies to requests made inside your Forge app code using the `withProvider()` function. |
| `bearerMethod` | `authorization-header`,  `form-encoded`,  `uri-query` or  [advanced bearer method](#advanced-bearer-method). | Yes | The method of sending the user's authentication token to the service after authentication.  One of `authorization-header`, `form-encoded`, `uri-query` or [advanced bearer method](#advanced-bearer-method).   * `authorization-header`: Sends the token in a HTTP header. * `form-encoded` ([deprecated](/platform/forge/changelog/#CHANGE-1431)): Sends the token in the POST body of the request. * `uri-query` ([deprecated](/platform/forge/changelog/#CHANGE-1431)): Sends the token as a query parameter of the request. |
| `actions` | [Actions](#actions) | Yes | The endpoints needed to perform several parts of the OAuth 2.0 flow. See [Actions](#actions). |

## Example

```
```
1
2
```



```
providers:
  auth:
    - key: google
      name: Google
      scopes:
        - 'profile'
        - 'https://www.googleapis.com/auth/userinfo.email'
      type: oauth2
      clientId: EXAMPLE
      remotes:
        - google-apis
      bearerMethod: authorization-header
      actions:
        authorization:
          remote: google-account
          path: /o/oauth2/v2/auth
        exchange:
          remote: google-oauth
          path: /token
        refreshToken:
          remote: google-oauth
          path: /token
        revokeToken:
          remote: google-oauth
          path: /revoke
        retrieveProfile:
          remote: google-apis
          path: /userinfo/v2/me
          resolvers:
            id: id
            displayName: email
            avatarUrl: picture
remotes:
  - key: google-apis
    baseUrl: https://www.googleapis.com
  - key: google-account
    baseUrl: https://accounts.google.com
  - key: google-oauth
    baseUrl: https://oauth2.googleapis.com
permissions:
  external:
    fetch:
      backend:
        - https://www.googleapis.com
        - https://accounts.google.com
        - https://oauth2.googleapis.com
```
```

## Actions

Defines the endpoints needed to perform several parts of the OAuth 2.0 flow.

### Authorization

Configure the [Authorization request](https://www.oauth.com/oauth2-servers/authorization/the-authorization-request/).

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `remote` | `string` | Yes | The key of a [remote](/platform/forge/manifest-reference/remotes) to use. |
| `path` | `string` | Yes | The path to the authorization endpoint. |
| `queryParameters` | `{[key: string]: string}` |  | Additional query parameters to add to the request.  For example, `access_type: "read"` adds `&access_type=read` to the URL. |

### Exchange

Configure the [Authorization code request](https://www.oauth.com/oauth2-servers/access-tokens/authorization-code-request/).
This request exchanges the authorization code from the user for an access token.

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `remote` | `string` | Yes | The key of a [remote](/platform/forge/manifest-reference/remotes) to use. |
| `path` | `string` | Yes | The path to the authorization endpoint. |
| `resolvers` | `{accessToken: string, accessTokenExpires: string, refreshToken: string}` |  | Some identity providers may have non-standard response. Use this option to resolve the required fields from the response.  Use `.` to access nested values, such as `user.token`   * `accessToken`: Default: `access_token` * `accessTokenExpires`: Default: `expires_in` * `refreshToken`: Default: `refresh_token` |
| `useBasicAuth` | `boolean` |  | Enables the use of HTTP Basic authentication to authenticate with the authorization server. See [RFC 6749: The OAuth 2.0 Authorization Framework](https://datatracker.ietf.org/doc/html/rfc6749#section-2.3.1) for more details. Default: `false` (send client credentials in the request body). |
| `overrides` | [request overrides](#request-overrides) |  | Custom request headers and body. Supported [runtime template](#runtime-templates) variables:   * `{{client_id}}` * `{{client_secret}}` * `{{authorization_code}}` * `{{redirect_uri}}` * `{{http_basic_auth_credentials}}` |

### Refresh token

Configure the [Refresh Access Tokens](https://www.oauth.com/oauth2-servers/access-tokens/refreshing-access-tokens/) request.
This request uses an existing refresh token to obtain new access tokens (along with new refresh tokens, if the auth provider allows it).

If not specifically configured, the request to refresh tokens will automatically default to using configuration for the [Exchange](#exchange).

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `remote` | `string` | Yes | The key of a [remote](/platform/forge/manifest-reference/remotes) to use. |
| `path` | `string` | Yes | The path to the authorization endpoint. |
| `resolvers` | `{accessToken: string, accessTokenExpires: string, refreshToken: string}` |  | Some identity providers may have non-standard response. Use this option to resolve the required fields from the response.  Use `.` to access nested values, such as `user.token`   * `accessToken`: Default: `access_token` * `accessTokenExpires`: Default: `expires_in` * `refreshToken`: Default: `refresh_token` |
| `useBasicAuth` | `boolean` |  | Enables the use of HTTP Basic authentication to authenticate with the authorization server. See [RFC 6749: The OAuth 2.0 Authorization Framework](https://datatracker.ietf.org/doc/html/rfc6749#section-2.3.1) for more details. Default: `false` (send client credentials in the request body). |
| `overrides` | [request overrides](#request-overrides) |  | Custom request headers and body. Supported [runtime template](#runtime-templates) variables:   * `{{client_id}}` * `{{client_secret}}` * `{{refresh_token}}` * `{{redirect_uri}}` * `{{http_basic_auth_credentials}}` |

### Revoke token

Before revoking a user token, this action is run to notify the identity provider of the revocation.

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `remote` | `string` | Yes | The key of a [remote](/platform/forge/manifest-reference/remotes) to use. |
| `path` | `string` | Yes | The path to the revocation endpoint. |
| `overrides` | [request overrides](#request-overrides) |  | Custom request headers and body. Supported [runtime template](#runtime-templates) variables: |

### Profile retriever

Retrieves profile information about the account once authenticated.

A profile retriever may be used to:

1. To allow the user to differentiate between multiple accounts on the
   [Connected Apps](https://id.atlassian.com/manage-profile/apps) screen.
2. To differentiate between a new account and an existing account.

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `remote` | `string` | Yes | The key of a [remote](/platform/forge/manifest-reference/remotes) to use. |
| `path` | `string` | Yes | The path to the authorization endpoint. |
| `function` | `string` | For a static profile retriever,  specify `resolvers`.  To use a dynamic profile retriever,  specify `function`. | Use a Forge function to map the API response.  See [Dynamic profile retriever](/platform/forge/implement-a-dynamic-profile-retriever-with-external-authentication/) for more information. |
| `resolvers` | [static profile retriever](#static-profile-retriever) | Maps the response shape using a fixed field mapping. |
| `method` | `string` |  | The HTTP method used to send the request when using a [static profile retriever](#static-profile-retriever).  Supported values are: `GET` (default), `POST`, and `PUT`. |
| `queryParameters` | `{[key: string]: string}` |  | Additional query parameters to add to the request when using a [static profile retriever](#static-profile-retriever).  For example, `foo: "bar"` adds `&foo=bar` to the URL.  The following [runtime template](#runtime-templates) variables can also be used: |

#### Static profile retriever

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `id` | `string` | Yes | Differentiates between multiple accounts. Must be a unique string for each account. Not displayed to the user.  The use of [runtime templates](#runtime-templates) for simple string interpolations is also supported. For example, `{{user.id}}:{{team.id}}`. |
| `displayName` | `string` | Yes | The account name displayed to the user for the purpose of distinguishing between multiple accounts.  Can be an email, username, or some other unique identifier that the user would recognize.  This should *not* be the name of the user, as this may be the same across multiple accounts.  The use of [runtime templates](#runtime-templates) for simple string interpolations is also supported. For example, `{{user.name}} at {{team.name}}`. |
| `avatarUrl` | `string` |  | Optional URL to an avatar image. |

## Advanced bearer method

Some services use non-standard header names or query parameters. The advanced `bearerMethod` object
allows you to override the values expected by the existing bearer method types.

See the above [Authentication](/platform/forge/manifest-reference/providers/#authentication) section
for other `bearerMethod` values.

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `type` | `authorization-header`,  `form-encoded` or  `uri-query` | Yes | Method to send the user authentication token to the service after authentication.   * `authorization-header`: Sends the token in the an HTTP header. * `form-encoded` ([deprecated](/platform/forge/changelog/#CHANGE-1431)): Sends the token in the POST body of the request. * `uri-query` ([deprecated](/platform/forge/changelog/#CHANGE-1431)): Sends the token as a query parameter of the request. |
| `prefix` | `string` |  | A prefix inserted before the token in `authorization-header` type requests. Defaults to `Bearer` .  We recommend adding a trailing space. |
| `parameter` | `string` |  | Either a custom header name (for `authorization-header`) or parameter name.  Defaults to `Authorization` for the `authorization-header` type. Otherwise, `access_token`. |

### Example

```
```
1
2
```



```
bearerMethod:
  type: authorization-header
  prefix: 'token '
  parameter: 'X-Custom-Header'
```
```

## Runtime templates

Runtime templates enable the dynamic injection of data into otherwise static configuration defined in the `manifest.yml` file. Unlike [variables](/platform/forge/manifest-reference/variables), which are populated at deployment time, runtime templates are always evaluated at runtime.

The syntax for the runtime templates is `{{template_variable}}`, while the availability of template variables depends on the context in which the template is used.

String interpolations are also supported, including combinations of both static values and template values. For example, `qux:{{client_id}}:{{team_id}}`.

### Request overrides

To accommodate providers that don't strictly adhere to [The OAuth 2.0 Authorization Framework](https://datatracker.ietf.org/doc/html/rfc6749) standard, use request overrides to customise the request headers and body for certain [actions](#actions).

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `headers` | `{[key: string]: string}` |  | The exact headers to be used for the request. |
| `body` | `{[key: string]: string}` |  | The exact body to be used for the request. For an empty body use `body: {}`. |

Avoid including sensitive information, such as passwords or secret data, as static values in overrides. Instead, use the available runtime template variables.

#### Example

```
```
1
2
```



```
overrides:
  headers:
    foo: bar # static value
    'x-client-id': '{{client_id}}' # template value
    'x-authorization': 'Basic {{http_basic_auth_credentials}}' # template with string interpolation
  body:
    # static values:
    client_assertion_type: 'urn:ietf:params:oauth:client-assertion-type:jwt-bearer'
    grant_type: 'urn:ietf:params:oauth:grant-type:jwt-bearer'
    # templates:
    client_id: '{{client_id}}'
    client_assertion: '{{client_secret}}'
    assertion: '{{authorization_code}}'
    redirect_uri: '{{redirect_uri}}'
```
```
