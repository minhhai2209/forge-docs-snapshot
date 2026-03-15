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
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
36
37
modules:
  macro:
    - key: hello-world-macro
      function: hello-world-macro-func
      title: Hello world macro!
      description: Inserts hello world!
  webtrigger:
    - key: webtrigger-sync
      function: my-forge-app-sync-func
      response:
        type: dynamic
    - key: my-webtrigger-async
      function: my-async-func
      response:
        type: dynamic
  trigger:
    - key: issue-creation-trigger
      events:
        - avi:jira:created:issue
        - avi:jira:updated:issue
      function: issue-trigger-func
  jira:workflowValidator:
    - key: my-forge-workflow-validator
      name: My example Forge workflow validator
      description: The description of my example Forge workflow validator
      function: my-forge-validator-function
  function:
    - key: my-forge-app-sync-func
      handler: index.runSync
    - key: my-async-func
      handler: index.runAsync
    - key: hello-world-macro-func
      handler: macro.run
    - key: issue-trigger-func
      handler: jira.issueCreationTrigger
    - key: my-forge-validator-function
      handler: index.runValidate
```

## Reference documentation

To learn more, check out the modules [reference documentation](/platform/forge/manifest-reference/modules/).
