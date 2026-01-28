# File picker (EAP)

UI components for [Forge Object Store](/platform/forge/storage-reference/object-store/)
are now available as part of our Early Access Program (EAP). These components can also be
used for remote object store back-ends. To start testing,
[sign up here](https://ecosystem.atlassian.net/servicedesk/customer/portal/1040/group/3496/create/18937).

By signing up for this Early Access Program (“EAP”), you acknowledge that use of the Forge Object Store UI Components is governed by the [Atlassian Developer Terms](https://developer.atlassian.com/platform/marketplace/atlassian-developer-terms/). The Forge Object Store UI Components are considered “Early Access Materials”, as set forth in Section 10 of the Atlassian Developer Terms and is subject to applicable terms, conditions, and disclaimers.

For more details, see [Forge EAP, Preview, and GA](/platform/forge/whats-coming/#eap).

# Supported Modules

This is supported in Bitbucket, Confluence, Jira, and Jira Service Management modules during EAP.

To add the `FilePicker` component to your app:

```
1
import { FilePicker } from "@forge/react";
```

## Description

The file picker allows the user to select files stored locally.

You can use the [file card](/platform/forge/ui-kit/components/file-card/) component to display selected files (along with
information about each file and upload progress).

[Example app

We published a sample app to demonstrate the basics of implementing object storage features in
a Forge app. This sample app uses the Forge Object Store as its backend and available Forge UI components
for its frontend. Refer to the app's README for additional guidance on exploring and testing the code.](https://bitbucket.org/atlassian/forge-ui-object-store-example-app/src/main/)

## Props

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| `description` | `string` | No | Additional helper text shown below the file picker to guide users. |
| `label` | `string` | No | Label displayed above the file picker. |
| `onChange` | `(files: SerializedFile[]) => void` | No | Callback triggered when files are selected; receives an array of serialized files. |

## Examples

### Default

The `onChange` property receives an array of serialized files and can be used to manage the selected files:

```
```
1
2
```



```
type SerializedFile = {
  data: string;
  name: string;
  size: number;
  type: string;
}
```
```

![Example image of file picker](https://dac-static.atlassian.com/platform/forge/ui-kit/images/file-picker/file-picker.png?_v=1.5800.1801)

```
```
1
2
```



```
export const FilePickerExample = () => {
  const [files, setFiles] = useState([]);

  const onChange = (files) => {
    const unserializedFiles = ...
    setFiles(unserializedFiles);
  };

  return <FilePicker onChange={onChange} />;
};
```
```

### Additional Elements

Use `label` to display text above the file picker input zone, helping users identify the purpose of the field. Use `description` to provide additional helper text (for example, allowed file types or size limits).

![Example image of file picker with additional elements](https://dac-static.atlassian.com/platform/forge/ui-kit/images/file-picker/file-picker-with-elements.png?_v=1.5800.1801)

```
```
1
2
```



```
const FilePickerWithElementsExample = () => {
  return (
    <FilePicker 
      label="Attachment"
      description="Hint text for file requirements"
    />
  );
};
```
```
