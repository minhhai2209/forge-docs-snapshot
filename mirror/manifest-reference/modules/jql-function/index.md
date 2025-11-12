# JQL function

The `jira:jqlFunction` module allows your app to define custom JQL functions which appear built-in from the user's perspective. This means that they're visible in the query editor and show up in the autocomplete dropdown.

See the [JQL functions](/cloud/jira/platform/jql-functions/) page for more information about the architecture of JQL functions.

## Properties

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `key` | `string` | Yes | A key for the module, which other modules can refer to. Must be unique within the manifest.  *Regex:* `^[a-zA-Z0-9_-]+$` |
| `name` | `string` | Yes | The name of the custom function.  Must be unique and different from the names of built-in JQL functions. In case of name collision, the built-in function will be called. |
| `operators` | `list` | Yes | List of operators supported by the custom function.  The following operators are available:   * `=` * `!=` * `>` * `>=` * `<` * `<=` * `in` * `not in` * `~` * `~=` * `is` * `is not` |
| `types` | `list` | Yes | Types of fields the custom function can be used with.  The following types are available:   * `issue` * `project` * `project_category` * `project_type` * `hierarchy_level` * `version` * `component` * `user` * `group` * `team` * `project_role` * `priority` * `resolution` * `issue_type` * `status` * `status_category` * `cascading_option` * `option` * `saved_filter` * `issue_security_level` * `issue_restriction` * `label` * `attachment` * `issue_list` * `issue_link_type` * `date` * `text` * `number` * `duration` * `url` |
| `arguments` | [Argument](#arguments) |  | List of arguments for the custom function. |
| `function` | `string` | No | A reference to the `function` module that provides the business logic of the custom JQL function. |
| `endpoint` | `string` | No | A reference to the `endpoint` that specifies the remote backend that receives the event if you're using [Forge Remote](/platform/forge/remote) to integrate with a remote backend.  Required if no `function` is specified. |

## Arguments

| Property | Type | Required | Description |
| --- | --- | --- | --- |
| `name` | `string` | Yes | The name of the custom function argument. |
| `required` | `boolean` | Yes | Whether the argument is required. |

## Example

##### Using a function

Manifest:

```
```
1
2
```



```
modules:
  jira:jqlFunction:
    - key: issuesWithText-function
      name: issuesWithText
      arguments:
        - name: text
          required: true
      types:
        - issue
      operators:
        - "in"
        - "not in"
      function: functionKey
  function:
    - key: functionKey
      handler: index.issuesWithText
```
```

Function implementation example:

```
```
1
2
```



```
export const issuesWithText = async (args) => {
    console.log('Hello from issuesWithText()');

    const { clause } = args;
    const { operator } = clause;
    const [text] = clause.arguments;

    const jqlFragment = `summary${operator === 'in' ? ' ~ ' : ' !~ '}'${text}'`;
    return { jql: jqlFragment };
};
```
```

##### Using Forge Remote

To learn more about Forge Remote, see [Remote essentials](/platform/forge/remote/essentials/).
There are a few caveats when using Forge Remote (like [Forge Invocation Token](/platform/forge/remote/essentials/#the-forge-invocation-token--fit-) validation) that you have to consider when implementing the remote backend.
However, in the context of JQL function business logic, everything described on the [JQL functions](/cloud/jira/platform/jql-functions/) page applies and your function should return a valid JQL fragment as a result of the processing.

Manifest example:

```
```
1
2
```



```
modules:
  jira:jqlFunction:
    - key: remote-jql-function
      name: testRemoteJqlFunction
      arguments:
        - name: text
          required: true
      types:
        - issue
      operators:
        - in
        - not in
      endpoint: remote-jql-endpoint
  endpoint:
    - key: remote-jql-endpoint
      remote: remote-app
      route:
        path: /jqlfunction

remotes:
  - key: remote-app
    baseUrl: "https://my-app-remote-example.com"
```
```

#### Usage in JQL

This is how to use the function in JQL:

```
```
1
2
```



```
issue in issuesWithText("hello, world!")
```
```
