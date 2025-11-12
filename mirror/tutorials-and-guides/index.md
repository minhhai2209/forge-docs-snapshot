# Tutorials and Guides

Work through these tutorials to learn more about developing on Forge.

### Automate Jira with triggers

This tutorial describes how to create a Forge app, and install it in a Jira Cloud site. The app
responds to issue created events in Jira and adds a comment to the created issue. You'll learn about
Atlassian app events, the runtime API, and tunneling.

See [Automate Jira using triggers](/platform/forge/automate-jira-using-triggers/).

### Incrementally adopting Forge from Connect

This documentation describes how to adopt Forge modules while keeping your existing Connect app functioning, allowing you to incrementally adopt Forge from Connect.

See [Adopting Forge from Connect](/platform/adopting-forge-from-connect/).

### Set up continuous delivery for Forge apps

This tutorial describes how to create a continuous delivery workflow for your Forge app (which you could later
integrate into a CI/CD pipeline). It includes a reference Bitbucket Cloud pipeline configuration for a hello world app built
in Forge. It also includes general guidance for GitHub users.

See [Set up continuous delivery for Forge apps](/platform/forge/set-up-cicd/)

### Build a Custom UI app in Confluence

This tutorial walks you through creating a Forge app that displays Custom UI content on a Confluence
page. Using Custom UI, you can define your own user interface using static resources, such as HTML,
CSS, JavaScript, and images. The Forge platform hosts your static resources, enabling your app
to display custom UI on Atlassian apps. Custom UI apps inherit modern security features to ensure
high trust between Atlassian, developers, and users.

You’ll learn how to create a Forge app in Confluence that uses Custom UI to display customized UI content.

See [Build a Custom UI app in Confluence](/platform/forge/build-a-custom-ui-app-in-confluence/).

### Build a Custom UI app in Jira

This tutorial walks you through creating a Forge app that displays Custom UI content in a Jira issue.
Using Custom UI, you can define your own user interface using static resources, such as HTML, CSS,
JavaScript, and images. The Forge platform hosts your static resources, enabling your app to
display custom UI on Atlassian apps. Custom UI apps inherit modern security features to ensure
high trust between Atlassian, developers, and users.

You’ll learn how to create a Forge app in Jira that uses Custom UI to display customized UI content.

See [Build a Custom UI app in Jira](/platform/forge/build-a-custom-ui-app-in-jira/).

### Build a Custom UI app in Jira Service Management

This tutorial walks through creating a Forge app to display content on the queues page of Jira Service Management.
Using Custom UI, you can define your own user interface using static resources, such as HTML, CSS,
JavaScript, and images. The Forge platform hosts your static resources, enabling your app to
display custom UI on Atlassian apps. Custom UI apps inherit modern security features to ensure
high trust between Atlassian, developers, and users.

You’ll learn how to create a Forge app in Jira Service Management that uses Custom UI to display customized UI content.

See [Build a Custom UI app in Jira Service Management](/platform/forge/build-a-custom-ui-app-in-jira-service-management/)

### Check whether Jira issues are assigned using a workflow validator

This tutorial describes how to create a Forge app that checks whether Jira issues are assigned when
transitioned. You'll learn how to use the Jira workflow validator module, and how to retrieve
issue details from the Jira REST API.

See [Check whether Jira issues are assigned using a workflow validator](/platform/forge/check-jira-issues-assigned-using-workflow-validator/).

### Use content actions to count the macros in a Confluence page

This tutorial describes how to create a Forge app that displays the number of macros in a Confluence
page. The app retrieves the body of the page, counts the number of macros, then displays the result
in a modal dialog. A user triggers the action from an entry in the more actions (...) menu.

See [Use content actions to count the macros in a Confluence page](/platform/forge/macros-in-the-page/).

### Use highlighted text in a Confluence Forge app

This tutorial describes how to make a Forge app that uses highlighted text from a Confluence page. You'll learn about the Forge [confluence:contextMenu](/platform/forge/manifest-reference/modules/confluence-context-menu) module, and how to output a selected text inside the app.

See [Use highlighted text in a Confluence Forge app](/platform/forge/create-confluence-contextmenu-module/).

### Use space settings and content byline item to implement space news

This tutorial describes how to create a Forge app with two modules, where an admin can create news content using `spaceSettings` module, and make the news content available using `contentBylineItem`.

See [Use space settings and content byline item to implement space news](/platform/forge/space-news/).

### Use the app storage API in a Confluence macro

This tutorial describes how to build Forge app that can display a list of acronyms
and associated definitions in a Confluence macro. Definitions for the acronyms are
stored within the app storage service and shared with other macros across the whole
Confluence site. You'll learn about using the storage API from a Forge function and
how to integrate storage with a UI Kit app.

See [Use the app storage API in a Confluence macro](/platform/forge/create-confluence-macro-with-storage-api)

### Use an external OAuth 2.0 API with fetch

This tutorial describes how to call an external API using the Forge
`fetch` function with OAuth 2.0 authentication handled by the Forge platform.

See [Use an external OAuth 2.0 API with fetch](/platform/forge/use-an-external-oauth-2.0-api-with-fetch/).

### Import Third Party data into Assets with Forge app

This tutorial describes how to create a Forge app that allows you to import third party data into Assets.
The app allows you to trigger actions from certain actions in the UI such as creating and deleting an import, starting and stopping an import.
Also uses the underlying Imports REST API to send data into Assets.

See [Import Third Party data into Assets](/platform/forge/assets-import-app/).

## Guides

The guides section provides quick references for common tasks when working with Forge.

### Add configuration to a macro

This page describes how to add configuration to an existing macro. The configuration enables users
to customize what displays in the macro.

See [Add configuration to a macro with UI Kit](/platform/forge/add-configuration-to-a-macro-with-ui-kit/).

### Add routing to a full page app

This page describes how to add routing to a full page app created with Forge, using React and
[React Router](https://reactrouter.com/). Routing enables your app to manipulate the current page URL.
Routing may be used to enable users to link directly to certain parts of your app.

See [Add routing to a full page app](/platform/forge/add-routing-to-a-full-page-app/).

### Add scopes to call an Atlassian REST API

This page describes how to add scopes to your Forge app to call an authenticated Atlassian REST API
as a user or as your app.

See [Add scopes to call an Atlassian REST API](/platform/forge/add-scopes-to-call-an-atlassian-rest-api/).

### Extending your app with a scheduled trigger

This page describes how to add a scheduled trigger to your Forge app while using a web trigger for developing your function.

See [Extending your app with a scheduled trigger](/platform/forge/add-scheduled-trigger/).

This page describes how to deploy your Forge app into the staging or production environments
and what extra protections are active in these environments.

See [Promote an app to staging or production](/platform/forge/staging-and-production-apps/).

### Implement a dynamic profile retriever with external authentication

Apps implementing external authentication may import the external profile to provide a rich
app experience. This guide demonstrates how to configure the dynamic profile retriever to
expose a Google account as an `AuthProfile` to use in a Forge app.

See [Implement a dynamic profile retriever with external authentication](/platform/forge/implement-a-dynamic-profile-retriever-with-external-authentication/).

### Rotating an OAuth 2.0 client ID and secret

Apps using external authentication require external client ID and secret values. This guide
contains the rotation procedure and highlights considerations for your users.

See [Rotating an OAuth2 client ID and secret](/platform/forge/rotating-an-oauth-2.0-client-id-and-secret/).

### Common issues with external authentication

External authentication has lots of moving parts that can lead to confusing error
conditions. This guide includes some common errors and issues you may face while
developing your app.

See [Common issues with external authentication](/platform/forge/common-issues-with-external-authentication/).

### Understanding UI modifications

This module is very complex and to use it properly it's crucial to understand the broader context and all
the moving parts that we provide.

See [Understanding UI modifications](/platform/forge/understanding-ui-modifications/).
