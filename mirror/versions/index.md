# App versions

When you deploy changes to your app, Forge will create a new app version in the environment you specified
(by default, this is the `development` environment). As you iterate on the app and deploy changes, you'll
create more versions. Each app version can be major or minor, depending on the app change you introduce:

| Major version | Minor version |
| --- | --- |
| Major versions involve significant app changes that require site admins to review them first. A new major version won’t be applied to a site until its admin consents to the upgrade. | Minor versions are incremental improvements to major versions. Forge automatically updates all installed apps to the latest minor version of their major version (without requiring admin consent).    By default, Forge creates new minor versions of the latest major version. However, you can also [backport](#backporting) new minor versions of older major versions. |
| See [Major version upgrades](#major-version-upgrades) for more details about what changes result in a new major version. | See [Minor version upgrades](#minor-version-upgrades) for more information. |

Forge handles versioning automatically, and creates major or minor versions depending on the app change you’re deploying.

## Versioning

Forge creates and maintains versions on a per-environment basis. As such, when you deploy app changes to
`production` resulting in a new major version, this version becomes available for all customer sites in
`production`.

Likewise, if you deploy a new minor version to a major version in `production`, it will automatically be
applied to all customer sites running that major version in `production`.

Forge apps created via the
[developer console](https://developer.atlassian.com/console/myapps/) or [Forge CLI](/platform/forge/cli-reference/)
will initially have a version of `1.1` (major version `1`, minor version `1`).

## Viewing installed versions

There are different ways to see what version of your app is installed on each site, in each environment:

* The `forge install list` [command](/platform/forge/cli-reference/install-list/) will display the major version installed on each site:
  ![forge install list](https://dac-static.atlassian.com/platform/forge/images/app-version/cli.png?_v=1.5800.1837)
* In the [developer console](https://developer.atlassian.com/console/myapps/), your app's **Installations** page (under **MONITOR**) will display the major and minor version. The first segment of the version is the major version
  number. All sites on the same major version will also be on the same minor version:
  ![Developer Console > MONITOR > Installations](https://dac-static.atlassian.com/platform/forge/images/app-version/dev-cons-install.png?_v=1.5800.1837)
* In the [developer console](https://developer.atlassian.com/console/myapps/), your app's
  **Deployments** page (under **BUILD**) will show who performed each deployment (**Contributor**), and when. It’ll also show which major version each deployment targeted within an environment:
  ![Developer Console > BUILD > Deployments](https://dac-static.atlassian.com/platform/forge/images/app-version/dev-cons-deploy.png?_v=1.5800.1837)

Each site’s admin can also see and upgrade their installed app’s version. See
[Manage app upgrades](https://support.atlassian.com/security-and-access-policies/docs/manage-your-users-third-party-apps/#Manage-app-upgrades) for more details.

## Viewing major version history

You can check for the major version history of any app at any time. To know more about checking
for the major version history of your app, go to the
[Forge CLI documentation](/platform/forge/cli-reference/version/).

### List major versions

Navigate to the app's top-level directory and check its list of major versions by running:

The output should look similar to the following:

```
```
1
2
```



```
✔ Getting app version list...

ℹ Details of a total of [5 major versions] in [development] can be seen below:

┌────────────────┬──────────────────────────┬──────────────────┬─────────────────┬──────────┬────────┬──────────────┬───────────┬─────────┬──────────┬─────────┐
│ Major Versions │ Deployment Date          │ Egresses         │ Analytics       │ Policies │ Scopes │ Connect keys │ Functions │ Remotes │ Modules  │ License │
├────────────────┼──────────────────────────┼──────────────────┼─────────────────┼──────────┼────────┼──────────────┼───────────┼─────────┼──────────┼─────────┤
│ 5              │ 2024-12-17T04:38:54.678Z │ fetch.backend: 1 │ fetch.client: 1 │          │ 2      │ 0            │ 1         │ 1       │ macro: 1 │ false   │
│                │                          │                  │                 │          │        │              │           │         │ sql: 1   │         │
├────────────────┼──────────────────────────┼──────────────────┼─────────────────┼──────────┼────────┼──────────────┼───────────┼─────────┼──────────┼─────────┤
│ 4              │ 2024-11-05T06:22:00.488Z │                  │ fetch.client: 1 │          │ 2      │ 0            │ 1         │ 1       │ macro: 1 │ false   │
├────────────────┼──────────────────────────┼──────────────────┼─────────────────┼──────────┼────────┼──────────────┼───────────┼─────────┼──────────┼─────────┤
│ 3              │ 2024-11-05T06:18:03.129Z │                  │                 │          │ 2      │ 0            │ 1         │ 0       │ macro: 1 │ false   │
├────────────────┼──────────────────────────┼──────────────────┼─────────────────┼──────────┼────────┼──────────────┼───────────┼─────────┼──────────┼─────────┤
│ 2              │ 2023-08-11T04:36:36.473Z │                  │                 │          │ 0      │ 0            │ 1         │ 0       │ macro: 1 │ false   │
├────────────────┼──────────────────────────┼──────────────────┼─────────────────┼──────────┼────────┼──────────────┼───────────┼─────────┼──────────┼─────────┤
│ 1              │ 2023-08-11T04:32:53.379Z │                  │                 │          │ 0      │ 0            │ 0         │ 0       │          │ false   │
└────────────────┴──────────────────────────┴──────────────────┴─────────────────┴──────────┴────────┴──────────────┴───────────┴─────────┴──────────┴─────────┘
```
```

Only the *latest version* of each major version is shown in the list. Some of the versions may not
have any installations linked to them as well.

### View major version details

Navigate to the app's top-level directory and check the details of what is included in a given major version by running:

```
```
1
2
```



```
forge version details --major-version [version]
```
```

The output should look similar to the following:

```
```
1
2
```



```
? Select option: Show all properties
✔ Getting app version details...

ℹ App [3] in [development] includes the following:

┌─────────────────┬───────────────────────────────────────────────────────────────────────────────┐
│ Property        │ Details                                                                       │
├─────────────────┼───────────────────────────────────────────────────────────────────────────────┤
│ analytics       │                                                                               │
├─────────────────┼───────────────────────────────────────────────────────────────────────────────┤
│ connect keys    │                                                                               │
├─────────────────┼───────────────────────────────────────────────────────────────────────────────┤
│ deployment date │ 2024-11-05T06:18:03.129Z                                                      │
├─────────────────┼───────────────────────────────────────────────────────────────────────────────┤
│ egress          │                                                                               │
├─────────────────┼───────────────────────────────────────────────────────────────────────────────┤
│ functions       │ - [main]: is configured with the following properties:                        │
│                 │   runtime: nodejs24.x                                                         │
│                 │   handler: index.run                                                          │
│                 │                                                                               │
├─────────────────┼───────────────────────────────────────────────────────────────────────────────┤
│ license         │ No                                                                            │
├─────────────────┼───────────────────────────────────────────────────────────────────────────────┤
│ modules         │ macro                                                                         │
│                 │ - [test-runtime-v2-hello-world]: is configured with the following properties: │
│                 │   title: test-runtime-v2                                                      │
│                 │   function: main                                                              │
│                 │   description: Inserts Hello world!                                           │
│                 │                                                                               │
├─────────────────┼───────────────────────────────────────────────────────────────────────────────┤
│ policies        │                                                                               │
├─────────────────┼───────────────────────────────────────────────────────────────────────────────┤
│ remotes         │                                                                               │
├─────────────────┼───────────────────────────────────────────────────────────────────────────────┤
│ scopes          │ - import:import-configuration:cmdb                                            │
│                 │ - read:servicedesk-request                                                    │
└─────────────────┴───────────────────────────────────────────────────────────────────────────────┘
```
```

The output should match the details that have been defined by the app developer in the manifest file.
However, how the details appear in the output may slightly differ to its manifest form.

### Compare major versions

Navigate to the app's top-level directory and compare two major versions by running:

```
```
1
2
```



```
forge version compare --version1 <version> --version2 <version>
```
```

The output should look similar to the following:

```
```
1
2
```



```
✔ Comparing app versions...

ℹ Comparison between app versions [3 and 5] in [development] is shown below:

┌─────────────────┬──────────────────────────────────────────────────┬──────────────────────────────────────────────────┐
│ Property        │ Version 1 [3]                                    │ Version 2 [5]                                    │
├─────────────────┼──────────────────────────────────────────────────┼──────────────────────────────────────────────────┤
│ analytics       │ []                                               │ [                                                │
│                 │                                                  │   {                                              │
│                 │                                                  │     "addresses": [                               │
│                 │                                                  │       "https://sentry.com"                       │
│                 │                                                  │     ],                                           │
│                 │                                                  │     "type": "fetch.client",                      │
│                 │                                                  │     "inScopeEUD": false                          │
│                 │                                                  │   }                                              │
│                 │                                                  │ ]                                                │
├─────────────────┼──────────────────────────────────────────────────┼──────────────────────────────────────────────────┤
│ deployment date │ "2024-11-05T06:18:03.129Z"                       │ "2024-12-17T04:38:54.678Z"                       │
├─────────────────┼──────────────────────────────────────────────────┼──────────────────────────────────────────────────┤
│ egress          │ []                                               │ [                                                │
│                 │                                                  │   {                                              │
│                 │                                                  │     "addresses": [                               │
│                 │                                                  │       "https://google.com"                       │
│                 │                                                  │     ],                                           │
│                 │                                                  │     "type": "fetch.backend"                      │
│                 │                                                  │   }                                              │
│                 │                                                  │ ]                                                │
├─────────────────┼──────────────────────────────────────────────────┼──────────────────────────────────────────────────┤
│ functions       │ [                                                │ [                                                │
│                 │   {                                              │   {                                              │
│                 │     "handler": "index.run",                      │     "handler": "index.run",                      │
│                 │     "key": "main",                               │     "key": "main",                               │
│                 │                                                  │                                                  │
│                 │     "runtimeName": "nodejs24.x"                  │     "runtimeName": "nodejs20.x"                  │
│                 │                                                  │                                                  │
│                 │   }                                              │   }                                              │
│                 │ ]                                                │ ]                                                │
├─────────────────┼──────────────────────────────────────────────────┼──────────────────────────────────────────────────┤
│ modules         │ [                                                │ [                                                │
│                 │   {                                              │   {                                              │
│                 │     "items": [                                   │     "items": [                                   │
│                 │       {                                          │       {                                          │
│                 │         "key": "test-runtime-v2-hello-world",    │         "key": "test-runtime-v2-hello-world",    │
│                 │         "properties": {                          │         "properties": {                          │
│                 │           "description": "Inserts Hello world!", │           "description": "Inserts Hello world!", │
│                 │           "function": "main",                    │           "function": "main",                    │
│                 │           "title": "test-runtime-v2"             │           "title": "test-runtime-v2"             │
│                 │         },                                       │         },                                       │
│                 │         "type": "xen:macro"                      │         "type": "xen:macro"                      │
│                 │       }                                          │       }                                          │
│                 │     ],                                           │     ],                                           │
│                 │     "type": "macro"                              │     "type": "macro"                              │
│                 │   },                                             │   },                                             │
│                 │                                                  │                                                  │
│                 │ ]                                                │   {                                              │
│                 │                                                  │     "items": [                                   │
│                 │                                                  │       {                                          │
│                 │                                                  │         "key": "test-sql-module",                │
│                 │                                                  │         "properties": {                          │
│                 │                                                  │           "dareCompliant": true,                 │
│                 │                                                  │           "engine": "mysql"                      │
│                 │                                                  │         },                                       │
│                 │                                                  │         "type": "core:sql"                       │
│                 │                                                  │       }                                          │
│                 │                                                  │     ],                                           │
│                 │                                                  │     "type": "sql"                                │
│                 │                                                  │   }                                              │
│                 │                                                  │                                                  │
│                 │                                                  │ ]                                                │
├─────────────────┼──────────────────────────────────────────────────┼──────────────────────────────────────────────────┤
│ remotes         │ []                                               │ [                                                │
│                 │                                                  │   {                                              │
│                 │                                                  │     "baseUrl": "https://backend.example.com",    │
│                 │                                                  │     "key": "remote-backend",                     │
│                 │                                                  │     "operations": [                              │
│                 │                                                  │       "fetch"                                    │
│                 │                                                  │     ]                                            │
│                 │                                                  │   }                                              │
│                 │                                                  │ ]                                                │
└─────────────────┴──────────────────────────────────────────────────┴──────────────────────────────────────────────────┘
```
```

## Major version upgrades

Major version upgrades are not applied to an app installation immediately. This is because
major versions involve significant changes that may require users and admins to re-consent or
review the changes before continuing.

Not all permission changes trigger a major version upgrade. Only changes that require user consent,
such as OAuth scopes and Atlassian app permissions, result in a major version change.

The following `manifest.yml` file changes are considered major version upgrades:

* Modifying [scope permissions](/platform/forge/manifest-reference/permissions/#oauth-2-scopes). This includes:
  * Adding a scope.
  * Swapping a scope for one not already listed.
  * Removing a scope.
* Modifying [content permissions](/platform/forge/manifest-reference/permissions/#content-permissions) CSP options. This includes:
  * Adding a CSP option.
  * Swapping a CSP option for one not already listed.
* Modifying [external permissions](/platform/forge/manifest-reference/permissions/#external-permissions) CSP options and URLs. This includes:
  * Adding a CSP option or URL.
  * Swapping a CSP option or URL for one not already listed.
* Adding or modifying [web trigger](/platform/forge/manifest-reference/modules/web-trigger) module functions. This includes:
  * Adding a new `dynamic` web trigger.
  * Modifying a `static` web trigger to `dynamic`.
* Adding or modifying the category of an existing [egress permission](/platform/forge/manifest-reference/permissions#egress-permissions).
* Modifying `inScopeEUD` from `false` to `true` for an
  [egress permission](/platform/forge/manifest-reference/permissions#egress-permissions) element for
  the first time.
* Enabling [licensing](/platform/marketplace/listing-forge-apps/#enabling-licensing-for-your-app):
  * Enabling licensing creates a new version that requires approval of the Marketplace listing, making it a major version upgrade.
* Adding or removing [providers](/platform/forge/manifest-reference/providers/).
* Changing a provider [client ID](/platform/forge/manifest-reference/providers/#authentication).
* In most cases, updating your app's remote backends will result in a new major version. See the
  [Remotes](/platform/forge/manifest-reference/remotes/) reference for details on which changes result in
  [major](/platform/forge/manifest-reference/remotes/#major-version-upgrades) and
  [minor](/platform/forge/manifest-reference/remotes/#minor-upgrades) versions.

You can use the [Forge CLI](/platform/forge/cli-reference/) to complete a major upgrade with `forge install --upgrade`.
Site admins can select **upgrade** from the manage apps screen to complete the app upgrade.

You can also use the Forge CLI to conduct a [bulk upgrade](/platform/forge/distribute-your-apps/#distributing-an-update-across-app-installations--preview-) of major versions across multiple installations at once without admin approval, where there has not been an elevation of privilege.

## Minor version upgrades

Forge creates a new minor version whenever you deploy app changes that don’t result in a new
major version. You can apply minor version updates to any major version, even older ones.

Unlike major versions, minor version upgrades do not require admin consent. When you deploy
a new minor version, Forge automatically installs it to all sites running the same major version.
This means that every site is always running the latest minor version of each app’s major version.

## Installing previous major versions

To support upgrade and migration testing, you can install a previous major version of your app using the Forge CLI. This is useful for reproducing customer issues, validating migration paths, or rolling forward/backward during development.

You must first uninstall the current version of your app before installing a previous major version. Use `forge uninstall` to remove the current installation.

### CLI command

Use the `--major-version` flag to specify which major version to install:

```
```
1
2
```



```
forge install --site https://example.atlassian.net --product jira --major-version 2
```
```

### Non-interactive mode

For scripting or CI/CD, you can use `--non-interactive` to bypass prompts:

```
```
1
2
```



```
forge install --site https://example.atlassian.net --product jira --major-version 2 --environment development --non-interactive
```
```

## Examples

The property `inScopeEUD` determines whether or not an app is compliant with data residency, as well as
whether or not an app is eligible for [Runs on Atlassian](/platform/forge/runs-on-atlassian/).

The examples below show different scenarios involving changes to `inScopeEUD` and how such changes
could result in either a major or a minor version upgrade.

### Example 1: Major version upgrade

This example shows a change to the `inScopeEUD` value, which is from `false` to `true`.
This change leads to a major version upgrade.

```
```
1
2
```



```
permissions:
  external:
    fetch:
      backend:
        - address: '*.example-dev.com'
          category: analytics
          inScopeEUD: true # inScopeEUD value was previously false
```
```

### Example 2: Major version upgrade

This example shows a change to one of the `inScopeEUD` values, from `false` to `true`, where in the
previous version of the app, all `inScopeEUD` values were `false`. This change leads to a
major version upgrade.

```
```
1
2
```



```
permissions:
  external:
    fetch:
      backend:
        - address: '*.example-dev.com'
          category: analytics
          inScopeEUD: true # inScopeEUD value was previously false, with all values previously false
        - address: '*.example-prod.com'
          category: analytics
          inScopeEUD: false # no change in value
```
```

### Example 3: Minor version upgrade

This example shows a change to one of the `inScopeEUD` values, from `false` to `true`, where in the
previous version of the app, there is already an existing `inScopeEUD` value that's set to `true`.
Because the previous version is already egressing in-scope End-User data, this change only leads
to a minor version upgrade.

```
```
1
2
```



```
permissions:
  external:
    fetch:
      backend:
        - address: '*.example-dev.com'
          category: analytics
          inScopeEUD: true # no change in value
        - address: '*.example-prod.com'
          category: analytics
          inScopeEUD: true # inScopeEUD value was previously false
```
```

## Backporting

In some cases, a site admin can’t or won’t upgrade from an older major version of your app. You can
still backport `minor version upgrades` to their app. When you do, Forge will automatically apply that
minor version upgrade to all sites running the same major version.

To do this, use the `--major-version` option:

```
```
1
2
```



```
forge deploy --major-version [version] --verbose
```
```

The `--verbose` option will provide you with more useful details about any deployment errors. These
details include whether your attempted deployment would have resulted in a new major version.

#### Limitations

* Any manifest file changes relating to
  [Custom Entities](/platform/forge/runtime-reference/custom-entities/)
  cannot be backported. When you use the `--major-version`, the `forge deploy`
  command will ignore the `storage` section of your manifest file.
* Due to a restriction in the Marketplace, the Version management screen displays only up to 9 backports for any single major version.
