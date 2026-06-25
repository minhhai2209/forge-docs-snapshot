# Forge Object Store limits

Forge Object Store is now in Preview, and therefore fully supported. However, it remains under active development and may be subject to shorter deprecation windows. Preview features are suitable for early adopters in production environments.

We release preview features so partners and developers can study, test, and integrate them prior to General Availability (GA). For more details, see [Forge EAP, Preview, and GA](https://developer.atlassian.com/platform/forge/whats-coming/#forge-preview).

The [Forge Object Store](/platform/forge/storage-reference/object-store/) is a hosted storage solution that let you manage large items such as data objects or media files. It provides you with a seamless way to efficiently store, retrieve, and manage objects directly from your Forge apps.

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
