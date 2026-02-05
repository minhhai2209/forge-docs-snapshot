# Migrating a Forge app to support multiple Atlassian apps

You can migrate an existing Forge app that supports only one Atlassian app to support multiple
Atlassian apps. This enables your app to be installed and used across Atlassian apps within the same
site. For more information, see [App compatibility](/platform/forge/app-compatibility).

Migrating your app to support multiple Atlassian apps involves updating your app’s manifest,
redeploying your app, and communicating changes to your users. This guide covers:

* Requirements and limitations
* Steps to add support for additional Atlassian apps
* Versioning and permission considerations
* Customer communication and data migration caveats
* Frequently asked questions

## Requirements and limitations

Once an app supports more than one Atlassian app, it cannot be migrated back to only supporting a
single Atlassian app whilst there are existing installations.

To add support for additional Atlassian apps to your existing app, it must meet the following requirements:

* **The app must be a Forge app.** Connect apps, including apps with a Forge manifest that still use
  Connect modules or contain a Connect key, are not eligible.
* **The app must not have any existing installations in non-required Atlassian apps.** For example, if your
  app only has active installations in Confluence, you will be able to set Confluence as required.
  However, if your app has active installations in Confluence and you would like to set Jira as
  required, your app must be uninstalled from Confluence before Jira can be declared in the manifest as
  the required Atlassian app.
* **The app must only be compatible with eligible Atlassian apps.** During Preview, the eligible
  Atlassian apps are Jira, Confluence, and Compass. Only Jira or Confluence can be the required Atlassian app;
  Compass can only be configured as an optional Atlassian app.
* **If listed on Marketplace, the app must be a paid app.** Forge apps that are compatible with
  multiple Atlassian apps can only be listed as paid apps; free listings are not supported.

## Versioning and permissions changes

The following table outlines the versioning impacts when making changes to your app. Generally, adding
support for additional Atlassian apps is a minor version change unless elevated permissions or egress are added.

| Change | Situation | Is a major version update required? | Example manifest change |
| --- | --- | --- | --- |
| **Add a required Atlassian app** | A developer decides to change their Jira app to support multiple Atlassian apps, with Jira as the required Atlassian app. | No, as long as no new scopes are added | ```  ``` 1 2 ```    ``` compatibility:   jira:     required: true ``` ``` |
| **Add an optional Atlassian app** | A developer wants to allow their app to be optionally connected to Confluence, in addition to the required app. | No, as long as no new scopes are added | ```  ``` 1 2 ```    ``` compatibility:   confluence:     required: false ``` ``` |
| **Add new permissions (scopes) or egress** | A developer adds new permissions or egress to their app, such as requesting additional API scopes. | Yes | ```  ``` 1 2 ```    ``` permissions:   scopes:     - storage:app     - read:app-system-token ``` ``` |
| **Add an optional Atlassian app *and* new permissions for that Atlassian app** | A developer adds Compass as an optional Atlassian app and also requests new permissions for Compass APIs. | Yes | ```  ``` 1 2 ```    ``` compatibility:   compass:     required: false permissions:   scopes:     - read:event:compass ``` ``` |
| **Remove an optional Atlassian app** | A developer removes Confluence as an optional Atlassian app from their app. | No | ```  ``` 1 2 ```    ``` compatibility:   confluence: (removed) ``` ``` |
| **Change the required Atlassian app** | A developer wants to change which Atlassian app is required. For example, making Jira required when previously, Confluence was required.  This is only possible if there are no existing installations. | No | ```  ``` 1 2 ```    ``` compatibility:   jira:     required: true   confluence:     required: false ``` ``` |
| **Revert to single-app compatibility** | A developer wants to revert their app to support only one Atlassian app.  This is only possible if there are no existing installations. | No | ```  ``` 1 2 ```    ``` compatibility:   jira:     required: true ``` ``` |

## Migration steps

### Before you begin

Before you begin, you will need to ensure you are using
the latest `@forge/cli` version.

To install, run:

```
```
1
2
```



```
npm install -g @forge/cli@latest
```
```

To make cross-Atlassian app storage calls, you will also need to ensure you are using the latest `@forge/api` version,
[version 5.1.1](https://www.npmjs.com/package/@forge/api/v/5.1.1?activeTab=code).

### Steps

To add support for additional Atlassian apps to your Forge app:

1. Add the `compatibility` property under `app` in the `manifest.yml` file and declare the required and
   optional Atlassian apps:

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
2. Navigate to the app's top-level directory and deploy your app by running:
3. Install your app by running:
4. Enter the URL for your development site. For example, *example.atlassian.net*.
   [View a list of your active sites at Atlassian administration](https://admin.atlassian.com/).
5. Your app will now automatically be installed into the required Atlassian app.
6. To install your app in other Atlassian apps, you can run the `forge install` command again and select
   your app's other supported Atlassian apps.

Once the successful installation message appears, your app is installed and ready to use on the
specified site. You can always uninstall your app from the site by running the `forge uninstall` command.

When uninstalling, you **must** uninstall your app from all optional Atlassian apps before you can uninstall it from the required Atlassian app.

### Example

Below is an example manifest of a Confluence hello world app:

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
  function:
    - key: resolver
      handler: index.handler
resources:
  - key: main
    path: src/frontend/index.jsx
app:
  id: '<app id>'
```
```

Below is what that same example app manifest would look like once Jira is added as a optional Atlassian app:

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

## Managing migration and customer communication

### Migrating to multi-app compatibility

When you update your Forge app to support multiple Atlassian apps (for example, adding Confluence
and Compass as optional Atlassian apps to an existing Jira app):

* **Existing installations remain:** All existing installations of your app in the original Atlassian
  app (in this case, Jira) will remain in place. You would set Jira as the required Atlassian app,
  and users can continue using the app and their data as before.
* **No disruption to users:** Admins do not need to reinstall or reconnect the app in the required
  Atlassian app. Their data and app functionality are preserved.
* **Optional Atlassian apps:** The app can be optionally installed in additional Atlassian apps
  (e.g., Confluence, Compass), but these are not connected by default. Admins can choose to connect
  the app to these new Atlassian apps when ready via Atlassian Administration.

### Combining or merging multiple apps

If you have separate apps for different Atlassian apps (for example, a Jira app, a Confluence app,
and a Compass app) and want to merge them into a single multi-app compatible app:

* **No automatic data migration:** Data from the old, separate apps will not be automatically migrated
  to your new app. Each app’s data remains unless you provide a manual migration path.
* **User action required:** Users will need to manually migrate any data they wish to retain from
  the old apps to the new app, if your app supports this.
* **Communicate clearly:** Partners should inform users about which app will become the main app
  (the required Atlassian app), which apps will be sunset, and provide clear instructions for
  any manual data migration and uninstalling old apps.

For example, if you merge existing Confluence and Compass apps into an existing Jira app (making Jira required
and Confluence and Compass optional), users will need to:

* Install the new app, if they only had the Confluence or Compass app, or connect the app in Confluence
  and Compass if they already have the Jira app.
* Manually migrate any data they need from the old Confluence and Compass apps, if supported.
* Uninstall the old Confluence and Compass apps once migration is complete.

### Guidance for customer communication

* **Announce the change:** Notify users in advance about the migration and what it means for their
  data and app usage.
* **Explain data handling:** Make it clear that data in the required Atlassian app remains unchanged,
  but data from other (now optional) contexts or merged apps will not be automatically migrated.
* **Provide migration steps:** If manual data migration is possible, provide clear, step-by-step instructions.
* **Provide guidance on uninstalling old apps:** Advise users to uninstall old, now-redundant apps
  after connecting and migrating to the new app if applicable.
