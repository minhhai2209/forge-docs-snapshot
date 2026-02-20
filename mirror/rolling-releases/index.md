# Rolling releases

Forge rolling releases is available through Forge's Early Access Program (EAP). This feature is currently only available in Jira, Confluence, and Bitbucket.

EAP grants selected users early testing access for feedback; APIs and features in EAP are experimental, unsupported, subject to change without notice, and not recommended for production. To join the EAP, please complete the [sign-up form](https://ecosystem.atlassian.net/servicedesk/customer/portal/1040/group/3496/create/18974).

For more details, see [Forge EAP, Preview, and GA](/platform/forge/whats-coming/).

## What are rolling releases?

Rolling releases decouple **permissions** (scopes, egress, and remotes) from **app code versions**. This means you can deploy new code without waiting for admin approval of new permissions.

Currently, when permissions change, the app remains on the old version of the code for all existing installations, and admins are sometimes slow to update the apps, causing version fragmentation.

With rolling releases, when you deploy a new version with permission changes:

* The new code runs on all installations sooner
* Permissions remain at the old version until the admin approves
* Your app checks for permissions at runtime and gracefully handles missing ones

## Why rolling releases?

One of the drivers for this change is developers having many customers not getting the latest version of the code, and developers need to back-port fixes and security patches to old major versions, increasing the load on developers to support old major versions. Some developers have expressed that they do not have the capacity to maintain old versions.

**Key benefits:**

* **Reduce version fragmentation**: All customers get the latest code sooner, eliminating the need to maintain multiple versions
* **Ship faster**: Deploy bug fixes, performance improvements, and new features continuously without waiting for approvals
* **Lower maintenance costs**: No need to backport fixes to multiple versions, reducing development overhead and infrastructure costs

## How it works

### Decoupled state / code only upgrades

When an installation is upgraded with a code-only upgrade:

1. **All installations get the new code**
2. **Permissions remain at the old version** until the admin approves
3. **Your app must check for permissions at runtime** and gracefully handle missing ones

This state is called "decoupled" because the code version is ahead of the permission version.

### Exiting decoupled state

When an admin approves new permissions, the permissions will then match the manifest of that version, and is no longer considered "decoupled".

## EAP scope

This EAP focuses on adopting the SDK and testing the decoupled state, it does *not* support rolling out code versions to end-users, only test sites you control.

## Getting started

## Opt into decoupled permissions

Update the permissions section in the app manifest to indicate that app is managing missing permissions. This is done by adding `enforcement: app-managed` config to app permissions.

```
```
1
2
```



```
app:
  id: ...
permissions:
  enforcement: app-managed
  scopes:
    - ...
  external:
    - ...
```
```

When the enforcement is set to app-managed, the app will be eligible to enter a decoupled state, and will encounter a permission denied error, or have their external request blocked if the app attempts to perform some action that requires a new permission that is not granted yet. It is up to the app to use the SDK to prevent crashes.

Please see [Permissions SDK](#permissions-sdk) to check for missing permissions at runtime.

## Permissions SDK

The updated code may include changes that depend on new permissions but since only the app code was upgraded, some permissions might be missing. To handle such cases, use the permissions SDK to verify if the permission exists and gracefully handle if the needed permission does not exist.

The Permissions SDK is available for both frontend (`@forge/react` for UIKit, `@forge/bridge` for Custom UI) and backend (`@forge/api`) code.

### Frontend SDK

```
```
1
2
```



```
npm install --save @forge/react
```
```

#### Check if app installation has required permissions

Import the `usePermissions` hook to check permissions:

```
```
1
2
```



```
import { usePermissions } from '@forge/react';

const MyComponent = () => {
  const { hasPermission, isLoading, missingPermissions, error } = usePermissions({
    scopes: ['read:confluence-content', 'write:confluence-content'],
    external: {
      fetch: {
        backend: ['https://api.example.com'],
        client: ['https://cdn.example.com']
      },
      images: ['https://images.example.com'],
      fonts: ['https://fonts.googleapis.com']
    }
  });

  if (isLoading) return <Text>Loading...</Text>;
  if (error) return <Text>Error: {error.message}</Text>;
  if (!hasPermission) {
    return <Text>Missing: {JSON.stringify(missingPermissions)}</Text>;
  }
  
  return <Text>All permissions granted!</Text>;
};
```
```

The hook returns an `isLoading` boolean, but this should not be `true` for any significant amount of time.

### Custom UI

```
```
1
2
```



```
npm install --save @forge/bridge
```
```

#### Check if app installation has required permissions

Import the `checkPermissions` function to check permissions:

```
```
1
2
```



```
import { checkPermissions } from '@forge/bridge';

const App = () => {
  const [hasPermission, setHasPermission] = useState(false);
  const [missingPermissions, setMissingPermissions] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  useEffect(() => {
    checkPermissions({
      scopes: ['read:jira-work'],
      external: {
        fetch: {
          backend: ['https://example.com/something'],
        },
      },
    }).then(({granted, missing}) => {
      setHasPermission(granted);
      setMissingPermissions(missing);
      setIsLoading(false);
    }).catch(err => {
      setError(err);
      setIsLoading(false);
    });
  }, []);

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;
  if (!hasPermission) {
    return <div>Missing: {JSON.stringify(missingPermissions)}</div>;
  }
  
  return <div>All permissions granted!</div>;
};
```
```

**Display conditions**

You can disable or show an alternative module in the frontend if permissions are missing using display conditions. See [Display conditions: Permissions](/platform/forge/manifest-reference/display-conditions/permissions/) for more information.

### Backend SDK

Install the `next` version of the `@forge/api` package:

```
```
1
2
```



```
npm install --save @forge/api@next
```
```

#### Check if app installation has a scope granted

```
```
1
2
```



```
import { permissions } from '@forge/api';

const isPermitted = permissions.hasScope('storage:app')
```
```

#### Check if backend permission is granted

```
```
1
2
```



```
import { permissions } from '@forge/api';

const isPermitted = permissions.canFetchFrom('backend', 'https://api.example.com')
```
```

#### Check if app has access to load resource

```
```
1
2
```



```
import { permissions } from '@forge/api';

const isPermitted = permissions.canLoadResource('images', 'https://api.example.com/image.png')
```
```

#### Check multiple types of permission grants

```
```
1
2
```



```
import { permissions } from '@forge/api';

const { granted, missing } = permissions.hasPermission({ 
    scopes: ['storage:app'],
    external: {
        fetch: {
            backend: ["https://api.example.com", "https://blah.com", "https://www.google.com"]
        },
        images: ["https://images.example.com", "https://cdn.example.com"],
    }
})
```
```

You must extract the `granted` property from the returned object.

## Atlassian app events filters

If your app doesn’t have the right permissions, running an [Atlassian app event](/platform/forge/events-reference/product_events/) can result in error from the app code. You can use a filter to stop the function from running at the platform level when the required permissions are missing.

Permissions object is added to the event object so that we can filter out Atlassian app events if certain permissions are missing. Update the [expression](/platform/forge/events-reference/product_events/#filter-out-atlassian-app-events) to filter events if certain permissions are missing. For example, to check the missing scopes use the following expression:

```
```
1
2
```



```
modules:
  trigger:
    - key: jira-issue-trigger-filtering-by-expression-for-bug-issue-type
      function: main
      events:
        - avi:jira:created:issue
      filter:
        expression: "event.permissions.scopes.includes('write:jira-work') && event.issue.fields?.issueType.name == 'Bug'"
  function:
    - key: main
      handler: index.run
```
```

External egress is also available in the `event.permissions` and can be used for filtering. The following expression can be used to filter out Atlassian app events based on external backend fetch permission:

```
```
1
2
```



```
modules:
  trigger:
    - key: jira-issue-trigger-filtering-by-expression-for-bug-issue-type
      function: main
      events:
        - avi:jira:created:issue
      filter:
        expression: "(event.permissions.external?.fetch?.backend || []).includes('*.example.com')"
  function:
    - key: main
      handler: index.run
permissions:
  enforcement: app-managed
  external:
    fetch:
      backend:
        - "*.example.com"
```
```

For more examples of expressions you can use, see [Filter out Atlassian app events](/platform/forge/events-reference/product_events/#filter-out-atlassian-app-events).

To try out your own event filtering expressions against a sample payload, use the [Expressions playground](/platform/forge/events-reference/expressions-playground/).

## Lifecycle events

### App upgrade event

When an admin consents to the new permissions for your Forge app, the [upgrade event](/platform/forge/events-reference/life-cycle/#upgrade) is triggered. The event payload now includes the app’s updated `permissions`, helping you track permission changes during major upgrades. For more information, see the [Forge app upgrade event documentation](/platform/forge/events-reference/life-cycle/#type-reference-1).

The upgrade event is not triggered for code-only upgrades (when only your app’s code changes, and there are no changes to the manifest or permissions).

## Developer testing

For a developer to ensure their app will work when apps upgrade from previous versions, and they have checked the correct permissions in the correct places, they need to enter a decoupled state with various permission combinations from previous major versions.

### Installing into a decoupled state

To test how your app behaves with different permission levels, you can install directly into a decoupled state:

```
```
1
2
```



```
# Install with permission version 2, code version 2 (coupled)
forge install --major-version 2

# Upgrade only code to version 4 (decoupled state: permissions v2, code v4)
forge install --upgrade code --major-version 4

# Upgrade both code and permissions to version 4 (coupled again)
forge install --upgrade --major-version 4
```
```

## EAP limitations

The following features are under development, therefore are not offered as part of EAP:

* Code auto-upgrade on customer site not supported.
* Only Jira, Confluence, and Bitbucket are supported.
* Forge Containers not supported.
* Upgrading from version without license to a version with license enabled is not supported.
* Upgrading from version without storage to a version with storage (KVS and SQL) is not supported.
* Upgrading from a version without any dynamic webtriggers to a version with a dynamic webtrigger is not supported.

## Known issues

* Forge [Remote Compute](/platform/forge/runtime-reference/invoke-remote-api/) endpoints cannot use the permissions encoded in the Forge Invocation Token (FIT).

## Tutorials and guides

For a hands-on walkthrough of building an app with rolling releases:
