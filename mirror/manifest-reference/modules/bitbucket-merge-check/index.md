# Bitbucket custom merge check

The `bitbucket:mergeCheck` module defines a custom merge check that runs in the context of a pull request. The module
allows a Forge app to define checks that can prevent pull requests from merging in Bitbucket until the specified conditions have been met.

The `bitbucket:mergeCheck` module is conceptually similar to the
[Forge trigger module](/platform/forge/manifest-reference/modules/trigger) in that the Forge infrastructure will invoke
the module only when the subscribed event occurs. A key difference is that `bitbucket:mergeCheck` is
triggered by granular, merge check specific, pull request focused [events](#triggers), as opposed to more general
[Product events](/platform/forge/events-reference/product_events/).

Another key difference is that the `bitbucket:mergeCheck` module must return a [response payload](#response-payload)
that indicates whether the check has passed or failed.

![Example of a bitbucket:mergeCheck in a pull request](https://dac-static.atlassian.com/platform/forge/images/bitbucket-merge-check-pr.png?_v=1.5800.1739)

Each module will be treated as its own **check** and have **independent results**. A check must pass for a
pull request to be merged if it is configured to be **Required** in either the **Workspace**, **Project**
or **Repository Settings** by an administrator. If the check is configured as **Not required**, then it is
informational only and will not block pull request merge. The check results are rendered on the pull request
page, which will help to guide the user towards the changes needed for the check to pass.

If the same check is configured at multiple levels (for example, in **Workspace** and **Repository** settings),
it will run once for each level. Results are still treated independently, so if the check was configured as
**Required** at one level, and it fails, the pull request merge will be blocked, regardless of whether or not
it was configured as **Not required** at another level.

Once a Forge app with a `bitbucket:mergeCheck` module has been installed into a Bitbucket workspace, the
**workspace admin** must [enable](https://support.atlassian.com/bitbucket-cloud/docs/set-up-and-use-custom-merge-checks/)
the `Custom merge checks` feature in the workspace settings before they can be configured.

![Enable the custom merge check feature in your workspace settings](https://dac-static.atlassian.com/platform/forge/images/bitbucket-merge-check-workspace-settings.png?_v=1.5800.1739)

After this, the check can be enabled by an appropriate admin at either the **repository**, **project** or **workspace**
level. The admin is also able to specify the PR target branch pattern that the check should be run against and whether
or not the check should be **Required**.

## Properties

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `key` | `string` | Yes | A key for the module, which other modules can refer to. Must be unique within the manifest.  *Regex:* `^[a-zA-Z0-9_-]+$` |
| `function` | `string` | Required if no `endpoint` is specified. | A reference to the `key` of the `function` that defines the check behavior.  *This function must return a [check result](#response-payload).* |
| `endpoint` | `string` | Required if no `function` is specified. | A reference to the `endpoint` that specifies the remote back end to invoke a check if you are using [Forge Remote](/platform/forge/remote) to integrate with a remote back end.  *This endpoint must return a [check result](#response-payload).* |
| `name` | `string` or `i18n object` | Yes | The name of the check which is displayed throughout the UI.  The `i18n object` allows for translation. See [i18n object](#i18n-object). |
| `description` | `string` or `i18n object` | No | The description of the check which is displayed in repository settings.  The `i18n object` allows for translation. See [i18n object](#i18n-object). |
| `triggers` | `Array<string>` | Yes | The list of [triggers](#triggers) the check is subscribed to / will be triggered by.  Requires *at least 1* element. |

### i18n object

| Key | Type | Required | Description |
| --- | --- | --- | --- |
| `i18n` | `string` | Yes | A key referencing a translated string in the translation files. For more details, see [Translations](/platform/forge/manifest-reference/translations). |

## Example

The snippet below defines a merge check that will be triggered when any commits have been pushed to the source branch of
the pull request.

```
```
1
2
```



```
modules:
  bitbucket:mergeCheck:
    - key: my-bitbucket-custom-merge-check
      function: check-function-impl
      name: My first custom merge check
      description: This is my first check
      triggers:
        - on-code-pushed
  function:
    - key: check-function-impl
      handler: index.myCheckFunction
```
```

## Scope

In order to subscribe to `bitbucket:mergeCheck` triggers, you need to add `read:pullrequest:bitbucket`
scope to your app manifest.

## Triggers

The triggers provide a mechanism for the `bitbucket:mergeCheck` module to control when the check should be invoked for a
given pull request. These can be seen as business events within the lifecycle of a pull request.

A `bitbucket:mergeCheck` module can subscribe to one or more existing triggers. This decision should be based on what
the check is validating. For instance, a check trying to enforce a code quality standard may only require the
`on-code-pushed` trigger, while a check preventing pull requests from being merged during a weekend may only require the
`on-merge` trigger.

It's important to remember that, unlike traditional Forge Functions, `bitbucket:mergeCheck` triggers will only invoke
the subscribed merge check functions if the repository that the event occurs within has the respective check enabled for
that repository. This prevents unnecessary invocations of the Forge functions containing the custom merge check logic.

| Trigger | Type | Description |
| --- | --- | --- |
| `on-code-pushed` | `pre-merge` | Will invoke the check every time new or updated commits are pushed to the `source` branch of the pull request. |
| `on-reviewer-status-changed` | `pre-merge` | Will invoke the check every time a reviewer status (*Approved* or *Changes Requested*) changes. This includes when a status is reset by a branch restriction due to the `source` branch of the pull request being modified (only available to Premium users).  Note that the check is **not** invoked when reviewers are added to or removed from the PR, only when the status of their review changes. |
| `on-merge` | `on-merge` | Will invoke the check as part of the process of merging the pull request. When the user attempts to merge the pull request, all `on-merge` custom merge checks will immediately be invoked, prior to the merge completing.  If this type of check ***fails***, the merge will be *aborted* if the check was configured to be **Required**. To **retry** the failed `on-merge` checks, another merge needs to be attempted by the **user.** |

## Invocation payload

Whenever a `bitbucket:mergeCheck` module is invoked, an event payload will be provided as an argument to the Forge
function. This payload provides the identifiers of the pull request that the check is being invoked against, and additional
properties where applicable.

| Parameter | Type | Description |
| --- | --- | --- |
| `workspace` | `Workspace` | The workspace containing the pull request the check is running against. |
| `repository` | `Repository` | The repository containing the pull request the check is running against. |
| `pullrequest` | `PullRequest` | The pull request the check is running against. |
| `trigger` | `Trigger` | The trigger that caused the invocation of the check. |
| `mergeProperties` | `MergeProperties` | The properties related to the pull request merge, including:  * The merge commit message (truncated at 1000 characters if necessary) * An indicator of whether the commit message was truncated * The merge strategy used * An indicator of whether to close the source branch after the merge   This is only included in the payload for `on-merge` checks. |

### Type reference

```
```
1
2
```



```
interface Workspace {
  uuid: string;
}

interface Repository {
  uuid: string;
}

interface PullRequest {
  id: number;
}

interface Trigger {
  type: string;
}

interface MergeProperties {
  commitMessage: string;
  commitMessageTruncated: boolean;
  mergeStrategy: string;
  closeSourceBranch: boolean;
}

interface PRCheckEvent {
  workspace: Workspace;
  repository: Repository;
  pullrequest: PullRequest;
  trigger: Trigger;
  mergeProperties?: MergeProperties;
}
```
```

### Example

This is an example payload of an on-code-pushed trigger.

```
```
1
2
```



```
{
  "workspace": {
    "uuid": "{cc8e193d-7603-4dfd-8771-fcc8960aa0fb}"
  },
  "repository": {
    "uuid": "{15a31549-1cff-45dc-9d0d-310114c5038b}"
  },
  "pullrequest": {
    "id": 123
  },
  "trigger": {
    "type": "on-code-pushed"
  }
}
```
```

### Example

This is an example payload of an on-merge trigger.

```
```
1
2
```



```
{
  "workspace": {
    "uuid": "{cc8e193d-7603-4dfd-8771-fcc8960aa0fb}"
  },
  "repository": {
    "uuid": "{15a31549-1cff-45dc-9d0d-310114c5038b}"
  },
  "pullrequest": {
    "id": 123
  },
  "trigger": {
    "type": "on-code-pushed"
  },
  "mergeProperties": {
    "commitMessage": "Merged in testbranch (pull request #5)\n\ntesting PR\n\n",
    "commitMessageTruncated": false,
    "mergeStrategy": "merge_commit",
    "closeSourceBranch": true
  }
}
```
```

## Response payload

The only responsibility of the function registered against the `bitbucket:mergeCheck` module is that it returns a
well-defined response payload every time the Bitbucket Forge infrastructure invokes it.

This result produced by each invocation of the `bitbucket:mergeCheck` module is handled and stored by the Bitbucket
Forge infrastructure, there is no requirement for the Forge app to store it, or send the response back to a specific
Bitbucket API. The merge check is only expected to calculate and return result in the correct response format.

If any exceptions are thrown when executing the check logic, the check result will be treated as a failure.
Note that the user can individually rerun failed checks.

### Merge check results in the Bitbucket UI

![Example of a bitbucket:mergeCheck in a pull request, annotated with identifiers](https://dac-static.atlassian.com/platform/forge/images/bitbucket-merge-check-details.png?_v=1.5800.1739)

1. **Merge check result:** derived from response payload `success` field.
2. **Merge check name:** derived from the module `name` field.
3. **Merge check message:** derived from the response payload `message` field.
4. **Configured branch:** the branch(es) the check has been configured to run against by the administrator.
5. **Configured resource:** the resource level the check has been configured at by the administrator.

### Properties

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `success` | `boolean` | Yes | Whether or not the check has passed.  *If `false` Bitbucket will prevent the pull request from being merged.* |
| `message` | `string` | No | A message related to the result of the check.  *Useful for providing detail to the users about why the check failed, giving hints to what needs to be fixed in the pull request.* |

### Type reference

```
```
1
2
```



```
interface MergeCheckResponse{
  success: boolean;
  message?: string;
}
```
```

### Example

```
```
1
2
```



```
{
  "success": false,
  "message": "No merges after 5pm"
}
```
```
