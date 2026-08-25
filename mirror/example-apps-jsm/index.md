# Example apps for Jira Service Management

Before you begin exploring these example apps, you'll need to set up the Forge CLI first.
[Learn more about getting started](/platform/forge/getting-started/).

Once the Forge CLI is up and running, clone an example app repository to explore and customize it locally.
Each repository's `README.md` file contains quickstart instructions and other details about the app.

For more information, refer to our getting started guides for building
[Bitbucket](/platform/forge/build-a-hello-world-app-in-bitbucket/),
[Confluence](/platform/forge/build-a-hello-world-app-in-confluence/),
[Jira](/platform/forge/build-a-hello-world-app-in-jira/),
and [Jira Service Management](/platform/forge/build-a-hello-world-app-in-jira-service-management/) apps.
Our [tutorials](/platform/forge/tutorials-and-guides/) and [guides](/platform/forge/guides/)
also offer useful information for common tasks.

The `forge register` command creates a unique app ID in the `manifest.yml` file
and links the ID to the current developer. Forge apps can currently only be deployed
and installed by the developer who is linked to the app.

The content on this page is written with standard cloud development in mind. To learn about developing
for Atlassian Government Cloud, go to our
[Atlassian Government Cloud developer portal](/platform/framework/agc/).

## Recent requests app

Displays the five latest user requests in the [Jira Service Management customer portal request](https://developer.atlassian.com/platform/forge/ui-kit-components/jira-service-management/portal-request-detail-panel/).

### Details

* **Code:** [Recent requests repository](https://bitbucket.org/atlassian/forge-ui-kit-jsm-recent-requests/src/main)
* **Atlassian app:** Jira Service Management
* **Modules:** `jiraServiceManagement:portalRequestDetailPanel`
* **Custom UI:** none
* **UI Kit:**
  * `DynamicTable`, `Spinner`, `Text`, `Link` components
  * `useProductContext` hooks
