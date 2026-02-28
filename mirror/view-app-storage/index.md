# View app storage

App storage lets you view the [storage](/platform/forge/storage/) usage of a Forge app across
development and staging environments of a site where the app is installed. Storage information
is accessible to app admins and contributors on the developer console if an app is storing data
using the [app storage API](/platform/forge/storage/#app-storage).

To view app storage:

1. Access the [developer console](/console/myapps).
2. In the left menu, select **Storage**.
3. Select the relevant **site** where the app is installed.
4. Select the relevant **environment**.

The screen shows the storage usage of an app for a selected site.

![Storage usage for a selected site](https://dac-static.atlassian.com/platform/forge/images/storage-screen.svg?_v=1.5800.1881)

### Storage usage

You can view both **unencrypted** and **encrypted** storage that an app is using per environment per site
where the app is installed:

* **Unencrypted storage usage**: Displays the total size of unencrypted data that the app is storing
  for a selected site.
* **Encrypted storage usage**: Displays the total size of encrypted data that the app is storing
  for a selected site. Encrypted data usually takes up more space than unencrypted data since
  each data point is encrypted separately.

### Unencrypted storage data

The table contains a list of the keys and values used in unencrypted storage:

### Filters

Use these filters to refine your storage:

* **Site**: Narrows down storage usage based on the site where your app is installed,
  for example `https://your-domain.atlassian.net`.

  You can't filter by Atlassian app. For example, you can't narrow down storage usage just for Jira
  instances on a particular site.
* **Environment**: Narrows down the storage for a specific app environment for your Forge app.

Unencrypted storage is shown for the selected environment of a selected site. To see the unencrypted
storage usage of another site, select the site and the corresponding environment.

### Limitations

The storage access functionality in the developer console is an evolving feature. We're exploring
ways to improve and overcome the following limitations:

* Storage filters don't allow for multi-select.
* Encrypted storage cannot be accessed.
* Unencrypted storage does not show data for production environment.
* Data and usage from custom entity store cannot be viewed in the developer console.
