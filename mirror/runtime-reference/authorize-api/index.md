# Authorize API

Forge Authorize API helps app developers verify user permissions before making requests using
the `asApp` method.

Import the Authorize API package in your app, as follows:

```
1import { authorize } from "@forge/api";
2
```

The `authorize` function returns a number of helper functions that check the current user's
permissions to issues, projects, or content. These are convenience methods that call the
[Jira bulk permissions API](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-permissions/)
and the [Confluence content permissions API](/cloud/confluence/rest/v1/api-group-content-permissions/#api-wiki-rest-api-content-id-permission-check-post).

```
1const canEdit = await authorize().onJiraIssue(issueId).canEdit();
2
3if (canEdit) {
4  await api.asApp().requestJira(route`/rest/api/3/issue/${issueId}`, {
5    method: "PUT",
6    headers: {
7      "Content-Type": "application/json",
8    },
9    body: JSON.stringify({ update: { summary: [{ set: "updated summary" }] } }),
10  });
11}
12
```

## Method signature

```
1type Id = number | string;
2
3type authorize = () => {
4  onJiraIssue: (issueIds: Id | Id[]) => {
5    canAssign: () => Promise<boolean>;
6    canCreate: () => Promise<boolean>;
7    canEdit: () => Promise<boolean>;
8    canMove: () => Promise<boolean>;
9    canDelete: () => Promise<boolean>;
10    canAddComments: () => Promise<boolean>;
11    canEditAllComments: () => Promise<boolean>;
12    canDeleteAllComments: () => Promise<boolean>;
13    canCreateAttachments: () => Promise<boolean>;
14    canDeleteAllAttachments: () => Promise<boolean>;
15  };
16  onJiraProject: (projectIds: Id | Id[]) => {
17    canAssignIssues: () => Promise<boolean>;
18    canCreateIssues: () => Promise<boolean>;
19    canEditIssues: () => Promise<boolean>;
20    canMoveIssues: () => Promise<boolean>;
21    canDeleteIssues: () => Promise<boolean>;
22    canAddComments: () => Promise<boolean>;
23    canEditAllComments: () => Promise<boolean>;
24    canDeleteAllComments: () => Promise<boolean>;
25    canCreateAttachments: () => Promise<boolean>;
26    canDeleteAllAttachments: () => Promise<boolean>;
27  };
28  onConfluenceContent: (contentIds: Id | Id[]) => {
29    canRead: () => Promise<boolean>;
30    canUpdate: () => Promise<boolean>;
31    canDelete: () => Promise<boolean>;
32  };
33  // useful for checking permissions of issues and projects in one call
34  onJira: (
35    perms: Array<{
36      permissions: string[];
37      issues?: Id[];
38      projects?: Id[];
39    }>
40  ) => Promise<{
41    permission: string;
42    issues?: number[];
43    projects?: number[];
44  }>;
45};
46
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `issueIds` | `number | string | (number | string)[]` | The issue IDs to check permissions for. |
| `projectIds` | `number | string | (number | string)[]` | The project IDs to check permissions for. |
| `contentIds` | `number | string | (number | string)[]` | The content IDs to check permissions for. |
| `perms` | `({ permissions: string[]; issues?: (number | string)[]; projects?: (number | string)[]; })[]` | Array of permissions to check for issues and projects. Passed as `projectPermissions` to the [Jira bulk permissions API.](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-permissions/#api-rest-api-3-permissions-check-post) |
