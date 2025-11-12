# Storage

Forge apps can store, retrieve, and delete data in Atlassian's cloud, either through
Forge hosted storage or through each Atlassian app.

## Forge hosted storage

Forge provides several options for persistent hosted storage. Each option provide data residency features that allow admins to control
where app data is hosted (see [Data residency](/platform/forge/data-residency/) for more information).

See [Storage overview](/platform/forge/runtime-reference/storage-api/) for more information about these options.

### Data recovery for apps with hosted storage

When a customer reinstalls an app that uses Forge hosted storage, data from the previous installation is not automatically restored. Forge hosted storage retains data for 28 days after uninstallation.

To recover this data for a customer, app developers must:

To submit a recovery request, raise a bug ticket on [Developer Support](https://developer.atlassian.com/support). Use **Re-linking reinstallation data** as the summary, and include the following in your request:

* Customer details
* Site ID
* Installation ID

See [Data lifecycle for Forge-hosted storage](/platform/forge/storage-reference/hosted-storage-data-lifecycle/) for related details.

## Atlassian app REST APIs

Forge can also use Atlassian app-specific APIs to store and retrieve data for Atlassian Cloud sites and workspaces. This data is accessible to all apps installed within the site (as well as users). See [Atlassian app REST APIs](/platform/forge/apis-reference/product-rest-api-reference/) for more details.

## Remote storage

Using the capabilities discussed in this section may make your app *not* eligible for **Runs on Atlassian**.

Go to [this page](/platform/forge/runs-on-atlassian/) to know more about the Runs on Atlassian program. To know how to check if your app is eligible for Runs on Atlassian, go to the
[Forge CLI documentation](/platform/forge/cli-reference/eligibility/).

Forge also lets you integrate your app with services hosted on other platforms. This allows Forge apps to
store data remotely on self-hosted databases or third-party storage services. For more information about
integrating with remote services, see [Forge Remote](/platform/forge/remote/).
