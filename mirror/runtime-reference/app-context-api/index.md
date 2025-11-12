# getAppContext

Use `getAppContext` to get a Forge function's context details, including the
[app environments and versions](/platform/forge/environments-and-versions/) it is executing in.

## Method signature

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
38
39
40
41
42
43
44
45
46
47
48
49
50
51
export declare function getAppContext(): AppContext;

export type AppContext = {
    appAri: AppAri;
    appVersion: string;
    environmentAri: EnvironmentAri;
    environmentType: string;
    invocationId: string;
    invocationRemainingTimeInMillis(): number;
    installationAri: InstallationAri;
    moduleKey: string;
    license?: License;
    installation?: Installation;
};

export type AppAri = {
    appId: string;
    toString: () => string;
};
export type EnvironmentAri = {
    environmentId: string;
    toString: () => string;
};
export type InstallationAri = {
    installationId: string;
    toString: () => string;
};

export type License = {
  isActive?: boolean;
  billingPeriod?: string;
  capabilitySet?: CapabilitySet;
  ccpEntitlementId?: string;
  ccpEntitlementSlug?: string;
  isEvaluation?: boolean;
  subscriptionEndDate?: string;
  supportEntitlementNumber?: string;
  trialEndDate?: string;
  type?: string;
};

export interface ContextAri {
  cloudId?: string;
  workspaceId?: string;
  toString: () => string;
}

export interface Installation {
  ari: InstallationAri;
  contexts: ContextAri[];
}
```

## Returns

This API returns the following string values:

| Name | Properties | Description |
| --- | --- | --- |
| `appAri` | `toString()` | The app's unique Atlassian Resource Identifier (ARI), as defined in the `app.id` field of the `manifest.yml` file. |
| `appId` | The UUID part of the full `appAri` string. |
| `appVersion` |  | App Version. |
| `environmentAri` | `toString()` | The app environment's full ARI. |
| `environmentId` | The UUID part of the full `environmentAri` string. |
| `environmentType` |  | The [environment](/platform/forge/environments-and-versions/) in which the app is running (for example, `DEVELOPMENT`, `STAGING`, or `PRODUCTION`). |
| `invocationId` |  | A unique identifier for the current invocation. |
| `invocationRemainingTimeInMillis()` |  | The number of milliseconds remaining before this function will time out. This information can be useful for long running functions. |
| `installationAri` | `toString()` | The app installation's full ARI. |
| `installationId` | The UUID part of the full `installationAri` string |
| `moduleKey` |  | The key for the module as defined in the `manifest.yml` file. |
| `license` |  | Contains information about the license of the app. This field is only present for paid apps in the production environment.  `license` is `undefined` for free apps, apps in `DEVELOPMENT` and `STAGING` environments, and apps that are not listed on the Atlassian Marketplace. See the `License` type in the `Method Signature` for what information is available. |
| `installation` | `ari` | An object of type `InstallationAri`. Includes `toString` method to fetch full ARI and `installationID`, which is the UUID part of the full ARI. |
| `contexts` | The list of contexts where the app is installed. Each item in the list is an object of type `ContextAri`. |

## Example

```
```
1
2
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
//{"isActive":true,"billingPeriod":"MONTHLY","ccpEntitlementId":"NULL","ccpEntitlementSlug":"NULL","isEvaluation":"NULL","subscriptionEndDate":"NULL","supportEntitlementNumber":"NULL","trialEndDate":"NULL","type":"commercial"}
```
```
