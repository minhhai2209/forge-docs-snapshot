# Example apps for Compass

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

## Compass details app with UI Kit

Displays details about various Compass entities on pages in the Compass component side navigation

* **Code:** [Component details repository](https://bitbucket.org/atlassian/forge-ui-kit-compass-component-details/src/main/)
* **Atlassian app:** Compass
* **Modules:** `compass:adminPage`, `compass:componentPage`, `compass:teamPage`
* **Custom UI:** none
* **UI Kit:**
  * `Text`, `DynamicTable`, `Spinner` and `Code` components
  * `useProductContext` hook
* **Other:**

## Compass web trigger app with UI Kit

Creates a web trigger to receive and display a message of the day on the Compass admin page for the app.

* **Code:** [Web trigger repository](https://bitbucket.org/atlassian/forge-compass-webtrigger-ui-kit/)
* **Atlassian app:** Compass
* **Modules:** `webtrigger`, `compass:adminPage`
* **Custom UI:** none
* **UI Kit:**
  * `CodeBlock`, `Heading`, `Stack`, and `Text` components.
  * `useState` and `useEffect` hooks from `react` library.
  * `webTrigger` and `storage` APIs.
* **Other:**

## Compass metrics and events ingestor app with Custom UI

Demonstrates a basic admin page skeleton for requesting API credentials.
Uses the `dataProvider` module and webtriggers to set up and ingest metrics and events on a Compass component.
