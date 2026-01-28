# Authorize API

Forge Authorize API helps app developers verify user permissions before making requests using
the `asApp` method.

Import the Authorize API package in your app, as follows:

```
1
import { authorize } from "@forge/api";
```

The `authorize` function returns a number of helper functions that check the current user's
permissions to issues, projects, or content. These are convenience methods that call the
[Jira bulk permissions API](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-permissions/)
and the [Confluence content permissions API](/cloud/confluence/rest/v1/api-group-content-permissions/#api-wiki-rest-api-content-id-permission-check-post).

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
const canEdit = await authorize().onJiraIssue(issueId).canEdit();

if (canEdit) {
  await api.asApp().requestJira(route`/rest/api/3/issue/${issueId}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ update: { summary: [{ set: "updated summary" }] } }),
  });
}
```

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
type Id = number | string;

type authorize = () => {
  onJiraIssue: (issueIds: Id | Id[]) => {
    canAssign: () => Promise<boolean>;
    canCreate: () => Promise<boolean>;
    canEdit: () => Promise<boolean>;
    canMove: () => Promise<boolean>;
    canDelete: () => Promise<boolean>;
    canAddComments: () => Promise<boolean>;
    canEditAllComments: () => Promise<boolean>;
    canDeleteAllComments: () => Promise<boolean>;
    canCreateAttachments: () => Promise<boolean>;
    canDeleteAllAttachments: () => Promise<boolean>;
  };
  onJiraProject: (projectIds: Id | Id[]) => {
    canAssignIssues: () => Promise<boolean>;
    canCreateIssues: () => Promise<boolean>;
    canEditIssues: () => Promise<boolean>;
    canMoveIssues: () => Promise<boolean>;
    canDeleteIssues: () => Promise<boolean>;
    canAddComments: () => Promise<boolean>;
    canEditAllComments: () => Promise<boolean>;
    canDeleteAllComments: () => Promise<boolean>;
    canCreateAttachments: () => Promise<boolean>;
    canDeleteAllAttachments: () => Promise<boolean>;
  };
  onConfluenceContent: (contentIds: Id | Id[]) => {
    canRead: () => Promise<boolean>;
    canUpdate: () => Promise<boolean>;
    canDelete: () => Promise<boolean>;
  };
  // useful for checking permissions of issues and projects in one call
  onJira: (
    perms: Array<{
      permissions: string[];
      issues?: Id[];
      projects?: Id[];
    }>
  ) => Promise<{
    permission: string;
    issues?: number[];
    projects?: number[];
  }>;
};
```

## Parameters

| Name | Type | Description |
| --- | --- | --- |
| `issueIds` | `number | string | (number | string)[]` | The issue IDs to check permissions for. |
| `projectIds` | `number | string | (number | string)[]` | The project IDs to check permissions for. |
| `contentIds` | `number | string | (number | string)[]` | The content IDs to check permissions for. |
| `perms` | `({ permissions: string[]; issues?: (number | string)[]; projects?: (number | string)[]; })[]` | Array of permissions to check for issues and projects. Passed as `projectPermissions` to the [Jira bulk permissions API.](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-permissions/#api-rest-api-3-permissions-check-post) |
