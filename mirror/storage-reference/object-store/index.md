# Object Store (Preview)

Forge Object Store is now in Preview, and therefore fully supported. However, it remains under active development and may be subject to shorter deprecation windows. Preview features are suitable for early adopters in production environments.

We release preview features so partners and developers can study, test, and integrate them prior to General Availability (GA). For more details, see [Forge EAP, Preview, and GA](https://developer.atlassian.com/platform/forge/whats-coming/#forge-preview).

The Forge Object Store is a hosted storage solution that lets you manage large items such as data objects or media files. It provides a seamless way to efficiently store, retrieve, and manage objects directly from your Forge apps.

The Forge Object Store integrates tightly with the Forge platform, enabling secure and reliable file management.

[Example app

We published a sample app to demonstrate the basics of implementing object storage features in
a Forge app. This sample app uses the Forge Object Store as its backend and available Forge UI components
for its frontend. Refer to the app's README for additional guidance on exploring and testing the code.](https://bitbucket.org/atlassian/forge-ui-object-store-example-app/src/main/)

## Limitations

The Forge Object Store is subject to following limitations:

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

## Acceptable use

All content stored through the Forge Object Store is subject to Atlassian's [Acceptable Use Policy](https://www.atlassian.com/legal/acceptable-use-policy#inappropriate-content).
Under this policy, we reserve the right to take swift, appropriate, and decisive action, should any objectionable content be reported or detected. This may include suspending an app's access to Forge Object Store, or outright suspension of the app.

We may also implement additional measures to screen stored content.

## Platform pricing resources

Learn more about Forge’s pricing structure, allowances, and billing by visiting [Forge platform pricing](/platform/forge/forge-platform-pricing/).

Estimate your app’s monthly costs using the [cost estimator](https://developer.atlassian.com/forge-cost-estimator), which lets you model usage and see potential charges.

Object Store pricing is currently in **Preview**, and charges for *requests* will take effect on July 1, 2026.

## Partitioning

Data in Forge hosted storage is namespaced. The namespace includes all metadata relevant to an app's current installation. As a result:

* Only your app can read and write your stored data.
* An app can only access its data for the same environment.
* Keys or table names only need to be unique for an individual installation of your app.
* Data stored by your Forge app for one Atlassian app is not accessible from other Atlassian apps.
  For example, data stored in Jira is not accessible from Confluence or vice versa.
* Your app cannot read stored data from different sites, Atlassian apps, and app environments.
* [Quotas and limits](/platform/forge/platform-quotas-and-limits/#storage-limits) are not
  shared between individual installations of your app.

## APIs

The Forge Object Store's capabilities are currently available only via Forge methods. See [Managing objects](/platform/forge/storage-reference/object-store-api/) for detailed information.

Currently, an experimental Forge Object Store [REST API](/platform/forge/rest/v2/api-group-forge-object-store/#api-group-forge-object-store) is available, but only accessible via
[Forge Containers](/platform/forge/containers-reference/). This REST API will also remain in EAP as
long as Forge Containers remains in EAP.

## Frontend components

Forge also provides components for building frontends that interact with the Forge Object Store:

* UI Kit components
  * [File picker](/platform/forge/ui-kit/components/file-picker/): lets users select files locally.
  * [File card](/platform/forge/ui-kit/components/file-card/): displays files selected through the file picker, along with file information and upload progress.
* [`objectStore`](/platform/forge/custom-ui-bridge/objectStore/) bridge methods: lets you integrate functions with Forge Object Store calls.
* [`useObjectStore`](/platform/forge/ui-kit/hooks/use-object-store/) hook: uses the `objectStore` bridge method to execute file management operations and track the state of objects.
