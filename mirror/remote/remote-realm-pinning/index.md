# Set up remotes for data residency realm pinning

Using the capabilities discussed on this page may make your app *not* eligible for **Runs on Atlassian**.

Go to [this page](/platform/forge/runs-on-atlassian/) to know more about the Runs on Atlassian program.
To know how to check if your app is eligible for Runs on Atlassian, go to the
[Forge CLI documentation](/platform/forge/cli-reference/eligibility/).

Forge Remote data residency provides you with the flexibility to help meet [data residency](/platform/forge/data-residency/) requirements by pinning [remote endpoints](/platform/forge/remote/) to specific regions. This guide walks you through setting up realm pinning for remotes in your Forge apps.

## What is realm pinning?

Realm pinning determines the selected geographic location of URLs defined as `baseUrl` during the initial installation of an app. If a customer pins their Atlassian app to a specific region, the app selects the corresponding location from the manifest upon installation. Even if the Atlassian app has not been pinned, the `baseUrl` defined for the region is still used during installation if the app supports the region where the Atlassian app is provisioned.

## Requirements for PINNED status

A `PINNED` status means that the Forge app's data is hosted in the same location as the Atlassian app data.

## Setup realm pinning in Forge Remote

To manage data residency for remotes in Forge:

1. Configure the Manifest: Add a `baseUrl` with region-specific URLs (`US`, `EU`, `AU`, etc.) and include a `storage` attribute with `inScopeEUD: true` for data storage compliance.

   ```
   ```
   1
   2
   ```



   ```
     remotes:
       - key: remote-backend
         baseUrl:
           default: "https://backend.example.com"
           US: "https://us-backend.example.com"
           EU: "https://eu-backend.example.com"
         operations:
           - storage
         storage:
           inScopeEUD: true
   ```
   ```

   If operations are not defined, `storage` and `inScopeEUD` will be treated as `true`. This means the remote will be considered to store in-scope End-User Data for data residency compliance purposes.
2. Help ensure compliance:

   * Ensure all remotes storing in-scope End-User Data use the same regions to maintain consistent compliance. For example, if `remote 1` uses `us`, `eu`, and `au` regions, all other remotes must include the same regions.
   * If a remote only sends data out (egresses data), declare it using `compute` or `fetch` operations. For more information on operation, see [Remotes properties](/platform/forge/manifest-reference/remotes/#properties).

## Supported locations for realm pinning

Forge currently supports several regions for realm pinning to meet data residency requirements.

* Global: In-scope data is hosted within realms determined by Atlassian: data may be moved between realms as needed.
* EU: In-scope data is hosted within the Dublin AWS regions.
* US: In-scope data is hosted within the US East and US West AWS regions.
* AU: In-scope data is hosted within the Sydney AWS region.
* DE: In-scope data is hosted within the Frankfurt AWS region.
* SG: In-scope data is hosted within the Singapore AWS region
* CA: In-scope data is hosted within the Canada AWS region
* IN: In-scope data is hosted within the Mumbai AWS region
* KR: In-scope data is hosted within the Seoul AWS region
* JP: In-scope data is hosted within the Tokyo AWS region
* GB: In-scope data is hosted within the London AWS region
* CH: In-scope data is hosted within the Zurich AWS region

## Realm migration for Forge Remote

Realm migration enables customers to move app data when their Atlassian host app changes regions. This applies to apps that use Forge Remote and have region-specific `baseUrl` configurations [defined for realm pinning](/platform/forge/remote/remote-realm-pinning/). Migration may be required if an app was initially installed in a global location due to missing region-specific `baseUrl` settings or if a customer later relocates their Atlassian app to meet data residency requirements.

To support these migrations, apps must implement the data residency migration hook in the `modules` field of the manifest and handle the required lifecycle hooks.

Find full details in [Supporting realm migrations for Forge Remote](/platform/forge/remote/remote-realm-migration/).

## Realm persistence in Forge

Realm persistence is a default capability that ensures apps retain their previously assigned region when reinstalled within 30 days following uninstallation. This helps ensure consistency in data residency, preventing apps from being reassigned to a different region upon reinstallation, provided the reinstallation occurs with the 30 day window.

If a customer uninstalls and later reinstalls an app within 30 days, their remote traffic will be redirected back to existing regions. If their reinstallation occurs after 30 days, the remote region will be determined based upon the current Atlassian app region which may differ from the originally assigned region.

## App version upgrades

Some actions required to set up data residency for remote storage will [trigger a major version change](/platform/forge/versions/#major-version-upgrades). These include:

* adding new regions
* modifying or removing URLs
* converting the baseUrl format
* altering external paths

Ensure you review and plan for these changes.
