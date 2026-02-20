# ADF renderer

To add the `AdfRenderer` component to your app:

```
1
import { AdfRenderer } from "@forge/react";
```

## Description

The `AdfRenderer` component provides a way to render a valid ADF document, using the same renderer that Atlassian uses internally to render ADF content in Confluence pages, Jira work items, and so on.
It allows you to replace node types that are unsupported in the context of a Forge app with replacement content, or remove them entirely.
See [Atlassian Document Format](/cloud/jira/platform/apis/document/structure/) for information on valid nodes.

This component uses [@atlaskit/renderer](https://www.npmjs.com/package/@atlaskit/renderer) under the hood.

Visit [Renderer editor](https://atlaskit.atlassian.com/examples/editor/renderer/basic) for a comprehensive list of different ADF document examples.

## Accessibility considerations

When using the `replaceUnsupportedNode` prop you will need to ensure that any content is replaced with accessible content.
This content needs to be clear to the user it has been replaced. Including an explanation as to why the content is replaced can also be useful.
Read more [about Readable content (as per WCAG success criterion)](https://www.w3.org/WAI/WCAG21/Understanding/readable)

This helps users who use:

* Screen readers
* Braille display
* Text-to-speech technology

## Props

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| `document` | [DocNode](https://developer.atlassian.com/cloud/jira/platform/apis/document/nodes/doc/) | Yes | An ADF document to render |
| `replaceUnsupportedNode` | [Visitor](https://bitbucket.org/atlassian/atlassian-frontend-mirror/src/master/editor/adf-utils/src/types/index.ts) | No | A function to determine behaviour for handling unsupported nodes:  * Return a new Node to replace the unsupported one * Return false to remove the node entirely * Return undefined to leave the node as-is (default behaviour) |

See [@atlaskit/renderer](https://atlaskit.atlassian.com/packages/editor/renderer) for the full list of props supported by the underlying component.

## Unsupported node types

| Node type | Support | Details |
| --- | --- | --- |
| `media` | Partial | Only supports media hosted by Atlassian when used in a Confluence macro module. You can identify Atlassian hosted `media` nodes as they have an `attrs.id` property, instead of `attrs.url` |
| `emoji` | Partial | Only standard Unicode emoji are supported, not [custom user-provided emoji](https://support.atlassian.com/confluence-cloud/docs/use-symbols-emojis-and-special-characters/#Add-your-own-emoji) |
| `bodiedExtension` | None | All types of Forge macros are supported, except for Forge bodied macros; see  [Rendering a UI Kit bodied macro](https://developer.atlassian.com/platform/forge/ui-kit/components/adf-renderer/#rendering-a-ui-kit-bodied-macro)  for the new EAP feature. However, core Confluence macros and Connect macros are not supported. |

## Examples

### Rendering a UI Kit bodied macro

The `AdfRenderer` component now supports rendering embedded Forge Custom UI and UI Kit apps as an Early Access Program (EAP). To start testing this feature, sign up using this [form](https://ecosystem.atlassian.net/servicedesk/customer/portal/1040/group/3496/create/18979).

By signing up for this Early Access Program (“EAP”), you acknowledge that use of the Forge embedded macros is governed by the Atlassian Developer Terms. Forge embedded macros are considered “Early Access Materials”, as set forth in Section 12 of the Atlassian Developer Terms and is subject to applicable terms, conditions, and disclaimers.

APIs and features under EAP are unsupported and subject to change without notice. APIs and features under EAP are not recommended for use in production environments.

For more details, see [Forge EAP, Preview, and GA](/platform/forge/whats-coming/#eap).

This demonstrates how to render the contents of a UI Kit bodied macro, including bodied macros that contain embedded UI Kit or Custom UI Forge apps. For Custom UI bodied macros, see [createAdfRendererIframeProps](/platform/forge/apis-reference/ui-api-bridge/view/#createadfrendereriframeprops--eap-).

#### Prerequisites:

* Your app must be a [Confluence bodied macro](/platform/forge/using-rich-text-bodied-macros/#step-3--render-rich-body-content) with [layout:bodied enabled](/platform/forge/using-rich-text-bodied-macros/#step-1--configure-the-manifest) in the macro module properties of the manifest file.
* This approach is for **UI Kit** apps only. For Custom UI, use `view.createAdfRendererIframeProps` instead.

![Screenshot showing a UI Kit bodied macro with "Hello world!" text above and below the rendered macro body content](https://dac-static.atlassian.com/platform/forge/ui-kit/images/adfRenderer/adfRenderer-ui-kit-bodied-macro.png?_v=1.5800.1869)

```
```
1
2
```



```
import React from "react";
import ForgeReconciler, {
  Text,
  useProductContext,
  AdfRenderer,
} from "@forge/react";

const App = () => {
  const context = useProductContext();
  const macroBody = context?.extension?.macro?.body;
  return (
    <>
      <Text>Hello world!</Text>
      <Text>Macro body below</Text>
      {macroBody ? (
        <AdfRenderer document={macroBody} />
      ) : (
        <Text>loading macro content...</Text>
      )}
      <Text>Macro body above</Text>
    </>
  );
};
ForgeReconciler.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```
```

If the UI Kit bodied macro contains multiple Forge embedded macro apps, you can optionally split it up and pass it to multiple `<AdfRenderer document={macroBody} />` instances.

### Basic text rendering

This demonstrates how a simple ADF document is rendered.

![Example image of a rendered valid basic ADF document](https://dac-static.atlassian.com/platform/forge/ui-kit/images/adfRenderer/adfRenderer-basic.png?_v=1.5800.1869)

```
```
1
2
```



```
import { AdfRenderer } from "@forge/react";

export const AdfRendererBasicExample = () => {
  const simpleDocumentToRender = {
    type: "doc",
    version: 1,
    content: [
      {
        type: "paragraph",
        content: [
          {
            type: "text",
            text: "This is a simple text example",
          },
        ],
      },
    ],
  };

  return <AdfRenderer document={simpleDocumentToRender} />;
};
```
```

### Rendering unsupported content

This demonstrates how unsupported content might render by default, without any explicit replacement logic defined.

![Example image of a rendered valid ADF document with unsupported content](https://dac-static.atlassian.com/platform/forge/ui-kit/images/adfRenderer/adfRenderer-unsupported-content-basic.png?_v=1.5800.1869)

```
```
1
2
```



```
import { AdfRenderer } from "@forge/react";

export const AdfRendererUnsupportedExample = () => {
  const simpleDocumentToRender = {
    type: "doc",
    version: 1,
    content: [
      {
        type: "paragraph",
        content: [
          {
            type: "emoji",
            attrs: {
              shortName: ":custom-emoji-hello:",
              id: "1e35b00f-cb17-4d28-91a5-ad38700715ae",
              text: ":hello!:",
            },
          },
        ],
      },
    ],
  };

  return <AdfRenderer document={simpleDocumentToRender} />;
};
```
```

### Replacing unsupported content

This demonstrates a simple replacement function that just replaces unsupported content with a paragraph.

![Example image of a rendered valid ADF document with unsupported content replaced](https://dac-static.atlassian.com/platform/forge/ui-kit/images/adfRenderer/adfRenderer-unsupported-content-replaced-basic.png?_v=1.5800.1869)

```
```
1
2
```



```
import { AdfRenderer } from "@forge/react";

export const AdfRendererUnsupportedContentExample = () => {
  const replaceUnsupportedNode = (node) => {
    return {
      type: "paragraph",
      content: [
        {
          type: "text",
          text: `Unsupported content: ${node.type}`,
        },
      ],
    };
  };

  const simpleDocumentToRender = {
    type: "doc",
    version: 1,
    content: [
      {
        type: "paragraph",
        content: [
          {
            type: "emoji",
            attrs: {
              shortName: ":custom-emoji-hello:",
              id: "1e35b00f-cb17-4d28-91a5-ad38700715ae",
              text: ":hello!:",
            },
          },
        ],
      },
    ],
  };

  return (
    <AdfRenderer
      document={simpleDocumentToRender}
      replaceUnsupportedNode={replaceUnsupportedNode}
    />
  );
};
```
```

### Replacing multiple content types

This demonstrates a more complex replacement function that either replaces content, removes it, and or leaves it as-is, depending on the node type.

![Example image of a rendered valid ADF document with unsupported content replaced](https://dac-static.atlassian.com/platform/forge/ui-kit/images/adfRenderer/adfRenderer-unsupported-content-replaced-complex.png?_v=1.5800.1869)

```
```
1
2
```



```
import { AdfRenderer } from "@forge/react";

export const AdfRendererMultipleContentTypesExample = () => {
  const replaceUnsupportedNode = (node) => {
    if (node.type.toLowerCase().includes("extension")) {
      // Show a message for all extension node types
      return {
        type: "paragraph",
        content: [
          {
            type: "text",
            text: "Unsupported macro",
          },
        ],
      };
    } else if (node.type === "emoji") {
      // Show the emoji's default textual representation as-is
      return undefined;
    }

    // Hide everything else
    return false;
  };

  const simpleDocumentToRender = {
    type: "doc",
    version: 1,
    content: [
      {
        type: "paragraph",
        content: [
          {
            type: "emoji",
            attrs: {
              shortName: ":custom-emoji-hello:",
              id: "1e35b00f-cb17-4d28-91a5-ad38700715ae",
              text: ":hello!:",
            },
          },
          {
            type: "bodiedExtension",
            attrs: {
              extensionType: "com.atlassian.fabric",
              extensionKey: "clock",
            },
            content: [
              {
                type: "paragraph",
                content: [
                  {
                    type: "text",
                    text: "This is the default content of the extension",
                  },
                ],
              },
            ],
          },
        ],
      },
    ],
  };

  return (
    <AdfRenderer
      document={simpleDocumentToRender}
      replaceUnsupportedNode={replaceUnsupportedNode}
    />
  );
};
```
```
