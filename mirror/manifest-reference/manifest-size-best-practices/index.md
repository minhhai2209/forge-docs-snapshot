# Manifest size best practices

The Forge platform enforces a maximum file size of 200 KB for `manifest.yml`. In practice, your working
target should be lower. A manifest can pass local validation and still fail during deployment, because
Forge expands and provisions parts of your manifest internally before it's released.

This guide explains why that happens, which modules contribute the most growth, and the design patterns
that keep your manifest small and maintainable.

Don't treat 200 KB as your working target. Set a softer internal budget of around 150 KB to leave room
for deployment-time expansion.

## Why valid manifests can still fail to deploy

Forge enforces the manifest size limit when you deploy, but deployment behavior adds an extra
consideration. A manifest that's under the published threshold can still fail later in the deployment
pipeline, because the platform provisions each [`function`](/platform/forge/manifest-reference/modules/function/)
entry across multiple regions behind the scenes. The effective internal representation of your manifest
is larger than the file on disk.

For more details on this known issue, see
[ECO-1310](https://jira.atlassian.com/browse/ECO-1310).

This distinction matters when you're debugging a failed deployment. Size management isn't only about the
file in your app directory. It's about the deployable manifest after Forge has expanded internal
structures.

## What makes manifests grow

### Large numbers of function modules

The biggest deployment-time risk comes from declaring many distinct
[`function`](/platform/forge/manifest-reference/modules/function/) entries. Even when the YAML is
comfortably under 200 KB, a large number of separate functions can inflate the internal deployed form
enough to fail the release.

This pattern is common in apps that declare many modules and give each module its own dedicated handler.

### Large inline prompts in Rovo Agents

The other common source of growth is the [`rovo:agent`](/platform/forge/manifest-reference/modules/rovo-agent/)
module, and specifically its `prompt` property. Prompts are verbose by nature, so a long prompt can
consume a meaningful share of your manifest budget. Apps that declare several Agents in one manifest
reach the limit faster.

## Reuse functions instead of declaring one per module

The most effective way to avoid deployment failures caused by manifest expansion is to reduce the number
of unique [`function`](/platform/forge/manifest-reference/modules/function/) entries. Where you can, point
multiple modules at a shared function and branch on the invocation context in your app code.

| Approach | Manifest impact | Recommendation |
| --- | --- | --- |
| One function per module | High growth in the internal manifest size | Avoid unless isolation is genuinely required |
| Shared function for related modules | Much smaller internal footprint | Preferred default pattern |

Shared handlers work well for:

* Groups of [Rovo actions](/platform/forge/manifest-reference/modules/rovo-action/) with similar logic.
* Related UI modules that differ only by context.
* Handlers that can route on module key, payload type, or operation name.

### Declare a shared function in your manifest

The following example shows three related Rovo actions that reuse one
[`function`](/platform/forge/manifest-reference/modules/function/) entry, instead of declaring a separate
function for each action:

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
17
18
19
20
21
```



```
modules:
  action:
    - key: create-issue
      name: Create work item
      function: shared-rovo-action
      actionVerb: CREATE
      description: Creates a Jira work item.
    - key: update-issue
      name: Update work item
      function: shared-rovo-action
      actionVerb: UPDATE
      description: Updates an existing Jira work item.
    - key: summarize-issue
      name: Summarize work item
      function: shared-rovo-action
      actionVerb: GET
      description: Summarizes a Jira work item.
  function:
    - key: shared-rovo-action
      handler: index.run
```
```

Keep the manifest responsible only for declaring modules and their shared entry point. Keep
module-specific behavior in your app code.

### Route invocations in the shared handler

A shared handler routes each invocation to the appropriate implementation. The context shape depends on
the module, so confirm the available invocation fields for the module you're using.

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
```



```
type Invocation = {
  context?: {
    moduleKey?: string;
  };
  payload?: unknown;
};

export async function run(invocation: Invocation) {
  const moduleKey = invocation.context?.moduleKey;

  try {
    switch (moduleKey) {
      case 'create-issue':
        return await createIssue(invocation.payload);
      case 'update-issue':
        return await updateIssue(invocation.payload);
      case 'summarize-issue':
        return await summarizeIssue(invocation.payload);
      default:
        throw new Error(`Unsupported module: ${moduleKey}`);
    }
  } catch (error) {
    console.error(`Failed to handle invocation for ${moduleKey}`, error);
    throw error;
  }
}
```
```

Keep the routing layer thin and move business logic into separate internal functions. Your manifest stays
small without sacrificing code quality.

## Keep Agent prompts short and modular

For [`rovo:agent`](/platform/forge/manifest-reference/modules/rovo-agent/), avoid a single large,
monolithic prompt when a modular design achieves the same result. Keep the top-level Agent prompt focused
on role, boundaries, and orchestration.

You can move detailed instructions into [`rovo:skill`](/platform/forge/manifest-reference/modules/rovo-skill/)
modules, which store their instructions in a `SKILL.md` file rather than in the manifest. The Agent's
prompt then only needs to describe when to use each capability.

Forge’s EAP offers experimental features to selected users for testing and feedback purposes.
These features are unsupported and not recommended for use in production environments. They
are also subject to change without notice.

To join the EAP for Forge Rovo Skills, [complete the sign up form](https://ecosystem.atlassian.net/servicedesk/customer/portal/1040/group/3496/create/18258).

For more details, see [Forge EAP, Preview, and GA](/platform/forge/whats-coming/#eap).

Until [`rovo:skill`](/platform/forge/manifest-reference/modules/rovo-skill/) is generally available, you
can still reduce prompt size by trimming repetition, removing examples that don't change Agent behavior,
and moving reference data into a [Rovo action](/platform/forge/manifest-reference/modules/rovo-action/)
that the Agent calls at runtime.

### Design skills around capabilities, not topics

When you split prompt content into [`rovo:skill`](/platform/forge/manifest-reference/modules/rovo-skill/)
modules, group instructions by reusable capability rather than by arbitrary section. Smaller, clearer
modules are easier to maintain.

Examples of capability-based skill boundaries include:

* Summarize content.
* Classify a work item or request.
* Draft a response.
* Extract structured fields.
* Apply domain-specific policy checks.

## Watch for cumulative growth

Manifest bloat usually comes from accumulation rather than a single change. A few extra functions, one
long prompt, and several feature additions can quietly push your app into the danger zone.

Review manifest size as part of normal development, especially before you add:

* New function-heavy modules.
* Additional Rovo Agents.
* Long prompt revisions.
* Parallel feature variants that duplicate handlers.

## Recommended guardrails

| Guardrail | Why it helps | Practical target |
| --- | --- | --- |
| Soft manifest budget | Leaves room for deployment-time expansion | Stay at or below 150 KB |
| Shared handler pattern | Reduces the number of `function` entries | Use as the default for related modules |
| Modular Rovo design | Prevents very large inline Agent prompts | Move detailed instructions out of the prompt |
| Ongoing manifest review | Catches growth before a deployment fails | Check after each major feature addition |

If deployment fails unexpectedly even though your manifest appears valid, check manifest size first. This
is especially important if you recently added many functions or expanded your app's Rovo capabilities.

Common warning signs include:

* The manifest is approaching the 200 KB limit.
* The app declares a large number of individual functions.
* Recent changes added or expanded one or more `rovo:agent` prompts.
* Deployment errors appear late in the process rather than during linting or initial validation.

Passing manifest validation doesn't guarantee a successful deployment. Internal expansion can push the
effective payload over platform limits after validation succeeds.

To check the size of your manifest, run:

## Key takeaways

The published 200 KB limit is only part of the story. An app can still fail at deployment because internal
provisioning expands the effective manifest size, particularly around
[`function`](/platform/forge/manifest-reference/modules/function/) modules. Large inline prompts in
[`rovo:agent`](/platform/forge/manifest-reference/modules/rovo-agent/) add further pressure.

Manage size proactively:

* Prefer fewer, smarter handlers over many small function declarations.
* Refactor early, when your function count starts trending up.
* Treat large prompts as architecture, not just content.
* Use [`rovo:skill`](/platform/forge/manifest-reference/modules/rovo-skill/) modules to distribute
  complexity in Rovo apps.
* Keep a safety margin instead of optimizing right up to the published limit.
