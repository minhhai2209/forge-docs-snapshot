# Adopt user-based billing for Forge apps

User-based billing is available as part of its first milestone release, allowing app developers
to build, deploy and test an app via Forge CLI on non-production environments.

The milestone releases to follow for user-based billing will enable app publishing, pricing setup,
app revision, and app approval to be available on Atlassian Marketplace.

The user-based billing model allows developers to separate user tiers, offering a more flexible
and tailored approach to app billing. This model allows customers to pay only for a specific subset
of users within an Atlassian app instance, rather than covering all users.

## Prerequisites

The app must be **a paid app that’s built on the Forge platform, and published on Atlassian
Marketplace**. Other apps used for testing may try user-based billing in non-production
environments only.

**User-based billing is not supported for Connect apps.**

To use the user-based billing feature, Connect apps must [adopt Forge](/platform/adopting-forge-from-connect/).
After a Connect app transitions to Forge and enables user-based billing, older versions of the
app will need to be upgraded to support this feature.
This transition ensures that all app versions align with the new billing model.

## Changes to the app manifest

The app manifest introduces a new field `access`. To enable user-based billing, you need to set
both `licensing.enabled=true` and `access.userAccess=true`, as in the example that follows.

```
```
1
2
```



```
modules:
  ...
resources:
  - key: main
    path: src/frontend/index.jsx
app:
  runtime:
    name: nodejs24.x
  id: ari:cloud:ecosystem::app/22a5950e-2b5a-4cb0-8fc0-cf9a6cc64b33
  licensing:
    enabled: true
  access:
    userAccess: true
```
```

You **must** set `licensing.enabled` to `true` if you've set `userAccess` to `true`.
Attempting `userAccess: true` with licensing set to `false` will result in a deployment failure.

After declaring user-based billing in the manifest, you can no longer remove or change this
declaration. You can no longer convert the app into a free app as well. We recommend taking
this into serious consideration before deciding to use user-based billing for your app.

After deploying an app to production with `userAccess` set to `true`, you can no longer change
this declaration. This is because the Atlassian Marketplace does not support transitions from
user-based billing to other billing models.

## Implementing access and license checks

After the app transitions to user-based billing and the admin configures user access, the app code
can retrieve the `userAccess` value to determine and adjust its behavior based on whether the
user has access to the app.

In this section, we’ll demonstrate how to add user access state to the app code context, and
how the app code can access that value.

User access checks should be backported for all previous major versions with app installation
too.

We provide `userAccess` data in different contexts with the same schema as follows:

```
```
1
2
```



```
    userAccess {
        enabled: boolean //indicates whether this installation adopts user-based billing or not
        hasAccess: boolean //indicates whether this user has access to the app
    }
```
```

## Implementing user-based billing

To access the `userAccess` value of the current user in the context object, you can use
the following approaches for UI Kit and Custom UI:

### UI Kit

Within a UI Kit module, you can use the [`useProductContext` hook](/platform/forge/ui-kit/hooks/use-product-context/#useproductcontext/)
from `@forge/react` to access the context object.

Here's a high-level explanation of how you can do it:

* Import the `useProductContext` hook from `@forge/react`
* Access `userAccess` property from the context object.

```
```
1
2
```



```
import { useProductContext } from '@forge/react';
const context = useProductContext();
const hasAccess = context?.userAccess?.hasAccess;
const enabledUserAccessDecoupling = context?.userAccess?.enabled
```
```

### Custom UI

In a Custom UI app, you can use the view module from `@forge/bridge` to get the context.
Here's how you can achieve this:

* Import the view module from `@forge/bridge`.
* Access `userAccess` property from the context object

```
```
1
2
```



```
import { view } from '@forge/bridge';
const context = await view.getContext();
const hasAccess = context?.userAccess?.hasAccess;
const enabledUserAccessDecoupling = context?.userAccess?.enabled
```
```

### Forge display condition

We also provide a new Forge display condition on Jira and Confluence. It is named `hasAppAccess`
whose value is resolved based on whether the user has access to the app. You can use this display
condition to show or hide the extension, based on whether the user has access to the app.

Refer our documentation for details about [display conditions](/platform/forge/manifest-reference/display-conditions/).

In the backend, developers can access the `userAccess` property in the Lambda context.
Here's how you can define a resolver to check user access:

* Begin by identifying the Lambda resolver `request.context`.
* Examine the `userAccess` property within the context to ascertain whether the user has the
  necessary access rights.
* Adjust the backend function's behavior accordingly, depending on whether the user has access or
  not.

The following shows a sample Lambda resolver implementation:

```
```
1
2
```



```
resolver.define('GET projects', async ({ payload, context }) => {
  if (!context.userAccess?.hasAccess) {
    return {
      'error': 'user does not have access',
    };
  }
  // Additional logic...
});
```
```

### Forge Remote

Developers can access `userAccess` in the Forge Invocation Token’s (FIT) context.
This is applicable if the [Forge Remote Compute (FRC)](/platform/forge/remote/) is a resolver.

* If Forge Remote Compute is initiated from the Forge UI, `userAccess` will be provided.
* If Forge Remote Compute is initiated via Forge Lambda, `userAccess` is not provided directly,

### Sample FIT

```
```
1
2
```



```
FIT: {
  app: {
...
    license: {
      isActive: true,
    }
  },
  context: {
  ...
    userAccess: { 
      hasAccess: true,
      enabled: true
    }
  },
...
}
```
```

## Connect iFrame on Connect on Forge app

This only applies to Connect on Forge apps.

The `userAccess` URL parameter in the Connect iFrame, set to either `true` or `false`,
indicates whether the user has access to the app.

When an error on Atlassian's side prevents the determination of user access state,
the `false` value will be returned.

## Backporting changes to prior versions

Backporting ensures that your customers can choose the user-based billing model for all versions of
your app. Additionally, your app revenue is maximized by preventing unauthorized access and enabling
accurate billing for all users.

**Backporting is a critical step and must not be overlooked.**

Ensure that the user access check is
[backported to all previous major versions](/platform/forge/versions/#backporting) with
active app installed instances.

If this is not done, all Atlassian app users with Marketplace app installations on
non-backported versions will have access to the Marketplace app without being charged.

### To backport an older version of an app:

**Step 1**: Update the app manifest.

**Step 2**: Implement user access checks in the code.

**Note that you will not be able to backport Connect versions of Connect on Forge apps.**

## Testing your changes

This section provides guidelines about how to install a Forge app with user-based billing being
enabled. Note that you can only do this with non-production environments.

**Prerequisites**

Before testing, ensure that:

* you’ve installed the latest version of the Forge CLI,
* you're using all Forge libraries in your app code with the latest version, and
* the Forge CLI is authenticated with your Atlassian account.

Overwriting the license of the Forge CLI only works on non-production environments.

## Install the app with user-based billing mode

After successfully modifying and deploying your app, use the Forge CLI to install it with the
user-access license mode. The command must include the `--license-modes` and `--users-with-acces`s
options.

Here’s the command format:

```
```
1
2
```



```
forge install --license-modes user-access --users-with-access <list_of_aaid>
```
```

Replace `<list_of_aaid>` with a comma-separated list of actual Atlassian Account IDs (AAIDs)
of the users you wish to grant access to.

Using the provided command, you can test the user access check by employing different accounts
— both with and without access.

## Getting an Atlassian account ID (AAID)

There are two ways to do this for Forge apps:

* You can run `forge whoami`.

See an example below:

```
```
1
2
```



```
➜  forge-test-arm forge whoami
Logged in as Khanh Nguyen (XXX@atlassian.com)
Account ID: aaid
```
```

* Alternatively, follow instructions on how to get an Atlassian Account ID.

To modify the user access configuration, you must first uninstall the app and then re-install
it with the updated settings.

### Result

When testing, if you have created and deployed your app using the `userAccess` flag without
installing the Forge app with the `--license-modes` override;
the userAccess attributes in your code will automatically default to true.
This happens because user-based billing will not be in effect.

The app should function as expected, with the specified users granted access under the
user-access license mode.

## Limitations

* The `--users-with-access` list does not work if the list is empty or if it exceeds 10 users.
* Production environments do not support `--license-modes` and `--users-with-access` options.
* Exceeding the user limit will return an error in the Forge CLI.
