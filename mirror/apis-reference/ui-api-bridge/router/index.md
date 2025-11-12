# router

The NavigationLocation object used in the navigate, open, and getUrl methods is in Preview and is supported only in Confluence and Jira.

We release preview features so partners and developers can study, test, and integrate
them prior to General Availability (GA). For more information,
see [Forge release phases: EAP, Preview, and GA](/platform/forge/whats-coming/#preview).

The `router` object enables you to navigate the host Atlassian app to another page. `router` supports four
methods:

1. `navigate`, which navigates to the page in the same tab.
2. `open`, which opens the page in a new tab or window, depending on the user’s browser configuration.
3. `getUrl`, which retrieves the URL for a given `NavigationLocation` object.
4. `reload`, which reloads the current page.

For `navigate` and `open`, there are two ways to declare the target page:

1. Pass a `NavigationLocation` (Preview), consisting of the [target location and the corresponding properties](#target-locations-and-properties).
2. Pass a URL directly.

Passing a `NavigationLocation` (Preview) object enables navigation with contextual and more human-readable data,
rather than using a URL. For a list of supported target locations, see [Target locations and properties](#target-locations-and-properties).

## navigate

The `navigate` method allows you to navigate to a page in the same tab.

### Function signature

```
```
1
2
```



```
function navigate(url: string | location: NavigationLocation): Promise<void>;
```
```

The shape of `NavigationLocation` (Preview) will vary according to the target location. Required
properties for each target location are defined in [Target locations and properties](#target-locations-and-properties).

If you’re using a URL to link to an external site, the user is prompted before opening the link
in a new tab. If the user declines to proceed, the returned `Promise` is rejected. If you’re using
relative URLs (starts with `/`), the user won’t be prompted.

### Example

Navigation location (Preview)

URL

```
```
1
2
```



```
import { router, NavigationTarget } from "@forge/bridge";

// To navigate to the view page for a piece of content in Confluence:
router.navigate({ target: "contentView", contentId: "12345" });

// To navigate to the view page for version 2 of a piece of content in Confluence:
router.navigate({ target: "contentView", contentId: "12345", version: 2 });

// To navigate to the edit page for a piece of content in Confluence:
router.navigate({ target: "contentEdit", contentId: "12345" });

// To navigate to the page of the given module key:
router.navigate({ target: "module", moduleKey: "my-global-page" });

// To navigate to the issue view page of an issue in Jira:
router.navigate({ target: "issue", issueKey: "TEST-1" });

// Alternatively, `NavigationTarget` can be imported and used for improved IDE autocompletion and documentation support:
router.navigate({ target: NavigationTarget.Issue, issueKey: "TEST-1" });
```
```

## open

The `open` method allows you to open a page in a new tab or window, depending on the user’s browser configuration.

### Function signature

```
```
1
2
```



```
function open(url: string | location: NavigationLocation): Promise<void>;
```
```

The shape of `NavigationLocation` (Preview) will vary according to the target location. Required
properties for each target location are defined in [Target locations and properties](#target-locations-and-properties).

If you’re using a URL to link to an external site, the user is prompted before opening the link
in a new tab. If the user declines to proceed, the returned `Promise` is rejected. If you’re using
relative URLs (starts with `/`), the user won’t be prompted.

### Example

Navigation location (Preview)

URL

```
```
1
2
```



```
import { router, NavigationTarget } from "@forge/bridge";

// Opens the view page for a piece of content in Confluence in a new tab or window:
router.open({ target: "contentView", contentId: "12345" });

// Opens the issue view page of an issue in Jira in a new tab or window:
router.open({ target: "issue", issueKey: "TEST-1" });

// Alternatively, `NavigationTarget` can be imported and used for improved IDE autocompletion and documentation support:
router.open({ target: NavigationTarget.Issue, issueKey: "TEST-1" });
```
```

## getUrl (Preview)

The `getUrl` method allows you to retrieve the URL for a given `NavigationLocation` object.

### Function signature

```
```
1
2
```



```
function getUrl(location: NavigationLocation): Promise<URL>;
```
```

The shape of `NavigationLocation` (Preview) will vary according to the target location. Required
properties for each target location are defined in [Target locations and properties](#target-locations-and-properties).

The return type of `getUrl` is a promise that resolves to a [URL](https://developer.mozilla.org/en-US/docs/Web/API/URL) object.

### Example

```
```
1
2
```



```
import { router } from "@forge/bridge";

const url = await router.getUrl({ target: "issue", issueKey: "TEST-1" });

// All URL properties and instance methods of the destination URL can now be accessed
console.log(url.pathname); // "/browse/TEST-1"
console.log(url.toString()); // "https://<tenant-name>/browse/TEST-1"
```
```

## reload

The `reload` method allows you to reload the host window.

### Function signature

```
```
1
2
```



```
function reload(): Promise<void>;
```
```

### Example

```
```
1
2
```



```
import { router } from "@forge/bridge";

router.reload();
```
```

## Target locations and properties

A `NavigationLocation` is a specific target within Confluence, Jira, or directory that can be
navigated to using the `navigate` or `open` methods. It consists of a target location and its
corresponding properties, which are outlined below.

### Confluence

#### `contentView`

The view page for pages, blogs, and custom content.

##### Example

To navigate to `/wiki/pages/viewpage.action?pageId=238945&pageVersion=2`:

```
```
1
2
```



```
router.navigate({ target: "contentView", contentId: "238945", version: 2 });
```
```

| Property | Required | Description |
| --- | --- | --- |
| `contentId` | Yes | The ID of the content. |
| `version` | No | If provided, will navigate to the specified version. |

#### `contentEdit`

The edit page for pages, blogs, and custom content.

##### Example

To navigate to `/wiki/spaces/${spaceKey}/pages/edit-v2/238945`:

```
```
1
2
```



```
router.navigate({ target: "contentEdit", contentId: "238945" });
```
```

| Property | Required | Description |
| --- | --- | --- |
| `contentId` | Yes | The ID of the content. |

#### `spaceView`

The space view page.

##### Example

To navigate to `/wiki/spaces/TEAM`:

```
```
1
2
```



```
router.navigate({ target: "spaceView", spaceKey: "TEAM" });
```
```

| Property | Required | Description |
| --- | --- | --- |
| `spaceKey` | Yes | The key of the space. |

#### `contentList`

The list page for pages, blogs, and custom content in a space.

##### Example 1

To navigate to `/wiki/spaces/TEAM/pages`:

```
```
1
2
```



```
router.navigate({
  target: "contentList",
  contentType: "page",
  spaceKey: "TEAM",
});
```
```

##### Example 2

To navigate to `/wiki/search?type=forge:${appId}:${environmentId}:my-custom-content-module`:

```
```
1
2
```



```
router.navigate({
  target: "contentList",
  contentType: "customContent",
  moduleKey: "my-custom-content-module",
});
```
```

| Property | Required | Description |
| --- | --- | --- |
| `contentType` | Yes | The content type. Accepts:* `page`, * `blogpost`, or * `customContent` |
| `spaceKey` | Yes, if `contentType` is `page` or `blogpost`. | The key of the space. |
| `moduleKey` | Yes, if `contentType` is `customContent`. | The module key of the page. |

#### `module`

The page containing the supported module. Supported Confluence modules:

##### Example

To navigate to `/wiki/apps/${appId}/${environmentId}/${route}`:

```
```
1
2
```



```
router.navigate({ target: "module", moduleKey: "my-global-page" });
```
```

| Property | Required | Description |
| --- | --- | --- |
| `moduleKey` | Yes | The module key of the page. |
| `spaceKey` | Yes, if using:* [Space page](/platform/forge/manifest-reference/modules/confluence-space-page) * [Space settings](/platform/forge/manifest-reference/modules/confluence-space-settings) | The key of the space. |

### Jira

#### `dashboard`

A dashboard in Jira.

##### Example

To navigate to `/jira/dashboards/10000`:

```
```
1
2
```



```
router.navigate({ target: "dashboard", dashboardId: "10000" });
```
```

| Property | Required | Description |
| --- | --- | --- |
| `dashboardId` | Yes | The ID of the dashboard. |

#### `issue`

An issue in Jira.

##### Example

To navigate to `/browse/FT-3`:

```
```
1
2
```



```
router.navigate({ target: "issue", issueKey: "FT-3" });
```
```

| Property | Required | Description |
| --- | --- | --- |
| `issueKey` | Yes | The key of the issue. |

#### `projectSettingsDetails`

The details of a Jira project. Only accessible to administrators.

##### Example

To navigate to `/jira/software/projects/FT/settings/details`:

```
```
1
2
```



```
router.navigate({ target: "projectSettingsDetails", projectKey: "FT" });
```
```

| Property | Required | Description |
| --- | --- | --- |
| `projectKey` | Yes | The key of the project. |

#### `module`

The page containing the supported module. Supported Jira modules:

##### Example

To navigate to `/jira/settings/apps/${appId}/${environmentId}`:

```
```
1
2
```



```
router.navigate({ target: "module", moduleKey: "my-admin-page" });
```
```

### Directory

#### `userProfile`

The profile page for a specific user.

##### Example

To navigate to `/people/12345`:

```
```
1
2
```



```
router.navigate({ target: "userProfile", accountId: "12345" });
```
```

| Property | Required | Description |
| --- | --- | --- |
| `accountId` | Yes | The ID of the user account. |
