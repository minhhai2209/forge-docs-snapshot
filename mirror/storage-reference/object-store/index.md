# Object Store (EAP)

Forge Object Store is now available as part of our Early Access Program (EAP). To start testing this feature, sign up using this [form](https://ecosystem.atlassian.net/servicedesk/customer/portal/3422/group/3571/create/18555).

Forge Object Store is an experimental feature offered for testing and feedback purposes. This feature is unsupported and subject to change without notice. Do not use Forge Object Store in apps that handle sensitive information, including personal data and customer data.

For more details, see [Forge EAP, Preview, and GA](https://developer.atlassian.com/platform/forge/whats-coming/#eap).

The Forge Object Store is a hosted storage solution that let you manage large items such as data objects or media files. It provides you with a seamless way to efficiently store, retrieve, and manage objects directly from your Forge apps.

The Forge Object Store integrates tightly with the Forge platform, enabling secure and reliable file management.

## Limitations

The Forge Object Store has the following limitations during the EAP:

* **Storage limits:** Objects can be up to 50 MB each, with a total storage cap of 1 GB across all objects.
* **Time-to-Live (TTL):** Objects have a default TTL of 90 days. Custom TTLs can be set but must be greater than 1 second and can't exceed 90 days. This limitation will only be in effect for the EAP.

  **All objects will be deleted at the end of the EAP.** Atlassian will provide notice before the end of the EAP to ensure you have time to download any stored data.
* **Accessing objects in UI:** Direct object upload and download links for UI components are not supported and must be managed through Forge functions. File uploads or downloads in UI Kit must be handled through a [Frame](/platform/forge/ui-kit/components/frame/) component, which acts as a container for a Custom UI application.
* **Pre-signed URLs:** Pre-signed URLs are only available in the UI Kit [Frame](/platform/forge/ui-kit/components/frame/) component or Custom UI. Support for resolver/Lambda is in progress and will be available soon.
* **Production deployments:** The EAP is only for testing purposes and deployment to production will not be available.

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
