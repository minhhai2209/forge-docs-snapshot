# Object Store (EAP)

Forge Object Store is now available as part of our Early Access Program (EAP). To start testing this feature, sign up using this [form](https://ecosystem.atlassian.net/servicedesk/customer/portal/3422/group/3571/create/18555).

Forge Object Store is an experimental feature offered for testing and feedback purposes. This feature is unsupported and subject to change without notice. Do not use Forge Object Store in apps that handle sensitive information, including personal data and customer data.

For more details, see [Forge EAP, Preview, and GA](https://developer.atlassian.com/platform/forge/whats-coming/#eap).

The Forge Object Store is a hosted storage solution that let you manage large items such as data objects or media files. It provides you with a seamless way to efficiently store, retrieve, and manage objects directly from your Forge apps.

The Forge Object Store integrates tightly with the Forge platform, enabling secure and reliable file management.

[Example app

We published a sample app to demonstrate the basics of implementing object storage features in
a Forge app. This sample app uses the Forge Object Store as its backend and available Forge UI components
for its frontend. Refer to the app's README for additional guidance on exploring and testing the code.](https://bitbucket.org/atlassian/forge-ui-object-store-example-app/src/main/)

## Limitations

The Forge Object Store is subject to following limitations:

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
[frontend components](/platform/forge/storage-reference/object-store/#frontend-components).

| Parameter | Limit |
| --- | --- |
| Maximum object size | 1 GB |
| Maximum request payload size | 10 kB |
| Pre-signed URL validity | 1 hour |

The maximum object size applies to objects uploaded through any [frontend component](/platform/forge/storage-reference/object-store/#frontend-components) used in conjunction with the Forge Object Store (for example, the `useObjectStore`
[UI Kit hook](/platform/forge/ui-kit/hooks/use-object-store/)).

Meanwhile, the maximum request payload size only applies to the actual [Forge Object Store request](/platform/forge/storage-reference/object-store-api/).
This request should only contain the object's name and other relevant metadata (not the object itself).

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

## Frontend components

Forge also provides components for building frontends that interact with the Forge Object Store:

* UI Kit components
  * [File picker](/platform/forge/ui-kit/components/file-picker/): lets users select files locally.
  * [FIle card](/platform/forge/ui-kit/components/file-card/): displays files selected through the file picker, along with file information and upload progress.
* [`objectStore`](/platform/forge/custom-ui-bridge/objectStore/) bridge methods: lets you integrate functions with Forge Object Store calls.
* [`useObjectStore`](/platform/forge/ui-kit/hooks/use-object-store/) hook: uses the `objectStore` bridge method to execute file management operations and track the state of objects.

## EAP Feedback

As part of the EAP, your feedback is invaluable in shaping the future of this feature. We encourage you to explore Forge Object Store's capabilities and share your insights to help us refine and enhance this service.
