# Keyboard shortcuts

Keyboard shortcuts, also known as accelerators, are memorable key combinations that can be used
to access commonly used functionality without having to find and interact with it on the user interface.
Adding a keyboard shortcut to a Forge module can help bring greater accessibility and adoption to a Forge
app due to users being able to trigger a specific Forge module more quickly, easily, and memorably.

With a keyboard shortcut, a user can go to a page, such as a `spacePage` or a `globalPage`, or trigger a
specific Forge module such as a `contentAction` or a `contentBylineItem` module when viewing a page. A Forge
module can be accessed via keyboard shortcut, so long as it is within view. For example, a `globalSettings` module
is not available on the Home page, so it couldn't be accessed with a keyboard shortcut since it is not within view.
However, it would be available if a user were viewing the General Settings page.

This functionality is provided by adding a `keyboardShortcut` property in the manifest to the specific module that
is getting an accelerator associated with it. The `keyboardShortcut` property is an object that contains the
`accelerator` and an optional `description` property.

Currently, keyboard shortcuts are only available in the following Confluence modules:

* `confluence:contentAction`
* `confluence:contentBylineItem`
* `confluence:contextMenu`
* `confluence:globalPage`
* `confluence:globalSettings`
* `confluence:homepageFeed`
* `confluence:spacePage`
* `confluence:spaceSettings`

If there exists a conflict between a Forge keyboard shortcut and one that is currently being
used by Confluence, Confluence will receive priority over that accelerator. For a comprehensive list of these
shortcuts, see the `Keyboard shortcuts` dialog in the Help sidebar on Confluence.

## Properties

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `accelerator` | `string` | Yes | Keyboard key(s)/combination(s) used to trigger this module. |
| `description` | `string` or `i18n object` |  | The description of the keyboard shortcut.  The `i18n object` allows for translation. See [i18n object](#i18n-object). |

### i18n object

| Key | Type | Required | Description |
| --- | --- | --- | --- |
| `i18n` | `string` | Yes | A key referencing a translated string in the translation files. For more details, see [Translations](/platform/forge/manifest-reference/translations). |

## Accelerator validation

In order to have a valid keyboard shortcut accelerator, the accelerator must:

1. Be non-empty string
2. Not have empty spaces on left or right of `+` character
   * `ctrl + g`, `ctrl+ g`, or `ctrl +g`
3. Have unique keys per key combination
   * `ctrl+g` as opposed to `ctrl+ctrl`
4. Have valid keys
   * Any of the [special](#special-keys) / [modifier](#modifier-keys) keywords or any single
     keyboard key that is not a `+` or empty space character
5. Have only one non-modifier key
6. Have the non-modifier key as the last in a combination with modifier keys
7. Be unique across other modules in the same manifest

### Single key

To map a keyboard shortcut to a single key, set the `accelerator` property to that character. For
example, to use the key `u` as a shortcut, set the configuration as:

```
```
1
2
```



```
modules:
  confluence: ...
    - key: ...
      ...
      keyboardShortcut:
        accelerator: u
```
```

If using a single number key as an accelerator, the accelerator should be wrapped with single or double quotes.
For example, to use the key `5` as a keyboard shortcut, set the value of the accelerator as `'5'` instead of just `5`.

### Key combination

A key combination is where a key is pressed with one or more modifier keys at the same time. The `accelerator`
property should be set to the desired keys, separated by a `+` character and no spaces. For example, to use the
combination of `ctrl` and `1` at the same time, set the configuration as:

```
```
1
2
```



```
modules:
  confluence: ...
    - key: ...
      ...
      keyboardShortcut:
        accelerator: ctrl+1
```
```

Note that the two keys must be unique, so `ctrl+ctrl` would be invalid, as well as `shift+2+shift`.

As far as spacing goes, there should not be any spaces between the keys. So `ctrl +1`, `ctrl+ 1`, and `ctrl + 1`
would also be invalid.

When modifying a key, there should only be one non-modifier key in a combination. For example, `a+b` would be
an invalid combination because `a` and `b` are both non-modifier keys. Similarly, `ctrl+c+d` would be an invalid
combination because `c` and `d` are both non-modifier keys. See the [list of modifier keys](#modifier-keys).

### Key sequence

A key sequence is where two or more keys or key combinations are pressed in sequence, or one after the other.
The `accelerator` property should be set to the desired key(s)/combination(s), separated by a single empty
space character. For example, to use the sequence of `1` and then `2`, set the configuration as:

```
```
1
2
```



```
modules:
  confluence: ...
    - key: ...
      ...
      keyboardShortcut:
        accelerator: 1 2
```
```

## Example

```
```
1
2
```



```
modules:
  confluence:contentAction:
    - key: content-action
      function: func-content-action
      title: My Content Action
      keyboardShortcut:
        accelerator: ctrl+1
  confluence:contentBylineItem:
    - key: content-byline-item
      function: func-content-byline-item
      title: My Content ByLine Item
      keyboardShortcut:
        accelerator: command+shift+1 shift+2
  function:
    - key: func-content-action
      handler: index.contentAction
    - key: func-content-byline-item
      handler: index.contentBylineItem
```
```

## Modifier keys

| Keyboard key | Accelerator keyword | Notes |
| --- | --- | --- |
| Control key | `ctrl` | Maps to `control` key on Mac and `ctrl` key on Windows/Linux. |
| Option or Alt key | `option` / `alt` | Both accelerator keywords map to `option` key on Mac and `alt` key on Windows / Linux. |
| Command or Windows Start key | `command` / `meta` | Both accelerator keywords map to `cmd` key on Mac and `start` key on Windows / Linux. |
| Cross-platform Command / Ctrl key | `mod` | Will map to `cmd` key on Mac and `ctrl` key on Windows/Linux. |
| Shift key | `shift` |  |

## Special keys

| Keyboard key | Accelerator keyword | Notes |
| --- | --- | --- |
| Return or Enter key | `return` / `enter` | Either keyword will work for both keys. |
| Escape key | `escape` / `esc` |  |
| Backspace key | `backspace` |  |
| Tab key | `tab` |  |
| Insert key | `ins` | Key is not available in Mac keyboards. |
| Delete key | `del` |  |
| Spacebar | `space` |  |
| Plus key | `plus` | The keyword `plus` is used because `+` is used to create key combinations with modifiers. i.e. `ctrl+1` |
| Caps Lock key | `capslock` | No space in between words. |
| Page Up key | `pageup` | No space in between words. |
| Page Down key | `pagedown` | No space in between words. |
| Home key | `home` |  |
| End key | `end` |  |
| Arrow keys | `left`, `up`, `right`, `down` |  |
| Function keys | `f1`, `f2`, ... , `f12` |  |
