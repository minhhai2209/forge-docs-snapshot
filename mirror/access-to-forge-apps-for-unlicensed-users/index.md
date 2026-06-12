# Access to Forge apps for unlicensed users

## Introduction

If the Atlassian app module you're using supports unlicensed access, you can optionally
allow one or more types of these unlicensed users to run your Forge app. This is
done by adding permissions in your app's `manifest.yml` file.

This guide covers unlicensed access for:

* **Jira and Jira Service Management** - modules rendered on Jira Service Management.
* **Jira Service Management** - unlicensed users in portals
* **Confluence** - guest users and anonymous users
* **Jira** - anonymous users for select modules

By default, only licensed, authenticated users of the Atlassian app within which an
app runs, can use that app. For Jira Service Management, these licensed users
include agents, project administrators, and collaborators. This means that
Forge apps won't work for unlicensed users in portals/views, such as the Jira
Service Management portal, that support unlicensed use cases unless you
configure your app to allow it.

## Overview of Forge unlicensed access

Before configuring unlicensed access, make sure you understand the different
types of unlicensed users. Jira Service Management has three unlicensed user
types, reflecting different levels of the user’s relationship with the site:

| Unlicensed user | Description |
| --- | --- |
| `unlicensed` | A user who is logged in to their Atlassian account but does **not** have that Atlassian app license on the site. For example, a user might be licensed for Confluence and Jira but not have an agent license for Jira Service Management on that site. That user is an `unlicensed` user of Jira Service Management, but a `licensed` user of Confluence and Jira.  To learn more about Atlassian accounts, see [What is an Atlassian account?](https://support.atlassian.com/atlassian-account/docs/what-is-an-atlassian-account/). |
| `customer` | A user who is logged in to their Atlassian account who has limited access to the Atlassian app on that site and can only perform certain actions in it. For example, in Jira Service Management, users with the customer role are considered to be customer unlicensed users.  For example, a Jira Service Management customer can view their own requests on a portal and receive notifications about them. However, they don't have access to the Jira Service Management project or the ability to create or edit issues.  To learn more about roles in Jira Service management, see [What are project roles in Jira Service Management?](https://support.atlassian.com/jira-service-management-cloud/docs/what-are-user-types-and-roles/). |
| `anonymous` | A user who is not logged in to an Atlassian account. |

Unlicensed access is currently supported for the following Jira Service Management modules:

And for the following Jira modules rendered on Jira Service Management Agent View:

And for the following Jira modules rendered on Jira Service Management Portal:

Note that full-page Jira modules (for example, `jira:globalPage`, `jira:fullPage`, and `jiraServiceManagement:queuePage`) do **not** support unlicensed or anonymous access.
To support `customer` (licensed), `unlicensed`, or `anonymous` users, use Jira Service Management portal modules such as `portalFooter`, `portalHeader`, or `portalSubheader`.

### Confluence Forge Modules

Confluence has two unlicensed user
types, reflecting different levels of the user’s relationship with the site:

| Guest user | Description |
| --- | --- |
| `unlicensed` | Users with an Atlassian account who have limited access to a single Confluence space. Guests are authenticated but don't consume a paid license. |
| `anonymous` | A user who is not logged in to an Atlassian account. |

Unlicensed access is currently supported for the following Confluence modules:

Note that the `confluence:fullPage` module does **not** support unlicensed or anonymous access. Full-page modules require a user with an Atlassian account.

### Jira Forge Modules

| Unlicensed user | Description |
| --- | --- |
| `anonymous` | A user who is not logged in to an Atlassian account. |

Unlicensed access is currently supported for the following Jira modules:

### Supported functionality

#### Authenticated Atlassian app API calls

Only JSM customer users can make `asUser()` API calls from frontend and backend contexts. Other `unlicensed` user types can't make these calls because they are unauthorized and don't have full Jira Service Management project access.
Making `asUser()` calls from a backend function on behalf of a user without an active session is currently not supported for unlicensed users.

Apps with the necessary permissions are able to make `asApp()`
API calls. Bear in mind that `asApp()` authenticates as your app's service account
which will usually have a higher level of privileges than anonymous users.
Ensure that you do not return any data to the front-end that you do not wish to expose to less privileged users.

| Authenticated Atlassian app API calls | Unlicensed access |
| --- | --- |
| `asUser` | Allowed for JSM `customer` users only |
| `asApp` | Allowed |

#### Frontend bridge calls from unlicensed users

Calls made utilising the Forge frontend bridge will make unauthenticated requests when a user is not present and the app has declared support for anonymous users.

#### AccountType property in resolver context

You can use the `AccountType` property in the `Resolver` context to customize your app's behavior. For more information
on this, see [How to customize app behavior for unlicensed users](/platform/forge/access-to-forge-apps-for-unlicensed-users/#customize-app-behavior-for-different-types-of-users) below.

#### Storage API

The app can use storage APIs to store and retrieve values from Forge storage using the Forge
storage API while invoking modules for unlicensed users.

Note that for anonymous users, `accountId` will be the string `unidentified`.
If you use it to populate storage keys, you might end up sharing the data among
all anonymous users.

For example:

```
```
1
2
```



```
const secretKey = await kvs.getSecret(`github-secret:${context.accountId}`)
```
```

For anonymous users `${context.accountId} === 'unidentified'`

Because all `anonymous` have the same `accountId`, `unidentified`, and this developer has keyed
storage on the `accountId`, they are sharing the same data across all anonymous users.

See [Storage API](/platform/forge/storage) to learn more.

#### Forge tunnel

You can tunnel development app invocations from `customer` and `anonymous` account types.

## Opt in to unlicensed access

Atlassian apps may cache invocation responses for up to five minutes, so wait five minutes before
attempting to validate an opt-in change using the app's user interface.

### Quickstart: Enable unlicensed access in specific JSM modules

By default, Forge modules don’t allow unlicensed user access. You can opt in for unlicensed
access via the manifest using the `unlicensedAccess` property on supported modules. This
is an optional property and its absence means that the module does not allow unlicensed users.

The `unlicensedAccess` property in the manifest expects an array of user types.

1. Check the [module table] (/platform/forge/access-to-forge-apps-for-unlicensed-users/#overview-of-forge-unlicensed-access)
   and make sure the module you’re adding is open to your target user types (customer, unlicensed, anonymous).
2. Add `unlicensedAccess` to each supported module. This property expects an array of user types.
   For example, the sample `manifest.yml` file section below shows an app
   that uses the `jiraServiceManagement:portalFooter` module.

```
```
1
2
```



```
modules:
  jiraServiceManagement:portalFooter:
    - key: hello-world-panel
      resource: main
      resolver:
        function: resolver
      viewportSize: medium
      unlicensedAccess:
        - anonymous
        - customer
```
```

This app allows `anonymous` and `customer` users to interact with the `hello-world-panel`
module. Hence, when an `anonymous` or `customer` user visits the portal page,
this app module will be run.
However, since this app doesn't allow users with `accountType: unlicensed`, this module won't run for that user type on the portal page.

3. Run `forge lint` then `forge deploy`.

The Atlassian app may cache invocation responses for up to ~5 minutes, so validate after that.

## Customize app behavior for different types of users

You can customize app behavior for different user types by fetching the
current user's account type from the `accountType` property. This property can
have one of the following possible values, three of which are the unlicensed user
types mentioned previously:

| AccountType | Description |
| --- | --- |
| `licensed` | Users who have Atlassian accounts and have that Atlassian app licensed on the site.  These users have access to the app by default, whether or not the developer has opted in to allowing access for one or more user types. |
| `unlicensed` | Users who have Atlassian accounts but do **not** have that Atlassian app license on that site.  For example, a user might be licensed for Confluence and Compass but not licensed for both Jira and Jira Service Management on that site. That user is an unlicensed user of Jira Service Management. |
| `anonymous` | Users who are not logged in, regardless of whether they do or do not have an Atlassian account. |
| `customer` | Users who have limited access to the Atlassian app and can only perform certain actions.  For example, a Jira Service Management customer can view their own requests on a portal and receive notifications about them but they don't have access to the Jira Service Management project or the ability to create or edit issues. |

### UI Kit and Custom UI

Apps can call a resolver if they need `accountType`. The resolver can access the
`accountType` property in the context and simply return its value back to the view:

```
```
1
2
```



```
resolver.define('getAccountType', (req) => {
  return req.context.accountType;
});
```
```

## Understand manifest validation errors for unlicensed access via the Forge CLI

Unlicensed access is only supported in certain Jira Service Management modules,
as mentioned above. The Forge CLI has been updated to validate your manifest
when running and prevent you from incorrectly configuring modules as follows:

* `forge lint` displays an error message if unlicensed access is configured incorrectly.
* `forge deploy` displays an error message and does not deploy your app if unlicensed access
  is configured incorrectly.

There are two types of errors you might encounter in the Forge CLI:

* Module does not support unlicensed access by any users.
* Module does not support unlicensed access by a specific unlicensed user type.

### Example: Unlicensed access is not supported by the module

If you try to add unlicensed access to modules that don’t support it, Forge displays an error
in this format:

```
```
1
2
```



```
${module} does not support the following Forge properties - 'unlicensedAccess'
```
```

Consider the following manifest that defines `unlicensedAccess` for the `hello-world-panel`
module using `jiraServiceManagement:queuePage`.

```
```
1
2
```



```
modules:
  jiraServiceManagement:queuePage:
    - key: hello-world-panel
      resource: main
      resolver:
        function: resolver
      viewportSize: medium
      unlicensedAccess:
        - anonymous
        - customer
```
```

As mentioned above, the `jiraServiceManagement:queuePage` module is not open for unlicensed
access. You will get the following error when you try to deploy this app:

```
```
1
2
```



```
$ forge deploy
error    jiraServiceManagement:queuePage does not support the following Forge properties - 'unlicensedAccess'  valid-document-required
```
```

Notice that the error message references the specific module. This indicates that
the module does not support any unlicensed access.

### Example: Unlicensed access is not supported by the module for a particular user type

If you try to add a user type that is not supported by a module, Forge displays an error
in this format:

```
```
1
2
```



```
Property "unlicensedAccess" in ${moduleKey} must be an array of one or more of the
following values: [unlicensed, customer, anonymous]
```
```

Consider the following manifest that defines `unlicensedAccess` for `anonymous` and `customer`
user types to `hello-world-panel` for `jiraServiceManagement:portalUserMenuAction`.

```
```
1
2
```



```
modules:
  jiraServiceManagement:portalUserMenuAction:
    - key: hello-world-panel
      resource: main
      resolver:
        function: resolver
      viewportSize: medium
      unlicensedAccess:
        - anonymous
        - customer
```
```

As mentioned above, although the `jiraServiceManagement:portalUserMenuAction` module is
open for unlicensed access but it only allows `unlicensed` and `customer` accounts to have access.
Therefore you will get the following error when you try to deploy this app:

```
```
1
2
```



```
$ forge deploy --verbose
  Upload URL is valid
  Found manifest file
  Manifest is a valid YAML
  Property "unlicensedAccess" in hello-world-panel-portal-user must be an array of one or more of the following values: [unlicensed, customer]

Error: Deployment failed
```
```

Notice that in this case, the error message references your app key. This indicates that the issue is that the module does support some types of unlicensed access, but does not support one or more of the user types you specified for your app.
