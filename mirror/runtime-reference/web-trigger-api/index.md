# Generating a webtrigger URL via SDK

The web trigger runtime API can be used to obtain web trigger URLs within your app programmatically.

See the [web trigger module](/platform/forge/manifest-reference/modules/web-trigger) for more details.

Import the Forge API package in your app as follows:

```
1
import { webTrigger } from "@forge/api";
```

## webTrigger.getUrl

Obtain the URL for the web trigger module specified by the given module key.

```
1
await webTrigger.getUrl("example-web-trigger-key");
```

The web trigger URL is stable for each combination of:

* module key
* app
* site
* Atlassian app
* Forge environment

For example, redeploying a new version of your app to the Forge production environment does not change the web trigger URL. However, the web trigger URL for the same app in the development environment is different.

### Method signature

```
1
webTrigger.getUrl(moduleKey: string): Promise<string>;
```
