# Promote an app to staging or production

This page describes how to take your existing Forge app from the *development* environment
and share it with your users in a *production* environment. You'll learn about Forge
environment restrictions and how to request the minimum set of permissions from your users.

## Configure API scopes

Forge apps must explicitly declare which scopes they require in the `manifest.yml` file
to use the authenticated [Product Fetch APIs](/platform/forge/runtime-reference/product-fetch-api/).

See the [Permissions](/platform/forge/manifest-reference/permissions/) page for a summarized
table of Forge supported OAuth 2.0 scopes for all Atlassian cloud apps. You
can also find supported scopes in each Atlassian app's REST API documentation on a per operation basis.

See the [Add scopes to call an Atlassian REST API](/platform/forge/add-scopes-to-call-an-atlassian-rest-api/)
page for step-by-step instructions on adding new scopes.

### Deploy to a specific environment

To deploy to a specific environment, provide the `-e` argument to your command.

1. Navigate to the app's top-level directory and deploy your app by running:

   ```
   1
   forge deploy -e production
   ```
2. Install your app by running:

   ```
   1
   forge install -e production
   ```
3. Select the Atlassian app.
4. Enter the URL for your development site (for example, *example.atlassian.net*).
5. Review the scopes your app is requesting then answer `y`.
