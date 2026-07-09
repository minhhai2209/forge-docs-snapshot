# Bitbucket events

Forge apps can subscribe to Bitbucket events for:

Your Forge app must have permission from the
workspace admin to access the data it provides within the event payload.
The OAuth scope required for each event is documented below.

In rare circumstances, Bitbucket event delivery can be significantly delayed.
If you need to ignore delayed events or handle them differently, check the
event timestamps — see the payload format sections for the timestamp fields
available for each event.

## Repository events

You can subscribe to these Bitbucket repository events in Forge apps:

Each event has a different payload format.

### Repository created

An event with the name `avi:bitbucket:created:repository` is sent when a repository is created.

The required OAuth scope is `read:repository:bitbucket`.

#### Payload

| Name | Type | Description |
| --- | --- | --- |
| eventType | `string` | The event name `avi:bitbucket:created:repository`. |
| timestamp | `string` | The timestamp the event was emitted in ISO 8601 format. |
| selfGenerated | `boolean` | Whether the event was triggered by the app receiving it. See [Detect and filter self-generated events](/platform/forge/events-reference/product_events/#ignoreself). |
| actor | `Actor` | The user that has caused the event. |
| repository | `Repository` | The repository the event is related to. |
| project | `Project` | The project of the repository the event is related to. |
| workspace | `Workspace` | The workspace of the repository the event is related to. |

#### Type reference

```
```
1
2
```



```
interface Actor {
  type: string;
  accountId: string;
  uuid: string;
}

interface Repository {
  uuid: string;
  slug?: string;
}

interface Project {
  uuid: string;
}

interface Workspace {
  uuid: string;
}
```
```

#### Example

This is an example payload of a newly created repository.

```
```
1
2
```



```
{
  "actor": {
    "type": "user",
    "accountId": "5ffed3379edf280075d75b20",
    "uuid": "{cc8e193d-7603-4dfd-8771-fcc8960aa0fb}"
  },
  "repository": {
    "uuid": "{15a31549-1cff-45dc-9d0d-310114c5038b}",
    "slug": "repository-slug"
  },
  "project": {
    "uuid": "{1860e69a-65c1-4ac2-8ab0-cbd2868e7573}"
  },
  "workspace": {
    "uuid": "{4c16a397-8e48-479c-8ca2-442e46c90570}"
  },
  "eventType": "avi:bitbucket:created:repository",
  "timestamp": "2026-03-23T06:03:12.361017Z"
}
```
```

### Repository updated

An event with the name `avi:bitbucket:updated:repository` is sent when a repository is updated.

The required OAuth scope is `read:repository:bitbucket`.

#### Payload

| Name | Type | Description |
| --- | --- | --- |
| eventType | `string` | The event name `avi:bitbucket:updated:repository`. |
| timestamp | `string` | The timestamp the event was emitted in ISO 8601 format. |
| selfGenerated | `boolean` | Whether the event was triggered by the app receiving it. See [Detect and filter self-generated events](/platform/forge/events-reference/product_events/#ignoreself). |
| actor | `Actor` | The user that has caused the event. |
| repository | `Repository` | The repository the event is related to. |
| project | `Project` | The project of the repository the event is related to. |
| workspace | `Workspace` | The workspace of the repository the event is related to. |
| changes | `Changes` | An object containing the changes that were applied to the repository. |

#### Type reference

```
```
1
2
```



```
interface Actor {
  type: string;
  accountId: string;
  uuid: string;
}

interface Repository {
  uuid: string;
  slug?: string;
}

interface Project {
  uuid: string;
}

interface Workspace {
  uuid: string;
}

interface TruncatedValue {
  value: string;
  truncated: boolean;
}

interface Changes {
  [key: string]: {
    old: TruncatedValue;
    new: TruncatedValue;
  };
}
```
```

#### Example

This is an example payload of an updated repository.

```
```
1
2
```



```
{
  "actor": {
    "type": "user",
    "accountId": "5ffed3379edf280075d75b20",
    "uuid": "{cc8e193d-7603-4dfd-8771-fcc8960aa0fb}"
  },
  "repository": {
    "uuid": "{15a31549-1cff-45dc-9d0d-310114c5038b}"
  },
  "project": {
    "uuid": "{1860e69a-65c1-4ac2-8ab0-cbd2868e7573}"
  },
  "workspace": {
    "uuid": "{4c16a397-8e48-479c-8ca2-442e46c90570}"
  },
  "changes": {
    "description": {
      "old": {
        "value": "",
        "truncated": false
      },
      "new": {
        "value": "New description",
        "truncated": false
      }
    }
  },
  "eventType": "avi:bitbucket:updated:repository",
  "timestamp": "2026-03-23T06:03:12.361017Z"
}
```
```

### Repository pushed

An event with the name `avi:bitbucket:push:repository` is sent when source code is being pushed onto a repository.

The required OAuth scope is `read:repository:bitbucket`.

#### Payload

| Name | Type | Description |
| --- | --- | --- |
| eventType | `string` | The event name `avi:bitbucket:push:repository`. |
| timestamp | `string` | The timestamp the event was emitted in ISO 8601 format. |
| selfGenerated | `boolean` | Whether the event was triggered by the app receiving it. See [Detect and filter self-generated events](/platform/forge/events-reference/product_events/#ignoreself). |
| actor | `Actor` | The user that has caused the event. |
| repository | `Repository` | The repository the event is related to. |
| project | `Project` | The project of the repository the event is related to. |
| workspace | `Workspace` | The workspace of the repository the event is related to. |
| push | `Push` | An object containing the push information. |

#### Type reference

```
```
1
2
```



```
interface Actor {
  type: string;
  accountId: string;
  uuid: string;
}

interface Repository {
  uuid: string;
  slug?: string;
}

interface Project {
  uuid: string;
}

interface Workspace {
  uuid: string;
}

interface TruncatedValue {
  value: string;
  truncated: boolean;
}

interface Author {
  user: Actor;
}

interface Commit {
  hash: string;
  message: TruncatedValue;
  date: string;
  author: Author;
}

interface CommitPush {
  ref: string;
  mainbranch: boolean;
  before?: string;
  after?: string;
  created: boolean;
  closed: boolean;
  forced: boolean;
  truncated: boolean;
  commits: Commit[];
}

interface TagPush {
  ref: string;
  created: boolean;
  forced: boolean;
  closed: boolean;
  before?: string;
  after?: string;
  date?: string;
  message?: TruncatedValue;
  author?: Author;
}

type Push = CommitPush | TagPush;
```
```

#### Example

This is an example payload of source code being pushed onto a repository.

```
```
1
2
```



```
{
  "actor": {
    "type": "user",
    "accountId": "5ffed3379edf280075d75b20",
    "uuid": "{cc8e193d-7603-4dfd-8771-fcc8960aa0fb}"
  },
  "repository": {
    "uuid": "{15a31549-1cff-45dc-9d0d-310114c5038b}",
    "slug": "repository-slug"
  },
  "project": {
    "uuid": "{1860e69a-65c1-4ac2-8ab0-cbd2868e7573}"
  },
  "workspace": {
    "uuid": "{4c16a397-8e48-479c-8ca2-442e46c90570}"
  },
  "push": {
    "ref": "main",
    "mainbranch": true,
    "after": "a37e0ad81173c7f6707d6b9f74dab4ce9938064d",
    "created": true,
    "closed": false,
    "forced": false,
    "truncated": false,
    "commits": [
      {
        "hash": "a37e0ad81173c7f6707d6b9f74dab4ce9938064d",
        "message": {
          "value": "Initial commit",
          "truncated": false
        },
        "date": "2023-05-12T01:40:22.000000Z",
        "author": {
          "user": {
            "type": "user",
            "accountId": "5ffed3379edf280075d75b20",
            "uuid": "{cc8e193d-7603-4dfd-8771-fcc8960aa0fb}"
          }
        }
      }
    ]
  },
  "eventType": "avi:bitbucket:push:repository",
  "timestamp": "2026-03-23T06:03:12.361017Z"
}
```
```

This is an example payload of an annotated tag being pushed.

```
```
1
2
```



```
{
  "actor": {
    "type": "user",
    "accountId": "5ffed3379edf280075d75b20",
    "uuid": "{cc8e193d-7603-4dfd-8771-fcc8960aa0fb}"
  },
  "repository": {
    "uuid": "{15a31549-1cff-45dc-9d0d-310114c5038b}",
    "slug": "repository-slug"
  },
  "project": {
    "uuid": "{1860e69a-65c1-4ac2-8ab0-cbd2868e7573}"
  },
  "workspace": {
    "uuid": "{4c16a397-8e48-479c-8ca2-442e46c90570}"
  },
  "push": {
    "ref": "main",
    "date": "2026-05-27T07:05:01.000000Z",
    "after": "a37e0ad81173c7f6707d6b9f74dab4ce9938064d",
    "created": true,
    "closed": false,
    "forced": false,
    "author": {
      "user": {
        "type": "user",
        "accountId": "712020:f44b4850-c6f6-44cb-9722-b800af116eb4",
        "uuid": "{c0de26c1-c01f-4d70-a19c-dad5a5b2e531}"
      }
    },
    "message": {
      "truncated": false,
      "value": "Release version 1.0\n"
    }
  },
  "eventType": "avi:bitbucket:push:repository",
  "timestamp": "2026-03-23T06:03:12.361017Z"
}
```
```

### Repository deleted

An event with the name `avi:bitbucket:deleted:repository` is sent when a repository is deleted.

The required OAuth scope is `read:repository:bitbucket`.

#### Payload

| Name | Type | Description |
| --- | --- | --- |
| eventType | `string` | The event name `avi:bitbucket:deleted:repository`. |
| timestamp | `string` | The timestamp the event was emitted in ISO 8601 format. |
| selfGenerated | `boolean` | Whether the event was triggered by the app receiving it. See [Detect and filter self-generated events](/platform/forge/events-reference/product_events/#ignoreself). |
| actor | `Actor` | The user that has caused the event. |
| repository | `Repository` | The repository the event is related to. |
| project | `Project` | The project of the repository the event is related to. |
| workspace | `Workspace` | The workspace of the repository the event is related to. |

#### Type reference

```
```
1
2
```



```
interface Actor {
  type: string;
  accountId: string;
  uuid: string;
}

interface Repository {
  uuid: string;
  slug?: string;
}

interface Project {
  uuid: string;
}

interface Workspace {
  uuid: string;
}
```
```

#### Example

This is an example payload of a repository being deleted.

```
```
1
2
```



```
{
  "actor": {
    "type": "user",
    "accountId": "5ffed3379edf280075d75b20",
    "uuid": "{cc8e193d-7603-4dfd-8771-fcc8960aa0fb}"
  },
  "repository": {
    "uuid": "{15a31549-1cff-45dc-9d0d-310114c5038b}"
  },
  "project": {
    "uuid": "{1860e69a-65c1-4ac2-8ab0-cbd2868e7573}"
  },
  "workspace": {
    "uuid": "{4c16a397-8e48-479c-8ca2-442e46c90570}"
  },
  "eventType": "avi:bitbucket:deleted:repository",
  "timestamp": "2026-03-23T06:03:12.361017Z"
}
```
```

### Build status created

An event with the name `avi:bitbucket:created:build-status` is sent when a build status is created for a commit in a repository.

The required OAuth scope is `read:repository:bitbucket`.

#### Payload

| Name | Type | Description |
| --- | --- | --- |
| eventType | `string` | The event name `avi:bitbucket:created:build-status`. |
| timestamp | `string` | The timestamp the event was emitted in ISO 8601 format. |
| selfGenerated | `boolean` | Whether the event was triggered by the app receiving it. See [Detect and filter self-generated events](/platform/forge/events-reference/product_events/#ignoreself). |
| actor | `Actor` | The user that has caused the event. |
| repository | `Repository` | The repository the event is related to. |
| project | `Project` | The parent project of the repository that the event is related to. |
| workspace | `Workspace` | The workspace of the repository the event is related to. |
| buildStatus | `BuildStatus` | The build status the event is related to. |

#### Type reference

```
```
1
2
```



```
interface Actor {
  type: string;
  accountId: string;
  uuid: string;
}

interface Repository {
  uuid: string;
  slug?: string;
}

interface Project {
  uuid: string;
}

interface Workspace {
  uuid: string;
}

interface BuildStatus {
    key: string;
    commit: {
        hash: string;
    };
    state: string;
    url: string;
    createdOn: string;
    updatedOn: string;
    refName?: string; // branch or tag name
}
```
```

#### Example

This is an example payload of a build status being created.

```
```
1
2
```



```
{
  "timestamp": "2025-01-31T00:42:46.935036Z",
  "actor": {
    "type": "user",
    "accountId": "5ffed3379edf280075d75b20",
    "uuid": "{cc8e193d-7603-4dfd-8771-fcc8960aa0fb}"
  },
  "repository": {
    "uuid": "{15a31549-1cff-45dc-9d0d-310114c5038b}"
  },
  "project": {
    "uuid": "{1860e69a-65c1-4ac2-8ab0-cbd2868e7573}"
  },
  "workspace": {
    "uuid": "{4c16a397-8e48-479c-8ca2-442e46c90570}"
  },
  "buildStatus": {
    "key": "my-build1",
    "state": "FAILED",
    "url": "https://some.url.com",
    "commit": {
      "hash": "b88c4b490b648bf960eba6f59123456797960e55"
    },
    "createdOn": "2025-01-31T00:42:46.866793Z",
    "updatedOn": "2025-01-31T00:42:46.866808Z",
    "refName": "main"
  },
  "eventType": "avi:bitbucket:created:build-status"
}
```
```

### Build status updated

An event with the name `avi:bitbucket:updated:build-status` is sent when a build status is updated for a commit in a repository.

The required OAuth scope is `read:repository:bitbucket`.

#### Payload

| Name | Type | Description |
| --- | --- | --- |
| eventType | `string` | The event name `avi:bitbucket:updated:build-status`. |
| timestamp | `string` | The timestamp the event was emitted in ISO 8601 format. |
| selfGenerated | `boolean` | Whether the event was triggered by the app receiving it. See [Detect and filter self-generated events](/platform/forge/events-reference/product_events/#ignoreself). |
| actor | `Actor` | The user that has caused the event. |
| repository | `Repository` | The repository the event is related to. |
| project | `Project` | The parent project of the repository that the event is related to. |
| workspace | `Workspace` | The workspace of the repository the event is related to. |
| buildStatus | `BuildStatus` | The build status the event is related to. |

#### Type reference

```
```
1
2
```



```
interface Actor {
  type: string;
  accountId: string;
  uuid: string;
}

interface Repository {
  uuid: string;
  slug?: string;
}

interface Project {
  uuid: string;
}

interface Workspace {
  uuid: string;
}

interface BuildStatus {
  key: string;
  commit: {
      hash: string;
  };
  state: string;
  url: string;
  createdOn: Date;
  updatedOn: Date;
  refName?: string; // branch or tag name
}
```
```

#### Example

This is an example payload of a build status being updated.

```
```
1
2
```



```
{
  "timestamp": "2025-01-31T01:03:17.137933Z",
  "actor": {
    "type": "user",
    "accountId": "5ffed3379edf280075d75b20",
    "uuid": "{cc8e193d-7603-4dfd-8771-fcc8960aa0fb}"
  },
  "repository": {
    "uuid": "{15a31549-1cff-45dc-9d0d-310114c5038b}",
    "slug": "repository-slug"
  },
  "project": {
    "uuid": "{1860e69a-65c1-4ac2-8ab0-cbd2868e7573}"
  },
  "workspace": {
    "uuid": "{4c16a397-8e48-479c-8ca2-442e46c90570}"
  },
  "buildStatus": {
    "key": "my-build1",
    "state": "SUCCESSFUL",
    "url": "https://some.url.com",
    "commit": {
      "hash": "b88c4b490b648bf960eba6f59123456797960e55"
    },
    "createdOn": "2025-01-31T00:42:46.866793Z",
    "updatedOn": "2025-01-31T01:03:17.105700Z",
    "refName": "main"
  },
  "eventType": "avi:bitbucket:updated:build-status"
}
```
```

An event with the name `avi:bitbucket:created:commit-comment` is sent when a commit comment is created.

The required OAuth scope is `read:repository:bitbucket`.

#### Payload

| Name | Type | Description |
| --- | --- | --- |
| eventType | `string` | The event name `avi:bitbucket:created:commit-comment`. |
| timestamp | `string` | The timestamp the event was emitted in ISO 8601 format. |
| selfGenerated | `boolean` | Whether the event was triggered by the app receiving it. See [Detect and filter self-generated events](/platform/forge/events-reference/product_events/#ignoreself). |
| actor | `Actor` | The user that has caused the event. |
| repository | `Repository` | The repository of the commit the event is related to. |
| project | `Project` | The project of the commit the event is related to. |
| workspace | `Workspace` | The workspace of the commit the event is related to. |
| commit | `Commit` | The commit the comment is created on. |
| comment | `Comment` | The commit comment that was created. |

#### Type reference

```
```
1
2
```



```
interface Actor {
  type: string;
  accountId: string;
  uuid: string;
}

interface Repository {
  uuid: string;
  slug?: string;
}

interface Project {
  uuid: string;
}

interface Workspace {
  uuid: string;
}

interface Commit {
  hash: string;
}

interface Comment {
  id: number;
}
```
```

#### Example

This is an example payload of a commit comment being created.

```
```
1
2
```



```
{
  "actor": {
    "type": "user",
    "accountId": "5ffec5f444065f013ff70150",
    "uuid": "{f9a75168-ed8e-4998-8850-d49e0cde4917}"
  },
  "repository": {
    "uuid": "{ea73e3cd-f7ee-4fac-aeaa-a4e4b77ba8c9}",
    "slug": "repository-slug"
  },
  "project": {
    "uuid": "{1000c478-a2f2-4f72-9b5f-cebbc2b5ba3d}"
  },
  "workspace": {
    "uuid": "{f0b805f1-c71c-46c7-b97a-b247b211ffc6}"
  },
  "commit": {
    "hash": "af9991d192278ce1a5737681b5f256a7f1c1f625"
  },
  "comment": {
    "id": 78675
  },
  "eventType": "avi:bitbucket:created:commit-comment",
  "timestamp": "2026-03-23T06:03:12.361017Z"
}
```
```

## Pull request events

You can subscribe to these Bitbucket pull request events in Forge apps:

Each event has a different payload format.

### Pull request created

An event with the name `avi:bitbucket:created:pullrequest` is sent when a pull request is created.

The required OAuth scope is `read:pullrequest:bitbucket`.

#### Payload

| Name | Type | Description |
| --- | --- | --- |
| eventType | `string` | The event name `avi:bitbucket:created:pullrequest`. |
| timestamp | `string` | The timestamp the event was emitted in ISO 8601 format. |
| selfGenerated | `boolean` | Whether the event was triggered by the app receiving it. See [Detect and filter self-generated events](/platform/forge/events-reference/product_events/#ignoreself). |
| actor | `Actor` | The user that has caused the event. |
| repository | `Repository` | The repository of the pull request the event is related to. |
| project | `Project` | The project of the pull request the event is related to. |
| workspace | `Workspace` | The workspace of the pull request the event is related to. |
| pullrequest | `PullRequest` | The pull request the event is related to. |

#### Type reference

```
```
1
2
```



```
interface Actor {
  type: string;
  accountId: string;
  uuid: string;
}

interface Repository {
  uuid: string;
  slug?: string;
}

interface Project {
  uuid: string;
}

interface Workspace {
  uuid: string;
}

interface Branch {
  branch: string;
  commit: {
    hash: string;
  };
}

interface Title {
  truncated: boolean;
  value: string;
}

interface Author {
  type: string;
  accountId: string;
  uuid: string;
  displayName: string;
}

interface PullRequest {
  id: number;
  state: string;
  source: Branch;
  destination: Branch;
  title?: Title;
  author?: Author;
  updatedOn?: string;
  createdOn?: string;
  commentCount?: number;
  taskCount?: number;
}
```
```

#### Example

This is an example payload of a pull request being created.

```
```
1
2
```



```
{
  "actor": {
    "type": "user",
    "accountId": "5ffed3379edf280075d75b20",
    "uuid": "{cc8e193d-7603-4dfd-8771-fcc8960aa0fb}"
  },
  "repository": {
    "uuid": "{15a31549-1cff-45dc-9d0d-310114c5038b}",
    "slug": "repository-slug"
  },
  "project": {
    "uuid": "{1860e69a-65c1-4ac2-8ab0-cbd2868e7573}"
  },
  "workspace": {
    "uuid": "{4c16a397-8e48-479c-8ca2-442e46c90570}"
  },
  "pullrequest": {
    "id": 3,
    "state": "OPEN",
    "source": {
      "branch": "Joshua-Tang/gitignore-edited-online-with-bitbucket-1683871668235",
      "commit": {
        "hash": "cc2758d231fc"
      }
    },
    "destination": {
      "branch": "master",
      "commit": {
        "hash": "a37e0ad81173"
      }
    },
    "updatedOn": "2026-06-01T03:12:16.159643+00:00",
    "createdOn": "2026-05-27T06:42:44.936130+00:00",
    "title": {
      "truncated": false,
      "value": "PR title"
    },
    "author": {
      "accountId": "712020:f44b4850-c6f6-54ce-9722-b800af117eb4",
      "type": "user",
      "uuid": "{c0de26c1-c01f-4d70-a19c-dac5a7b2e531}",
      "displayName": "Jane Smith"
    },
    "commentCount": 2,
    "taskCount": 2
  },
  "eventType": "avi:bitbucket:created:pullrequest",
  "timestamp": "2026-03-23T06:03:12.361017Z"
}
```
```

### Pull request updated

An event with the name `avi:bitbucket:updated:pullrequest` is sent when a pull request is updated.

The required OAuth scope is `read:pullrequest:bitbucket`.

#### Payload

| Name | Type | Description |
| --- | --- | --- |
| eventType | `string` | The event name `avi:bitbucket:updated:pullrequest`. |
| timestamp | `string` | The timestamp the event was emitted in ISO 8601 format. |
| selfGenerated | `boolean` | Whether the event was triggered by the app receiving it. See [Detect and filter self-generated events](/platform/forge/events-reference/product_events/#ignoreself). |
| actor | `Actor` | The user that has caused the event. |
| repository | `Repository` | The repository of the pull request the event is related to. |
| project | `Project` | The project of the pull request the event is related to. |
| workspace | `Workspace` | The workspace of the pull request the event is related to. |
| pullrequest | `PullRequest` | The pull request the event is related to. |

#### Type reference

```
```
1
2
```



```
interface Actor {
  type: string;
  accountId: string;
  uuid: string;
}

interface Repository {
  uuid: string;
  slug?: string;
}

interface Project {
  uuid: string;
}

interface Workspace {
  uuid: string;
}

interface Branch {
  branch: string;
  commit: {
    hash: string;
  };
}

interface Title {
  truncated: boolean;
  value: string;
}

interface Author {
  type: string;
  accountId: string;
  uuid: string;
  displayName: string;
}

interface PullRequest {
  id: number;
  state: string;
  source: Branch;
  destination: Branch;
  title?: Title;
  author?: Author;
  updatedOn?: string;
  createdOn?: string;
  commentCount?: number;
  taskCount?: number;
}
```
```

#### Example

This is an example payload of a pull request being updated.

```
```
1
2
```



```
{
  "actor": {
    "type": "user",
    "accountId": "5ffed3379edf280075d75b20",
    "uuid": "{cc8e193d-7603-4dfd-8771-fcc8960aa0fb}"
  },
  "repository": {
    "uuid": "{15a31549-1cff-45dc-9d0d-310114c5038b}",
    "slug": "repository-slug"
  },
  "project": {
    "uuid": "{1860e69a-65c1-4ac2-8ab0-cbd2868e7573}"
  },
  "workspace": {
    "uuid": "{4c16a397-8e48-479c-8ca2-442e46c90570}"
  },
  "pullrequest": {
    "id": 3,
    "state": "OPEN",
    "source": {
      "branch": "Joshua-Tang/gitignore-edited-online-with-bitbucket-1683871668235",
      "commit": {
        "hash": "cc2758d231fc"
      }
    },
    "destination": {
      "branch": "master",
      "commit": {
        "hash": "a37e0ad81173"
      }
    },
    "updatedOn": "2026-06-01T03:12:16.159643+00:00",
    "createdOn": "2026-05-27T06:42:44.936130+00:00",
    "title": {
      "truncated": false,
      "value": "PR title"
    },
    "author": {
      "accountId": "712020:f44b4850-c6f6-54ce-9722-b800af117eb4",
      "type": "user",
      "uuid": "{c0de26c1-c01f-4d70-a19c-dac5a7b2e531}",
      "displayName": "Jane Smith"
    },
    "commentCount": 2,
    "taskCount": 2
  },
  "eventType": "avi:bitbucket:updated:pullrequest",
  "timestamp": "2026-03-23T06:03:12.361017Z"
}
```
```

### Pull request fulfilled

An event with the name `avi:bitbucket:fulfilled:pullrequest` is sent when a pull request is merged.

The required OAuth scope is `read:pullrequest:bitbucket`.

#### Payload

| Name | Type | Description |
| --- | --- | --- |
| eventType | `string` | The event name `avi:bitbucket:fulfilled:pullrequest`. |
| timestamp | `string` | The timestamp the event was emitted in ISO 8601 format. |
| selfGenerated | `boolean` | Whether the event was triggered by the app receiving it. See [Detect and filter self-generated events](/platform/forge/events-reference/product_events/#ignoreself). |
| actor | `Actor` | The user that has caused the event. |
| repository | `Repository` | The repository of the pull request the event is related to. |
| project | `Project` | The project of the pull request the event is related to. |
| workspace | `Workspace` | The workspace of the pull request the event is related to. |
| pullrequest | `PullRequest` | The pull request the event is related to. |

#### Type reference

```
```
1
2
```



```
interface Actor {
  type: string;
  accountId: string;
  uuid: string;
}

interface Repository {
  uuid: string;
  slug?: string;
}

interface Project {
  uuid: string;
}

interface Workspace {
  uuid: string;
}

interface Hash {
  hash: string;
}

interface Branch {
  branch: string;
  commit: Hash;
}

interface Title {
  truncated: boolean;
  value: string;
}

interface Author {
  type: string;
  accountId: string;
  uuid: string;
  displayName: string;
}

interface PullRequest {
  id: number;
  state: string;
  source: Branch;
  destination: Branch;
  title?: Title;
  author?: Author;
  mergeCommit: Hash;
  updatedOn?: string;
  createdOn?: string;
  commentCount?: number;
  taskCount?: number;
}
```
```

#### Example

This is an example payload of a pull request being merged.

```
```
1
2
```



```
{
  "actor": {
    "type": "user",
    "accountId": "5ffed3379edf280075d75b20",
    "uuid": "{cc8e193d-7603-4dfd-8771-fcc8960aa0fb}"
  },
  "repository": {
    "uuid": "{15a31549-1cff-45dc-9d0d-310114c5038b}",
    "slug": "repository-slug"
  },
  "project": {
    "uuid": "{1860e69a-65c1-4ac2-8ab0-cbd2868e7573}"
  },
  "workspace": {
    "uuid": "{4c16a397-8e48-479c-8ca2-442e46c90570}"
  },
  "pullrequest": {
    "id": 3,
    "state": "MERGED",
    "source": {
      "branch": "Joshua-Tang/gitignore-edited-online-with-bitbucket-1683871668235",
      "commit": {
        "hash": "cc2758d231fc"
      }
    },
    "destination": {
      "branch": "master",
      "commit": {
        "hash": "a37e0ad81173"
      }
    },
    "mergeCommit": {
      "hash": "71e4ecfcd2ba"
    },
    "updatedOn": "2026-06-01T03:12:16.159643+00:00",
    "createdOn": "2026-05-27T06:42:44.936130+00:00",
    "title": {
      "truncated": false,
      "value": "PR title"
    },
    "author": {
      "accountId": "712020:f44b4850-c6f6-54ce-9722-b800af117eb4",
      "type": "user",
      "uuid": "{c0de26c1-c01f-4d70-a19c-dac5a7b2e531}",
      "displayName": "Jane Smith"
    },
    "commentCount": 2,
    "taskCount": 2
  },
  "eventType": "avi:bitbucket:fulfilled:pullrequest",
  "timestamp": "2026-03-23T06:03:12.361017Z"
}
```
```

### Pull request rejected

An event with the name `avi:bitbucket:rejected:pullrequest` is sent when a pull request is declined.

The required OAuth scope is `read:pullrequest:bitbucket`.

#### Payload

| Name | Type | Description |
| --- | --- | --- |
| eventType | `string` | The event name `avi:bitbucket:rejected:pullrequest`. |
| timestamp | `string` | The timestamp the event was emitted in ISO 8601 format. |
| selfGenerated | `boolean` | Whether the event was triggered by the app receiving it. See [Detect and filter self-generated events](/platform/forge/events-reference/product_events/#ignoreself). |
| actor | `Actor` | The user that has caused the event. |
| repository | `Repository` | The repository of the pull request the event is related to. |
| project | `Project` | The project of the pull request the event is related to. |
| workspace | `Workspace` | The workspace of the pull request the event is related to. |
| pullrequest | `PullRequest` | The pull request the event is related to. |

#### Type reference

```
```
1
2
```



```
interface Actor {
  type: string;
  accountId: string;
  uuid: string;
}

interface Repository {
  uuid: string;
  slug?: string;
}

interface Project {
  uuid: string;
}

interface Workspace {
  uuid: string;
}

interface Hash {
  hash: string;
}

interface Branch {
  branch: string;
  commit: Hash;
}

interface Title {
  truncated: boolean;
  value: string;
}

interface Author {
  type: string;
  accountId: string;
  uuid: string;
  displayName: string;
}

interface PullRequest {
  id: number;
  state: string;
  source: Branch;
  destination: Branch;
  title?: Title;
  author?: Author;
  mergeCommit: Hash;
  updatedOn?: string;
  createdOn?: string;
  commentCount?: number;
  taskCount?: number;
}
```
```

#### Example

This is an example payload of a pull request being declined.

```
```
1
2
```



```
{
  "actor": {
    "type": "user",
    "accountId": "5ffed3379edf280075d75b20",
    "uuid": "{cc8e193d-7603-4dfd-8771-fcc8960aa0fb}"
  },
  "repository": {
    "uuid": "{15a31549-1cff-45dc-9d0d-310114c5038b}",
    "slug": "repository-slug"
  },
  "project": {
    "uuid": "{1860e69a-65c1-4ac2-8ab0-cbd2868e7573}"
  },
  "workspace": {
    "uuid": "{4c16a397-8e48-479c-8ca2-442e46c90570}"
  },
  "pullrequest": {
    "id": 2,
    "state": "DECLINED",
    "source": {
      "branch": "Joshua-Tang/gitignore-edited-online-with-bitbucket-1683871668235",
      "commit": {
        "hash": "cc2758d231fc"
      }
    },
    "destination": {
      "branch": "master",
      "commit": {
        "hash": "a37e0ad81173"
      }
    },
    "updatedOn": "2026-06-01T03:12:16.159643+00:00",
    "createdOn": "2026-05-27T06:42:44.936130+00:00",
    "title": {
      "truncated": false,
      "value": "PR title"
    },
    "author": {
      "accountId": "712020:f44b4850-c6f6-54ce-9722-b800af117eb4",
      "type": "user",
      "uuid": "{c0de26c1-c01f-4d70-a19c-dac5a7b2e531}",
      "displayName": "Jane Smith"
    },
    "commentCount": 2,
    "taskCount": 2
  },
  "eventType": "avi:bitbucket:rejected:pullrequest",
  "timestamp": "2026-03-23T06:03:12.361017Z"
}
```
```

An event with the name `avi:bitbucket:created:pullrequest-comment` is sent when a pull request comment is created.

The required OAuth scope is `read:pullrequest:bitbucket`.

#### Payload

| Name | Type | Description |
| --- | --- | --- |
| eventType | `string` | The event name `avi:bitbucket:created:pullrequest-comment`. |
| timestamp | `string` | The timestamp the event was emitted in ISO 8601 format. |
| selfGenerated | `boolean` | Whether the event was triggered by the app receiving it. See [Detect and filter self-generated events](/platform/forge/events-reference/product_events/#ignoreself). |
| actor | `Actor` | The user that has caused the event. |
| repository | `Repository` | The repository of the pull request the event is related to. |
| project | `Project` | The project of the pull request the event is related to. |
| workspace | `Workspace` | The workspace of the pull request the event is related to. |
| pullrequest | `PullRequest` | The pull request the event is related to. |
| comment | `Comment` | The pull request comment that was created. |

#### Type reference

```
```
1
2
```



```
interface Actor {
  type: string;
  accountId: string;
  uuid: string;
}

interface Repository {
  uuid: string;
  slug?: string;
}

interface Project {
  uuid: string;
}

interface Workspace {
  uuid: string;
}

interface Hash {
  hash: string;
}

interface Branch {
  branch: string;
  commit: Hash;
}

interface Title {
  truncated: boolean;
  value: string;
}

interface Author {
  type: string;
  accountId: string;
  uuid: string;
  displayName: string;
}

interface PullRequest {
  id: number;
  state: string;
  source: Branch;
  destination: Branch;
  title?: Title;
  author?: Author;
  updatedOn?: string;
  createdOn?: string;
  commentCount?: number;
  taskCount?: number;
}

interface Comment {
  id: number;
}
```
```

#### Example

This is an example payload of a pull request comment being created.

```
```
1
2
```



```
{
    "timestamp": "2023-06-26T06:34:41.624814Z",
    "actor": {
      "type": "user",
      "accountId": "5ebbbc49ad226b0ba4518e11",
      "uuid": "{b0670c4c-4b6c-4f89-b47c-be2de5a64d58}"
    },
    "repository": {
      "uuid": "{30cbb1be-00da-425d-b3b1-29695ceb11f9}",
      "slug": "repository-slug"
    },
    "project": {
      "uuid": "{7805fc96-8fee-4a5c-91e5-457368075853}"
    },
    "workspace": {
      "uuid": "{6d1a0dc3-2eb4-4bdc-952f-af3b8fcbe13d}"
    },
    "pullrequest": {
      "id": 4,
      "state": "OPEN",
      "source": {
        "branch": "testbranch1",
        "commit": {
          "hash": "ea92ba633eac"
        }
      },
      "destination": {
        "branch": "master",
        "commit": {
          "hash": "ec8950c039c0"
        }
      },
      "updatedOn": "2026-06-01T03:12:16.159643+00:00",
      "createdOn": "2026-05-27T06:42:44.936130+00:00",
      "title": {
        "truncated": false,
        "value": "PR title"
      },
      "author": {
        "accountId": "712020:f44b4850-c6f6-54ce-9722-b800af117eb4",
        "type": "user",
        "uuid": "{c0de26c1-c01f-4d70-a19c-dac5a7b2e531}",
        "displayName": "Jane Smith"
      },
      "commentCount": 2,
      "taskCount": 2
    },
    "comment": {
      "id": 406336310
    },
    "eventType": "avi:bitbucket:created:pullrequest-comment"
}
```
```

An event with the name `avi:bitbucket:updated:pullrequest-comment` is sent when a pull request comment is updated 10 or more minutes after the comment was created or last updated.

The required OAuth scope is `read:pullrequest:bitbucket`.

#### Payload

| Name | Type | Description |
| --- | --- | --- |
| eventType | `string` | The event name `avi:bitbucket:updated:pullrequest-comment`. |
| timestamp | `string` | The timestamp the event was emitted in ISO 8601 format. |
| selfGenerated | `boolean` | Whether the event was triggered by the app receiving it. See [Detect and filter self-generated events](/platform/forge/events-reference/product_events/#ignoreself). |
| actor | `Actor` | The user that has caused the event. |
| repository | `Repository` | The repository of the pull request the event is related to. |
| project | `Project` | The project of the pull request the event is related to. |
| workspace | `Workspace` | The workspace of the pull request the event is related to. |
| pullrequest | `PullRequest` | The pull request the event is related to. |
| comment | `Comment` | The pull request comment that was updated. |

#### Type reference

```
```
1
2
```



```
interface Actor {
  type: string;
  accountId: string;
  uuid: string;
}

interface Repository {
  uuid: string;
  slug?: string;
}

interface Project {
  uuid: string;
}

interface Workspace {
  uuid: string;
}

interface Hash {
  hash: string;
}

interface Branch {
  branch: string;
  commit: Hash;
}

interface Title {
  truncated: boolean;
  value: string;
}

interface Author {
  type: string;
  accountId: string;
  uuid: string;
  displayName: string;
}

interface PullRequest {
  id: number;
  state: string;
  source: Branch;
  destination: Branch;
  title?: Title;
  author?: Author;
  updatedOn?: string;
  createdOn?: string;
  commentCount?: number;
  taskCount?: number;
}

interface Comment {
  id: number;
}
```
```

#### Example

This is an example payload of a pull request comment being updated.

```
```
1
2
```



```
{
    "timestamp": "2023-06-26T06:33:54.051247Z",
    "actor": {
        "type": "user",
        "accountId": "5ebbbc49ad226b0ba4518e11",
        "uuid": "{b0670c4c-4b6c-4f89-b47c-be2de5a64d58}"
    },
    "repository": {
        "uuid": "{30cbb1be-00da-425d-b3b1-29695ceb11f9}"
    },
    "project": {
        "uuid": "{7805fc96-8fee-4a5c-91e5-457368075853}"
    },
    "workspace": {
        "uuid": "{6d1a0dc3-2eb4-4bdc-952f-af3b8fcbe13d}"
    },
    "pullrequest": {
        "id": 4,
        "state": "OPEN",
        "source": {
            "branch": "testbranch1",
            "commit": {
                "hash": "ea92ba633eac"
            }
        },
        "destination": {
            "branch": "master",
            "commit": {
                "hash": "ec8950c039c0"
            }
        }
    },
    "comment": {
        "id": 398501799
    },
    "changes": {
        "content": {}
    },
    "eventType": "avi:bitbucket:updated:pullrequest-comment"
}
```
```

An event with the name `avi:bitbucket:deleted:pullrequest-comment` is sent when a pull request comment is deleted.

The required OAuth scope is `read:pullrequest:bitbucket`.

#### Payload

| Name | Type | Description |
| --- | --- | --- |
| eventType | `string` | The event name `avi:bitbucket:deleted:pullrequest-comment`. |
| timestamp | `string` | The timestamp the event was emitted in ISO 8601 format. |
| selfGenerated | `boolean` | Whether the event was triggered by the app receiving it. See [Detect and filter self-generated events](/platform/forge/events-reference/product_events/#ignoreself). |
| actor | `Actor` | The user that has caused the event. |
| repository | `Repository` | The repository of the pull request the event is related to. |
| project | `Project` | The project of the pull request the event is related to. |
| workspace | `Workspace` | The workspace of the pull request the event is related to. |
| pullrequest | `PullRequest` | The pull request the event is related to. |
| comment | `Comment` | The pull request comment that was deleted. |

#### Type reference

```
```
1
2
```



```
interface Actor {
  type: string;
  accountId: string;
  uuid: string;
}

interface Repository {
  uuid: string;
  slug?: string;
}

interface Project {
  uuid: string;
}

interface Workspace {
  uuid: string;
}

interface Hash {
  hash: string;
}

interface Branch {
  branch: string;
  commit: Hash;
}

interface Title {
  truncated: boolean;
  value: string;
}

interface Author {
  type: string;
  accountId: string;
  uuid: string;
  displayName: string;
}

interface PullRequest {
  id: number;
  state: string;
  source: Branch;
  destination: Branch;
  title?: Title;
  author?: Author;
  updatedOn?: string;
  createdOn?: string;
  commentCount?: number;
  taskCount?: number;
}

interface Comment {
  id: number;
}
```
```

#### Example

This is an example payload of a pull request comment being deleted.

```
```
1
2
```



```
{
    "timestamp": "2023-06-26T06:35:15.832298Z",
    "actor": {
        "type": "user",
        "accountId": "5ebbbc49ad226b0ba4518e11",
        "uuid": "{b0670c4c-4b6c-4f89-b47c-be2de5a64d58}"
    },
    "repository": {
        "uuid": "{30cbb1be-00da-425d-b3b1-29695ceb11f9}"
    },
    "project": {
        "uuid": "{7805fc96-8fee-4a5c-91e5-457368075853}"
    },
    "workspace": {
        "uuid": "{6d1a0dc3-2eb4-4bdc-952f-af3b8fcbe13d}"
    },
    "pullrequest": {
        "id": 4,
        "state": "OPEN",
        "source": {
          "branch": "testbranch1",
          "commit": {
              "hash": "ea92ba633eac"
          }
        },
        "destination": {
          "branch": "master",
          "commit": {
              "hash": "ec8950c039c0"
          }
        }
    },
    "comment": {
        "id": 406336310
    },
    "eventType": "avi:bitbucket:deleted:pullrequest-comment"
}
```
```

An event with the name `avi:bitbucket:resolved:pullrequest-comment` is sent when a pull request comment is resolved.

The required OAuth scope is `read:pullrequest:bitbucket`.

#### Payload

| Name | Type | Description |
| --- | --- | --- |
| eventType | `string` | The event name `avi:bitbucket:resolved:pullrequest-comment`. |
| timestamp | `string` | The timestamp the event was emitted in ISO 8601 format. |
| selfGenerated | `boolean` | Whether the event was triggered by the app receiving it. See [Detect and filter self-generated events](/platform/forge/events-reference/product_events/#ignoreself). |
| actor | `Actor` | The user that has caused the event. |
| repository | `Repository` | The repository of the pull request the event is related to. |
| project | `Project` | The project of the pull request the event is related to. |
| workspace | `Workspace` | The workspace of the pull request the event is related to. |
| pullrequest | `PullRequest` | The pull request the event is related to. |
| comment | `Comment` | The pull request comment that was resolved. |

#### Type reference

```
```
1
2
```



```
interface Actor {
  type: string;
  accountId: string;
  uuid: string;
}

interface Repository {
  uuid: string;
  slug?: string;
}

interface Project {
  uuid: string;
}

interface Workspace {
  uuid: string;
}

interface Hash {
  hash: string;
}

interface Branch {
  branch: string;
  commit: Hash;
}

interface Title {
  truncated: boolean;
  value: string;
}

interface Author {
  type: string;
  accountId: string;
  uuid: string;
  displayName: string;
}

interface PullRequest {
  id: number;
  state: string;
  source: Branch;
  destination: Branch;
  title?: Title;
  author?: Author;
  updatedOn?: string;
  createdOn?: string;
  commentCount?: number;
  taskCount?: number;
}

interface Comment {
  id: number;
}
```
```

#### Example

This is an example payload of a pull request comment being resolved.

```
```
1
2
```



```
{
    "timestamp": "2023-06-26T06:35:15.832298Z",
    "actor": {
        "type": "user",
        "accountId": "5ebbbc49ad226b0ba4518e11",
        "uuid": "{b0670c4c-4b6c-4f89-b47c-be2de5a64d58}"
    },
    "repository": {
        "uuid": "{30cbb1be-00da-425d-b3b1-29695ceb11f9}"
    },
    "project": {
        "uuid": "{7805fc96-8fee-4a5c-91e5-457368075853}"
    },
    "workspace": {
        "uuid": "{6d1a0dc3-2eb4-4bdc-952f-af3b8fcbe13d}"
    },
    "pullrequest": {
        "id": 4,
        "state": "OPEN",
        "source": {
          "branch": "testbranch1",
          "commit": {
              "hash": "ea92ba633eac"
          }
        },
        "destination": {
          "branch": "master",
          "commit": {
              "hash": "ec8950c039c0"
          }
        }
    },
    "comment": {
        "id": 406336310
    },
    "eventType": "avi:bitbucket:resolved:pullrequest-comment"
}
```
```

An event with the name `avi:bitbucket:reopened:pullrequest-comment` is sent when a pull request comment is reopened.

The required OAuth scope is `read:pullrequest:bitbucket`.

#### Payload

| Name | Type | Description |
| --- | --- | --- |
| eventType | `string` | The event name `avi:bitbucket:reopened:pullrequest-comment`. |
| timestamp | `string` | The timestamp the event was emitted in ISO 8601 format. |
| selfGenerated | `boolean` | Whether the event was triggered by the app receiving it. See [Detect and filter self-generated events](/platform/forge/events-reference/product_events/#ignoreself). |
| actor | `Actor` | The user that has caused the event. |
| repository | `Repository` | The repository of the pull request the event is related to. |
| project | `Project` | The project of the pull request the event is related to. |
| workspace | `Workspace` | The workspace of the pull request the event is related to. |
| pullrequest | `PullRequest` | The pull request the event is related to. |
| comment | `Comment` | The pull request comment that was reopened. |

#### Type reference

```
```
1
2
```



```
interface Actor {
  type: string;
  accountId: string;
  uuid: string;
}

interface Repository {
  uuid: string;
  slug?: string;
}

interface Project {
  uuid: string;
}

interface Workspace {
  uuid: string;
}

interface Hash {
  hash: string;
}

interface Branch {
  branch: string;
  commit: Hash;
}

interface Title {
  truncated: boolean;
  value: string;
}

interface Author {
  type: string;
  accountId: string;
  uuid: string;
  displayName: string;
}

interface PullRequest {
  id: number;
  state: string;
  source: Branch;
  destination: Branch;
  title?: Title;
  author?: Author;
  updatedOn?: string;
  createdOn?: string;
  commentCount?: number;
  taskCount?: number;
}

interface Comment {
  id: number;
}
```
```

#### Example

This is an example payload of a pull request comment being reopened.

```
```
1
2
```



```
{
    "timestamp": "2023-06-26T06:35:15.832298Z",
    "actor": {
        "type": "user",
        "accountId": "5ebbbc49ad226b0ba4518e11",
        "uuid": "{b0670c4c-4b6c-4f89-b47c-be2de5a64d58}"
    },
    "repository": {
        "uuid": "{30cbb1be-00da-425d-b3b1-29695ceb11f9}"
    },
    "project": {
        "uuid": "{7805fc96-8fee-4a5c-91e5-457368075853}"
    },
    "workspace": {
        "uuid": "{6d1a0dc3-2eb4-4bdc-952f-af3b8fcbe13d}"
    },
    "pullrequest": {
        "id": 4,
        "state": "OPEN",
        "source": {
          "branch": "testbranch1",
          "commit": {
              "hash": "ea92ba633eac"
          }
        },
        "destination": {
          "branch": "master",
          "commit": {
              "hash": "ec8950c039c0"
          }
        }
    },
    "comment": {
        "id": 406336310
    },
    "eventType": "avi:bitbucket:reopened:pullrequest-comment"
}
```
```

### Pull request reviewer status updated

An event with the name `avi:bitbucket:updated:pullrequest-reviewer-status` is
sent when a reviewer status (approved, changes requested) is updated. This
includes when their status is cleared because the source branch of the pull
request changed.

The required OAuth scope is `read:pullrequest:bitbucket`.

#### Payload

| Name | Type | Description |
| --- | --- | --- |
| eventType | `string` | The event name `avi:bitbucket:updated:pullrequest-reviewer-status`. |
| timestamp | `string` | The timestamp the event was emitted in ISO 8601 format. |
| selfGenerated | `boolean` | Whether the event was triggered by the app receiving it. See [Detect and filter self-generated events](/platform/forge/events-reference/product_events/#ignoreself). |
| actor | `Actor` | The user that has caused the event. |
| repository | `Repository` | The repository of the pull request the event is related to. |
| project | `Project` | The project of the pull request the event is related to. |
| workspace | `Workspace` | The workspace of the pull request the event is related to. |
| pullrequest | `PullRequest` | The pull request the event is related to. |
| reviewers | `Reviewers` | The reviewers and their review statuses. |

#### Type reference

```
```
1
2
```



```
interface Actor {
  type: string;
  accountId?: string;
  uuid?: string;
  kind?: string;
}

interface Repository {
  uuid: string;
  slug?: string;
}

interface Project {
  uuid: string;
}

interface Workspace {
  uuid: string;
}

interface Hash {
  hash: string;
}

interface Branch {
  branch: string;
  commit: Hash;
}

interface Title {
  truncated: boolean;
  value: string;
}

interface Author {
  type: string;
  accountId: string;
  uuid: string;
  displayName: string;
}

interface PullRequest {
  id: number;
  state: string;
  source: Branch;
  destination: Branch;
  title?: Title;
  author?: Author;
  updatedOn?: string;
  createdOn?: string;
  commentCount?: number;
  taskCount?: number;
}

interface Reviewer {
  user: Actor;
  status: string;
  timestamp: string;
}

interface Reviewers {
  value: Reviewer[];
  truncated: boolean;
}
```
```

#### Example

This is an example payload of a pull request reviewer status being updated.

```
```
1
2
```



```
{
    "timestamp": "2023-06-26T06:35:15.832298Z",
    "actor": {
        "type": "user",
        "accountId": "5ebbbc49ad226b0ba4518e11",
        "uuid": "{b0670c4c-4b6c-4f89-b47c-be2de5a64d58}"
    },
    "repository": {
        "uuid": "{30cbb1be-00da-425d-b3b1-29695ceb11f9}",
        "slug": "repository-slug"
    },
    "project": {
        "uuid": "{7805fc96-8fee-4a5c-91e5-457368075853}"
    },
    "workspace": {
        "uuid": "{6d1a0dc3-2eb4-4bdc-952f-af3b8fcbe13d}"
    },
    "pullrequest": {
        "id": 4,
        "state": "OPEN",
        "source": {
          "branch": "testbranch1",
          "commit": {
              "hash": "ea92ba633eac"
          }
        },
        "destination": {
          "branch": "master",
          "commit": {
              "hash": "ec8950c039c0"
          }
        },
        "updatedOn": "2026-06-01T03:12:16.159643+00:00",
        "createdOn": "2026-05-27T06:42:44.936130+00:00",
        "title": {
          "truncated": false,
          "value": "PR title"
        },
        "author": {
          "accountId": "712020:f44b4850-c6f6-54ce-9722-b800af117eb4",
          "type": "user",
          "uuid": "{c0de26c1-c01f-4d70-a19c-dac5a7b2e531}",
          "displayName": "Jane Smith"
        },
        "commentCount": 2,
        "taskCount": 2
    },
    "eventType": "avi:bitbucket:updated:pullrequest-reviewer-status",
    "reviewers": {
      "value": [
        {
          "user": {
            "type": "user",
            "accountId": "5d5353ed-743a-4f0a-8a86-1234567890ab",
            "uuid": "{87654321-4321-4321-4321-cba987654321}"
          },
          "status": "changes_requested",
          "timestamp": "2023-06-27T11:45:00Z"
        }
      ],
      "truncated": false
    }
}
```
```

## Deployment events

You can subscribe to these Bitbucket deployment events in Forge apps:

Each event has a different payload format.

### Deployment pending

An event with the name `avi:bitbucket:pending:deployment` is sent when a deployment step, in Bitbucket Pipelines, is ready to be triggered.

The required OAuth scope is `read:pipeline:bitbucket`.

#### Payload

| Name | Type | Description |
| --- | --- | --- |
| eventType | `string` | The event name `avi:bitbucket:pending:deployment`. |
| timestamp | `string` | The timestamp the event was emitted in ISO 8601 format. |
| selfGenerated | `boolean` | Whether the event was triggered by the app receiving it. See [Detect and filter self-generated events](/platform/forge/events-reference/product_events/#ignoreself). |
| repository | `Repository` | The repository of the deployment the event is related to. |
| workspace | `Workspace` | The workspace of the deployment the event is related to. |
| pipeline | `Pipeline` | The pipeline of the deployment the event is related to. |
| deployment | `Deployment` | The deployment the event is related to. |
| environment | `Environment` | The environment of the deployment the event is related to. |

#### Type reference

```
```
1
2
```



```
interface Repository {
  uuid: string;
  slug?: string;
}

interface Project {
  uuid: string;
}

interface Workspace {
  uuid: string;
}
interface Pipeline {
  uuid: string;
}
interface Deployment {
  uuid: string;
  state: string;
  status?: string;
  updatedTimestamp: string;
}
interface Environment {
  uuid: string;
  type: string;
  name: string;
}
```
```

#### Example

This is an example payload of a deployment step that is ready to be triggered.

```
```
1
2
```



```
{
  "repository": {
    "uuid": "{15a31549-1cff-45dc-9d0d-310114c5038b}"
  },
  "workspace": {
    "uuid": "{4c16a397-8e48-479c-8ca2-442e46c90570}"
  },
  "pipeline": {
    "uuid": "{2c727cf1-ae19-4b2d-96c0-5d513f12e004}"
  },
  "deployment": {
    "uuid": "{e057287a-3b30-4aaf-8ab4-7c638937b357}",
    "state": "UNKNOWN",
    "updatedTimestamp": "2024-11-15T03:08:01.556468172Z"
  },
  "environment": {
    "uuid": "{fc0697a9-b1d3-44b1-b296-2d7ed47ff150}",
    "type": "PRODUCTION",
    "name": "us-east-1"
  },
  "eventType": "avi:bitbucket:pending:deployment",
  "timestamp": "2024-11-15T03:08:01.556468Z"
}
```
```

### Deployment started

An event with the name `avi:bitbucket:started:deployment` is sent when a deployment step, in Bitbucket Pipelines, is started.

The required OAuth scope is `read:pipeline:bitbucket`.

#### Payload

| Name | Type | Description |
| --- | --- | --- |
| eventType | `string` | The event name `avi:bitbucket:started:deployment`. |
| timestamp | `string` | The timestamp the event was emitted in ISO 8601 format. |
| selfGenerated | `boolean` | Whether the event was triggered by the app receiving it. See [Detect and filter self-generated events](/platform/forge/events-reference/product_events/#ignoreself). |
| repository | `Repository` | The repository of the deployment the event is related to. |
| workspace | `Workspace` | The workspace of the deployment the event is related to. |
| pipeline | `Pipeline` | The pipeline of the deployment the event is related to. |
| deployment | `Deployment` | The deployment the event is related to. |
| environment | `Environment` | The environment of the deployment the event is related to. |

#### Type reference

```
```
1
2
```



```
interface Repository {
  uuid: string;
  slug?: string;
}

interface Project {
  uuid: string;
}

interface Workspace {
  uuid: string;
}
interface Pipeline {
  uuid: string;
}
interface Deployment {
  uuid: string;
  state: string;
  status?: string;
  updatedTimestamp: string;
}
interface Environment {
  uuid: string;
  type: string;
  name: string;
}
```
```

#### Example

This is an example payload of a deployment step being started.

```
```
1
2
```



```
{
  "repository": {
    "uuid": "{15a31549-1cff-45dc-9d0d-310114c5038b}"
  },
  "workspace": {
    "uuid": "{4c16a397-8e48-479c-8ca2-442e46c90570}"
  },
  "pipeline": {
    "uuid": "{2c727cf1-ae19-4b2d-96c0-5d513f12e004}"
  },
  "deployment": {
    "uuid": "{e057287a-3b30-4aaf-8ab4-7c638937b357}",
    "state": "IN_PROGRESS",
    "updatedTimestamp": "2024-11-15T03:08:01.556468172Z"
  },
  "environment": {
    "uuid": "{fc0697a9-b1d3-44b1-b296-2d7ed47ff150}",
    "type": "PRODUCTION",
    "name": "us-east-1"
  },
  "eventType": "avi:bitbucket:started:deployment",
  "timestamp": "2024-11-15T03:08:01.556468Z"
}
```
```

### Deployment completed

An event with the name `avi:bitbucket:completed:deployment` is sent when a deployment step, in Bitbucket Pipelines, is completed.

The required OAuth scope is `read:pipeline:bitbucket`.

#### Payload

| Name | Type | Description |
| --- | --- | --- |
| eventType | `string` | The event name `avi:bitbucket:completed:deployment`. |
| timestamp | `string` | The timestamp the event was emitted in ISO 8601 format. |
| selfGenerated | `boolean` | Whether the event was triggered by the app receiving it. See [Detect and filter self-generated events](/platform/forge/events-reference/product_events/#ignoreself). |
| repository | `Repository` | The repository of the deployment the event is related to. |
| workspace | `Workspace` | The workspace of the deployment the event is related to. |
| pipeline | `Pipeline` | The pipeline of the deployment the event is related to. |
| deployment | `Deployment` | The deployment the event is related to. |
| environment | `Environment` | The environment of the deployment the event is related to. |

#### Type reference

```
```
1
2
```



```
interface Repository {
  uuid: string;
  slug?: string;
}

interface Project {
  uuid: string;
}

interface Workspace {
  uuid: string;
}
interface Pipeline {
  uuid: string;
}
interface Deployment {
  uuid: string;
  state: string;
  status?: string;
  updatedTimestamp: string;
}
interface Environment {
  uuid: string;
  type: string;
  name: string;
}
```
```

#### Example

This is an example payload of a deployment step being completed.

```
```
1
2
```



```
{
  "repository": {
    "uuid": "{15a31549-1cff-45dc-9d0d-310114c5038b}"
  },
  "workspace": {
    "uuid": "{4c16a397-8e48-479c-8ca2-442e46c90570}"
  },
  "pipeline": {
    "uuid": "{2c727cf1-ae19-4b2d-96c0-5d513f12e004}"
  },
  "deployment": {
    "uuid": "{e057287a-3b30-4aaf-8ab4-7c638937b357}",
    "state": "COMPLETED",
    "status": "SUCCESSFUL",
    "updatedTimestamp": "2024-11-15T03:08:01.556468172Z"
  },
  "environment": {
    "uuid": "{fc0697a9-b1d3-44b1-b296-2d7ed47ff150}",
    "type": "PRODUCTION",
    "name": "us-east-1"
  },
  "eventType": "avi:bitbucket:completed:deployment",
  "timestamp": "2024-11-15T03:08:01.556468Z"
}
```
```
