# Example apps for Jira

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

## Issue translator app with UI Kit

Adds a [Jira issue panel](/platform/forge/manifest-reference/modules/jira-issue-panel/) module that translates the contents of an issue into a range of different languages using the [Azure Translator Text API](https://docs.microsoft.com/en-us/azure/cognitive-services/translator/).

### Details

* **Code:** [Issue translator repository](https://bitbucket.org/atlassian/forge-ui-kit-2-translate/src/main/)
* **Atlassian app:** Jira
* **Modules:** `jira:issuePanel`
* **Custom UI:** `@forge/bridge`
* **UI Kit:**
  * `Button`, `ButtonSet`, `Strong` and `Text` components from `@forge/react` library
  * `Fragment`, `useEffect` and `useState` component and hooks from `react` library
* **Runtime:**: `@forge/resolver` and `@forge/api`
* **Other:**
  * Translates the Jira summary and description fields using Azure Translator Text API
  * Uses secure environment variables for Azure API authentication tokens.

## Jira project stats app with UI Kit

Displays Jira project stats in a pie chart and allows for the export of issue data as a `.json` file.
The app adds the items 'Show stats' and 'Export issue data' to the more actions (•••) menu of the
Jira board and backlog views.

### Details

* **Code:** [Jira project stats app repository](https://bitbucket.org/atlassian/jira-project-stats-app/)
* **Atlassian app:** Jira
* **Modules:** `jira:backlogAction` and `jira:boardAction`
* **Custom UI:** none
* **UI Kit:**
  * `Inline`, `PieChart`, `SingleValueChart`, `Spinner`, `Stack`, `Text` and `useProductContext` components and hooks from `@forge/react` library
  * `useEffect`, `useRef` and `useState` component and hooks from `react` library
  * `requestJira`, `showFlag` and `useRef` APIs from `@forge/bridge` library
* **Runtime:** none

## Project introduction app with UI Kit

The app displays a summary of the project's objective and milestones using [Jira Global page](/platform/forge/manifest-reference/modules/jira-global-page/) module.

### Details

## Todo app with Custom UI

Adds a simple todo list to a Jira issue for simple tasks that do not require a description, tracking, or workflow.

### Details

* **Code:** [Todo repository](https://bitbucket.org/atlassian/todo-app-custom-ui/)
* **Atlassian app:** Jira
* **Modules:** `jira:issuePanel`
* **Custom UI:** Use of resources, resolvers, and bridge.
* **Other:**
  * Implements a set of backend resolver functions for Custom UI to communicate with a Faas backend.
  * Uses a combination of Atlaskit and custom styled components

## UI modifications with Custom UI

This app serves as an end-to-end example of how to write and use UI modifications in Jira Cloud.

### Details

* **Code:** [Jira UI modifications](https://bitbucket.org/atlassian/forge-ui-modifications-example/)
* **Atlassian app:** Jira
* **Modules:** `jira:uiModifications` and `jira:adminPage`
* **Custom UI:** Use of `@forge/jira-bridge`
* **Other:**
  * Uses REST endpoints to assign UI modification entities to specific contexts.
  * Uses [react-router@^6.2](https://reactrouter.com/) to handle each subpage route.

## JQL editor app with Custom UI

Adds a JQL editor to any Jira project page. This editor visualizes the statuses of all issues matching a query.

### Details

* **Code:** [JQL editor repository](https://bitbucket.org/atlassian/forge-jql-editor-custom-ui/)
* **Atlassian app:** Jira
* **Modules:** `jira:projectPage`
* **Custom UI:** `@forge/bridge`
* **Other:**

## JQL function - subtaskOf()

Adds a JQL function that allows you to search for issues that are subtasks of the issues returned by the query passed as an argument.

### Details
