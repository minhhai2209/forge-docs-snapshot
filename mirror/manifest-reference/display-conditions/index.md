# Display conditions

Using display conditions, you can control the visibility of your app modules in the UI.

Display conditions evaluate static context at the manifest level (user role, issue type,
project) and cannot reference [feature flags](/platform/forge/feature-flags/overview/).
Feature flags are evaluated at runtime within your app code — use them to control
behaviour inside your app, not module visibility.

You should not rely on display conditions as a mechanism to protect sensitive data.
This is because display conditions are executed on the client-side, and it is impossible to guarantee
that the execution results won't be overridden using the developer tools of a browser.

We strongly recommend that you apply appropriate permission checks in your code on top of
display conditions for any sensitive data you are going to operate with.

## Operators

Display conditions support the following logical operators:

* `and`: all child conditions must be true
* `or`: at least one child condition must be true
* `not`: none of the child conditions are true

Conditions at the same level are combined with `and` by default.

### Example

In the example below, the Jira issue panel module will only be rendered on issues of a Bug type.

```
1jira:issuePanel:
2- key: hello-world-panel
3  function: issue-panel-function
4  title: Hello world!
5  icon: https://developer.atlassian.com/platform/forge/images/issue-panel-icon.svg
6  displayConditions:
7    issueType: Bug
8
```

In the example below, the display conditions for the Jira issue panel module are slightly more complex.

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
```



```
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
```

In this example, the Jira issue panel module will only be rendered if the following conditions are met:

* the user can delete all the comments in the given issue `or`
* the project key is TEST `and` the issue is `not` of the epic type

### Use the same condition more than once (Jira and Jira Service Management)

Each condition name is a key in the manifest, and keys must be unique at each level. If you
repeat a condition at the same level, the manifest fails validation:

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

In Jira and Jira Service Management modules, the `and`, `or`, and `not` operators accept either a
single condition object or an array of condition objects. Each array item is a separate object,
so you can repeat conditions and operators:

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
```



```
jira:issuePanel:
- key: hello-world-panel
  function: issue-panel-function
  title: Hello world!
  icon: https://developer.atlassian.com/platform/forge/images/issue-panel-icon.svg
  displayConditions:
    and:
      - isLoggedIn: true
      - or:
          - hasGlobalPermission: permission1
          - hasGlobalPermission: permission2
```
```

Arrays also let you group conditions of the same type. The example below shows the module when
the user has both properties `a` and `b`, or both properties `c` and `d`:

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
```



```
displayConditions:
  or:
    - and:
        - entityPropertyExists: { entity: user, propertyKey: a }
        - entityPropertyExists: { entity: user, propertyKey: b }
    - and:
        - entityPropertyExists: { entity: user, propertyKey: c }
        - entityPropertyExists: { entity: user, propertyKey: d }
```
```

## Common properties

Common properties are supported in the following modules:

| Property | Type | Description |
| --- | --- | --- |
| `isAdmin` | `boolean` | Checks if the current user is an Atlassian app admin |
| `isLoggedIn` | `boolean` | Checks if the current user is authenticated |
| `isSiteAdmin` | `boolean` | Checks if the current user is a site admin |

## More information

Explore the usage of display conditions:
