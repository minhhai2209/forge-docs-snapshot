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
1import { getEditorContent, getMacroContent, updateMacro, setMacroViewportHeight } from '@forge/confluence-bridge';
2
3const editorContent = await getEditorContent();
4
5const macroContent = await getMacroContent();
6
7// Replace <updatedMacroADF> with your updated macro ADF content
8const updateMacroContentResult = await updateMacro(<updatedMacroADF>);
9
10const setMacroViewportHeightResult = await setMacroViewportHeight('200');
11
```

Use the `updateBylineProperties()` bridge method to update the `title`, `icon`, and `tooltip` of a `confluence:contentBylineItem` app programmatically, like this:

```
1import { updateBylineProperties } from "@forge/confluence-bridge";
2
3await updateBylineProperties({ propertyKey, valueUpdate });
4
```
