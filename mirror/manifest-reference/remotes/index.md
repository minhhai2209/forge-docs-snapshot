# Remotes

When using Connect or external authentication, or when invoking a remote backend from a Forge app using the [Forge Remote](/platform/forge/remote), the external domains that the app communicates with are listed in the `remotes` section of the `manifest.yml` file, and are referenced by `key`.

## Properties

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `key` | `string` | Yes | A key for the remote, which other modules can refer to. Must be unique within the list of remotes and have a maximum of 23 characters.  *Regex:* `^[a-zA-Z0-9_-]+$` |
| `baseUrl` | `string`  or `object` (if using region specific URLs) | Yes | Base URL of the remote resource when not using region-specific URLs. |
| `baseUrl.default` | `string` | Yes  (if using region-specific URLs) | Default base URL of the remote resource, required when using region-specific URLs. |
| `baseUrl.<region>` | `string` | Yes  (if using region-specific URLs) | Region-specific base URL (e.g., `US`, `EU`), required for each supported region. |
| `operations` | `array` | No | Indicates the purpose of the data being egressed. For now, this property only accepts four values:   * `storage`: app egresses data to be stored on a remote location. * `compute`: app egresses data to be processed (but not stored) on a remote compute service;   **setting this value is required for   [invokeRemote](/platform/forge/runtime-reference/invoke-remote-api/)   to work.** * `fetch`: app uses a remote endpoint for [client fetch permissions](/platform/forge/manifest-reference/permissions/#fetch) * `other`: data is being egressed for logging, diagnostics, or any purpose other than `storage`,   `compute`, or `fetch`.   If a remotes entry contains no operations property, Forge will assume that the app is egressing end-user data to be stored on a remote back end. See [Data residency](#data-residency) for more information. |
| `auth` | `object` | No | An object that defines the authentication tokens to be provided to the remote endpoint |
| `auth.appUserToken.enabled` | `boolean` | No | If `true` and the remote endpoint is invoked within a user's login session, Forge includes an `appUserToken` in the Forge Invocation Token it sends to the remote app.  This token can be used by the remote app when invoking an Atlassian app API, to invoke the API with the permissions of the user in whose login session the app is running.  Specifically, the API will have only as much access to the site's data as that user does. For example, if the user does not have permission to see pages in a particular space or issues in a particular project, the API won't provide them access to that space or page, either.  Forge modules that run outside of a user's login session, such as an app lifecycle event or Atlassian app event are not associated with a user and cannot send an `appUserToken` to the remote app.  If an endpoint opts to enable remote user token access, the `read:app-user-token` scope must also be specified in the [Permissions](/platform/forge/manifest-reference/permissions) section of the manifest. |
| `auth.appSystemToken.enabled` | `boolean` | No | If `true`, Forge includes an `appSystemToken` in the Forge Invocation Token it sends to the remote app.  This token can be used by the remote app when invoking an Atlassian app API, to invoke the API with the permissions of the generic "bot user" for the app.  If an endpoint opts to enable remote system token access, the `read:app-system-token` scope must also be specified in the [Permissions](/platform/forge/manifest-reference/permissions) section of the manifest. |
| `storage` | `string` | Yes (if `operations` property contains the `storage` value) | Indicates whether you are egressing end-user data to store it on a remote location, through the `inScopeEUD` boolean.  See [Data residency](#data-residency) for more information. |

## Data residency

When an app contains a remotes declaration, Forge will (by default) assume the app is storing in-scope End-User Data on a remote backend. Storing in-scope End-User Data on a remote backend will make your app ineligible for `PINNED` status unless region-based URLs are used.

### Minimum requirements for PINNED status

1. **Remotes using region-based URLs to store in-scope End-User Data:**
2. **Remotes using region-based URLs without storing in-scope End-User Data:**
3. **Apps that egress data but do not store it on a remote backend:**
4. **With hosted storage, remotes not storing in-scope End-User Data:**

By meeting these requirements, Forge will consider your app eligible for `PINNED` status in the admin's **Data residency** interface. This also means that when your app is installed on an Atlassian app with the `PINNED` status, so will your app.

![App pinned to same location as Atlassian app](https://dac-static.atlassian.com/platform/forge/images/dare-pinned-app.png?_v=1.5800.1827)

See [Data residency](/platform/forge/data-residency/) for more information about the `PINNED`
status (for both Atlassian apps and installed apps).

## Realm migration for Forge Remote

Realm migration enables customers to move app data when their Atlassian host app changes regions. This applies to apps that use Forge Remote and have region-specific `baseUrl` configurations [defined for realm pinning](/platform/forge/remote/remote-realm-pinning/). Migration may be required if an app was initially installed in a global location due to missing region-specific `baseUrl` settings or if a customer later relocates their Atlassian app to meet data residency requirements.

To support these migrations, apps must implement the data residency migration hook in the `modules` field of the manifest and handle the required lifecycle hooks.

Find full details in [Supporting realm migrations for Forge Remote](/platform/forge/remote/remote-realm-migration/).

## Major version upgrades

Manifest file updates that add new `remotes` entry or expand an existing remote’s scope will
result in a [major version upgrade](/platform/forge/environments-and-versions/#major-upgrades)
of your app upon deployment. This ensures that whenever an app starts egressing data to a new
back end, admins can review and re-consent first before updating. Such manifest file updates
include:

| Manifest file update | Description |
| --- | --- |
| Adding a new `remotes` section | The app uses a new remote back end, and admins need to be explicitly notified whenever this happens. |
| Changing the `baseUrl` or `baseUrl.<region>` of an existing `remotes` entry | The app now technically egresses data to a new remote back end. |
| Adding a new region URL to `baseUrl` for an existing `remotes` entry entry | The app now technically egresses data to a new remote back end. |
| Converting `baseURL` from string to object type and adding new region URLs | The app now technically egresses data to a new remote back end. |
| Removing region based URLs from `baseURL` | If the app data does not move to the default location after the location is removed, customers may incur data loss. |
| Changing the storage property of a remotes entry from `inScopeEUD: false` to `inScopeEUD: true` | The app is now storing end-user-data on the remote. |

## Minor upgrades

Removing a remotes entry or any update that decrease an existing remote’s scope will only result
in a [minor upgrade](/platform/forge/environments-and-versions/#minor-upgrades). Such manifest
file updates include:

| Manifest file update | Description |
| --- | --- |
| Changing the storage property of a remotes entry from `inScopeEUD: true` to `inScopeEUD: false` | The app previously stored in-scope End-User Data on a remote back end, but now it doesn’t. This reduces the scope of the back end. |
| Converting `baseUrl` from string to object type without adding new URLs | The type of the property changes, but not where the app is egressing data to. |
| Removing one or more (but not all) purposes from an `operations` property | The remote back end’s scope is now reduced, as it is no longer being used for a specific purpose. |
| Moving a URL from a `fetch.backend` declaration to the `remotes` section | The remote back end hasn’t changed in scope, it is now simply declared in a different way. |

Minor upgrades are automatic, and will not require any action by users or admins.

## Example

The following example shows two remotes (`remote-backend` and `loggingserver`) that *do not*
egress in-scope End-User Data to be stored remotely:

```
```
1
2
```



```
permissions:
  scopes:
    - "storage:app"
  external:
    fetch:
      backend:
        - remote: remote-backend
remotes:
  - key: remote-backend
    baseUrl: "https://backend.example.com"
    operations:
      - storage
      - fetch
    storage:
      inScopeEUD: false
  - key: loggingserver
    baseURL: "https://logging.example.com"
    operations:
      - other
```
```
