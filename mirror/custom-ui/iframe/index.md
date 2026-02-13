# Custom UI iframe

All [Custom UI](/platform/forge/custom-ui/) apps are run within an iframe. This provides a secure and isolated hosting environment for custom-built
user interfaces. This page describes the preset permissions of the iframe.

## iframe permissions

The following permissions are applied to the iframe by default and cannot be modified by the developer of the Forge application.

### Feature policies

A number of feature policies are specified for the Custom UI iframe. These policies define the features that are available to the iframe based on the origin of the request.

The following table lists the feature policies configured for the Custom UI iframe.

| Feature policy | Description |
| --- | --- |
| camera | Allows the use of video input devices. |
| clipboard-write | Allows data to be written to the clipboard. |
| display-capture | Allows the use of the [Screen Capture API](https://developer.mozilla.org/en-US/docs/Web/API/Screen_Capture_API). |
| fullscreen | Allows the use of the [Element.requestFullscreen()](https://developer.mozilla.org/en-US/docs/Web/API/Element/requestFullscreen) function. |
| microphone | Allows the use of audio input devices. |

### Sandbox restrictions

The iframe also has a set of `sandbox` attributes that enable extra restrictions for the content in the iframe.

The following table lists the `sandbox` attributes applied to the Custom UI iframe.

| Sandbox attribute | Description |
| --- | --- |
| allow-downloads | Allows downloads to be started via a user gesture. |
| allow-forms | Allows the resource to submit forms. |
| allow-modals | Allows the resource to open modal windows. |
| allow-pointer-lock | Allows the resource to use the [Pointer Lock API](https://developer.mozilla.org/en-US/docs/Web/API/Pointer_Lock_API). |
| allow-same-origin | Allows the iframe content to be treated as being from the same origin as its parent. |
| allow-scripts | Allows the resource to run scripts, but not create pop-up windows. |
