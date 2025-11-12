# Forge scopes

Certain platform features, such as the [App storage API](/platform/forge/runtime-reference/storage-api/),
are authenticated using OAuth 2.0.

| Scope | Description |
| --- | --- |
| `read:app-system-token` | Enables Forge to pass a token to a remote backend, that can be used to invoke Atlassian app REST APIs with the permissions of the app "bot" user.  For more information see [Forge Remote](/platform/forge/remote). |
| `read:app-user-token` | Enables Forge to pass a token to a remote backend, that can be used to invoke Atlassian app REST APIs with the permissions of the logged-in user.  Only app modules can have this scope, because they are associated with a logged-in user session. App event and lifecycle event modules are not associated with a logged-in user session, therefore they cannot have this scope.  For more information [Forge Remote](/platform/forge/remote). |
| `storage:app` | Enables the [App storage API](/platform/forge/runtime-reference/storage-api/). |
| `report:personal-data` | Enables the [User privacy API](/platform/forge/user-privacy-guidelines/). |
| `read:chat:rovo` | Enables [actions](/platform/forge/manifest-reference/modules/rovo-action/) from your Forge app to be used by agents [created by customers](https://support.atlassian.com/rovo/docs/create-and-edit-agents/). |
| `read:app-global-channel:realtime` | Enables usage of `subscribeGlobal()` calls in the [Realtime API](platform/forge/realtime/). For more information see [Authorizing Realtime channels](platform/forge/realtime/authorizing-realtime-channels/#using-global-channels) |

## Atlassian app scopes

Atlassian app scopes enable a Forge app to request a level of access to an Atlassian app. You can find details about each Atlassian app operation's required scopes through the
[REST API](/platform/forge/apis-reference/product-rest-api-reference/) documentation (specifically, in the
operation's *Oauth scopes required* field). For information about each Atlassian app event's
required scopes, see our [events](/platform/forge/events-reference/product_events/)
documentation.

For more details about each Atlassian app's OAuth 2.0 (3LO) and Forge scopes,
refer to the pages below:
