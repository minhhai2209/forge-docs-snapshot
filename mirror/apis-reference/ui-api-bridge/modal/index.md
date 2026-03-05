# Modal

The `Modal` class enables your Custom UI app to open a modal dialog with a specified resource.

The Modal bridge API is exclusive to Custom UI; If you are using UI Kit, you can use the UI Kit [Modal](/platform/forge/ui-kit/components/modal/) component instead.

## Class signature

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
11
12
13
14
15
interface ModalOptions {
  resource?: string | null;
  onClose?: (payload?: any) => any;
  size?: 'small' | 'medium' | 'large' | 'xlarge' | 'max';
  context?: any;
  closeOnEscape?: boolean;
  closeOnOverlayClick?: boolean;
  title?: string;
  icon?: string;
}

class Modal {
  constructor(opts?: ModalOptions);
  open(): Promise<void>;
}
```

## Arguments

* **resource**: The key of the static resource to open in the modal dialog. If not provided, resource
  defaults current resource.
* **onClose**: A callback function to run when the modal dialog is closed. The function accepts an
  optional payload that is passed when calling `view.close(payload)` from inside the modal resource.
* **size**: The size of the modal dialog.

  * **small** - w: `400px` h: `20vh` minHeight: `320px`
  * **medium** - w: `600px` h: `40vh` minHeight: `520px`
  * **large** - w: `800px` h: `70vh` minHeight: `720px`
  * **xlarge** - w: `968px` h: `90vh`
  * **max** - w: `100%` h: `100%`
  * [**fullscreen**](#fullscreen-eap) - w: `100vw` h: `100vh` (fills entire viewport)
* **context**: Custom context that can be added to the context in the modal resource. It will appear
  under the `extension.modal` key in the context object returned from `view.getContext()`.
* **closeOnEscape**: If set to false, the modal will not close when pressing escape.
* **closeOnOverlayClick**: If set to false, the modal will not close when clicking the overlay.
* **title**: If provided, the modal will render a header with the title and a close button.
* **icon**: If provided, the modal will render a header with an icon next to the title, and a close button.

`fullscreen` viewport sizing is now available for Confluence and Jira as part of our Early Access Program (EAP). This allows your `@forge/bridge` modal to fill the entire viewport. You can also provide a `title` and an `icon` to display in the header. To start testing, [sign up here](https://ecosystem.atlassian.net/servicedesk/customer/portal/1040/group/3496/create/18983). To use these features, run `npm install -g @forge/cli@latest` in your terminal.

By signing up for this Early Access Program (“EAP”), you acknowledge that use of the Forge Full Page Modals is governed by the [Atlassian Developer Terms](https://developer.atlassian.com/platform/marketplace/atlassian-developer-terms/). The Forge Full Page Modals are considered “Early Access Materials”, as set forth in Section 10 of the Atlassian Developer Terms and is subject to applicable terms, conditions, and disclaimers.

For more details, see [Forge EAP, Preview, and GA](/platform/forge/whats-coming/#eap).

## Example

Implementing a Custom UI modal requires two files:

1. the `index.js` file in your app logic
2. the resource file you defined in the manifest file, which is the `my-modal-resource.js` file
   in the example below

**`index.js`**

```
```
1
2
```



```
import { Modal } from '@forge/bridge';

const modal = new Modal({
  resource: 'my-modal-resource',
  onClose: (payload) => {
    console.log('onClose called with', payload);
  },
  size: 'medium',
  context: {
    customKey: 'custom-value',
  },
  title: 'My Modal',
  icon: './icon.png'
});

modal.open();
```
```

**`my-modal-resource.js`**

```
```
1
2
```



```
import { view } from '@forge/bridge';

const context = await view.getContext();
const customValue = context.extension.modal.customKey;

view.close({
  formValues: [],
});
```
```
