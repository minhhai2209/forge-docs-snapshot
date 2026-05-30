# The Forge REST API

`1
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
26``{
"installations": [
{
"id": "<installation-1-id-uuid>",
"installationContext": "ari:cloud:confluence::site/<cloudId>",
"version": "12.0.3",
"secondaryInstallationContexts": [
"<secondary-installation-context-1>",
"<secondary-installation-context-2>"
]
},
{
"id": "<installation-2-id-uuid>",
"installationContext": "ari:cloud:jira::site/<cloudId>",
"version": "11.0.0",
"secondaryInstallationContexts": []
},
{
"id": "<installation-3-id-uuid>",
"installationContext": "ari:cloud:jira::site/<cloudId>",
"version": "11.0.0",
"secondaryInstallationContexts": []
}
],
"cursor": null
}`
