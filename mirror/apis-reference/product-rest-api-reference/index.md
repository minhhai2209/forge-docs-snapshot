# Atlassian app REST APIs

Forge apps can use the following Atlassian app REST APIs:

To call an Atlassian app REST API using the Authenticated [Atlassian app Fetch APIs](/platform/forge/runtime-reference/product-fetch-api/) the operation must support OAuth 2.0 authentication.
In the Atlassian app API documentation, this is shown by the *OAuth scopes required* field,
which documents the required OAuth 2.0 scope for that operation.

Calling an unsupported operation with `asUser()` returns a `401` error.

Jira Cloud REST API version 2 is not supported by the `forge lint` command.
Only `/rest/api/3` paths are supported.

## Atlassian app fetch API

The [fetch API](/platform/forge/runtime-reference/fetch-api/#fetch-api) also enables you to make requests to Atlassian app APIs through the following endpoints:

## OAuth 2.0 scopes

Scopes define the operations that an app is permitted to use in an Atlassian app REST API.

See [Add scopes to call an Atlassian REST API](/platform/forge/add-scopes-to-call-an-atlassian-rest-api/) for instructions on how to add scopes to Forge apps, or [Scopes](/platform/forge/manifest-reference/permissions/#scopes) for the list of supported OAuth 2.0 scopes.

## GraphQL APIs

Atlassian apps such as Compass use the [Atlassian platform GraphQL API](https://developer.atlassian.com/platform/atlassian-graphql-api/graphql/) rather than a REST API. To call GraphQL APIs from a Forge app, use Forge's [requestGraph](/platform/forge/runtime-reference/product-fetch-api/#requestgraph) method.

As an alternative to `requestGraph`, Compass also provides a [GraphQL API Toolkit](https://www.npmjs.com/package/@atlassian/forge-graphql) for commonly used calls to the GraphQL API.
