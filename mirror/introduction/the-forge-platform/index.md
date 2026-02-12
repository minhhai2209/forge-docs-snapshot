# The Forge platform

Reading time: Under 5 minutes

# The Forge platform

Forge is Atlassian’s cloud app development platform, allowing developers to host apps on infrastructure that is provisioned, managed, monitored, and scaled automatically by Atlassian. Forge provides a complete toolkit for extending Atlassian apps.

Forge apps are built in JavaScript; however, the environment differs a little from a traditional Node.js environment. [Learn more](https://developer.atlassian.com/platform/forge/runtime-reference/)

Below is a diagram demonstrating the Forge platform architecture.

![Forge Architecture diagram](https://dac-static.atlassian.com/platform/forge/images/introduction/forge-architecture.png?_v=1.5800.1846)

## Forge runtime

At the heart of Forge is a serverless FaaS hosting platform, powered by AWS Lambda. Apps created with Forge run inside a security layer that enforces data egress restriction by design.

[Learn more about the Forge runtime](https://developer.atlassian.com/platform/forge/runtime-reference/)

[Learn more about security for Forge apps](https://developer.atlassian.com/platform/forge/security/)

### Forge resolver

The Forge resolver is a function that provides a backend for apps that use UI Kit or Custom UI to implement the user experience of an app. Use of the resolver is optional, but it's useful if you need to run some app logic server-side instead of client-side.

[Learn more about the Forge resolver](https://developer.atlassian.com/platform/forge/runtime-reference/custom-ui-resolver/)

### Events

A Forge app can subscribe to events or set up an HTTP endpoint to invoke a function within the app without any user interaction.

[Learn more about events](https://developer.atlassian.com/platform/forge/events/)

## Forge storage

Forge's hosted storage lets you store data partitioned by Atlassian app and site. Hosted storage also provides data residency features that allow admins to control where app data is hosted.

[Learn more about Forge storage](https://developer.atlassian.com/platform/forge/runtime-reference/storage-api/)

## App frontend

[Modules](https://developer.atlassian.com/platform/forge/modules/) are used by Forge apps to extend and interact with Atlassian apps.

Forge offers two options for building the user interface of your apps: Custom UI and the UI Kit. Both Custom UI and UI Kit apps inherit modern security features to ensure high trust between Atlassian, developers, and users.

### Custom UI

Custom UI provides a means of building the user interface of an app from scratch. Custom UI runs within an iframe, providing an isolated environment for the app's interface to be displayed.
[Learn more about Custom UI](https://developer.atlassian.com/platform/forge/custom-ui/)

### UI Kit

The UI Kit is a flexible declarative language that allows you to build user interfaces across Atlassians apps with just a few lines of code.
[Learn more about the latest UI Kit](https://developer.atlassian.com/platform/forge/ui-kit-2/index/)

### Forge bridge

The bridge API is a JavaScript API that enables UI Kit and Custom UI apps to securely integrate with Atlassian apps.

[Learn more about the App bridge API](https://developer.atlassian.com/platform/forge/apis-reference/ui-api-bridge/bridge/)

## Atlassian app APIs

Forge apps can use the Atlassian app REST APIs using the [fetch API](/platform/forge/runtime-reference/fetch-api/), a partial implementation of the `fetch` API from
[Undici](https://nodejs.org/en/learn/getting-started/fetch#using-the-fetch-api-with-undici-in-nodejs).

[Learn more about the Atlassian app REST APIs](/platform/forge/apis-reference/product-rest-api-reference/)
