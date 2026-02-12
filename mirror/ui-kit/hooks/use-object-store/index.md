# useObjectStore (EAP)

UI components for [Forge Object Store](/platform/forge/storage-reference/object-store/)
are now available as part of our Early Access Program (EAP). These components can also be
used for remote object store back-ends. To start testing,
[sign up here](https://ecosystem.atlassian.net/servicedesk/customer/portal/1040/group/3496/create/18937).

By signing up for this Early Access Program (“EAP”), you acknowledge that use of the Forge Object Store UI Components is governed by the [Atlassian Developer Terms](https://developer.atlassian.com/platform/marketplace/atlassian-developer-terms/). The Forge Object Store UI Components are considered “Early Access Materials”, as set forth in Section 10 of the Atlassian Developer Terms and is subject to applicable terms, conditions, and disclaimers.

For more details, see [Forge EAP, Preview, and GA](/platform/forge/whats-coming/#eap).

# Supported Modules

This is supported in Bitbucket, Confluence, Jira, and Jira Service Management modules during EAP.

The `useObjectStore` hook lets you perform file management operations and track the state of each objects. This hook provides a way for your
app's frontend to interact with the [Forge Object Store](/platform/forge/storage-reference/object-store/) through the the
[objectStore bridge API](/platform/forge/custom-ui-bridge/objectStore/).

The following diagram shows how the hook integrates the backend resolver with the
[File picker](/platform/forge/ui-kit/components/file-picker/) and [File card](/platform/forge/ui-kit/components/file-card/):

![Diagram of how the hook interacts with the resolver and File components](https://dac-static.atlassian.com/platform/forge/ui-kit/images/hook/useObjectStore.png?_v=1.5800.1846)

[Example app

We published a sample app to demonstrate the basics of implementing object storage features in
a Forge app. This sample app uses the Forge Object Store as its backend and available Forge UI components
for its frontend. Refer to the app's README for additional guidance on exploring and testing the code.](https://bitbucket.org/atlassian/forge-ui-object-store-example-app/src/main/)

## Before you begin

Make sure you have the following:

* The latest version of Forge CLI (`^12.8.0`). To update your CLI version, run `npm install -g @forge/cli@latest`
  on the command line.
* The latest version of UI Kit (`^11.7.0`). To update your version, navigate to the app's top-level
  directory, and run `npm install @forge/react@latest --save` on the command line.

## Usage

To add the `useObjectStore` hook to your app:

```
```
1
2
```



```
import { useObjectStore } from "@forge/react";
```
```

The following example shows a file manager app using `useObjectStore`:

```
```
1
2
```



```
import React from 'react';
import ForgeReconciler, { 
  Heading, 
  Stack,
  FilePicker,
  FileCard,
  useObjectStore 
} from '@forge/react';

const FileManager = () => {
  const { 
    objectStates, 
    uploadObjects, 
    deleteObjects, 
    downloadObjects
  } = useObjectStore();

  const handleFileChange = async (files) => {
    const base64Objects = files.map(file => ({
      data: file.data,
      mimeType: file.type
    }));
    
    try {
      await uploadObjects({
        functionKey: 'generateUploadUrls',
        objects: base64Objects
      });
    } catch (error) {
      // Handle error
    }
  };

  const handleDownload = async (key: string) => {
    try {
      const results = await downloadObjects({
        functionKey: 'generateDownloadUrls',
        keys: [key]
      });
      
      const result = results[0];
      if (result?.success && result?.blob) {
        return result.blob;
      }
    } catch (error) {
      // Handle error
    }
  };

  const handleDelete = async (key: string) => { 
    try {
      await deleteObjects({
        functionKey: 'deleteObject',
        keys: [key]
      });
    } catch (error) {
      // Handle error
    }
  };

  return (
    <Stack>
      <Heading as='h3'>File Manager</Heading>
      
      <FilePicker 
        onChange={handleFileChange}
        label="Upload Files"
        description="Select files to upload to object store"
      />

      <Stack>
        {objectStates.map((object) => {
          const fileName = object.key.split('/').pop() || object.key;
          return (
            <FileCard
              key={object.key}
              fileName={fileName}
              fileSize={object.objectSize}
              fileType={object.objectType}
              isUploading={object.isUploading}
              error={object.error}
              onDownload={object.success && !object.isUploading ? () => handleDownload(object.key) : undefined}
              onDelete={object.success && !object.isUploading ? () => handleDelete(object.key) : undefined}
            />
          );
        })}
      </Stack>
    </Stack>
  );
};

ForgeReconciler.render(
  <React.StrictMode>
    <FileManager />
  </React.StrictMode>
);
```
```

## Function signature

```
```
1
2
```



```
function useObjectStore(props?: UseObjectStoreProps): {
  objectStates: ObjectState[];
  getObjectMetadata: (key: string) => ObjectState | null;
  uploadObjects: (params: UploadParams) => Promise<void>;
  deleteObjects: (params: DeleteParams) => Promise<void>;
  downloadObjects: (params: DownloadParams) => Promise<DownloadResult[]>;
}

interface UseObjectStoreProps {
  defaultValues?: ObjectState[];
}

interface ObjectState {
  /** The unique identifier for the object (required) */
  key: string;
  /** Whether the last operation on this object was successful */
  success?: boolean;
  /** HTTP status code from the last operation */
  status?: number;
  /** Error message if an operation failed */
  error?: string;
  /** Whether the object is currently being uploaded */
  isUploading?: boolean;
  /** Whether the object is currently being downloaded */
  isDownloading?: boolean;
  /** Whether the object is currently being deleted */
  isDeleting?: boolean;
  /** Type information about the object */
  objectType?: string;
  /** Size of the object in bytes */
  objectSize?: number;
}

interface UploadParams {
  functionKey: string;
  objects: Blob[] | Base64Object[];
}

interface Base64Object {
  data: string;
  mimeType?: string;
}

interface DeleteParams {
  functionKey: string;
  keys: string[];
}

interface DownloadParams {
  functionKey: string;
  keys: string[];
}

interface UploadResult {
  success: boolean;
  key: string;
  status?: number;
  error?: string;
}

interface DownloadResult {
  success: boolean;
  key: string;
  blob?: Blob;
  status?: number;
  error?: string;
}
```
```

## Arguments

* **props** (optional): Configuration object for the hook.
  * **defaultValues** (optional): An array of `ObjectState` objects to initialize the hook with. These represent objects that already exist or have been previously uploaded.

## Returns

The hook returns an object with the following properties:

* **objectStates**: An array of `ObjectState` objects representing all tracked objects. Each object includes:

  * **key** (required): The unique identifier for the object
  * **success** (optional): Whether the last operation on this object was successful
  * **status** (optional): HTTP status code from the last operation
  * **error** (optional): Error message if an operation failed
  * **isUploading** (optional): Whether the object is currently being uploaded
  * **isDownloading** (optional): Whether the object is currently being downloaded
  * **isDeleting** (optional): Whether the object is currently being deleted
  * **objectType** (optional): Type information about the object
  * **objectSize** (optional): Size of the object in bytes
* **getObjectMetadata**: A function that retrieves metadata for a specific object by its key. Returns the `ObjectState` object if found, or `null` if not found.
* **uploadObjects**: An async function that uploads objects to the object store. Takes `UploadParams`:

  * **functionKey**: The key of the resolver function that generates pre-signed upload URLs
  * **objects**: An array of `Blob` objects or `Base64Object` objects to upload

  The function automatically tracks upload progress and updates the state for each object. Temporary keys are used during upload and replaced with actual keys upon successful completion. Upload results are available in the `objectStates` array, where each object contains the `UploadResult` information (success, key, status, error), `objectType` and `objectSize`.
* **deleteObjects**: An async function that deletes objects from the object store. Takes `DeleteParams`:

  * **functionKey**: The key of the resolver function that handles deletion
  * **keys**: An array of object keys to delete

  The function updates the state to mark objects as being deleted, and removes them from the state upon successful deletion.
* **downloadObjects**: An async function that downloads objects from the object store. Takes `DownloadParams`:

  * **functionKey**: The key of the resolver function that generates pre-signed download URLs
  * **keys**: An array of object keys to download

  Returns a Promise that resolves to an array of `DownloadResult` objects, each containing the download result for the corresponding key. The function updates the `objectState` for each object by setting `isDownloading` to `true` during the download, and `false` when complete. If a download fails, `error` is also set. Note that `success` and other fields are not updated for download operations.
