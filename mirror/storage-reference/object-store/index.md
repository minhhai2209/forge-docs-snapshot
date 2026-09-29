# Object Store (Preview)

Forge Object Store is now in Preview, and therefore fully supported. However, it remains under active development and may be subject to shorter deprecation windows. Preview features are suitable for early adopters in production environments.

We release preview features so partners and developers can study, test, and integrate them prior to General Availability (GA). For more details, see [Forge EAP, Preview, and GA](https://developer.atlassian.com/platform/forge/whats-coming/#forge-preview).

The Forge Object Store is a hosted storage solution that lets you manage large items such as data objects or media files. It provides a seamless way to efficiently store, retrieve, and manage objects directly from your Forge apps.

The Forge Object Store integrates tightly with the Forge platform, enabling secure and reliable file management.

[Example app

We published a sample app to demonstrate the basics of implementing object storage features in
a Forge app. This sample app uses the Forge Object Store as its backend and available Forge UI components
for its frontend. Refer to the app's README for additional guidance on exploring and testing the code.

[Explore sample app object storage features](https://bitbucket.org/atlassian/forge-ui-object-store-example-app/src/main/)](https://bitbucket.org/atlassian/forge-ui-object-store-example-app/src/main/)

## Limitations

The Forge Object Store is subject to following limitations:

Forge Object Store is not supported on Bitbucket apps.

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

## Data residency

The Atlassian cloud provides features that allow admins to control and verify where their Jira and Confluence data is hosted. These features support them in meeting company requirements or regulatory obligations relating to data residency.

Forge's [persistent storage options](/platform/forge/storage-reference/#persistent)
use this same cloud infrastructure to store data. This allows Forge to extend similar data residency
features to your app. All data stored on Forge persistent storage automatically inherit these features.

Specifically, if your app stores data on Forge persistent storage, an admin can control where that
data is stored.
For more details about how this works, see [Data residency](/platform/forge/data-residency/).

The Forge Object Store is data residency-enabled, in the same way as the Key-Value Store, the Custom Entity Store, and Forge SQL. An app that stores all of its in-scope End-User Data in the Forge Object Store meets the storage criterion for [`PINNED` status](/platform/forge/data-residency/#eligibility) and for the [Runs on Atlassian](/platform/forge/runs-on-atlassian/) badge.

## Data lifecycle

Objects follow the [data lifecycle for Forge-hosted storage](/platform/forge/storage-reference/hosted-storage-data-lifecycle/) that applies to every Forge hosted storage capability.

When a customer uninstalls your app, Forge soft deletes the app's objects instead of destroying them immediately, and retains them for the rest of the retention period set by Atlassian's Standard Data Retention and Disposal policy. Reinstalling the app doesn't restore the objects automatically. To have them re-linked to the new installation, submit a recovery request within 21 days of the uninstallation. See [Data recovery for apps with hosted storage](/platform/forge/storage-reference/#data-recovery) for the steps.

When your app deletes an object while it's still installed, the object becomes unavailable to the app straight away. The platform keeps a soft-deleted copy so that Atlassian can restore it after an accidental deletion, and then destroys it at the end of the retention period. Raise a support ticket within 21 days of the deletion to request a restore. After the retention period, the copy and any backups that contain it are destroyed under Atlassian's Standard Data Retention and Disposal policy, described in the [Atlassian SOC 2 report](https://www.atlassian.com/trust/compliance/resources/soc2).

The retention periods above are platform guarantees, not a data archive. If your app needs to keep objects for a defined period, or to prove that an object was destroyed on a given date, track that in your app rather than relying on the retention window.

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

The Forge Object Store is accessible via two interfaces:

## Frontend components

Forge also provides components for building frontends that interact with the Forge Object Store:

* UI Kit components
  * [File picker](/platform/forge/ui-kit/components/file-picker/): lets users select files locally.
  * [File card](/platform/forge/ui-kit/components/file-card/): displays files selected through the file picker, along with file information and upload progress.
* [`objectStore`](/platform/forge/custom-ui-bridge/objectStore/) bridge methods: lets you integrate functions with Forge Object Store calls.
* [`useObjectStore`](/platform/forge/ui-kit/hooks/use-object-store/) hook: uses the `objectStore` bridge method to execute file management operations and track the state of objects.
