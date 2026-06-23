# Deprecated Object Store methods

Forge Object Store is now in Preview, and therefore fully supported. However, it remains under active development and may be subject to shorter deprecation windows. Preview features are suitable for early adopters in production environments.

We release preview features so partners and developers can study, test, and integrate them prior to General Availability (GA). For more details, see [Forge EAP, Preview, and GA](https://developer.atlassian.com/platform/forge/whats-coming/#forge-preview).

The following methods and method signatures are now deprecated. If your app uses any of them, replace them
immediately with [supported Forge Object Store methods](/platform/forge/storage-reference/object-store-api/).

## Upload/Update object

Store large files or media efficiently from your app using the Forge-hosted storage.
Use the `put` method to upload an object with the following parameters:

* `key` (string): A unique identifier for the object being stored. If an object already exists with the same `key`, the new upload will add a new version of the object, effectively functioning as an update operation.
* `object` (any): The data to be stored, which is buffered internally for efficient handling.
* `ttlSeconds` (number): Allows you to set a custom TTL for an object. If no TTL is set, the object's TTL will default to 90 days. Custom TTLs must be greater than 1 second and can't exceed 90 days.

### Method signature

```
1
os.put(key: string, object: any, ttlSeconds?: number): Promise<void>;
```

### Example

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

## Download

Retrieve the data of the latest version of an object stored in the Forge Object Store using the `download` method.

The `download` method works as follows:

* `key` (string): The unique identifier for the object to download.
* **Returns**: A `Buffer` containing the latest object data if it exists, or `undefined` if the object is not found.

### Method signature

```
```
1
2
```



```
os.download(key: string): Promise<Buffer | undefined>;
```
```

### Example

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
      console.info('Object was not found', { key })
    }
    return object
  } catch (error) {
    console.error('Error downloading object', JSON.stringify(error))
  }
}
```
```
