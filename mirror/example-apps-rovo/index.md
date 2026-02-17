# Example apps for Rovo

Before you begin exploring these example apps, you'll need to set up the Forge CLI first.
[Learn more about getting started](/platform/forge/getting-started/).

Once the Forge CLI is up and running, clone an example app repository to explore and customize it locally.
Each repository's `README.md` file contains quickstart instructions and other details about the app.

For more information, refer to our getting started guides for building
[Confluence](/platform/forge/build-a-hello-world-app-in-confluence/)
and [Jira](/platform/forge/build-a-hello-world-app-in-jira/) apps.

The `forge register` command creates a unique app ID in the `manifest.yml` file
and links the ID to the current developer. Forge apps can currently only be deployed
and installed by the developer who is linked to the app.

The content on this page is written with standard cloud development in mind. To learn about developing
for Atlassian Government Cloud, go to our
[Atlassian Government Cloud developer portal](/platform/framework/agc/).

## Jira issue analyst

A Forge Rovo Agent app, Jira issue analyst that uses [Rovo Agent](/platform/forge/manifest-reference/modules/rovo-agent/) and [Action](/platform/forge/manifest-reference/modules/rovo-action) modules to help support and engineering teams analyze issue queues effectively.

To see this app in action, watch this video

### Details

## Question and answer creator

A Forge Rovo Agent app, Question and answer creator that uses Confluence page through the [Rovo Agent](/platform/forge/manifest-reference/modules/rovo-agent/) and [Action](/platform/forge/manifest-reference/modules/rovo-action) modules.

### Details

* **Code**: [Forge Q&A Creator](https://bitbucket.org/atlassian/forge-q-and-a-creator/src/main/)
* **Atlassian app**: Confluence
* **Modules**:
* **UI Kit**:
  * `Heading`, `Inline`, `Label`, `ProgressBar`, `Stack`, `Strong`, `Text`,`Toggle`
* **Runtime**: `@forge/resolver`, `@forge/api`

## Weather forecaster

A Forge Rovo Agent app, Weather forecaster that uses Confluence page through the [Rovo Agent](/platform/forge/manifest-reference/modules/rovo-agent/) and [Action](/platform/forge/manifest-reference/modules/rovo-action) modules.

### Details
