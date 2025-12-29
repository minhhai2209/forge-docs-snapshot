# Jira global background script (Preview)

This section describes a Forge *preview* feature. Preview features are deemed stable;
however, they remain under active development and may be subject to shorter deprecation
windows. Preview features are suitable for early adopters in production environments.

We release preview features so partners and developers can study, test, and integrate
them prior to General Availability (GA). For more information,
see [Forge release phases: EAP, Preview, and GA](/platform/forge/whats-coming/#preview).

The `jira:globalBackgroundScript` module adds an invisible container that can coordinate data and behavior across all pages on Jira. This makes it the perfect candidate for.

* distributing shared data
* making heavy calculations
* other optimizations

## Examples

Use the [events](/platform/forge/custom-ui-bridge/events/) API for communication between
global background scripts and other modules, such as custom fields. Because modules may be rendered in a different order, we recommend handling both scenarios where the background script loads before or after the consumer.

Below is an example with a dropdown-based custom field that emits an event when its value changes. The global background script listens for this event and displays a [flag](/platform/forge/custom-ui-bridge/showFlag/) when the selected value is "flag".

Global background script (listens and responds to field events):

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
16
17
18
19
20
21
22
import { events, showFlag } from "@forge/bridge";

// Optionally, announce that the background script is ready
events.emit("app.bg.ready");

// React to field-level changes from the dropdown
events.on("app.field-change", (payload) => {
  // Perform side effects or coordinate shared state
  // For example, broadcast to other interested modules
  const value = payload?.value;
  events.emit("app.data-change", { value });

  // Show a flag when the selected value is "flag"
  if (value === "flag") {
    showFlag({
      title: "Special value selected",
      description: "You selected the dropdown value 'flag'.",
      appearance: "info", // 'info' | 'success' | 'warning' | 'error'
      isAutoDismiss: true,
    });
  }
});
```

Custom field (edit) module with dropdown menu (emits changes that the background script can react to):

```
```
1
2
```



```
import { events } from "@forge/bridge";
import { Select } from "@forge/react";
import { useState } from "react";

export default function CustomFieldEdit({ onSave }) {
  const options = [
    { label: "Flag", value: "flag" },
    { label: "Alpha", value: "alpha" },
    { label: "Beta", value: "beta" },
  ];
  const [value, setValue] = useState(options[0].value);

  const handleChange = (val) => {
    setValue(val);
    // Notify background script of field changes
    events.emit("app.field-change", { value: val });
  };

  useEffect(() => {
    // if global background script loads before custom field
    events.on("app.bg.ready", () => {
      events.emit("app.field-change", { value });
    });
  }, [value]);

  return (
    <Select
      options={options}
      value={value}
      onChange={handleChange}
      placeholder="Choose a value"
    />
  );
}
```
```

### Manifest

```
```
1
2
```



```
modules:
  jira:globalBackgroundScript:
    - key: global-background-script-with-fcf-demo
      resource: main
      render: native
  jira:customField:
    - key: global-background-script-custom-field-ui-kit
      name: Custom Field with Events
      description: Jira Custom field that sends events to global background script
      type: string
      view:
        render: native
        resource: custom-field
        experience:
          - issue-view
          - portal-view
      edit:
        resource: custom-field-edit
        render: native
        isInline: true
        experience:
          - issue-create
          - issue-transition
          - issue-view
```
```

## Properties

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `key` | `string` | Yes | A key for the module, which other modules can refer to. Must be unique within the manifest.   *Regex:* `^[a-zA-Z0-9_-]+$` |
| `resource` | `string` | Yes | A reference to the static `resources` entry that your context menu app wants to display. See [resources](/platform/forge/manifest-reference/resources) for more details. |
| `render` | `'native'` | Yes for [UI Kit](/platform/forge/ui-kit/components/) | Indicates the module uses [UI Kit](/platform/forge/ui-kit/components/). |
| `resolver` | `{ function: string }` or `{ endpoint: string }` | Yes | Set the `function` property if you are using a hosted `function` module for your resolver.  Set the `endpoint` property if you are using [Forge Remote](/platform/forge/forge-remote-overview) to integrate with a remote back end. |

## Extension context

| Property | Type | Description |
| --- | --- | --- |
| `type` | `string` | The type of the module. |
| `location` | `string` | The full URL of the host page where this module is displayed. |
