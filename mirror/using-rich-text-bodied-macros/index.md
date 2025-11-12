# Using rich-text bodied macros

This tutorial demonstrates how you can use rich-text bodied macros in Forge. It shows how to configure your manifest and
render rich body content, using the ADF Renderer React component, or the Confluence convert content body APIs.

You can add simple configuration to a macro using UI Kit components,
[as described here](/platform/forge/add-configuration-to-a-macro-with-ui-kit/).

You can add custom configuration to a macro,
[as described here](/platform/forge/add-custom-configuration-to-a-macro/).

You can also see a sample implementation of a rich-text bodied macro in the [rich-text-custom-config-macro sample app](https://bitbucket.org/atlassian/forge-rich-text-custom-config-macro).

## Before you begin

Make sure you have the following:

* A Forge app with a Confluence macro created using [UI Kit](/platform/forge/ui-kit/) or [Custom UI](/platform/forge/custom-ui/).
* The latest version of Forge CLI. To update your CLI version, run `npm install -g @forge/cli@latest`
  on the command line.

## Step 1: Configure the manifest

To set your macro as a bodied macro, navigate to the app's `manifest.yml` file and add the line `layout: bodied` in the macro module properties.

```
1
2
3
4
macro:
  - key: my-macro
    ...
    layout: bodied
```

## Step 2: Extract the macro body

The macro body is the content that the user enters in the editor. This can be retrieved from the context provided by
[useProductContext()](/platform/forge/ui-kit-hooks-reference/#useproductcontext) or
[view.getContext()](/platform/forge/apis-reference/ui-api-bridge/view/#getcontext).

In a UI Kit app, we can use `useProductContext()` to extract the macro body.

```
```
1
2
```



```
import React from 'react';
import ForgeReconciler, { useProductContext } from '@forge/react';

const App = () => {
  const context = useProductContext();
  const macroBody = context?.extension?.macro?.body;
  // ...
}

ForgeReconciler.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```
```

## Step 3: Render rich body content

The ADF body can be rendered in two ways; using the renderer components, or by rendering the raw HTML.

### Comparison between using renderer components or HTML export

The following content types are supported by the HTML export, but not supported by the ADF renderer component:

The following content types are not supported at all by the HTML export or the ADF renderer component:

See detailed documentation for the [AdfRenderer](/platform/forge/ui-kit/components/adf-renderer/).

### Using renderer components

For UI Kit, you can use the `AdfRenderer` component, while for Custom UI, you can use the `ReactRenderer` component.
Both the `AdfRenderer` and `ReactRenderer` component require the prop `document`, which is an ADF document with the following structure:

```
```
1
2
```



```
"body": {
  "type": "doc",
  "version": 1,
  "content": [
    // ADF content
  ]
}
```
```

We can pass the macro body that we extracted [previously](#step-2--extract-the-macro-body) into the `document`
prop of `AdfRenderer` and `ReactRenderer` components for UI Kit and Custom UI respectively.

To render in UI Kit, you can use the `AdfRenderer` component from [@forge/react](https://www.npmjs.com/package/@forge/react).

```
```
1
2
```



```
import { AdfRenderer } from "@forge/react";

const App = () => {
  // ...
  return macroBody && <AdfRenderer document={macroBody} />
}
```
```

### Using the Confluence API to export to HTML

Alternatively, you can use [requestConfluence()](/platform/forge/apis-reference/ui-api-bridge/requestConfluence/) to make a request
to the Confluence Cloud platform REST API to convert the macro body into HTML. We can render this HTML directly in our Forge app.

This approach requires the `read:confluence-content.all` scope, which we'll add to the manifest later in this section.

The following code imports `requestConfluence`, and extracts `contentId` and `macroBody` from the `context` obtained in
[step 2](/platform/forge/using-rich-text-bodied-macros/?tabId=2&tab=custom+ui#step-2--extract-the-macro-body).

Next, we can construct the async API call for the macro body in HTML form using the
[Asynchronously convert content body](/cloud/confluence/rest/v1/api-group-content-body/#api-wiki-rest-api-contentbody-convert-async-to-post) call.

If we want to support rendering embedded content, we must also provide the following query parameters:

* `contentIdContext`: The content ID for resolving embedded content in the content body
* `expand`: Return CSS and JavaScript tags in the response for rendering embedded content

Note that this embedded content includes core Confluence macros, but does not support other Connect or Forge macros.

Also note the ADF body (`value`) is stringified again.
This is because the API accepts bodies in various formats, including XML,
so it cannot make any assumptions about the format of the body.

```
```
1
2
```



```
import { requestConfluence } from "@forge/bridge";

async function convertMacroBody(to, macroBody, contentId) {
  const params = new URLSearchParams({
    contentIdContext: contentId,
    expand: "webresource.tags.all,webresource.superbatch.tags.all",
  }).toString();

  const response = await requestConfluence(
    `/wiki/rest/api/contentbody/convert/async/${to}?${params}`,
    {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        value: JSON.stringify(macroBody),
        representation: "atlas_doc_format",
      }),
    }
  );

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return (await response.json()).asyncId;
}

const macroBody = context?.extension?.macro?.body;
const contentId = context?.extension?.content?.id;

if (macroBody) {
  const asyncId = await convertMacroBody(
    "styled_view",
    macroBody,
    contentId
  );
}
```
```

Use `"atlas_doc_format"` for the `representation` parameter in `body`. This indicates that the macro body is in ADF format.

Use `"styled_view"` for the `to` parameter. This will convert the macro body to an HTML document with embedded styles.

We can obtain the HTML body from the `id` that is returned from `convertMacroBody()` using the
[Get asynchronously converted content body from the id or the current status of the task](/cloud/confluence/rest/v1/api-group-content-body/#api-wiki-rest-api-contentbody-convert-async-id-get) call.

Note that we inject the expanded CSS and JavaScript tags into the HTML body.

```
```
1
2
```



```
async function fetchConvertedMacroBody(id) {
  const response = await requestConfluence(
    `/wiki/rest/api/contentbody/convert/async/${id}`,
    {
      headers: {
        Accept: "application/json",
      },
    }
  );

  const { status, error, value, webresource } = await response.json();
  if (status === "FAILED") {
    throw new Error(`Conversion failed: ${error}`);
  } else if (status === "COMPLETED") {
    const scripts = webresource.superbatch.tags.all + webresource.tags.all;
    const html = value.replace("</head>", `${scripts}</head>`);
    return html;
  }
  // Keep polling until completed
  return fetchConvertedMacroBody(id);
}


const htmlBody = await fetchConvertedMacroBody(asyncId);
```
```

#### Rendering the export HTML

Finally, we can directly render the HTML.

For UI Kit, we can render the HTML in a `Frame` component.
See [Frame](/platform/forge/ui-kit/components/frame/) for more details.

First define the `Frame` in the `resources` section of the `manifest.yml` file.
See an example manifest structure [here](/platform/forge/ui-kit/components/frame/#example-manifest-yml-file).

```
```
1
2
```



```
resources:
  ...
  - key: html-frame
    path: resources/html-frame/build
```
```

Next, create an `index.js` and `index.html` file in the path specified in the manifest resources.
See [here](/platform/forge/ui-kit/components/frame/#setting-up-resources) for more information on setting up resources.

The [onPropsUpdate](/platform/forge/ui-kit/components/frame/#receiving-props-in-the-frame-component-using-frame-onpropsupdate)
function will be called each time the parent component provides HTML, which we will then render directly inside our `Frame`.

```
```
1
2
```



```
import { events } from "@forge/bridge";

events.on("PROPS", ({ html }) => {
// Create a fragment, allowing any embedded content scripts to be executed when appended
const documentFragment = document
  .createRange()
  .createContextualFragment(html);
document.body.innerHTML = "";
document.body.appendChild(documentFragment);
});
```
```

This frame can now be used in your UI Kit app to render the HTML body. This is your `src/frontend/index.jsx` file.
The following code uses [createFrame](/platform/forge/ui-kit/components/frame/#using-createframe).

```
```
1
2
```



```
import { events } from "@forge/bridge";
import { Frame } from "@forge/react"

const App = () => {
  useEffect(() => {
    events.emit("PROPS", { html: htmlBody });
  }, [htmlBody]);

  return <Frame resource="html-frame" />
}
```
```

Add the `read:confluence-content.all` scope in the permissions section of the `manifest.yml` file.

```
```
1
2
```



```
permissions:
  scopes:
    - "read:confluence-content.all"
```
```

Additionally, if we want to render embedded content, we must specify the following permissions in the `manifest.yml` file:

```
```
1
2
```



```
permissions:
  content:
    styles:
      - "unsafe-inline" # Required for styled_view inline styles in the converted HTML
    scripts:
      - "unsafe-inline" # Rendering embedded content when converted to HTML with expand
  external:
    fetch:
      client:
        - "*.atlassian.net" # Embedded content can call back to Atlassian sites
    images:
      - "*" # Required for images in the converted HTML
    styles:
      # Rendering embedded content when converted to HTML with expand
      - "*.atl-paas.net"
      - "*.cloudfront.net"
    scripts:
      # Rendering embedded content when converted to HTML with expand
      - "*.atl-paas.net"
      - "*.cloudfront.net"
```
```

## Use the body in an `adfExport` function

When the page is exported to PDF, Word, or viewed in the page history, you can specify how the macro should be displayed.
This is done by specifying an `adfExport` function, and referencing it in your app's `manifest.yml` file.

When there is no export function defined, by default, the macro body will be returned.

Accessing the rich text body is done via the `extensionPayload.macro.body` property.

If you would like to customise the export:

1. Create a new ADF document
2. Insert any extra ADF nodes for customisation (such as paragraphs, shown in the sample code)
3. Insert the rich-text body content from the macro into the document

See the full `adfExport` tutorial [here](/platform/forge/change-the-confluence-frontend-with-the-ui-kit/#specify-the-export-view).

```
```
1
2
```



```
import { doc, p } from '@atlaskit/adf-utils/builders';

export function adfExport(payload) {
  const macroBody = payload.extensionPayload.macro.body;

  return doc(
    p("This is my export function. Here's the macro content:"),
    ...macroBody.content
  )
}
```
```

## Troubleshooting

| Issue | Solution |
| --- | --- |
| Macro does not have a body | * Check if the macro has correctly defined the `layout: bodied` property in the manifest. |
| Body is not set when calling `view.submit()` | * Check the [error codes](/platform/forge/manifest-reference/modules/macro/#error-code-guide) for more guidance - specifically `INVALID_EXTENSION_TYPE` and `INVALID_BODY`. * Check if the `body` parameter has been provided to `view.submit()` if the body is missing. * Ensure that the body is a valid   [ADF](/cloud/jira/platform/apis/document/structure/#atlassian-document-format) object. |
| Body not present in the app context | * Check the correct context location is being referenced. * It differs between view (`extension.macro.body`) and export (`extensionPayload.macro.body`). |
| Body ADF not rendered at all or not rendered correctly | * Ensure that the body is a valid [ADF](/cloud/jira/platform/apis/document/structure/#atlassian-document-format) object. * If you are rendering the content as HTML, ensure you are using the export API as detailed in the [example](/platform/forge/using-rich-text-bodied-macros/?tabId=2&tab=custom+ui#using-the-confluence-api-to-export-to-html). * See [ADF Renderer](/platform/forge/ui-kit/components/adf-renderer) for UI Kit ADF rendering, or [AtlasKit ReactRenderer](https://atlaskit.atlassian.com/packages/editor/renderer) for Custom UI ADF rendering. |
| Cannot upgrade a Connect bodied macro |  |
| Body is not exported as expected | * Check the manifest for the `adfExport` parameter and ensure the function is valid. * By default, if no `adfExport` is provided, the body will be exported (the value of `extensionPayload.macro.body`). * See the section [above](/platform/forge/using-rich-text-bodied-macros/?tabId=2&tab=custom+ui#use-the-body-in-an-adfexport-function) for more information. |
