# Fetch API

The Forge Fetch API is a partial implementation of `undici`, which fetches data from an HTTP server.
In the most basic use, `fetch` is a simple HTTP client. See [Basic fetch client](/platform/forge/runtime-reference/fetch-api.basic/) for more information.

However, `fetch` also supports multiple options for managed authentication to remote APIs:

## Atlassian app authentication

You can also make requests directly to an Atlassian app's REST API through the following fetch endpoints:

## External authentication

The `withProvider` method enables your Forge app to communicate with an API that
requires OAuth 2.0 tokens. Access is via the `asUser` method, in the `@forge/api` package.
See [External authentication](/platform/forge/runtime-reference/external-fetch-api/) for
more information.
