# Common issues with external authentication

Working with OAuth 2.0 providers involves more complexity in your app, as you manage
multiple places to configure things correctly. This page covers ways to solve common error
conditions, helping you to successfully develop a Forge app with external authentication.

## Token exchange issues

**Error message**:

* `could not retrieve access token from the provider`
* `could not retrieve access token from the provider: Unexpected response status code 502 from api.atlassian.com`
* `could not retrieve access token from the provider: Birdy Timeout Error`

**Action**:

1. Ensure the client secret has been set using the
   [configure providers](/platform/forge/cli-reference/providers/) CLI command.
2. Confirm the [exchange](/platform/forge/manifest-reference/providers/#exchange) URL is correct in
   the `manifest.yml` file.
3. If it’s still not working, try again later. The provider might be having connection issues.

## Profile retriever issues

**Error message**:

* `could not retrieve profile information`
* `could not retrieve profile information: Birdy Timeout Error`

**Action**:

1. Confirm the [profileRetriever](/platform/forge/manifest-reference/providers/#profile-retriever)
   URL is correct in the `manifest.yml` file.
2. If it’s still not working, try again later. The provider might be having connection issues.

**Error message**:

* `could not retrieve profile information: Authorization Failed: Could not extract internalAccountId from the response`

**Action**:

The `id` parameter in the [static profile retriever](/platform/forge/manifest-reference/providers/#static-profile-retriever)
is incorrect. Check the identity provider's documentation for the endpoint you are using to
ensure the field name is correct and is a string.

## Function issues

**Error message**:

* `There was an error invoking the function - Authentication required`

**Action**:

Ensure this function's manifest entry has the `providers` reference on it.

## Unsupported cases

### Different OAuth 2.0 types

External authentication only supports [authorization code grants](https://tools.ietf.org/html/rfc6749#section-4.1).
