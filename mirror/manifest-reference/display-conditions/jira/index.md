# Usage with Jira/JSM modules

You can use display conditions for Jira and Jira Service Management modules that extend Jira UI to control their visibility.
Depending on the module and where it's rendered, different conditions are available.

## Combining conditions

Use the `and`, `or`, and `not` [operators](/platform/forge/manifest-reference/display-conditions/#operators)
to combine conditions. In Jira and Jira Service Management modules, each operator accepts either a
single condition object or an array of condition objects. Use an array when you need the same
condition more than once at the same level. The example below shows the module to users with
either of two global permissions:

```
1displayConditions:
2  or:
3    - hasGlobalPermission: ADMINISTER
4    - hasGlobalPermission: CREATE_PROJECT
5
```

## Global conditions

Global conditions check the state of the entire Jira instance for the current user regardless of the display context.
They are available in all Jira modules that support display conditions.

| Condition | Type | Description |
| --- | --- | --- |
| `hasCoreAccess` | `boolean` | Checks if the current user has access to Jira |
| `hasSoftwareAccess` | `boolean` | Checks if the current user has access Jira Software |
| `hasServiceDeskAccess` | `boolean` | Checks if the current user has access to Jira Service Management |
| `hasGlobalPermission` | `String` | Checks if the current user has a global permission with the given key.   The following global permission keys are supported:  * `ADMINISTER` * `SYSTEM_ADMIN` * `USER_PICKER` * `CREATE_SHARED_OBJECTS` * `MANAGE_GROUP_FILTER_SUBSCRIPTIONS` * `BULK_CHANGE` * `CREATE_PROJECT` * `CREATE_CLASSIC_BUSINESS_PROJECT`   Additionally, permissions from [Forge](/platform/forge/manifest-reference/modules/jira-global-permission/) and [Connect](/cloud/jira/platform/modules/global-permission/) apps can also be checked. |
| `canAdministerJira` | `boolean` | Checks if the current user has the permission to administer the Jira instance. |
| `hasAppAccess` | `boolean` | Checks if the current user has access to the app. |
| `appIsLicensed` | `boolean` | Checks if the app's license is active. |
| `appEdition` | `String` | Checks the installed [app edition](/platform/app-plans/). Available values: |
| `entityPropertyExists`  `entityPropertyEqualTo`  `entityPropertyContainsAny`  `entityPropertyContainsAll` | [EntityProperty](/platform/forge/manifest-reference/display-conditions/entity-property-conditions/#parameters) | A set of [entity property conditions](/platform/forge/manifest-reference/display-conditions/entity-property-conditions/) available for the following entities:  * `app`: properties of your app that can be set with the [Set app property (Forge)](/cloud/jira/platform/rest/v3/api-group-app-properties/#api-rest-forge-1-app-properties-propertykey-put) REST API * `user`: properties of the current user |
| `jiraExpression` | `String` | Checks if the given [Jira expression](/cloud/jira/software/jira-expressions/) evaluates to `true`. The following [context variables](/cloud/jira/software/jira-expressions/#context-variables) are available:  * `user` ([User](/cloud/jira/software/jira-expressions-type-reference/#user)): The current user * `app` ([App](/cloud/jira/software/jira-expressions-type-reference/#app)): Your app |

## Issue view conditions

Issue view conditions are supported in modules that extend the issue view and will evaluate to `false` if used in other modules.

| Condition | Type | Description |
| --- | --- | --- |
| `issueKey` | `Array<string>` or `string` | Checks if the key of the currently displayed issue matches any of the provided values. |
| `issueId` | `Array<string>` or `string` | Checks if the key of the currently displayed issue matches any of the provided values. |
| `issueType` | `Array<string>` or `string` | Checks if the name of the type of the currently displayed issue matches any of the provided values. |
| `hasIssuePermission` | `String` | Checks if the current user has a project permission with the given key for the current issue.   The following project permission keys are supported: `ADMINISTER_PROJECTS`, `BROWSE_PROJECTS`, `VIEW_DEV_TOOLS`, `VIEW_READONLY_WORKFLOW`, `CREATE_ISSUES`, `EDIT_ISSUES`, `TRANSITION_ISSUES`, `SCHEDULE_ISSUES`, `MOVE_ISSUES`, `ASSIGN_ISSUES`, `ASSIGNABLE_USER`, `RESOLVE_ISSUES`, `CLOSE_ISSUES`, `MODIFY_REPORTER`, `DELETE_ISSUES`, `ARCHIVE_ISSUES`, `UNARCHIVE_ISSUES`, `LINK_ISSUES`, `SET_ISSUE_SECURITY`, `VIEW_VOTERS_AND_WATCHERS`, `MANAGE_WATCHERS`, `ADD_COMMENTS`, `EDIT_ALL_COMMENTS`, `EDIT_OWN_COMMENTS`, `DELETE_ALL_COMMENTS`, `DELETE_OWN_COMMENTS`, `CREATE_ATTACHMENTS`, `DELETE_ALL_ATTACHMENTS`, `DELETE_OWN_ATTACHMENTS`, `WORK_ON_ISSUES`, `EDIT_OWN_WORKLOGS`, `EDIT_ALL_WORKLOGS`, `DELETE_OWN_WORKLOGS`, `DELETE_ALL_WORKLOGS`, `EDIT_WORKFLOW`, `EDIT_ISSUE_LAYOUT` Additionally, permissions from [Forge](/platform/forge/manifest-reference/modules/jira-project-permission/) and [Connect](/cloud/jira/platform/modules/project-permission/) apps can also be checked. |
| `entityPropertyExists`  `entityPropertyEqualTo`  `entityPropertyContainsAny`  `entityPropertyContainsAll` | [EntityProperty](/platform/forge/manifest-reference/display-conditions/entity-property-conditions/#parameters) | A set of [entity property conditions](/platform/forge/manifest-reference/display-conditions/entity-property-conditions/) available for the following entities:  * `app`: properties of your app that can be set with the [Set app property (Forge)](/cloud/jira/platform/rest/v3/api-group-app-properties/#api-rest-forge-1-app-properties-propertykey-put) REST API * `user`: properties of the current user * `issue`: properties of the current issue * `issueType`: properties of the issue type of the current issue * `project`: properties of the project of the current issue |
| `jiraExpression` | `String` | Checks if the given [Jira expression](/cloud/jira/software/jira-expressions/) evaluates to `true`. The following [context variables](/cloud/jira/software/jira-expressions/#context-variables) are available:  * `user` ([User](/cloud/jira/software/jira-expressions-type-reference/#user)): The current user * `app` ([App](/cloud/jira/software/jira-expressions-type-reference/#app)): Your app * `issue` ([Issue](/cloud/jira/software/jira-expressions-type-reference/#issue)): The current issue * `project` ([Project](/cloud/jira/software/jira-expressions-type-reference/#project)): The project of the current issue * `customerRequest` ([CustomerRequest](/cloud/jira/software/jira-expressions-type-reference/#customerrequest)): The current customer request, for JSM projects * `serviceDesk` ([ServiceDesk](/cloud/jira/software/jira-expressions-type-reference/#servicedesk)): The service desk of the current issue, for JSM projects |

## Project view conditions

Project view conditions are evaluated against the current project (or the project of the current issue).
They are available for modules that render in context of an issue or project and will evaluate to `false` if used in other modules.

| Condition | Type | Description |
| --- | --- | --- |
| `projectKey` | `Array<string>` or `string` | Checks if the key of the project of the currently displayed issue matches any of the provided values. |
| `projectId` | `Array<string>` or `string` | Checks if the ID of the project of the currently displayed issue matches any of the provided values. |
| `projectName` | `Array<string>` or `string` | Checks if the names of the project of the currently displayed issue matches any of the provided values. |
| `projectType` | `Array<string>` or `string` | Checks if the type of the project of the currently displayed issue matches any of the provided values. Available types are:  * `business` * `software` * `product_discovery` * `service_desk` * `customer_service` * `ops` |
| `isProjectArchived` | `boolean` | Checks if the current project is archived |
| `hasProjectPermission` | `String` | Checks if the current user has a project permission with the given key in the current project (or the project of the current issue).   The following project permission keys are supported: `ADMINISTER_PROJECTS`, `BROWSE_PROJECTS`, `VIEW_DEV_TOOLS`, `VIEW_READONLY_WORKFLOW`, `CREATE_ISSUES`, `EDIT_ISSUES`, `TRANSITION_ISSUES`, `SCHEDULE_ISSUES`, `MOVE_ISSUES`, `ASSIGN_ISSUES`, `ASSIGNABLE_USER`, `RESOLVE_ISSUES`, `CLOSE_ISSUES`, `MODIFY_REPORTER`, `DELETE_ISSUES`, `ARCHIVE_ISSUES`, `UNARCHIVE_ISSUES`, `LINK_ISSUES`, `SET_ISSUE_SECURITY`, `VIEW_VOTERS_AND_WATCHERS`, `MANAGE_WATCHERS`, `ADD_COMMENTS`, `EDIT_ALL_COMMENTS`, `EDIT_OWN_COMMENTS`, `DELETE_ALL_COMMENTS`, `DELETE_OWN_COMMENTS`, `CREATE_ATTACHMENTS`, `DELETE_ALL_ATTACHMENTS`, `DELETE_OWN_ATTACHMENTS`, `WORK_ON_ISSUES`, `EDIT_OWN_WORKLOGS`, `EDIT_ALL_WORKLOGS`, `DELETE_OWN_WORKLOGS`, `DELETE_ALL_WORKLOGS`, `EDIT_WORKFLOW`, `EDIT_ISSUE_LAYOUT` Additionally, permissions from [Forge](/platform/forge/manifest-reference/modules/jira-project-permission/) and [Connect](/cloud/jira/platform/modules/project-permission/) apps can also be checked. |
| `entityPropertyExists`  `entityPropertyEqualTo`  `entityPropertyContainsAny`  `entityPropertyContainsAll` | [EntityProperty](/platform/forge/manifest-reference/display-conditions/entity-property-conditions/#parameters) | A set of [entity property conditions](/platform/forge/manifest-reference/display-conditions/entity-property-conditions/) available for the following entities:  * `app`: properties of your app that can be set with the [Set app property (Forge)](/cloud/jira/platform/rest/v3/api-group-app-properties/#api-rest-forge-1-app-properties-propertykey-put) REST API * `user`: properties of the current user * `project`: properties of the current project |
| `jiraExpression` | `String` | Checks if the given [Jira expression](/cloud/jira/software/jira-expressions/) evaluates to `true`. The following [context variables](/cloud/jira/software/jira-expressions/#context-variables) are available:  * `user` ([User](/cloud/jira/software/jira-expressions-type-reference/#user)): The current user * `app` ([App](/cloud/jira/software/jira-expressions-type-reference/#app)): Your app * `project` ([Project](/cloud/jira/software/jira-expressions-type-reference/#project)): The current project * `serviceDesk` ([ServiceDesk](/cloud/jira/software/jira-expressions-type-reference/#servicedesk)): The service desk of the current project, for JSM projects |

## Project permission conditions

These conditions check project permissions of the current user against the issue (for issue view modules) or project (for project view modules).
They are simpler versions of `hasIssuePermission` and `hasProjectPermission` documented in [issue view](#issue-view-conditions) and [project view](#issue-view-conditions) conditions respectively.
They will evaluate to `false` for modules that aren't rendered in context of an issue or project.

| Condition | Type | Description |
| --- | --- | --- |
| `isProjectAdmin` / `canAdministerProjects` | `boolean` | Checks if the current user has the permission to administer the current project. |
| `canAddComments` | `boolean` | Checks if the current user has the permission to add issue comments. |
| `canAssignIssues` | `boolean` | Checks if the current user has the permission to assign issues. |
| `canBeAssignedToIssues` | `boolean` | Checks if the current user may be assigned to issues. |
| `canCloneIssues` | `boolean` | Checks if the current user has the permission to clone issues. |
| `canCreateAttachments` | `boolean` | Checks if the current user has the permission to create issue attachments. |
| `canCreateChildren` | `boolean` | Checks if the current user has the permission to create children issues. |
| `canCreateSubtasks` | `boolean` | Checks if the current user has the permission to create subtasks, which means that:  * the user has the create subtasks permission * subtasks creation is enabled on the instance * the project has subtask issue types |
| `canDeleteAllAttachments` | `boolean` | Checks if the current user has the permission to delete all issue attachments. |
| `canDeleteAllComments` | `boolean` | Checks if the current user has the permission to delete all issue comments. |
| `canDeleteAllWorklogs` | `boolean` | Checks if the current user has the permission to delete all worklogs. |
| `canDeleteIssues` | `boolean` | Checks if the current user has the permission to delete issues. |
| `canDeleteOwnAttachments` | `boolean` | Checks if the current user has the permission to delete their own issue attachments. |
| `canDeleteOwnComments` | `boolean` | Checks if the current user has the permission to delete their own comments. |
| `canDeleteOwnWorklogs` | `boolean` | Checks if the current user has the permission to delete their own worklogs. |
| `canEditAllComments` | `boolean` | Checks if the current user has the permission to edit all comments. |
| `canEditAllWorklogs` | `boolean` | Checks if the current user has the permission to edit all worklogs. |
| `canEditIssues` | `boolean` | Checks if the current user has the permission to edit issues. |
| `canEditOwnComments` | `boolean` | Checks if the current user has the permission to edit their own comments. |
| `canEditOwnWorklogs` | `boolean` | Checks if the current user has the permission to edit their own worklogs. |
| `canLinkIssues` | `boolean` | Checks if the current user has the permission to link issues. |
| `canLogWork` | `boolean` | Checks if the current user has the permission to log work. |
| `canManageWatchers` | `boolean` | Checks if the current user has the permission to add and remove watchers. |
| `canModifyReporters` | `boolean` | Checks if the current user has the permission to change the issue reporter. |
| `canMoveIssues` | `boolean` | Checks if the current user has the permission to move issues from the current project. |
| `canScheduleIssues` | `boolean` | Checks if the current user has the permission to schedule issues. |
| `canBrowseUsers` | `boolean` | Checks if the current user has the permission to browse users. |
| `canViewDevTools` | `boolean` | Checks if the current user has the permission to view dev tools. |
| `canViewWatchers` | `boolean` | Checks if the current user has the permission to view watches. |

## Time tracking conditions

These conditions are designed to be used in combination with the [time tracking provider](/platform/forge/manifest-reference/modules/jira-time-tracking-provider/) module.

For example:

```
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
```



```
modules:
  jira:timeTrackingProvider:
    - key: my-time-tracking
      name: Forge time tracking provider
      # time tracking provider specific properties
  jira:issuePanel:
    - key: forge-time-tracking-issue-panel
      title: Panel to show if our time tracking is used
      displayConditions:
        timeTrackingProviderEnabled:
          key: my-time-tracking
    - key: jira-time-tracking-issue-panel
      title: Panel to show if native Jira time tracking is used
      displayConditions:
        jiraTimeTrackingProviderEnabled: true
```
```

| Condition | Type | Description |
| --- | --- | --- |
| `jiraTimeTrackingProviderEnabled` | `boolean` | Checks if the standard Jira time tracking provider is used (as opposed to custom time tracking provided by apps). |
| `timeTrackingProviderEnabled` | `String` | Checks if the instance uses the given time tracking provider identified by the key of its module as defined in the manifest. |

## Jira Service Management conditions

These conditions are based on JSM-specific properties.

Display conditions are supported in the following JSM modules:

| Condition | Type | Description |
| --- | --- | --- |
| `hasServiceDeskAccess` | `boolean` | Checks if the current user has access to Jira Service Management. |
| `canUseServiceManagementAgentFeatures` | `boolean` | Checks if the current user is an agent in the current Jira Service Management project. Returns `false` if the extension isn't rendered in context of an issue or project. |
| `jiraExpression` | `String` | Checks if the given [Jira expression](/cloud/jira/software/jira-expressions/) evaluates to `true`. The following [context variables](/cloud/jira/software/jira-expressions/#context-variables) are available:  * `user` ([User](/cloud/jira/software/jira-expressions-type-reference/#user)): The current user * `app` ([App](/cloud/jira/software/jira-expressions-type-reference/#app)): Your app * `project` ([Project](/cloud/jira/software/jira-expressions-type-reference/#project)): The current project * `issue` ([Issue](/cloud/jira/software/jira-expressions-type-reference/#issue)): The current issue * `serviceDesk` ([ServiceDesk](/cloud/jira/software/jira-expressions-type-reference/#servicedesk)): The service desk of the current issue * `customerRequest` ([CustomerRequest](/cloud/jira/software/jira-expressions-type-reference/#customerrequest)): The current customer request |
