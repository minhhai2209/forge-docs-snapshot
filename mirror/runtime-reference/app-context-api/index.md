# getAppContext

Use `getAppContext` to get a Forge function's context details, including the
[app environments and versions](/platform/forge/environments-and-versions/) it is executing in.

## Method signature

```
1export declare function getAppContext(): AppContext;
2
3export type AppContext = {
4    appAri: AppAri;
5    appVersion: string;
6    environmentAri: EnvironmentAri;
7    environmentType: string;
8    invocationId: string;
9    invocationRemainingTimeInMillis(): number;
10    installationAri: InstallationAri;
11    moduleKey: string;
12    license?: License;
13    installation?: Installation;
14};
15
16export type AppAri = {
17    appId: string;
18    toString: () => string;
19};
20export type EnvironmentAri = {
21    environmentId: string;
22    toString: () => string;
23};
24export type InstallationAri = {
25    installationId: string;
26    toString: () => string;
27};
28
29export type License = {
30  active?: boolean;
31  /** @deprecated Use `active` instead. */
32  isActive?: boolean;
33  billingPeriod?: string;
34  capabilitySet?: CapabilitySet;
35  ccpEntitlementId?: string;
36  ccpEntitlementSlug?: string;
37  isEvaluation?: boolean;
38  subscriptionEndDate?: string;
39  supportEntitlementNumber?: string;
40  trialEndDate?: string;
41  type?: string;
42};
43
44export interface ContextAri {
45  cloudId?: string;
46  workspaceId?: string;
47  resourceOwner?: string;
48  toString: () => string;
49}
50
51export interface Installation {
52  ari: InstallationAri;
53  contexts: ContextAri[];
54}
55
```

## Returns

This API returns an `AppContext` object with the following fields:

| Name | Properties | Description |
| --- | --- | --- |
| `appAri` | `toString()` | The app's unique Atlassian Resource Identifier (ARI), as defined in the `app.id` field of the `manifest.yml` file. |
| `appId` | The UUID part of the full `appAri` string. |
| `appVersion` |  | The app's [major and minor version](/platform/forge/versions/). |
| `ContextAri (type of installation.contexts elements)` | `cloudId` | A unique identifier for the cloud instance of a context, such as the ID of a Jira or Confluence instance. |
| `workspaceId` | The workspace ID for a given context. This is specific to Bitbucket. |
| `resourceOwner` | The product that owns the context, such as Jira or Confluence. |
| `toString()` | The context's full ARI. |
| `environmentAri` | `toString()` | The app environment's full ARI. |
| `environmentId` | The UUID part of the full `environmentAri` string. |
| `environmentType` |  | The [environment](/platform/forge/environments-and-versions/) in which the app is running (for example, `DEVELOPMENT`, `STAGING`, or `PRODUCTION`). |
| `invocationId` |  | A unique identifier for the current invocation. |
| `invocationRemainingTimeInMillis()` |  | The number of milliseconds remaining before this function will time out. This information can be useful for long-running functions. |
| `installationAri` | `toString()` | The app installation's full ARI. |
| `installationId` | The UUID part of the full `installationAri` string. |
| `moduleKey` |  | The key for the module as defined in the `manifest.yml` file. |
| `license` |  | Contains information about the license of the app. This field is only present for paid apps in the production environment.  `license` is `undefined` for free apps, apps in `DEVELOPMENT` and `STAGING` environments, and apps that are not listed on the Atlassian Marketplace. See the `License` type in the `Method Signature` for what information is available. |
| `installation` | `ari` | An object of type `InstallationAri`. Includes `toString` method to fetch full ARI and `installationId`, which is the UUID part of the full ARI. |
| `contexts` | The list of contexts where the app is installed. Each item in the list is an object of type `ContextAri`. |

## Example

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
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
```



```
import { getAppContext } from "@forge/api";

const { appAri, appVersion, environmentAri, environmentType, invocationId, installationAri, moduleKey, license } = getAppContext();

console.log(appAri.toString());
// 'ari:cloud:ecosystem::app/00000000-0000-0000-0000-000000000000'

console.log(appAri.appId);
// '00000000-0000-0000-0000-000000000000'

console.log(appVersion);
// '1.0.0'

console.log(environmentAri.toString());
// 'ari:cloud:ecosystem::environment/00000000-0000-0000-0000-000000000000/11111111-1111-1111-0111-111111111111'

console.log(environmentAri.environmentId);
// '11111111-1111-1111-0111-111111111111'

console.log(environmentType);
// 'DEVELOPMENT'

console.log(invocationId);
// '33333333-3333-3333-0333-333333333333'

console.log(installationAri.toString());
// 'ari:cloud:ecosystem::installation/22222222-2222-2222-0222-222222222222'

console.log(installationAri.installationId);
// '22222222-2222-2222-0222-222222222222'

console.log(moduleKey);
// 'hello-world'

console.log(JSON.stringify(license));
//{"active":true,"billingPeriod":"MONTHLY","ccpEntitlementId":"NULL","ccpEntitlementSlug":"NULL","isEvaluation":"NULL","subscriptionEndDate":"NULL","supportEntitlementNumber":"NULL","trialEndDate":"NULL","type":"commercial"}
```
```
