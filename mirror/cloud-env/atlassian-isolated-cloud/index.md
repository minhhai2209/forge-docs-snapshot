# Atlassian Isolated Cloud for Forge developers

Atlassian Isolated Cloud (AIC) is a dedicated, single-tenant cloud environment managed by Atlassian for organizations with strict security, compliance, or data isolation requirements. Each AIC customer gets their own dedicated compute, storage, and networking in a virtual private cloud (VPC), completely separated from other Atlassian Cloud customers.

Key characteristics of the AIC environment:

* **Dedicated infrastructure** — dedicated servers, storage, applications, databases, VPC, domain, edge, network, and firewall per customer
* **Data egress blocked by default** — outbound data is controlled by security rules; customers have additional control over egress and ingress
* **Customer-managed encryption (CMK)** — customers hold the encryption keys for all long-term persistent user-generated content
* **Includes Cloud Enterprise and Atlassian Guard Premium** — by default

For more information about how AIC works from an administration perspective, see [How Atlassian Isolated Cloud works](https://support.atlassian.com/organization-administration/docs/how-atlassian-isolated-cloud-works/) in the Atlassian support documentation.

## How AIC differs for Forge developers

* **App availability:** Your app is not available to AIC customers by default. It must be listed on the [Isolated Cloud Marketplace](https://marketplace.atlassian.com/collections/isolated-cloud).
* **App deployment:** Build and test on Atlassian Cloud as usual. To validate on an AIC test site, deploy to the `staging` Forge environment (`forge deploy -e staging`). For production AIC sites, deploy to the `production` environment.
* **App installation:** On production AIC sites, customers install apps through the in-product Marketplace (not the public Marketplace website). On AIC test sites, install via GraphQL mutation. See [Testing your app on Atlassian Isolated Cloud](#testing-your-app-on-atlassian-isolated-cloud).
* **Forge Remote:** The `icLabel` claim in the Forge Invocation Token (FIT) identifies whether a request originates from a Commercial or AIC environment. Your remote backend must use URL templates to derive the correct JSON Web Key Set (JWKS) and Storage URLs. See [Isolated Cloud support](/platform/forge/remote/essentials/#isolated-cloud-support) for implementation details.
* **App logs:** Developers cannot access AIC customer logs via Developer Console. AIC customers must download logs from Admin Hub and share them with you directly.

## AIC limitations for Forge features

The following Forge features are not currently supported for Atlassian Isolated Cloud apps:

Everything else in Forge is supported on AIC unless stated otherwise in the specific feature's documentation.

## Testing your app on Atlassian Isolated Cloud

You can build and test your Forge app on Atlassian Cloud as usual. Test on your AIC test site to validate your app's capabilities on AIC, and to reproduce customer-reported bugs in a similar environment.

### Step 1: Request an AIC test site

Contact Atlassian through [ECOHELP](https://ecosystem.atlassian.net/servicedesk/customer/portal/14) to request an AIC pre-production test site. This process is similar to [getting access to an AGC environment](/platform/framework/agc/guides/get-access-to-agc/).

In your request, include the following:

#### CMK/BYOK keys

All AIC organizations require Bring Your Own Key (BYOK) encryption. Provide two Customer Managed Keys (CMKs), one from each of the following AWS regions:

For instructions on creating a CMK compatible with Atlassian Isolated Cloud, see the [AIC BYOK runbook](https://isolated-cloud-guide.atlassian.net/wiki/external/YzczZGFmMzhkZGM3NDQ5MmFiMmYyYzFiZGUzYTAzZjk).

#### Identity Provider (IdP) details

Provide the following information about your organization's identity provider:

* Which IdP you use (for example, Okta, Google Workspace, Microsoft Active Directory)
* Whether you use **System for Cross-domain Identity Management (SCIM) sync** to automatically provision users from your IdP

Once your request is received, Atlassian provisions your AIC test site and configures your identity provider. You receive a notification when the environment is ready.

### Step 2: Install your app on your AIC test site

Once your AIC test site is ready, follow these steps to install your Forge app for testing. Production AIC customers install apps through the in-product Marketplace. On AIC test sites, install via a GraphQL mutation instead.

These test-site steps must use the **`staging`** Forge environment. Using any other environment (`development`, `production`) may cause installation to fail or the app to behave incorrectly.

#### Deploy the staging version of your app

From your app's root directory, run:

```
```
1
2
```



```
forge deploy -e staging
```
```

#### Enable sharing for your app

In [Developer Console](/console/myapps/), navigate to your app's **Distribution** settings and set the distribution status to **Sharing**. Save your changes.

#### Run the installation mutation

Log in to your AIC test site, then navigate to its GraphQL endpoint:

```
```
1
2
```



```
https://<YOUR_AIC_INSTANCE>/gateway/api/graphql
```
```

Run the following mutation:

```
```
1
2
3
4
5
6
7
8
9
10
11
12
13
14
```



```
mutation ForgeAppInstall($input: AppInstallationInput!) {
  installApp(input: $input) {
    success
    taskId
    errors {
      message
      extensions {
        errorType
        statusCode
      }
    }
  }
}
```
```

With the following variables (Atlassian provides the `CLOUD_ID` and `ACTIVATION_ID` when your AIC test site is set up):

```
```
1
2
3
4
5
6
7
8
```



```
{
  "input": {
    "installationContext": "ari:cloud:<jira|confluence>:<CLOUD_ID>:workspace/<ACTIVATION_ID>",
    "appId": "ari:cloud:ecosystem::app/<YOUR_APP_ID>",
    "environmentKey": "staging"
  }
}
```
```

Replace:

* `<jira|confluence>` — the product to install the app on
* `<CLOUD_ID>` and `<ACTIVATION_ID>` — provided by Atlassian as part of your AIC test site setup
* `<YOUR_APP_ID>` — your app's ID from [Developer Console](/console/myapps/)

If you're testing a paid app and want to simulate different license states, add the optional `licenseOverride` field to the input:

```
```
1
2
```



```
"licenseOverride": "ACTIVE"
```
```

Allowed values: `ACTIVE`, `INACTIVE`, `TRIAL`, `STANDARD`, `ADVANCED`.

Save the `taskId` from the response; you'll need it to check the installation status.

#### Check the installation status

Installation is asynchronous and may take several minutes. Poll the following query every 30 seconds or so to check progress (avoid querying too frequently, as it is rate-limited):

```
```
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
```



```
query ForgeInstallStatus {
  appInstallationTask(id: "<taskId>") {
    id
    appId
    state
    errors {
      message
      extensions {
        statusCode
        errorType
      }
    }
  }
}
```
```

Replace `<taskId>` with the value returned from the installation mutation.

Possible states:

| State | Meaning |
| --- | --- |
| `PENDING` | Installation is queued |
| `IN_PROGRESS` | Installation is actively running |
| `SUCCEEDED` | Installation completed successfully |
| `FAILED` | Installation failed — check the `errors` field |
