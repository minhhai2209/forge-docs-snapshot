# Storing, downloading, and deleting large objects

Forge Object Store is now available as part of our Early Access Program (EAP). To start testing this feature, sign up using this [form](https://ecosystem.atlassian.net/servicedesk/customer/portal/3422/group/3571/create/18555).

Forge Object Store is an experimental feature offered for testing and feedback purposes. This feature is unsupported and subject to change without notice. Do not use Forge Object Store in apps that handle sensitive information, including personal data and customer data.

For more details, see [Forge EAP, Preview, and GA](https://developer.atlassian.com/platform/forge/whats-coming/#eap).

The Forge Object Store API lets you upload, download, and manage large items (like data objects and media files) directly from your app. This API also lets you create pre-signed URLs for download and upload requests.

To start using the Forge Object Store, add the required package (`@forge/os`) to your project first:

Then, import the package to your app, as follows:

```
1
import os from '@forge/os'
```

To integrate the Forge Object Store with your app's frontend, use the [objectStore](/platform/forge/custom-ui-bridge/objectStore/) bridge methods.

## Limitations

The Forge Object Store has the following limitations during the EAP:

### EAP limitations

The Forge Object Store EAP is only available for testing purposes; apps using this feature can't be deployed to production.
In addition, objects stored during EAP will have a time-to-live (TTL) of 90 days.

**All stored objects will be deleted at the end of the EAP.** Atlassian will provide notice before the end of the EAP to ensure you have time to download any stored
data.

### Rate limits per installation

If the following rate limits are exceeded, Forge will return a `TOO_MANY_REQUESTS` error.

| Parameter | Limit |
| --- | --- |
| Object Store requests per second | 5000 |
| Pre-signed URL requests per second | 1000 |

### Operation limits

When building interfaces for object download/uploads, you must use the available
[frontend components](/platform/forge/storage-reference/object-store/#frontend-components)

| Parameter | Limit |
| --- | --- |
| Storage limits | Objects size can be up to 1 GB each. |
| Payload limits | The maximum payload size for all operations is 10 kB. |
| Pre-signed URL validity | Pre-signed URLs are valid for a maximum of 1 hr. |

Retrieve the metadata for objects stored in the Forge-hosted object store using the `get` method.

This method works as follows:

* `key` (string): The unique identifier for the object metadata to retrieve.
* **Returns**: The `objectReference` if found, or `undefined` if the object does not exist.

To integrate with the frontend, use the `objectStore` bridge API's [get](/platform/forge/custom-ui-bridge/objectStore/#getmetadata) method.

### Method signature

```
```
1
2
```



```
os.get(key: string): Promise<ObjectReference | undefined>;

interface ObjectReference {
  key: string;
  checksum: string;
  size: number;
  createdAt?: string;
  currentVersion?: string;
}
```
```

### Example

```
```
1
2
```



```
export const getObjectRef = async (key: string): Promise<ObjectReference | undefined> => {
  try {
    const objectRef = os.get(key);
    if (objectRef === undefined) {
      console.info('Object was not found',  { key })
    }
    return objectRef
  } catch (error) {
    console.error('Error getting object reference', JSON.stringify(error))
  }
};
```
```

## Delete

Remove objects from the Forge-hosted object store using the `delete` method.

The `delete` method works as follows:

* `key` (string): The unique identifier for the object to delete.

To integrate with the frontend, use the `objectStore` bridge API's [deleteObjects](/platform/forge/custom-ui-bridge/objectStore/#deleteobjects) method.

### Method signature

```
```
1
2
```



```
os.delete(key: string): Promise<void>;
```
```

### Example

```
```
1
2
```



```
export const deleteObject = async (key: string): Promise<void> => {
  try {
    await os.delete(key)
  } catch (error) {
    console.error('Error deleting object', JSON.stringify(error))
  }
}
```
```

## Create pre-signed download URL

Create a URL with temporary permissions to download a specific object to a client using the `createDownloadUrl` method.
The created URL will expire after 1 hour.

To integrate with the frontend, use the `objectStore` bridge API's [download](/platform/forge/custom-ui-bridge/objectStore/#download) method.

Don’t store pre-signed URLs in a global context. Doing this could potentially let customer data persist across app invocations between different installations. See [Developer responsibilities](/platform/forge/function-reference/nodejs-runtime/#developer-responsibilities) for related information.

### Method signature

When generating a pre-signed download URL, you need to include the `key` (string) in your request. The `createDownloadUrl` method uses this as a unique identifier for your URL.

The method will then return a `PresignedUrlResponse`. The object's `content-type` will be what was specified  
via the [pre-signed upload URL](#method-signature-3); otherwise, the `content-type` will be `application/octet-stream`.

```
```
1
2
```



```
os.createDownloadUrl(key: string): Promise<PresignedUrlResponse | undefined>

interface PresignedUrlResponse {
  url: string;
}
```
```

Use a `GET` operation to download an object via the returned `PresignedUrlResponse`.
This `GET` operation accepts the `Range` header to download parts of the object.
For example, the following header will request the first 500 bytes of the object:

### Example

```
```
1
2
```



```
export const createDownloadUrl = async (key: string): Promise<PresignedUrlResponse | undefined> => {
  try {
    return await os.createDownloadUrl(key);
  } catch (error) {
    console.error('Error creating pre-signed download URL', JSON.stringify(error))
  }
};

export const downloadUsingUrl = async (objectId: string): Promise<any> => {
  const { url } = await createDownloadUrl(objectId);
  if (url) {
    const response = await fetch(url);
    if (response.ok) {
      return response;
    } else {
      console.error('Failed to download object: ', objectId);
    }
  }
};
```
```

## Create pre-signed upload URL

Create a URL with temporary permissions to upload a single object using the `createUploadUrl` method. Pre-signed upload URLs can only be used for objects under 1GB. The created URL will expire after 1 hour.

To integrate with the frontend, use the `objectStore` bridge API's [upload](/platform/forge/custom-ui-bridge/objectStore/##upload) method.

Don’t store pre-signed URLs in a global context. Doing this could potentially let customer data persist across app invocations between different installations. See [Developer responsibilities](/platform/forge/function-reference/nodejs-runtime/#developer-responsibilities) for related information.

### Method signature

When generating a pre-signed upload URL through `createUploadUrl`, your request must include an `UploadUrlBody` containing the properties of the file you’re uploading. These properties are:

* `key`: The unique identifier for the object.
* `length`: The byte size of the object.
* `checksum`: Hash digest of the file content, encoded as base64. Used to verify data integrity.
* `checksumType`: Algorithm used to generate the checksum.
* `ttlSeconds` (optional): Allows you to set a custom TTL for and object.
* `overwrite` (optional): Indicates whether to replace an existing object with the same key. This defaults to true.

The method will then return a `PresignedUrlResponse`.

```
```
1
2
```



```
os.createUploadUrl(body: UploadUrlBody): Promise<PresignedUrlResponse>

interface UploadUrlBody {
  key: string;
  length: number;
  checksum: string;
  checksumType: 'SHA1' | 'SHA256' | 'CRC32' | 'CRC32C';
  ttlSeconds?: number;
  overwrite?: boolean;
}

interface PresignedUrlResponse {
  url: string;
}
```
```

Use a `PUT` operation to upload an object via the returned `PresignedUrlResponse`.
This `PUT` operation does not require any additional headers.

However, we strongly advise that you send the `content-type` header,
as this value will be retained on the object and returned when downloaded. By default, objects will use `application/octet-stream`
as their `content-type` header.

### Example

```
```
1
2
```



```
export const createUploadUrl = async (key: string, object: any, objectLength: number, ttlSeconds?: number): Promise<PresignedUrlResponse | undefined> => {
  try {
    const bufferedObject = Buffer.from(object)
    // Create SHA256 checksum from buffer
    const checksum = crypto.createHash('sha256').update(bufferedObject).digest('base64');
    const body: UploadUrlBody = {
      key: key,
      length: objectLength,
      checksum,
      checksumType: 'SHA256',
      ttlSeconds,
      overwrite: true,
    };
    const resp = await os.createUploadUrl(body);
    return resp;
  } catch (error) {
    console.error('Error creating pre-signed upload URL', JSON.stringify(error))
  }
};

export const uploadUsingUrl = async (uploadObjectProperties: any): Promise<void> => {
  const { objectId, object, objectLength, ttlSeconds } = uploadObjectProperties
  const { url } = await createUploadUrl(objectId, object, objectLength, ttlSeconds);
  if (url) {
    const response = await fetch(url, {
      method: 'PUT',
      headers: {
        'content-type': 'application/octet-stream', // or the actual content type of your object
      },
      body: object,
    });
    if (!response.ok) {
      console.error('Failed to upload object: ', objectId);
    }
  }
};
```
```

## Deprecated methods

The following methods are now deprecated, and will be removed once Forge Object Store transitions to [Preview](/platform/forge/whats-coming/#forge-preview).

### Upload/Update object

Store large files or media efficiently from your app using the Forge-hosted storage.
Use the `put` method to upload an object with the following parameters:

* `key` (string): A unique identifier for the object being stored. If an object already exists with the same `key`, the new upload will add a new version of the object, effectively functioning as an update operation.
* `object` (any): The data to be stored, which is buffered internally for efficient handling.
* `ttlSeconds` (number): Allows you to set a custom TTL for an object. If no TTL is set, the object's TTL will default to 90 days. Custom TTLs must be greater than 1 second and can't exceed 90 days.

#### Method signature

```
```
1
2
```



```
os.put(key: string, object: any, ttlSeconds?: number): Promise<void>;
```
```

#### Example

```
```
1
2
```



```
export const uploadObject = async (key: string, object: any, ttlSeconds?: number): Promise<void> => {
  try {
    const bufferedObject = Buffer.from(object)
    await os.put(key, bufferedObject, ttlSeconds)
  } catch (error) {
    console.error('Error uploading object', JSON.stringify(error))
  }
}
```
```

### Download

Retrieve the data of the latest version of an object stored in the Forge Object Store using the `download` method.

The `download` method works as follows:

* `key` (string): The unique identifier for the object to download.
* **Returns**: A `Buffer` containing the latest object data if it exists, or `undefined` if the object is not found.

#### Method signature

```
```
1
2
```



```
os.download(key: string): Promise<Buffer | undefined>;
```
```

#### Example

```
```
1
2
```



```
export const downloadObject = async (key: string): Promise<Buffer | undefined> => {
try {
    const object = os.download(key);
    if (object === undefined) {
      console.info('Object was not found',  { key })
    }
    return object
  } catch (error) {
    console.error('Error downloading object', JSON.stringify(error))
  }
}
```
```

## EAP Feedback

As part of the EAP, your feedback is invaluable in shaping the future of this feature. We encourage you to explore Forge Object Store's capabilities and share your insights to help us refine and enhance this service.
