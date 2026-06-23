# Storing, downloading, and deleting large objects

Forge Object Store is now in Preview, and therefore fully supported. However, it remains under active development and may be subject to shorter deprecation windows. Preview features are suitable for early adopters in production environments.

We release preview features so partners and developers can study, test, and integrate them prior to General Availability (GA). For more details, see [Forge EAP, Preview, and GA](https://developer.atlassian.com/platform/forge/whats-coming/#forge-preview).

The Forge Object Store API lets you upload, download, and manage large items (like data objects and media files) directly from your app. This API also lets you create pre-signed URLs for download and upload requests.

To start using the Forge Object Store, add the required package (`@forge/object-store`) to your project first:

```
1
npm install @forge/object-store
```

Then, import the package to your app, as follows:

```
1
import fos from '@forge/object-store'
```

To integrate the Forge Object Store with your app's frontend, use the [objectStore](/platform/forge/custom-ui-bridge/objectStore/) bridge methods.

## Limitations

The Forge Object Store has the following limitations:

### Rate limits per installation

If the following rate limits are exceeded, Forge will return a `TOO_MANY_REQUESTS` error.

| Parameter | Limit |
| --- | --- |
| Object Store requests per minute | 5000 |
| Pre-signed URL requests per second | 1000 |

### Operation limits

When building interfaces for object download/uploads, you must use the available
[frontend components](/platform/forge/storage-reference/object-store/#frontend-components).

| Parameter | Limit |
| --- | --- |
| Maximum object size | 1 GB |
| Maximum request payload size | 1 kB |
| Pre-signed URL validity | 1 hour |

The maximum object size applies to objects uploaded through any [frontend component](/platform/forge/storage-reference/object-store/#frontend-components) used in conjunction with the Forge Object Store (for example, the `useObjectStore`
[UI Kit hook](/platform/forge/ui-kit/hooks/use-object-store/)).

Meanwhile, the maximum request payload size only applies to the actual [Forge Object Store request](/platform/forge/storage-reference/object-store-api/).
This request should only contain the object's name and other relevant metadata (not the object itself).

### Versioning

If you add Forge Object Store to an existing app, admins of that app's current installations must review and consent before updating.

As such, adding Forge Object Store to an existing app will require a [major version upgrade](/platform/forge/versions/#major-version-upgrades). This will be triggered through the `objectStore`
[module](/platform/forge/manifest-reference/modules/object-store/)
(which is required to enable the feature on an app).

Retrieve the metadata for objects stored in the Forge-hosted object store using the `get` method.

To integrate with the frontend, use the `objectStore` bridge API's [get](/platform/forge/custom-ui-bridge/objectStore/#getmetadata) method.

### Method signature

```
```
1
2
```



```
fos.get(key: string, options?: { cdn?: boolean }): Promise<ObjectReference | undefined>;

interface ObjectReference {
  key: string;
  checksum: string;
  size: number;
  createdAt?: string;
  updatedAt?: string;
  currentVersion?: string;
}
```
```

This method accepts the following properties:

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `key` | string | Yes | The unique identifier for the object metadata to retrieve. |
| `options` | object | No | Additional options for the request. |
| `options.cdn` | boolean | No | Whether to retrieve metadata from the CDN bucket (defaults to `false`). The CDN bucket is the storage bucket that backs CDN URLs — only objects uploaded to the CDN bucket can be served over the CDN. Objects stored in the default bucket cannot be shared via CDN URLs. |

**Returns:** The `ObjectReference` if found, or `undefined` if the object does not exist.

### Example

```
```
1
2
```



```
export const getObjectRef = async (key: string): Promise<ObjectReference | undefined> => {
  try {
    const objectRef = await fos.get(key);
    if (objectRef === undefined) {
      console.info('Object was not found', { key })
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

To integrate with the frontend, use the `objectStore` bridge API's [deleteObjects](/platform/forge/custom-ui-bridge/objectStore/#deleteobjects) method.

### Method signature

```
```
1
2
```



```
fos.delete(key: string, options?: { cdn?: boolean }): Promise<void>;
```
```

This method accepts the following properties:

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `key` | string | Yes | The unique identifier for the object to delete. |
| `options` | object | No | Additional options for the request. |
| `options.cdn` | boolean | No | Whether to delete the object from the CDN bucket (defaults to `false`). |

### Example

```
```
1
2
```



```
export const deleteObject = async (key: string): Promise<void> => {
  try {
    await fos.delete(key)
  } catch (error) {
    console.error('Error deleting object', JSON.stringify(error))
  }
}
```
```

## Create download URL

To create a URL with temporary permissions to download a specific object, use the `createDownloadUrl` method.
The created URL will expire after 1 hour.

To integrate with the frontend, use the `objectStore` bridge API's [download](/platform/forge/custom-ui-bridge/objectStore/#download) method.

If you need a pre-signed URL accessible to browsers or clients outside of Atlassian Cloud, use [`createPublicDownloadUrl`](#create-public-download-url) instead.

Don’t store pre-signed URLs in a global context. Doing this could potentially let customer data persist across app invocations between different installations. See [Developer responsibilities](/platform/forge/function-reference/nodejs-runtime/#developer-responsibilities) for related information.

### Method signature

```
```
1
2
```



```
fos.createDownloadUrl(key: string, options?: { cdn?: boolean }): Promise<PresignedUrlResponse | undefined>

interface PresignedUrlResponse {
  url: string;
}
```
```

This method accepts the following properties:

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `key` | string | Yes | The unique identifier for the object. The `createDownloadUrl` method uses this as a unique identifier for your URL. |
| `options` | object | No | Additional options for the request. |
| `options.cdn` | boolean | No | Whether to generate a download URL from the CDN bucket (defaults to `false`). |

**Returns:** A `PresignedUrlResponse`. The object's `content-type` will be what was specified via the [pre-signed upload URL](#create-upload-url); otherwise, the `content-type` will be `application/octet-stream`.

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
    return await fos.createDownloadUrl(key);
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

## Create public download URL

To create a pre-signed download URL accessible to browsers and clients outside of Atlassian Cloud, use the `createPublicDownloadUrl` method. The created URL will expire after 1 hour.

If you need a pre-signed download URL for use inside Atlassian Cloud (such as within Lambda resolvers), use [`createDownloadUrl`](#create-download-url) instead.

Don't store pre-signed URLs in a global context. Doing this could potentially let customer data persist across app invocations between different installations. See [Developer responsibilities](/platform/forge/function-reference/nodejs-runtime/#developer-responsibilities) for related information.

### Method signature

```
```
1
2
```



```
fos.createPublicDownloadUrl(key: string, options?: { cdn?: boolean }): Promise<PresignedUrlResponse | undefined>
```
```

This method accepts the following properties:

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `key` | string | Yes | The unique identifier for the object. |
| `options` | object | No | Additional options for the request. |
| `options.cdn` | boolean | No | Whether to generate a download URL from the CDN bucket (defaults to `false`). |

**Returns:** A `PresignedUrlResponse`. The object's `content-type` will be what was specified via the [pre-signed upload URL](#create-upload-url); otherwise, the `content-type` will be `application/octet-stream`.

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
export const createPublicDownloadUrl = async (key: string): Promise<PresignedUrlResponse | undefined> => {
  try {
    return await fos.createPublicDownloadUrl(key);
  } catch (error) {
    console.error('Error creating public pre-signed download URL', JSON.stringify(error));
  }
};

export const downloadUsingPublicUrl = async (objectId: string): Promise<any> => {
  const { url } = await createPublicDownloadUrl(objectId);
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

## Create upload URL

To create a URL with temporary permissions to upload a single object, use the `createUploadUrl` method. Pre-signed upload URLs can only be used for objects under 1GB. The created URL will expire after 1 hour.

To integrate with the frontend, use the `objectStore` bridge API's [upload](/platform/forge/custom-ui-bridge/objectStore/#upload) method.

If you need a pre-signed URL accessible to browsers or clients outside of Atlassian Cloud, use [`createPublicUploadUrl`](#create-public-upload-url) instead.

Don’t store pre-signed URLs in a global context. Doing this could potentially let customer data persist across app invocations between different installations. See [Developer responsibilities](/platform/forge/function-reference/nodejs-runtime/#developer-responsibilities) for related information.

### Method signature

```
```
1
2
```



```
fos.createUploadUrl(body: UploadUrlBody): Promise<PresignedUrlResponse>

interface UploadUrlBody {
  key: string;
  length: number;
  checksum: string;
  checksumType: 'SHA1' | 'SHA256' | 'CRC32' | 'CRC32C';
  ttlSeconds?: number;
  overwrite?: boolean;
  cdn?: boolean;
}

interface PresignedUrlResponse {
  url: string;
}
```
```

When generating a pre-signed upload URL through `createUploadUrl`, your request must include an `UploadUrlBody` containing the properties of the file you’re uploading. These properties are:

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `key` | string | Yes | The unique identifier for the object. |
| `length` | number | Yes | The byte size of the object. |
| `checksum` | string | Yes | Hash digest of the file content, encoded as base64. Used to verify data integrity. |
| `checksumType` | string | Yes | Algorithm used to generate the checksum. |
| `ttlSeconds` | number | No | Allows you to set a custom TTL for an object. |
| `overwrite` | boolean | No | Indicates whether to replace an existing object with the same key. Defaults to `true`. |
| `cdn` | boolean | No | Whether to upload the object to the CDN bucket. Objects in the CDN bucket may be cached (defaults to `false`). |

**Returns:** A `PresignedUrlResponse`.

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
    const resp = await fos.createUploadUrl(body);
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

## Create public upload URL

To create a URL with temporary permissions to upload a single object for browsers and clients outside of Atlassian Cloud, use the `createPublicUploadUrl` method.
Pre-signed upload URLs can only be used for objects under 1GB. The created URL will expire after 1 hour.

Don't store pre-signed URLs in a global context. Doing this could potentially let customer data persist across app invocations between different installations. See [Developer responsibilities](/platform/forge/function-reference/nodejs-runtime/#developer-responsibilities) for related information.

### Method signature

```
```
1
2
```



```
fos.createPublicUploadUrl(body: UploadUrlBody): Promise<PresignedUrlResponse>

interface UploadUrlBody {
  key: string;
  length: number;
  checksum: string;
  checksumType: 'SHA1' | 'SHA256' | 'CRC32' | 'CRC32C';
  ttlSeconds?: number;
  overwrite?: boolean;
  cdn?: boolean;
}

interface PresignedUrlResponse {
  url: string;
}
```
```

When generating a pre-signed upload URL through `createPublicUploadUrl`, your request must include an `UploadUrlBody` containing the properties of the file you're uploading. These properties are:

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `key` | string | Yes | The unique identifier for the object. |
| `length` | number | Yes | The byte size of the object. |
| `checksum` | string | Yes | Hash digest of the file content, encoded as base64. Used to verify data integrity. |
| `checksumType` | string | Yes | Algorithm used to generate the checksum. |
| `ttlSeconds` | number | No | Allows you to set a custom TTL for an object. |
| `overwrite` | boolean | No | Indicates whether to replace an existing object with the same key. Defaults to `true`. |
| `cdn` | boolean | No | Whether to upload the object to the CDN bucket. Objects in the CDN bucket may be cached (defaults to `false`). |

**Returns:** A `PresignedUrlResponse`.

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
export const createPublicUploadUrl = async (key: string, object: any, objectLength: number, ttlSeconds?: number): Promise<PresignedUrlResponse | undefined> => {
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
    const resp = await fos.createPublicUploadUrl(body);
    return resp;
  } catch (error) {
    console.error('Error creating public pre-signed upload URL', JSON.stringify(error))
  }
};

export const uploadUsingPublicUrl = async (uploadObjectProperties: any): Promise<void> => {
  const { objectId, object, objectLength, ttlSeconds } = uploadObjectProperties
  const { url } = await createPublicUploadUrl(objectId, object, objectLength, ttlSeconds);
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

## Create CDN URL

To generate a CDN URL for accessing an object, use the `createCDNUrl` method. Unlike pre-signed URLs, CDN URLs serve cached content for faster delivery.

### Method signature

```
```
1
2
```



```
fos.createCDNUrl(key: string, options?: CDNOptions): Promise<PresignedUrlResponse | undefined>

type CDNOptions = {
  ttlSeconds?: number;
};
```
```

When generating a URL through `createCDNUrl`, supply the following properties in your request:

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `key` | string | Yes | The unique identifier for the object. |
| `options` | CDNOptions | No | Optional configuration for the CDN URL. |
| `options.ttlSeconds` | number | No | TTL for the CDN URL in seconds. Must be greater than 0 and at most 2,505,600 seconds (29 days). |

### Example

```
```
1
2
```



```
export const getCDNUrl = async (key: string, options?: CDNOptions): Promise<PresignedUrlResponse | undefined> => {
  try {
    return await fos.createCDNUrl(key, options);
  } catch (error) {
    console.error('Error creating CDN URL', JSON.stringify(error));
  }
};
```
```
