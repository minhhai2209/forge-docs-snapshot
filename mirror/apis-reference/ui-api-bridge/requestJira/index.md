# requestJira

Previously, you'd need to define a [resolver](/platform/forge/runtime-reference/custom-ui-resolver/) to use the `requestJira` bridge method. With the release of [Forge bridge version 2.0](/platform/forge/changelog/), Custom UI and UI Kit can now use the method directly.

The `requestJira` bridge method enables Forge apps to call the
[Jira Cloud platform REST API](https://developer.atlassian.com/cloud/jira/platform/rest/v2/) **on behalf of the user who is currently interacting with the app** in the browser. There is no equivalent of `asApp()` on the `@forge/bridge` package: calls from front-end code always run with the permissions of the current user.

This means that, in addition to the app declaring the correct [scopes](/platform/forge/manifest-reference/permissions/) in its manifest, the current user must have the Jira permissions required by the REST API operation being called. If the user does not have those permissions, the request fails with a `403 Forbidden` response — even when the app's scopes are configured correctly.

If you need to call the Jira REST API as the app itself (for example, to access data that the current user cannot see, or to make a request from a [scheduled trigger](/platform/forge/manifest-reference/modules/scheduled-trigger/) or [event handler](/platform/forge/events-reference/)), use the [`requestJira`](/platform/forge/runtime-reference/product-fetch-api/#requestjira) method from the `@forge/api` package in a back-end function, and call it with `api.asApp()`. See [Contextual methods](/platform/forge/runtime-reference/product-fetch-api/#contextual-methods) for more information on the differences between `asUser()` and `asApp()`.

## Function signature

```
1
2
3
4
function requestJira(
  uri: string,
  options?: RequestInit,
): Promise<Response>
```

## Arguments

## Returns

## Example

```
```
1
2
```



```
import { requestJira } from '@forge/bridge';

const response = await requestJira('/rest/api/3/issue/ISSUE-1');
console.log(await response.text());
```
```
