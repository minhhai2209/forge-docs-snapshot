# Function Arguments

Forge functions receive two arguments: a module-specific payload, and an object containing contextual information for the function
invocation.

```
1export const handler = (payload, context) => {
2  // Do something
3}
4
```

## Payload Schema

The payload is entirely module specific, for example [a webtriggers request](/platform/forge/events-reference/web-trigger/#request).

## Context Schema

Context is the same for all modules.

```
1export type Context = {
2  installContext: string;
3  principal?: Principal;
4  license?: License;
5  installation?: Installation;
6  workspaceId?: string;
7}
8
9export type Principal = {
10  accountId: string;
11}
12
13export type License = {
14  active: boolean;
15  
16  isActive: boolean;
17  billingPeriod?: string | null;
18  capabilitySet?: string | null;
19  ccpEntitlementId?: string | null;
20  ccpEntitlementSlug?: string | null;
21  isEvaluation?: boolean | null;
22  subscriptionEndDate?: string | null;
23  supportEntitlementNumber?: string | null;
24  trialEndDate?: string | null;
25  type?: string | null;
26};
27
28export type Installation = {
29  ari: InstallationAri;
30  contexts: ContextAri[];
31}
32
33export type InstallationAri = {
34    installationId: string;
35    toString: () => string;
36};
37
38export type ContextAri = {
39  cloudId?: string;
40  workspaceId?: string;
41  toString: () => string;
42}
43
```

| Property | Type | Description |
| --- | --- | --- |
| `principal` | `Principal | undefined` | The principal containing the Atlassian ID of the user that interacted with the component. |
| `installContext` | `string` | The ARI identifying the cloud or Atlassian app context of this component installation. |
| `workspaceId` | `string | undefined` | The ID of the workspace on which the extension is working. |
| `license` | `License | undefined` | Contains information about the license of the app. This field is only present for paid apps in the production environment.  `license` is `undefined` for free apps, apps in `DEVELOPMENT` and `STAGING` environments, and apps that are not listed on the Atlassian Marketplace. |
| `installation` | `Installation | undefined` | A summary of the app installation, including the installation ARI and the contexts where the app is installed. |
