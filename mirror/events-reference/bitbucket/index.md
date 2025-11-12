# Bitbucket events

Forge apps can subscribe to Bitbucket events for:

Your Forge app must have permission from the
workspace admin to access the data it provides within the event payload.
The OAuth scope required for each event is documented below.

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
| actor | `Actor` | The user that has caused the event. |
| repository | `BitbucketResource` | The repository the event is related to. |
| project | `BitbucketResource` | The project of the repository the event is related to. |
| workspace | `BitbucketResource` | The workspace of the repository the event is related to. |

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

interface BitbucketResource {
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
    "uuid": "{15a31549-1cff-45dc-9d0d-310114c5038b}"
  },
  "project": {
    "uuid": "{1860e69a-65c1-4ac2-8ab0-cbd2868e7573}"
  },
  "workspace": {
    "uuid": "{4c16a397-8e48-479c-8ca2-442e46c90570}"
  },
  "eventType": "avi:bitbucket:created:repository"
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
| actor | `Actor` | The user that has caused the event. |
| repository | `BitbucketResource` | The repository the event is related to. |
| project | `BitbucketResource` | The project of the repository the event is related to. |
| workspace | `BitbucketResource` | The workspace of the repository the event is related to. |
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

interface BitbucketResource {
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
| actor | `Actor` | The user that has caused the event. |
| repository | `BitbucketResource` | The repository the event is related to. |
| project | `BitbucketResource` | The project of the repository the event is related to. |
| workspace | `BitbucketResource` | The workspace of the repository the event is related to. |
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

interface BitbucketResource {
  uuid: string;
}

interface TruncatedValue {
  value: string;
  truncated: boolean;
}

interface Commit {
  hash: string;
  message: TruncatedValue;
  date: string;
  author: Actor;
}

interface CommitPush {
  ref: string;
  before: string | null;
  after: string | null;
  created: boolean;
  closed: boolean;
  forced: boolean;
  truncated: boolean;
  commits: Commit[];
}

interface TagPush {
  date: string | null;
  message: TruncatedValue | null;
  author: Actor | null;
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
    "uuid": "{15a31549-1cff-45dc-9d0d-310114c5038b}"
  },
  "project": {
    "uuid": "{1860e69a-65c1-4ac2-8ab0-cbd2868e7573}"
  },
  "workspace": {
    "uuid": "{4c16a397-8e48-479c-8ca2-442e46c90570}"
  },
  "push": {
    "ref": "main",
    "before": null,
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
  "eventType": "avi:bitbucket:push:repository"
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
| actor | `Actor` | The user that has caused the event. |
| repository | `BitbucketResource` | The repository the event is related to. |
| project | `BitbucketResource` | The project of the repository the event is related to. |
| workspace | `BitbucketResource` | The workspace of the repository the event is related to. |

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

interface BitbucketResource {
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
  "eventType": "avi:bitbucket:deleted:repository"
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
| actor | `Actor` | The user that has caused the event. |
| repository | `BitbucketResource` | The repository the event is related to. |
| project | `BitbucketResource` | The parent project of the repository that the event is related to. |
| workspace | `BitbucketResource` | The workspace of the repository the event is related to. |
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

interface BitbucketResource {
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
    "updatedOn": "2025-01-31T00:42:46.866808Z"
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
| actor | `Actor` | The user that has caused the event. |
| repository | `BitbucketResource` | The repository the event is related to. |
| project | `BitbucketResource` | The parent project of the repository that the event is related to. |
| workspace | `BitbucketResource` | The workspace of the repository the event is related to. |
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

interface BitbucketResource {
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
    "state": "SUCCESSFUL",
    "url": "https://some.url.com",
    "commit": {
      "hash": "b88c4b490b648bf960eba6f59123456797960e55"
    },
    "createdOn": "2025-01-31T00:42:46.866793Z",
    "updatedOn": "2025-01-31T01:03:17.105700Z"
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
| actor | `Actor` | The user that has caused the event. |
| repository | `BitbucketResource` | The repository of the commit the event is related to. |
| project | `BitbucketResource` | The project of the commit the event is related to. |
| workspace | `BitbucketResource` | The workspace of the commit the event is related to. |
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

interface BitbucketResource {
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
    "uuid": "{ea73e3cd-f7ee-4fac-aeaa-a4e4b77ba8c9}"
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
| actor | `Actor` | The user that has caused the event. |
| repository | `BitbucketResource` | The repository of the pull request the event is related to. |
| project | `BitbucketResource` | The project of the pull request the event is related to. |
| workspace | `BitbucketResource` | The workspace of the pull request the event is related to. |
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

interface BitbucketResource {
  uuid: string;
}

interface Branch {
  branch: string;
  commit: {
    hash: string;
  };
}

interface PullRequest {
  id: number;
  state: string;
  source: Branch;
  destination: Branch;
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
    "uuid": "{15a31549-1cff-45dc-9d0d-310114c5038b}"
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
    }
  },
  "eventType": "avi:bitbucket:created:pullrequest"
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
| actor | `Actor` | The user that has caused the event. |
| repository | `BitbucketResource` | The repository of the pull request the event is related to. |
| project | `BitbucketResource` | The project of the pull request the event is related to. |
| workspace | `BitbucketResource` | The workspace of the pull request the event is related to. |
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

interface BitbucketResource {
  uuid: string;
}

interface Branch {
  branch: string;
  commit: {
    hash: string;
  };
}

interface PullRequest {
  id: number;
  state: string;
  source: Branch;
  destination: Branch;
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
    "uuid": "{15a31549-1cff-45dc-9d0d-310114c5038b}"
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
    }
  },
  "eventType": "avi:bitbucket:updated:pullrequest"
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
| actor | `Actor` | The user that has caused the event. |
| repository | `BitbucketResource` | The repository of the pull request the event is related to. |
| project | `BitbucketResource` | The project of the pull request the event is related to. |
| workspace | `BitbucketResource` | The workspace of the pull request the event is related to. |
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

interface BitbucketResource {
  uuid: string;
}

interface Hash {
  hash: string;
}

interface Branch {
  branch: string;
  commit: Hash;
}

interface PullRequest {
  id: number;
  state: string;
  source: Branch;
  destination: Branch;
  mergeCommit: Hash;
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
    "uuid": "{15a31549-1cff-45dc-9d0d-310114c5038b}"
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
    }
  },
  "eventType": "avi:bitbucket:fulfilled:pullrequest"
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
| actor | `Actor` | The user that has caused the event. |
| repository | `BitbucketResource` | The repository of the pull request the event is related to. |
| project | `BitbucketResource` | The project of the pull request the event is related to. |
| workspace | `BitbucketResource` | The workspace of the pull request the event is related to. |
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

interface BitbucketResource {
  uuid: string;
}

interface Hash {
  hash: string;
}

interface Branch {
  branch: string;
  commit: Hash;
}

interface PullRequest {
  id: number;
  state: string;
  source: Branch;
  destination: Branch;
  mergeCommit: Hash;
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
    "uuid": "{15a31549-1cff-45dc-9d0d-310114c5038b}"
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
    }
  },
  "eventType": "avi:bitbucket:rejected:pullrequest"
}
```
```

An event with the name `avi:bitbucket:created:pullrequest-comment` is sent when a pull request comment is created.

The required OAuth scope is `read:pullrequest:bitbucket`.

#### Payload

| Name | Type | Description |
| --- | --- | --- |
| eventType | `string` | The event name `avi:bitbucket:created:pullrequest-comment`. |
| actor | `Actor` | The user that has caused the event. |
| repository | `BitbucketResource` | The repository of the pull request the event is related to. |
| project | `BitbucketResource` | The project of the pull request the event is related to. |
| workspace | `BitbucketResource` | The workspace of the pull request the event is related to. |
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

interface BitbucketResource {
  uuid: string;
}

interface Hash {
  hash: string;
}

interface Branch {
  branch: string;
  commit: Hash;
}

interface PullRequest {
  id: number;
  state: string;
  source: Branch;
  destination: Branch;
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
| actor | `Actor` | The user that has caused the event. |
| repository | `BitbucketResource` | The repository of the pull request the event is related to. |
| project | `BitbucketResource` | The project of the pull request the event is related to. |
| workspace | `BitbucketResource` | The workspace of the pull request the event is related to. |
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

interface BitbucketResource {
  uuid: string;
}

interface Hash {
  hash: string;
}

interface Branch {
  branch: string;
  commit: Hash;
}

interface PullRequest {
  id: number;
  state: string;
  source: Branch;
  destination: Branch;
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
| actor | `Actor` | The user that has caused the event. |
| repository | `BitbucketResource` | The repository of the pull request the event is related to. |
| project | `BitbucketResource` | The project of the pull request the event is related to. |
| workspace | `BitbucketResource` | The workspace of the pull request the event is related to. |
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

interface BitbucketResource {
  uuid: string;
}

interface Hash {
  hash: string;
}

interface Branch {
  branch: string;
  commit: Hash;
}

interface PullRequest {
  id: number;
  state: string;
  source: Branch;
  destination: Branch;
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
| actor | `Actor` | The user that has caused the event. |
| repository | `BitbucketResource` | The repository of the pull request the event is related to. |
| project | `BitbucketResource` | The project of the pull request the event is related to. |
| workspace | `BitbucketResource` | The workspace of the pull request the event is related to. |
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

interface BitbucketResource {
  uuid: string;
}

interface Hash {
  hash: string;
}

interface Branch {
  branch: string;
  commit: Hash;
}

interface PullRequest {
  id: number;
  state: string;
  source: Branch;
  destination: Branch;
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
| actor | `Actor` | The user that has caused the event. |
| repository | `BitbucketResource` | The repository of the pull request the event is related to. |
| project | `BitbucketResource` | The project of the pull request the event is related to. |
| workspace | `BitbucketResource` | The workspace of the pull request the event is related to. |
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

interface BitbucketResource {
  uuid: string;
}

interface Hash {
  hash: string;
}

interface Branch {
  branch: string;
  commit: Hash;
}

interface PullRequest {
  id: number;
  state: string;
  source: Branch;
  destination: Branch;
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
| actor | `Actor` | The user that has caused the event. |
| repository | `BitbucketResource` | The repository of the pull request the event is related to. |
| project | `BitbucketResource` | The project of the pull request the event is related to. |
| workspace | `BitbucketResource` | The workspace of the pull request the event is related to. |
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

interface BitbucketResource {
  uuid: string;
}

interface Hash {
  hash: string;
}

interface Branch {
  branch: string;
  commit: Hash;
}

interface PullRequest {
  id: number;
  state: string;
  source: Branch;
  destination: Branch;
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
    "eventType": "avi:bitbucket:updated:pullrequest-reviewer-status",
    "reviewers": {
      "value": [
        {
          "user": {
            "type": "user",
            "accountId": "5d5353ed-743a-4f0a-8a86-1234567890ab",
            "uuid": "{87654321-4321-4321-4321-cba987654321}",
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
