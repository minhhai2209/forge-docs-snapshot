# Jira action validator (Preview)

This section describes a Forge *preview* feature. Preview features are deemed stable;
however, they remain under active development and may be subject to shorter deprecation
windows. Preview features are suitable for early adopters in production environments.

We release preview features so partners and developers can study, test, and integrate
them prior to General Availability (GA). For more information,
see [Forge release phases: EAP, Preview, and GA](/platform/forge/whats-coming/#preview).

The `jira:actionValidator` module lets developers define custom validation against specific Jira actions. Currently, the only supported way to provide this custom validation is by using Jira expressions.

## Properties

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `key` | `string` | Yes | A key for the module, which other modules can refer to. Must be unique within the manifest.  *Regex:* `^[a-zA-Z0-9_-]+$` |
| `action` | `string` | Yes | The name of the action. Allowed actions are: |
| `expression` | `string` | Yes | The Jira expression that provides the custom validation logic.  The expression should return a boolean value:   * `true` means that the validation was successful, and the operation is allowed. * `false` means that the validation failed. The error message defined in the manifest's `errorMessage` property will be shown to the user. |
| `errorMessage` | `string` | No | Error message to display when the validation fails due to Action validator. |

## Supported Actions

The `jira:actionValidator` module can be used against specific Jira actions.

### workItemTypeChanged

This action lets an app execute custom validation whenever a user changes the type of a work item. The validator is triggered across the following flows:

* **Issue view** - the user changes the work item type from the type field on the issue view.
* **Move issue** - when the work item type changes as part of moving an issue.
* **Bulk move/migrate** - the work item type changes as part of a bulk move or migration.
* **Convert to subtask** - when a standard work item is converted to a subtask type.
* **Convert subtask to a work item** - when a subtask is converted to a standard work item.

The validator is only invoked when the target type is different from the current type.

The following [context variables](https://developer.atlassian.com/cloud/jira/platform/jira-expressions/#context-variables)
are available in the validation expression:

* `user` ([User](https://developer.atlassian.com/cloud/jira/platform/jira-expressions-type-reference#user)):
  The user that wants to perform the action.
* `issue` ([Issue](https://developer.atlassian.com/cloud/jira/platform/jira-expressions-type-reference#issue)):
  The issue being modified.
* `project` ([Project](https://developer.atlassian.com/cloud/jira/platform/jira-expressions-type-reference#project)):
  The project the issue belongs to.
* `newIssueType` ([String](https://developer.atlassian.com/cloud/jira/platform/jira-expressions-type-reference#string)): The new issue type ID that the work item is being changed to.
* `newIssueTypeData` ([IssueType](https://developer.atlassian.com/cloud/jira/platform/jira-expressions-type-reference/#issuetype)): The new issue type that the work item is being changed to.

## Example

This example shows manifest file of `jira:actionValidator` module for `workItemTypeChanged` action.

```
```
1
2
```



```
modules:
  'jira:actionValidator':
    - key: workitem-type-validator
      action: 'workItemTypeChanged'
      expression: 'issue.key=="HSP-1" && newIssueType=="1"'
      errorMessage: "Work Item type change was blocked by action validator."
```
```

## Limitations

The following limitations apply to apps that use the `jira:actionValidator` module:

* **One validator per action type**: You can declare only one `jira:actionValidator` module per action type.
