# Confluence UI bridge

The Confluence UI bridge is a JavaScript API that enables [Forge macros](/platform/forge/manifest-reference/modules/macro) to securely integrate with Confluence.

Install the Confluence UI bridge using the
[@forge/confluence-bridge](https://www.npmjs.com/package/@forge/confluence-bridge) npm package.
Import `@forge/confluence-bridge` using a bundler, such as [Webpack](https://webpack.js.org/).

You can start by creating a new app from one of the Custom UI templates.
In the `static/hello-world` directory, run `npm install && npm build` to bundle the
static web application template with the Confluence UI bridge into the `static/hello-world/build`
directory. Use this directory as the resource path in the Forge app's `manifest.yml`.

In the template, use the bridge in `static/hello-world/src/App.js` like this:

```
1
2
3
4
5
6
7
8
9
10
import { getEditorContent, getMacroContent, updateMacroContent, setMacroViewportHeight } from '@forge/confluence-bridge';

const editorContent = await getEditorContent();

const macroContent = await getMacroContent();

// Replace <updatedMacroADF> with your updated macro ADF content
const updateMacroContentResult = await updateMacroContent(<updatedMacroADF>);

const setMacroViewportHeightResult = await setMacroViewportHeight('200');
```

Use the `updateBylineProperties()` bridge method to update the `title`, `icon`, and `tooltip` of a `confluence:contentBylineItem` app programmatically, like this:

```
1
2
3
import { updateBylineProperties } from '@forge/confluence-bridge';

await updateBylineProperties({ propertyKey, valueUpdate });
```
