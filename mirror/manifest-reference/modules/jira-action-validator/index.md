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
| `expression` | `string` | Yes | The Jira expression that provides the custom validation logic. |
| `errorMessage` | `string` | No | Error message to display when the validation fails due to Action validator. |

## Supported Actions

The `jira:actionValidator` module can be used against specific Jira actions.

### workItemTypeChanged

This action will let app to execute custom validation when user tries to change work item type through issueView screen.

The following [context variables](https://developer.atlassian.com/cloud/jira/platform/jira-expressions/#context-variables)
are available in the validation expression:

* `user` ([User](https://developer.atlassian.com/cloud/jira/platform/jira-expressions-type-reference#user)):
  The user that wants to perform the action.
* `issue` ([Issue](https://developer.atlassian.com/cloud/jira/platform/jira-expressions-type-reference#issue)):
  The issue being modified.
* `project` ([Project](https://developer.atlassian.com/cloud/jira/platform/jira-expressions-type-reference#project)):
  The project the issue belongs to.
* `newIssueType` ([String](https://developer.atlassian.com/cloud/jira/platform/jira-expressions-type-reference#string)): The new issue type ID that the work item is being changed to.

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
