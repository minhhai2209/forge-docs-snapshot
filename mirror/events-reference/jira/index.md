# Jira events

Forge apps can subscribe to Jira events for:

## Core issue events

| Event | Description |
| --- | --- |
| [Issues](#issue-events) | Subscribe to core issue lifecycle events (created, updated, deleted, assigned, viewed, mentioned). Essential for automation workflows, notifications, and audit trails. |
| [Issue links](#issue-link-events) | Track relationship changes between issues (blocks, relates to, etc.). Only supports links within a single Jira instance. |
| [Issue worklogs](#issue-worklog-events) | Monitor time tracking changes for reporting and billing integrations. Includes author, time spent, and work description data. |
| [Issue type](#issue-type-events) | Track changes to issue type definitions (Story, Bug, Task, etc.). Useful for workflow and field configuration management. |

## Content and collaboration events

| Event | Description |
| --- | --- |
| [Comments](#comment-events) | Monitor comment activity and @mentions for collaboration features. Includes rich text content and visibility settings. |
| [Custom fields](#custom-field-events) | Track custom field lifecycle including Forge app fields. Supports trash/restore operations for safe field management. |
| [Custom field context](#custom-field-context-events) | Monitor field scope changes (which projects/issue types use a field). Essential for field configuration management. |
| [Custom field context configuration](#custom-field-context-configuration-events) | Single event type for field behavior updates. Tracks configuration changes like default values and options. |

## Workflow and project events

| Event | Description |
| --- | --- |
| [Workflows](#workflow-events) | Monitor workflow transitions and Forge function execution. Includes error handling for failed expressions and post-functions. |
| [Project versions](#project-version-events) | Track release management lifecycle (created, released, archived, merged). Includes version replacement data for deletions. |
| [Projects](#project-events) | Monitor project lifecycle and administration changes. Includes soft-delete (trash) and restoration capabilities. |
| [Components](#component-events) | Monitor project component changes for team organization. Includes assignee type and lead information. |

| Event | Description |
| --- | --- |
| [Attachments](#attachment-events) | Track file uploads and deletions on issues. Includes metadata like file size, MIME type, and author information. |
| [Users](#user-events) | Track user account changes for access management. Requires `read:jira-user` scope for user administration features. |
| [Filters](#filter-events) | Monitor saved search filter changes. Includes JQL queries and ownership information for dashboard integrations. |

## System configuration events

| Event | Description |
| --- | --- |
| [Time tracking provider](#time-tracking-provider-events) | Single event for time tracking system changes. Monitors switches between Jira's built-in and third-party time tracking apps. |
| [Configuration](#configuration-events) | Monitor Jira global settings changes (subtasks, voting, watching, issue linking). Essential for system administration apps. |

Your Forge app must have permission from the
site admin to access the data it provides within the event payload.
The OAuth scope required for each event is documented below.

## Issue events

[↑ Back to top](#core-issue-events)

You can subscribe to these Jira issue events in Forge apps:

Each event has a different payload format.

### Issue created

An event with the name `avi:jira:created:issue` is sent when an issue is created.

The required OAuth scope is `read:jira-work`.

Payload

Type reference

Example

| Name | Type | Description |
| --- | --- | --- |
| eventType | `string` | The event name `avi:jira:created:issue`. |
| issue | `Issue` | The issue the event is related to. |
| atlassianId? | `string` | [Optional] The ID of the user that has caused the event. |
| associatedUsers? | `AssociatedUsers` | [Optional] An object containing an array of one user, with the user being the one who created the issue. |

### Issue updated

An event with the name `avi:jira:updated:issue` is sent when any field on an issue is modified.
The level of detail in the event's changelog depends on which field is changed.

The required OAuth scope is `read:jira-work`.

Payload

Type reference

Example

| Name | Type | Description |
| --- | --- | --- |
| eventType | `string` | The event name `avi:jira:updated:issue`. |
| issue | `Issue` | The issue the event relates to. |
| atlassianId? | `string` | [Optional] The ID of the user that has caused the event. |
| changelog | `Changelog` | A list of changes that have occurred in the update. The `to` and `from` fields display the previous and new values for each changed field respectively, or `null` when a field was empty or is being cleared. |
| associatedUsers? | `AssociatedUsers` | [Optional] An object containing an array of users, with the users being the one who made the update, and any assigned or unassigned users in the update being made. |
| associatedStatuses? | `AssociatedStatuses` | [Optional] If the issue status is updated, this contains an array of the current and previous statuses. Otherwise, this field is undefined. You can tell which is the current status by checking the changelog field. |

### Issue deleted

An event with the name `avi:jira:deleted:issue` is sent when an issue is deleted.

Keep in mind that cascading events aren’t emitted. For more information, see: [Cascading events guide](/platform/forge/events/#handling-cascading-events-in-jira).

The required OAuth scope is `read:jira-work`.

Payload

Type reference

Example

| Name | Type | Description |
| --- | --- | --- |
| eventType | `string` | The event name `avi:jira:deleted:issue`. |
| issue | `Issue` | The issue the event relates to. |
| atlassianId? | `string` | [Optional] The ID of the user that triggered the event. |
| associatedUsers? | `AssociatedUsers` | [Optional] An array containing the name of the user who deleted the issue. |

### Issue assigned

An event with the name `avi:jira:assigned:issue` is sent when a user is assigned or unassigned from an issue.
An "[issue updated](#issue-updated)" event will also be sent when this occurs.

The required OAuth scope is `read:jira-work`.

Payload

Type reference

Example

| Name | Type | Description |
| --- | --- | --- |
| eventType | `string` | The event name `avi:jira:assigned:issue`. |
| issue | `Issue` | The issue the event is related to. |
| atlassianId? | `string` | [Optional] The ID of the user that has caused the event. |
| changelog | `Changelog` | A list of changes that have occurred in the update. The `to` and `from` fields display the accounts IDs of the assignees that the issue was to and from respectively, or `null` when the issue is unassigned or was previously unassigned. |
| associatedUsers? | `AssociatedUsers` | [Optional] An object containing an array of users, with the users being the one who made the update, and any users assigned or unassigned in the update being made. |

### Issue viewed

An event with the name `avi:jira:viewed:issue` is sent every time an issue is viewed by a user.

The required OAuth scope is `read:jira-work`.

Payload

Type reference

Example

| Name | Type | Description |
| --- | --- | --- |
| eventType | `string` | The event name `avi:jira:viewed:issue`. |
| issue | `Issue` | The issue the event is related to. |
| atlassianId | `string` | The ID of the user that has caused the event. |
| user | `User` | The user who has viewed the issue. |

### Mentioned on issue

An event with the name `avi:jira:mentioned:issue` is sent every time an issue description is updated and users are mentioned.
All users mentioned in the description are included in one event. A user mentioning themselves does not count as a mention.

The required OAuth scope is `read:jira-work`.

Payload

Type reference

Example

| Name | Type | Description |
| --- | --- | --- |
| eventType | `string` | The event name `avi:jira:mentioned:issue`. |
| issue | `Issue` | The issue the event is related to. |
| atlassianId? | `string` | [Optional] The ID of the user that has caused the event. |
| mentionedAccountIds | `string[]` | A list of account IDs of mentioned users. |

## Issue link events

[↑ Back to top](#core-issue-events)

You can subscribe to the following Jira issue link events in Forge apps:

* created: `avi:jira:created:issuelink`
* deleted: `avi:jira:deleted:issuelink`

The payload for all of these events is the same.

The required OAuth scope is `read:jira-work`.

We only support issue links within a single Jira instance.

This means that an event will not be triggered for links created between two Jira instances.

Payload

Type reference

Example

| Name | Type | Description |
| --- | --- | --- |
| eventType | `string` | The event name, such as `avi:jira:created:issuelink`. |
| id | `string` | ID of the link. |
| sourceIssueId | `string` | ID of the source issue. |
| destinationIssueId | `string` | ID of the destination issue. |
| issueLinkType | `IssueLinkType` | An object containing information about the link type. |

## Issue worklog events

[↑ Back to top](#core-issue-events)

You can subscribe to these worklog events in Forge apps:

* Created: `avi:jira:created:worklog`
* Updated: `avi:jira:updated:worklog`
* Deleted: `avi:jira:deleted:worklog`

Keep in mind that for deletions, cascading events aren’t emitted. For more information, see: [Cascading events guide](/platform/forge/events/#handling-cascading-events-in-jira).

OAuth 2.0 scopes required:

**Classic**: `read:jira-work`

**Granular**: `read:comment:jira`, `read:group:jira`, `read:issue-worklog:jira`, `read:issue-worklog.property:jira`, `read:project-role:jira`, `read:user:jira`, `read:avatar:jira`

Payload

Type reference

Example

| Name | Type | Description |
| --- | --- | --- |
| eventType | `string` | The event name, such as `avi:jira:updated:worklog`. |
| worklog | `Worklog` | The worklog the event is related to. |

## Issue type events

[↑ Back to top](#core-issue-events)

Your app must have permission from the
site admin to access the data it provides within the event payload.
The OAuth scopes required for each event are documented below.
You can subscribe to the following issue type events in Forge apps:

* Issue type created: `avi:jira:created:issuetype`
* Issue type updated: `avi:jira:updated:issuetype`
* Issue type deleted: `avi:jira:deleted:issuetype`

OAuth 2.0 scopes required:

**Classic**: `manage:jira-configuration`

**Granular**: `read:issue-type:jira`

All events have the same payload format.

Payload

Type reference

Example

| Name | Type | Description |
| --- | --- | --- |
| eventType | `string` | The event name, such as `avi:jira:created:issuetype`. |
| issueType | `issueType` | The `issueType` the event is related to. |
| atlassianId? | `string` | [Optional] The ID of the user that has caused the event. |

[↑ Back to top](#content-and-collaboration-events)

Forge apps can subscribe to these Jira comment events:

An event with the name `avi:jira:commented:issue` is sent each time a comment is created or edited.

The required OAuth scope is `read:jira-work`.

Payload

Type reference

Example

| Name | Type | Description |
| --- | --- | --- |
| eventType | `string` | The event name `avi:jira:commented:issue`. |
| issue | `Issue` | The issue the event is related to. |
| atlassianId? | `string` | [Optional] The ID of the user that has caused the event. |
| associatedUsers? | `AssociatedUsers` | [Optional] The user who has made the comment. |
| comment | `Comment` | An object describing the comment, including its author, body content, and other metadata. |

An event with the name `avi:jira:mentioned:comment` is sent each time users are mentioned when a comment is created or edited.
All users mentioned in the comment are included in one event.

The required OAuth scope is `read:jira-work`.

Payload

Type reference

Example

| Name | Type | Description |
| --- | --- | --- |
| eventType | `string` | The event name `avi:jira:mentioned:comment`. |
| issue | `Issue` | The issue the event is related to. |
| atlassianId? | `string` | [Optional] The ID of the user that has caused the event. |
| mentionedAccountIds | `string[]` | A list of the account IDs of the users mentioned in the comment. |
| comment | `Comment` | An object describing the comment, including its author, body content, and other metadata. |

An event with the name `avi:jira:deleted:comment` is sent each time a comment is deleted.

Keep in mind that cascading events aren’t emitted. For more information, see: [Cascading events guide](/platform/forge/events/#handling-cascading-events-in-jira).

The required OAuth scope is `read:jira-work`.

Payload

Type reference

Example

| Name | Type | Description |
| --- | --- | --- |
| eventType | `string` | The event name `avi:jira:deleted:comment`. |
| issue | `Issue` | The issue the event is related to. |
| atlassianId? | `string` | [Optional] The ID of the user that has caused the event. |
| comment | `Comment` | An object describing the comment, including its author, body content, and other metadata. |

## Custom field events

[↑ Back to top](#content-and-collaboration-events)

You can subscribe to these Jira custom field events in Forge apps:

* Created: `avi:jira:created:field`
* Updated: `avi:jira:updated:field`
* Trashed: `avi:jira:trashed:field`
* Restored: `avi:jira:restored:field`
* Deleted: `avi:jira:deleted:field`

The payload for all of these events is the same.

The required OAuth scope is `manage:jira-configuration`.

| Name | Type | Description |
| --- | --- | --- |
| eventType | `string` | The event name, such as `avi:jira:created:field`. |
| id | `string` | ID of the custom field. |
| key | `string` | Key of the custom field. |
| type | `string` | Custom field type. |
| typeName | `string` | Custom field type name. |
| name | `string` | Name of the custom field. |
| description | `string` | Description of the custom field. |

## Custom field context events

[↑ Back to top](#content-and-collaboration-events)

You can subscribe to these Jira custom field context events in Forge apps:

* Created: `avi:jira:created:field:context`
* Updated: `avi:jira:updated:field:context`
* Deleted: `avi:jira:deleted:field:context`

The payload for all of these events is the same.

The required OAuth scope is `manage:jira-configuration`.

| Name | Type | Description |
| --- | --- | --- |
| eventType | `string` | The event name, such as `avi:jira:created:field:context`. |
| id | `string` | ID of the context. |
| fieldId | `string` | ID of the custom field. |
| fieldKey | `string` | Key of the custom field. |
| name | `string` | Name of the custom field context. |
| description | `string` | Description of the custom field context. |
| projectIds | `long[]` | List of project IDs associated with the context. If the list is empty, the context is global. |
| issueTypeIds | `string[]` | List of issue types IDs for the context. If the list is empty, the context refers to all issue types. |

## Custom field context configuration events

[↑ Back to top](#content-and-collaboration-events)

| Name | Type | Description |
| --- | --- | --- |
| eventType | `string` | The event name `avi:jira:updated:field:context:configuration`. |
| customFieldId | `string` | ID of the custom field. |
| customFieldKey | `string` | Key of the custom field. |
| configurationId | `long` | ID of the configuration. |
| fieldContextId | `long` | ID of the context. |
| configuration | `string` | Stringified JSON of the updated configuration. |

## Workflow events

[↑ Back to top](#workflow-and-project-events)

You can subscribe to these Jira workflow events in Forge apps:

Other Jira events can also be sent after transitioning an issue, depending on what has changed during the transition:

* [Issue created](#issue-created): `avi:jira:created:issue` for the initial transition
* [Issue updated](#issue-updated): `avi:jira:updated:issue` for other transitions
* [Issue deleted](#issue-deleted): `avi:jira:deleted:issue` when issue has been deleted
* [Issue assigned](#issue-assigned): `avi:jira:assigned:issue` if the issue is assigned while making a transition
* [Mentioned on issue](#mentioned-on-issue): `avi:jira:mentioned:issue` when a user is mentioned on an issue while making a transition
* [Comment on issue](#comment-on-issue): `avi:jira:commented:issue` if a comment is added while making a transition

### Expression evaluation failed

Whenever an
app-registered [Forge workflow condition](/platform/forge/manifest-reference/modules/jira-workflow-condition) or
[Forge workflow validator](/platform/forge/manifest-reference/modules/jira-workflow-validator)
based on a Jira expression fails while executing, an `avi:jira:failed:expression` event is sent.

You can subscribe to this event in Forge apps. This event will only reach the app that registered the failing
expression.

OAuth 2.0 scopes required:

**Classic**: `manage:jira-configuration`

**Granular**: `read:workflow:jira`, `read:issue:jira`, `read:project:jira`

Payload

Type reference

Example

| Name | Type | Description |
| --- | --- | --- |
| eventType | `string` | The event name `avi:jira:failed:expression`. |
| timestamp | `string` | The time when the expression failed to evaluate, in epoch milliseconds. |
| extensionId | `string` | The ID of the extension where the expression is defined. |
| workflowId | `string` | The ID of the workflow where the expression was evaluated. |
| workflowName | `string` | The name of the workflow where the expression was evaluated. |
| conditionId | `string` | [Optional] The ID of the workflow condition where the expression is used. |
| validatorId | `string` | [Optional] The ID of the workflow validator where the expression is used. |
| expression | `string` | The evaluated Jira expression. |
| errorMessages | `string[]` | The reasons why the expression failed to evaluate. |
| context | `Context` | The context of the expression's execution. |

### Run post function event

A post function event is sent each time the transition with configured [Forge workflow post function](/platform/forge/manifest-reference/modules/jira-workflow-post-function) is performed.
It is used to invoke the Forge function defined in the `jira:workflowPostFunction` module.

OAuth 2.0 scopes required:

**Classic**: `read:jira-work`, `manage:jira-configuration`

**Granular**: `read:issue-meta:jira`, `read:issue-security-level:jira`, `read:issue.vote:jira`, `read:issue.changelog:jira`, `read:avatar:jira`,
`read:issue:jira`, `read:status:jira`, `read:user:jira`, `read:field-configuration:jira`, `read:issue.transition:jira`, `read:comment:jira`, `read:comment.property:jira`,
`read:group:jira`, `read:project:jira`, `read:project-role:jira`, `read:screen:jira`, `read:workflow:jira`, `read:webhook:jira`, `read:project-category:jira`

Payload

Type reference

Example

| Name | Type | Description |
| --- | --- | --- |
| issue | `Issue` | The issue the event is related to. |
| transition | `Transition` | The workflow transition details. The `executionId` field displays a random string that has the same value for all post functions executed as part of single issue transition. |
| workflow | `Workflow` | The workflow to which the post function is related. |
| atlassianId | `string` | The ID of the user that triggered the event. |
| changelog | `Changelog` | A list of changes that occurred on the transition. |
| comment | `Comment` | An object containing the comment ID if the comment has been added on the transition. |
| configuration | `any` | A JSON object of the post function configuration. |
| context | `Context` | A JSON object of the event context. |
| retryContext | `RetryOptions` | A JSON object of the retry context if a retry occurred. |

## Project version events

[↑ Back to top](#workflow-and-project-events)

You can subscribe to these project version events in Forge apps:

* Created: `avi:jira:created:version`
* Updated: `avi:jira:updated:version`
* Deleted: `avi:jira:deleted:version`
* Released: `avi:jira:released:version`
* Unreleased: `avi:jira:unreleased:version`
* Archived: `avi:jira:archived:version`
* Unarchived: `avi:jira:unarchived:version`
* Moved: `avi:jira:moved:version`
* Merged: `avi:jira:merged:version`

OAuth 2.0 scopes required:

**Classic**: `read:jira-work`

**Granular**: `read:project-version:jira`

| Name | Type | Description |
| --- | --- | --- |
| eventType | `string` | The event name, such as `avi:jira:created:version`. |
| version | `Version` | The version which triggered the event. |
| mergedVersion? | `Version` | [Optional] The version that was merged with the version which triggered the event. Applicable only with `avi:jira:merged:version`. |
| atlassianId? | `string` | [Optional] The ID of the user that has caused the event. |

### Project version deleted

Payload

Type reference

Example

| Name | Type | Description |
| --- | --- | --- |
| eventType | `string` | The event name `avi:jira:deleted:version`. |
| version | `Version` | The version which triggered the event. |
| mergedVersion? | `Version` | [Optional] The version that was merged with the version which triggered the event. |
| newAffectsVersion? | `Version` | [Optional] The version that was placed into the field "Affects versions" instead of the deleted version. |
| newFixVersion? | `Version` | [Optional] The version that was placed into the field "Fix versions" instead of the deleted version. |
| customFieldReplacements | `CustomFieldReplacement[]` | The versions that were placed into custom fields instead of the deleted version. |
| atlassianId? | `string` | [Optional] The ID of the user that has caused the event. |

## Project events

[↑ Back to top](#workflow-and-project-events)

You can subscribe to the following Jira project events in Forge apps:

* Project created: `avi:jira:created:project`
* Project updated: `avi:jira:updated:project`
* Project moved to trash: `avi:jira:softdeleted:project`
* Project deleted permanently: `avi:jira:deleted:project`
* Project archived: `avi:jira:archived:project`
* Project unarchived: `avi:jira:unarchived:project`
* Project restored: `avi:jira:restored:project`

OAuth 2.0 scopes required:

**Classic**: `read:jira-work`

**Granular**: `read:project:jira`

All events have the same payload format.

Payload

Type reference

Example

| Name | Type | Description |
| --- | --- | --- |
| eventType | `string` | The event name `avi:jira:created:project`. |
| project | `Project` | The project the event is related to. |

## Attachment events

[↑ Back to top](#file-and-metadata-events)

You can subscribe to this Jira attachment event in Forge apps:

* Attachment created: `avi:jira:created:attachment`
* Attachment deleted: `avi:jira:deleted:attachment`

Keep in mind that for deletions, cascading events aren’t emitted. For more information, see: [Cascading events guide](/platform/forge/events/#handling-cascading-events-in-jira).

OAuth 2.0 scopes required:

**Classic**: `read:jira-work`

**Granular**: `read:attachment:jira`

Payload

Type reference

Example

| Name | Type | Description |
| --- | --- | --- |
| eventType | `string` | The event name `avi:jira:created:attachment`. |
| attachment | `Attachment` | The attachment the event is related to. |

## Component events

[↑ Back to top](#workflow-and-project-events)

You can subscribe to these component events in Forge apps:

* Component created: `avi:jira:created:component`
* Component updated: `avi:jira:updated:component`
* Component deleted: `avi:jira:deleted:component`

Keep in mind that cascading events for deleted components aren’t emitted. For more information, see: [Cascading events guide](/platform/forge/events/#handling-cascading-events-in-jira).

OAuth 2.0 scopes required:

**Classic**: `read:jira-work`

**Granular** (Component created/updated): `read:project:jira`, `read:user:jira`  
**Granular** (Component deleted): `read:project:jira`, `read:user:jira`, `read:project.component:jira`

All events have the same payload format.

Payload

Type reference

Example

| Name | Type | Description |
| --- | --- | --- |
| eventType | `string` | The event name, such as `avi:jira:created:component`. |
| component | `Component` | The component the event is related to. |
| atlassianId? | `string` | [Optional] The ID of the user that has caused the event. |

## User events

[↑ Back to top](#file-and-metadata-events)

You can subscribe to these user events in Forge apps:

* User created: `avi:jira:created:user`
* User updated: `avi:jira:updated:user`
* User deleted: `avi:jira:deleted:user`

OAuth 2.0 scopes required:

**Classic**: `read:jira-user`

**Granular**: `read:application-role:jira`, `read:group:jira`, `read:user:jira`, `read:avatar:jira`

### User created/updated

User created and updated events have the same payload format.

Payload

Type reference

Example

| Name | Type | Description |
| --- | --- | --- |
| eventType | `string` | The event name, such as `avi:jira:created:user`. |
| user | `UserDetails` | The user the event is related to. |

### User deleted

User deleted event has the following payload format.

Payload

Type reference

Example

| Name | Type | Description |
| --- | --- | --- |
| eventType | `string` | The event name `avi:jira:deleted:user`. |
| user | `User` | The user the event is related to. |

## Filter events

[↑ Back to top](#file-and-metadata-events)

You can subscribe to these filter events in Forge apps:

* Filter created: `avi:jira:created:filter`
* Filter updated: `avi:jira:updated:filter`
* Filter deleted: `avi:jira:deleted:filter`

The payload for all of these events is the same.

OAuth 2.0 scopes required:

**Classic**: `manage:jira-configuration`

**Granular**: `read:filter:jira`, `read:jql:jira`

Payload

Type reference

Example

| Name | Type | Description |
| --- | --- | --- |
| eventType | `string` | The event name, such as `avi:jira:created:filter`. |
| filter | `Filter` | The filter the event is related to. |
| atlassianId? | `string` | [Optional] The ID of the user that has caused the event. |

## Time tracking provider events

[↑ Back to top](#system-configuration-events)

An event with the name `avi:jira:timetracking:provider:changed` is sent each time the
[time tracking provider](/cloud/jira/platform/rest/v3/api-group-time-tracking#api-rest-api-3-configuration-timetracking-put)
is changed.

You can subscribe to this event in Forge apps.

The required OAuth scopes are:

**Classic**: `manage:jira-configuration`

**Granular**: `read:issue.time-tracking:jira`

Payload

Type reference

Example

| Name | Type | Description |
| --- | --- | --- |
| eventType | `string` | The event name `avi:jira:timetracking:provider:changed`. |
| property | `Property` | The property with key set to `jira.timetracking.selected` and value indicating the selected time tracking provider. |

## Configuration events

[↑ Back to top](#system-configuration-events)

An event with the name `avi:jira:changed:configuration` is sent each time any of the
[global settings](/cloud/jira/platform/rest/v3/api-group-jira-settings/#api-rest-api-3-configuration-get)
is changed.

The required OAuth scopes are:

**Classic**: `manage:jira-configuration`

**Granular**: `read:instance-configuration:jira`.

Payload

Type reference

Example

| Name | Type | Description |
| --- | --- | --- |
| eventType | `string` | The event name `avi:jira:changed:configuration`. |
| property | `Property` | The property consists of a key that is one of  * `jira.option.allowsubtasks` * `jira.option.allowunassigned` * `jira.option.voting` * `jira.option.watching` * `jira.option.issuelinking`  and a value that is either `true` or `false`. |
| atlassianId? | `string` | [Optional] The ID of the user that has caused the event. |
