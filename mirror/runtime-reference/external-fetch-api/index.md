# External authentication

The `withProvider` method enables your Forge app to communicate with an API that
requires OAuth 2.0 tokens. Access is via the `asUser` method, in the `@forge/api` package.

```
1import api from "@forge/api";
2
3const response = await api
4  .asUser()
5  .withProvider("google", "google-apis")
6  .fetch("/userinfo/v2/me");
7
```

Working with OAuth 2.0 providers involves more complexity in your app, as you manage
multiple places to configure things correctly. See [Common issues with external authentication](/platform/forge/common-issues-with-external-authentication/) for troubleshooting information.

```
1export interface ExternalAuthAccount {
2  id: string;
3  displayName: string;
4  avatarUrl?: string;
5  scopes: string[];
6}
7export interface ExternalAuthAccountMethods {
8  hasCredentials: (scopes?: string[]) => Promise<boolean>;
9  requestCredentials: (scopes?: string[]) => Promise<boolean>;
10  fetch: FetchMethodAllowingRoute;
11  getAccount: () => Promise<ExternalAuthAccount | undefined>;
12}
13export interface ExternalAuthFetchMethods extends ExternalAuthAccountMethods {
14  listAccounts: () => Promise<ExternalAuthAccount[]>;
15  asAccount: (externalAccountId: string) => ExternalAuthAccountMethods;
16}
17export interface ExternalAuthFetchMethodsProvider {
18  withProvider: (
19    provider: string,
20    remoteName?: string
21  ) => ExternalAuthFetchMethods;
22}
23
```

## hasCredentials

Determines whether the user has already granted those specific scopes. If `scopes` is provided, the function will check whether user grants those scopes.

### Method signature

```
```
1
2
```



```
api.asUser().withProvider(provider).hasCredentials(scopes?: string[]) => Promise<boolean>
```
```

#### Example usage

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
```



```
const [data] = useState(async () => {
  const google = api.asUser().withProvider('google', 'google-apis');
  if (!await google.hasCredentials()) {
    await google.requestCredentials();
  }
  const response = await google.fetch('/userinfo/v2/me');
  ...
})
```
```

## requestCredentials

Triggers the OAuth 2.0 consent flow. The app is replaced with a button for the user
to select to start the flow. During consent flow, the user will be asked to grant consent to the list of scopes provided in the function.
If `scopes` is not provided, then the user will be asked to grant all scopes of the auth provider defined in the manifest file.

When you want to ask for some missing scopes, make sure you also ask for scopes that user already granted.
To obtain granted scopes, use `getAccount` or `listAccounts` calls.

```
```
1
2
```



```
api.asUser().withProvider(provider).requestCredentials(scopes?: string[])
```
```

### Example usage

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
```



```
const google = api.asUser().withProvider("google", "google-apis");
if (!(await google.hasCredentials())) {
  await google.requestCredentials();
}

//another example with scopes provided
const profileScopes = [
  "https://www.googleapis.com/auth/userinfo.profile",
  "https://www.googleapis.com/auth/userinfo.email",
];
if (!(await google.hasCredentials(profileScopes))) {
  //ask for profileScopes and any scope that user already granted
  await google.requestCredentials([
    ...new Set([...profileScopes, ...google.getAccount().scopes]),
  ]);
}
``;
```
```

Alternatively, you can use a declarative approach to achieve the same by specifying `requiredScopes` for the function in the manifest file. See [Providers](/platform/forge/manifest-reference/modules/function/#provider-reference).

Calling `requestCredentials` will throw a platform exception, and function execution will stop at that point. Using the latest version of the `@forge/api` package should prevent this exception from being written to logs and treated as a failed invocation in the [developer console](/console/myapps/).

## fetch

Before using `fetch` for authenticated requests, ensure the user is valid with
[hasCredentials](#hascredentials) or [requestCredentials](#requestcredentials). If the
user is not authenticated, an exception is raised.

Once a user is authenticated, the `fetch` method automatically includes their authentication
token for each request.

Apps using external authentication must define the external domains in the `remotes` section of the
manifest file. See [Remotes](/platform/forge/manifest-reference/remotes).

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| `url` | `string` | Yes | Relative path from the remote specified in [withProvider](#withprovider).  If the `url` parameter starts with a `/`, the remote `baseUrl` path is ignored.  | Remote `baseUrl` | Fetch `url` | Result | | --- | --- | --- | | https://example.atlassian.com/api/v1/ | /api/v1/endpoint | https://example.atlassian.com/api/v1/endpoint | | https://example.atlassian.com/api/v1/ | endpoint | https://example.atlassian.com/api/v1/endpoint | | https://example.atlassian.com/api/v1/ | /endpoint | https://example.atlassian.com/endpoint | |
| `options` | `object` |  | See the node-fetch library’s [Options documentation](https://www.npmjs.com/package/node-fetch#options) for the accepted values. |

## getAccount

Return the account information of an `ExternalAuthAccount`. This account information includes:

* `id`: the unique ID for each account obtained from `ProfileRetriever`
* `displayName`: the `displayName` obtained from `ProfileRetriever`
* `avatarUrl`: the `avatarUrl` obtained from `ProfileRetriever`
* `scopes`: the list of `scopes` that the user granted

The returned account will be used to call external API via `fetch`.
If the user has no integrated external accounts, this function will return `undefined`.

This information is only available if granted consent or token refresh happen after this feature is released. Please make sure to handle when the information is empty.

### Method signature

```
```
1
2
```



```
api.asUser().withProvider(provider).getAccount();
```
```

## listAccounts

A user can integrate multiple external accounts to the Forge app. This function returns all information about those integrated accounts.

### Method signature

```
```
1
2
```



```
api.asUser().withProvider(provider).listAccounts();
```
```

## asAccount

Specify which account should be used to call an external API. Use the `id` (provided by `listAccounts`) for this call.

### Method signature

```
```
1
2
```



```
api.asUser().withProvider(provider).asAccount(externalAccountId: string)
```
```

#### Example usage

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
```



```
// example on how to switch to account whose displayName is `example@gmail.com` to make API call
const selectedDisplayName = "example@gmail.com";
const selectedAccount = (await google.listAccounts()).find(
  (account) => account.displayName == selectedDisplayName
);
const response = await google
  .asAccount(selectedAccount.id)
  .fetch("/userinfo/v2/me");
```
```

## AuthProfile

The return value of a dynamic profile retriever should be an `AuthProfile` object.
See the [dynamic profile retriever](/platform/forge/implement-a-dynamic-profile-retriever-with-external-authentication/)
guide for more information.

The file containing a dynamic profile retriever cannot import `@forge/react`,
because when executed, the dynamic profile retriever is run in a different context
outside of the UI.

```
```
1
2
```



```
AuthProfile({ id, displayName, avatarUrl });
```
```

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `id` | `string` | Yes | Used to de-duplicate accounts and add new accounts. Must be a unique string per account. |
| `displayName` | `string` | Yes | Account name displayed to the user for the purpose of distinguishing between multiple accounts.  Should be one of email, username, or some other unique identifier that the user would recognize.  This should **NOT** be a name value, as that may be the same across multiple accounts. |
| `avatarUrl` | `string` |  | URL providing the avatar picture. |

#### Example usage

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
```



```
interface ProfileRetrieverParameters {
  status: number;
  body: {
    [key: string]: any;
  };
}

export const retriever = (response: ProfileRetrieverParameters) => {
  const { status, body: externalProfile } = response;

  if (status === 200) {
    return new AuthProfile({
      id: externalProfile.user.id,
      displayName: externalProfile.user.name,
    });
  } else {
    // handle error
  }
};
```
```

## withProvider

```
```
1
2
```



```
withProvider(provider[, remoteName])
```
```

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| `provider` | `string` | Yes | The provider `key` from the [manifest](/platform/forge/manifest-reference/providers/#authentication) file. |
| `remoteName` | `string` |  | The remote to use when using [fetch](#fetch). The `remoteName` must be in the `providers.auth.<key>.remotes` list in the [manifest](/platform/forge/manifest-reference/providers/#authentication) file.  `remoteName` may be omitted if only one remote is defined for the provider. |
