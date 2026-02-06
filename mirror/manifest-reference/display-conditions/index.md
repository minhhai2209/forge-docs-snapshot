# Display conditions

Using display conditions, you can control the visibility of your app modules in the UI.

You should not rely on display conditions as a mechanism to protect sensitive data.
This is because display conditions are executed on the client-side, and it is impossible to guarantee
that the execution results won't be overridden using the developer tools of a browser.

We strongly recommend that you apply appropriate permission checks in your code on top of
display conditions for any sensitive data you are going to operate with.

## Operators

Display conditions supports the following logical operators:

By default, the `and` operator comes with multiple display conditions.

### Example

In the example below, the Jira issue panel module will only be rendered on issues of a Bug type.

```
1
2
3
4
5
6
7
jira:issuePanel:
- key: hello-world-panel
  function: issue-panel-function
  title: Hello world!
  icon: https://developer.atlassian.com/platform/forge/images/issue-panel-icon.svg
  displayConditions:
    issueType: Bug
```

In the example below, the display conditions for the Jira issue panel module are slightly more complex.

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
jira:issuePanel:
- key: hello-world-panel
  function: issue-panel-function
  title: Hello world!
  icon: https://developer.atlassian.com/platform/forge/images/issue-panel-icon.svg
  displayConditions:
    or:
      canDeleteAllComments: true
      and:
        projectKey: TEST
        not:
          issueType: Epic
```

In this example, the Jira issue panel module will only be rendered if the following conditions are met:

* the user can delete all the comments in the given issue `or`
* the project key is TEST `and` the issue is `not` of the epic type

If you add multiple similar display conditions at the same level as shown below, you will run into validation errors due to yaml validation constraints:

```
```
1
2
```



```
jira:issuePanel:
- key: hello-world-panel
  function: issue-panel-function
  title: Hello world!
  icon: https://developer.atlassian.com/platform/forge/images/issue-panel-icon.svg
  displayConditions:
    and:
      isLoggedIn: true
      or:
        hasGlobalPermission: permission1 # WRONG - error    manifest.yml failed to parse content - Map keys must be unique  valid-yaml-required
        hasGlobalPermission: permission2 # WRONG - error    manifest.yml failed to parse content - Map keys must be unique  valid-yaml-required
```
```

Instead, you should add similar display conditions at the same level in the format shown below.

```
```
1
2
```



```
jira:issuePanel:
- key: hello-world-panel
  function: issue-panel-function
  title: Hello world!
  icon: https://developer.atlassian.com/platform/forge/images/issue-panel-icon.svg
  displayConditions:
    and:
      isLoggedIn: true
      or:
        hasGlobalPermission: permission1
        and: 
          hasGlobalPermission: permission2
```
```

You should not rely on display conditions as a mechanism to protect sensitive data. Instead, you
should perform a permission check in your code to confirm if the user does have the required permission
to delete comments.

## Common properties

Common properties are supported in the following modules:

| Property | Type | Description |
| --- | --- | --- |
| `isAdmin` | `boolean` | Checks if the current user is an Atlassian app admin |
| `isLoggedIn` | `boolean` | Checks if the current user is authenticated |
| `isSiteAdmin` | `boolean` | Checks if the current user is a site admin |

## More information

Explore the usage of display conditions:
