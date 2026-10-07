# Modules

Modules are defined in the [manifest](/platform/forge/manifest/), and they describe how Forge
apps extend and interact with Atlassian apps.

Here are some examples of what you can do with Forge modules:

* Create new custom fields in Jira
* Add new menu items in Jira issues
* Display app content in Confluence pages and blogs
* Create Confluence custom content, such as templates, forms, or macros
* Add a pull request card in Bitbucket
* Use webhooks to listen for events

## Example

Here's an example of how modules appear in the `manifest.yml` file.

```
1modules:
2  macro:
3    - key: hello-world-macro
4      function: hello-world-macro-func
5      title: Hello world macro!
6      description: Inserts hello world!
7  webtrigger:
8    - key: webtrigger-sync
9      function: my-forge-app-sync-func
10      urlFormat: v2
11      response:
12        type: dynamic
13    - key: my-webtrigger-async
14      function: my-async-func
15      urlFormat: v2
16      response:
17        type: dynamic
18  trigger:
19    - key: issue-creation-trigger
20      events:
21        - avi:jira:created:issue
22        - avi:jira:updated:issue
23      function: issue-trigger-func
24  jira:workflowValidator:
25    - key: my-forge-workflow-validator
26      name: My example Forge workflow validator
27      description: The description of my example Forge workflow validator
28      function: my-forge-validator-function
29  function:
30    - key: my-forge-app-sync-func
31      handler: index.runSync
32    - key: my-async-func
33      handler: index.runAsync
34    - key: hello-world-macro-func
35      handler: macro.run
36    - key: issue-trigger-func
37      handler: jira.issueCreationTrigger
38    - key: my-forge-validator-function
39      handler: index.runValidate
40
```

## Reference documentation

To learn more, check out the modules [reference documentation](/platform/forge/manifest-reference/modules/).
