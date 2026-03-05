# Forge bridge APIs

The Forge bridge API is a JavaScript API that enables [UI Kit](/platform/forge/ui-kit/) and
[Custom UI](/platform/forge/custom-ui) apps to securely integrate with Atlassian apps.

Install the Forge bridge API using the
[@forge/bridge](https://www.npmjs.com/package/@forge/bridge) npm package.
Import `@forge/bridge` using a bundler, such as [Webpack](https://webpack.js.org/).

You can start by creating a new app from one of the UI templates.
In the `static/hello-world` directory, run `npm install && npm build` to bundle the
static web application template with the Forge bridge API into the `static/hello-world/build`
directory. Use this directory as the resource path in the Forge app's `manifest.yml`.

In the template, use the bridge in `static/hello-world/src/App.js` like this:

```
1
2
3
import { invoke } from '@forge/bridge';

invoke('getText', { example: 'my-invoke-variable' }).then(setData);
```
