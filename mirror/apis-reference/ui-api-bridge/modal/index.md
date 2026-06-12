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
  size?: 'small' | 'medium' | 'large' | 'xlarge' | 'max' | 'fullscreen' | 'resizable';
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
  * **fullscreen** - w: `100vw` h: `100vh` (fills entire viewport, and `title` and `icon` will be displayed in the header)
  * **resizable** - w: `auto` h: `auto` minHeight: `320px` minWidth: `400px` maxHeight: `100%` maxWidth: `calc(100vw - 120px)`
* **context**: Custom context that can be added to the context in the modal resource. It will appear
  under the `extension.modal` key in the context object returned from `view.getContext()`.
* **closeOnEscape**: If set to false, the modal will not close when pressing escape.
* **closeOnOverlayClick**: If set to false, the modal will not close when clicking the overlay.
* **title**: If provided, the modal will render a header with the title and a close button.
* **icon**: If provided, the modal will render a header with an icon next to the title, and a close button.

## Resizable design guidelines

The resizable size behaviour has been provided to accommodate apps with content-driven sizing — for example, rendering a list with an unknown number of items. We recommend using this as a last resort over fixed modal dimensions, to avoid unexpected layout shifts and a jarring user experience.
To ensure the iframe resizes to your app's content rather than the document's default full-width body, you may need to explicitly set `width: fit-content` on your top-level container, for example `body { width: fit-content; }`

If your app imports `@atlaskit/css-reset`, be aware that it sets `width: 100%` on the `body` and `html` elements, overriding the `width: fit-content` recommendation above. To make sure your custom style takes effect, either:

* add `!important` to your inline styling, for example `body { width: fit-content !important; }`, or
* import `@atlaskit/css-reset` before your own stylesheet so your styles take precedence:

```
```
1
2
```



```
import '@atlaskit/css-reset';
import './index.css';
```
```

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
