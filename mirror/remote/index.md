# Forge Remote

Using the capabilities discussed on this page may make your app *not* eligible for **Runs on Atlassian**.

Go to [this page](/platform/forge/runs-on-atlassian/) to know more about the Runs on Atlassian program.
To know how to check if your app is eligible for Runs on Atlassian, go to the
[Forge CLI documentation](/platform/forge/cli-reference/eligibility/).

Forge Remote allows you to integrate a Forge app with services hosted on other platforms that you control.

It offers additional functionality, compared to the standard REST API `fetch()` approach, that is
useful to services that interoperate with Forge apps. These include:

* Ability to configure your app to send auth tokens to the remote endpoint that allow the remote endpoint
  to make authenticated calls back to the Atlassian platform to access Atlassian app APIs and Forge Storage
  using Atlassian account credentials.
* Optional ability to define a module that links your remote directly to an extension point, so that
  you have less code to maintain.
* Ability to validate that incoming requests to your remote originated from the Atlassian Forge platform.
* Automatically sending key information about the source of the invocation to your remote in a Forge Remote request,
  so that you don't have to manually copy the site's Base URL, license status, and other commonly-required
  information into your request.
* Ability to meet Atlassian data residency eligibility requirements if your app satisfies certain criteria.

Specific tasks you can perform using Forge Remote include:

## Using Forge Remote

* [Remote essentials](/platform/forge/remote/essentials) - the key things you need to connect to your remote
* Specifics and guides on remote capabilities:

## Use cases

Some use cases for these capabilities:

* Create an integration app that sends or receives data between an Atlassian app and a third-party app where you control the third-party auth and infrastructure.
* Invoke a complex existing application, for example, your own customized large language model that provides AI services to your app that runs on a non-Atlassian platform
  that you control.
* Provide a webhook endpoint for an external app such as Slack to send a request to an Atlassian app upon an arbitrary event.

## See the code for a working reference app

### Reference Forge application (frontend code):

The Forge portion of the app demonstrates how to define:

* A remote resolver for a Confluence macro using Custom UI and targeting a Node.js or Spring Boot remote endpoint.
* A remote resolver for a Confluence macro using Custom UI, performing a backend invocation of a Node.js or Spring Boot remote endpoint.
* A webtrigger that performs a backend invocation of a Node.js or Spring Boot remote endpoint.
* A remote receiver for the `avi:confluence:created:comment` and `avi:confluence:created:page` events targeting a Spring Boot endpoint.
* A remote receiver for the `avi:confluence:created:page` event targeting a Node.js endpoint.

### Reference backend endpoints:

The remote app code demonstrates how to:

* Validate and retrieve key information from a Forge Invocation Token (FIT).
* Set, get, and delete an entry from Forge Storage using GraphQL.
* Invoke Atlassian app APIs with app and user permissions.
* Invoke a Confluence API with app permission to place a comment on a page in response to the `avi:confluence:created:page` event.
* Invoke a Confluence API with app permissions to fetch a page in response to the `avi:confluence:created:comment` event.
* Provide a webhook endpoint for an external app to perform a request to Confluence as an app.

# Running local reference backends

You must run your own copy of the reference backends in order to be able to send and receive responses from the reference frontend. This is because the reference backends are configured to only accept requests from a specific frontend app ID.

You will need to update the remote `baseUrl`s in the frontend app manifest to point to your own backend services. Your own reference backends must be accessible from the internet, as requests to them will be sent from the Forge platform.
