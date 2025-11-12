# App compatibility

App compatibility defines which Atlassian apps and platform experiences your Forge app can work with.

This page explains the different possibilities for Forge app compatibility and how to declare the
compatibility of your app.

## Single-app compatibility

If your Forge app is designed to work with only one Atlassian app, you do not need to declare
compatibility in your app’s manifest. In this case, your app will only be available for installation
in that specific Atlassian app.

If you list your app on the Atlassian Marketplace, it will appear as compatible only with the Atlassian
app you built it for. Users will only be able to install your app into this particular Atlassian app.

For example, a Forge app that is designed to only work with Confluence does not require any compatibility
declaration in the manifest. You can simply build your app using Confluence modules and call Confluence APIs as
needed. If published on the Atlassian Marketplace, it will only be available for installation in Confluence.

### Example manifest

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
modules:
  macro:
    - key: hello-world-app-hello-world
      resource: main
      render: native
      resolver:
        function: resolver
      title: Forge app for Mia
      description: Inserts hello world!
  function:
    - key: resolver
      handler: index.handler
resources:
  - key: main
    path: src/frontend/index.jsx
app:
  id: '<app id>'
```

### Tutorials

To learn how to build an Forge app that is compatible with only one Atlassian app, check out these
tutorials:

## Multiple-app compatibility (Preview)

The ability to build Forge apps that are compatible with multiple Atlassian apps is now available as a Forge *preview* feature. Preview features are deemed stable; however, they remain under active development and may be subject to shorter deprecation windows. Preview features are suitable for early adopters in production environments.

The following flows are ready for testing as part of this Preview:

* Create, deploy and install an app via the CLI
* Distribute the app via a direct distribution link
* View and connect/disconnect compatible Atlassian apps in Connected Apps
* Add the app to Marketplace

**Important considerations:**

* **Customer release (GA)** is planned for end of January 2025.
* **Until GA:** We recommend keeping Marketplace apps **private** as customer-facing changes are not yet available (admins currently only see the required app in the consent screen when installing).
* **Migrating existing apps:** See our [migration guidelines](/platform/forge/migrating-a-forge-app-to-support-multiple-atlassian-apps/) for best practices.

For more information, see [Forge EAP, Preview, and GA](/platform/forge/whats-coming/#eap).

If your Forge app is designed to work with more than one Atlassian app, you must declare
compatibility in your app’s `manifest.yml` file. This allows your app to be installed and used
in each of the specified Atlassian apps.

This functionality is currently in Preview and only supports a limited set of Atlassian apps. The
supported Atlassian apps are:

This means you can create a Forge app that uses modules and calls APIs across any combination of
Jira, Confluence, and Compass. Note that apps with multiple-app compatibility are still restricted
to a single site. You cannot build Forge apps that work across multiple sites.

### Required and optional Atlassian apps

When building a Forge app that is compatible with multiple Atlassian apps, you need to define
which Atlassian apps are required and which are optional in the `manifest.yml` file.
This determines where admins can install and connect your app.

* **Required Atlassian app**: Every Forge app must have one required Atlassian app. That is,
  one Atlassian app where the app must be deployed and installed in before it can be connected to other
  Atlassian apps.
* **Optional Atlassian apps**: These are the additional Atlassian apps that your app is compatible with.
  Your app can support as many optional Atlassian apps as you'd like, and it can be connected to those
  optional Atlassian apps after it has been installed in the required Atlassian app.

The installation ID of your app is shared across both the required and optional Atlassian apps. In
the manifest, the app's compatibility is defined under `app`:

```
```
1
2
```



```
app:
  id: '<app id>'
  compatibility:
    confluence:
      required: true
    jira:
      required: false
```
```

#### Storage and Data Residency

The required Atlassian app is significant for storage and data residency.

For app data stored in Forge Storage, data from all optional Atlassian apps
will be associated with the pinned location of the required Atlassian app. For example, if the required
Atlassian app is pinned to Australia and the other optional Atlassian app is pinned to Europe,
all data will be stored in Australia.

Additionally, the [data residency](/platform/forge/data-residency/) status of the app depends on the required Atlassian app.

The required Atlassian app governs the processes of installation, upgrade, and uninstallation, as well as
the app's storage and Data Residency posture.
Consequently, when your app is uninstalled from the required Atlassian app, it will also be uninstalled from all
optional Atlassian apps.

### Example manifest

This manifest defines Confluence as the required Atlassian app and Jira as optional.

```
```
1
2
```



```
modules:
  macro:
    - key: hello-world-app-hello-world
      resource: main
      render: native
      resolver:
        function: resolver
      title: Forge app for Mia
      description: Inserts hello world!
  jira:issuePanel:
    - key: hello-world-hello-world-issue-panel
      resource: main
      resolver:
        function: resolver
      render: native
      title: Forge app for Mia
      icon: https://developer.atlassian.com/platform/forge/images/icons/issue-panel-icon.svg
  function:
    - key: resolver
      handler: index.handler
resources:
  - key: main
    path: src/frontend/index.jsx
app:
  id: <your app id>
  # required and optional Atlassian apps added here:
  compatibility:
    confluence:
      required: true
    jira:
      required: false
```
```

### Tutorials

To learn how to build an Forge app that is compatible with multiple Atlassian apps, or to change
the compatibility of an existing app, check out these tutorials:

### FAQs

| Question | Answer |
| --- | --- |
| Once I have added support for more Atlassian apps, can I change my app back to only support one Atlassian app? | This is possible if the app has no existing installations. |
| Can I change the required Atlassian app? | You can only change or remove the required Atlassian app if the app has no existing installations. |
| Is adding or removing a required Atlassian app a major version change? | No. Any changes to the required Atlassian app is a minor version change unless elevated permissions or egress are added. |
| Can I have more than one required Atlassian app? | No. You can only have one required Atlassian app, which is defined in the `manifest.yml` file. |
