# Managing web trigger URLs via SDK

The web trigger runtime API can be used to manage web trigger URLs within your app programmatically.

See the [web trigger module](/platform/forge/manifest-reference/modules/web-trigger) for more details.

The web trigger URL is stable for each combination of:

* module key
* app
* site
* Atlassian app
* Forge environment

For example, redeploying a new version of your app to the Forge production environment does not change the web trigger URL. However, the web trigger URL for the same app in the development environment is different.

Import the Forge API package in your app as follows:

```
1
import { webTrigger } from "@forge/api";
```

## Get a URL

Obtain the URL for the web trigger module specified by the given module key.

```
1
await webTrigger.getUrl("example-web-trigger-key");
```

### Method signature

```
1
webTrigger.getUrl(moduleKey: string, forceCreate?: boolean) => Promise<string>;
```

### Parameters

| Name | Type | Description |
| --- | --- | --- |
| `moduleKey` | `string` | The module key to create the URL for. |
| `forceCreate` | `boolean | undefined` | Whether a new URL should be created or any existing one for the module can be reused. |

## Query for URLs

Retrieve all web trigger URLs for the specified `moduleKey`. Returns all active web trigger URLs for the app if no `moduleKey` is specified.

```
```
1
2
```



```
await webTrigger.queryUrls("example-web-trigger-key"); // returns URLs for the specified module
await webTrigger.queryUrls(); // returns all URLs for the app
```
```

### Method signature

```
```
1
2
```



```
type WebTriggerQueryResult = {
  moduleKey: string;
  url: string;
};
webTrigger.queryUrls(moduleKey?: string) => Promise<WebTriggerQueryResult[]>;
```
```

### Parameters

| Name | Type | Description |
| --- | --- | --- |
| `moduleKey` | `string | undefined` | The module key to query for URLs. |

## Delete a URL

Deletes the provided web trigger URL. Deleted URLs, if reused, will not be able to invoke the underlying module function.

```
```
1
2
```



```
await webTrigger.deleteUrl("example-web-trigger-key");
```
```

### Method signature

```
```
1
2
```



```
webTrigger.deleteUrl(webTriggerUrl: string) => Promise<void>;
```
```

### Parameters

| Name | Type | Description |
| --- | --- | --- |
| `webTriggerUrl` | `string` | The web trigger URL to delete. |
