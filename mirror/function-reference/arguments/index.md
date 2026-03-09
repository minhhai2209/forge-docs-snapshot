# Function Arguments

Forge functions receive two arguments: a module-specific payload, and an object containing contextual information for the function
invocation.

```
1
2
3
export const handler = (payload, context) => {
  // Do something
}
```

## Payload Schema

The payload is entirely module specific, for example [a webtriggers request](/platform/forge/events-reference/web-trigger/#request).

## Context Schema

Context is the same for all modules.

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
export type Context = {
  installContext: string;
  principal?: Principal;
  license?: License;
  installation?: Installation;
  workspaceId?: string;
}

export type Principal = {
  accountId: string;
}

export type License = {
  isActive: boolean;
  billingPeriod?: string | null;
  capabilitySet?: string | null;
  ccpEntitlementId?: string | null;
  ccpEntitlementSlug?: string | null;
  isEvaluation?: boolean | null;
  subscriptionEndDate?: string | null;
  supportEntitlementNumber?: string | null;
  trialEndDate?: string | null;
  type?: string | null;
};

export type Installation = {
  ari: InstallationAri;
  contexts: ContextAri[];
}

export type InstallationAri = {
    installationId: string;
    toString: () => string;
};

export type ContextAri = {
  cloudId?: string;
  workspaceId?: string;
  toString: () => string;
}
```

| Property | Type | Description |
| --- | --- | --- |
| `principal` | `Principal | undefined` | The principal containing the Atlassian ID of the user that interacted with the component. |
| `installContext` | `string` | The ARI identifying the cloud or Atlassian app context of this component installation. |
| `workspaceId` | `string | undefined` | The ID of the workspace on which the extension is working. |
| `license` | `License | undefined` | Contains information about the license of the app. This field is only present for paid apps in the production environment.  `license` is `undefined` for free apps, apps in `DEVELOPMENT` and `STAGING` environments, and apps that are not listed on the Atlassian Marketplace. |
| `installation` | `Installation | undefined` | A summary of the app installation, including the installation ARI and the contexts where the app is installed. |
