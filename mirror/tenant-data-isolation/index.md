# Tenant data isolation in Forge apps

Forge apps run in a multi-tenant environment where the same runtime process can
serve multiple Atlassian customers (tenants). This means **module-level
variables and in-memory caches are shared across tenant invocations** unless
you explicitly scope data to a single invocation.

This guide explains the risk, shows unsafe and safe code patterns, and provides
actionable checklists for auditing your app.

Storing tenant-specific data in module-level (global) variables is one of the
most common causes of cross-tenant data leaks in Forge apps. Data written
during one tenant's invocation may be visible to a subsequent invocation for a
different tenant if it shares the same process.

## Why this happens

The Forge runtime is built on AWS Lambda. Lambda optimizes performance by
**reusing warm execution environments** (process containers) across multiple
invocations. When a warm environment is reused:

* The Node.js module cache is **not cleared** between invocations.
* Any variable declared at module scope retains its value from the previous
  invocation.
* If the previous invocation belonged to **a different tenant**, that tenant's
  data is now visible in the new invocation's scope.

This is a standard characteristic of serverless runtimes, not a Forge-specific
bug. However, it conflicts with the intuitive assumption that each function call
starts with a clean slate.

The [Shared responsibility model](/platform/forge/shared-responsibility-model/#tenant-safety)
requires developers to keep tenant data isolated. Atlassian ensures that tenant
A cannot call tenant B's app, but **you are responsible for ensuring that
in-memory state from one invocation does not leak into another**.

## Unsafe patterns

The following patterns all share the same root cause: mutable state is declared
at module scope and updated during a handler invocation. Because Forge reuses
warm execution environments, that state survives into the next invocation, which
may belong to a completely different tenant.

### Module-level cache

The following pattern is common in Node.js but is **unsafe in Forge** because
`cache` persists across invocations that may belong to different tenants.

```
```
1
2
```



```
// UNSAFE: module-level cache shared across all tenants
const cache = {};

export async function handler(context) {

  if (cache['currentUser']) {
    // This could return another tenant's user data!
    return cache['currentUser'];
  }

  const response = await api.asUser().requestJira('/rest/api/3/myself');
  const user = await response.json();

  cache['currentUser'] = user; // Leaks to the next invocation
  return user;
}
```
```

**Why it's unsafe:** If this warm process is reused for a different tenant's
invocation, `cache['currentUser']` still holds the previous tenant's user
object.

### Shared mutable object

```
```
1
2
```



```
// UNSAFE: shared object that accumulates data from multiple tenants
const issueCache = {};

export async function onIssueCreated({ payload, context }) {
  // Issue keys are NOT globally unique - the same key can exist
  // in different tenants' Jira instances
  issueCache[payload.issue.key] = payload.issue;
}
```
```

## Safe patterns

Each pattern below eliminates the risk in a different way: avoiding module-level
state entirely, scoping it to a tenant identifier, or delegating persistence to
Forge Storage, which is tenant-scoped by design.

### Scope all data to the invocation context

The safest approach is to **never store tenant data in module-level variables**.
Compute or fetch everything within the handler function itself.

```
```
1
2
```



```
// SAFE: all state is local to the function invocation
export async function handler(context) {
  // Fetch fresh data every invocation - no cross-tenant risk
  const response = await api.asUser().requestJira('/rest/api/3/myself');
  const user = await response.json();
  return user;
}
```
```

### Partition a cache by tenant identifier

If you need in-process caching for performance, **always key the cache by a
tenant-specific identifier**, such as `cloudId`. This ensures that a warm
process reused for tenant B will only find tenant B's data.

```
```
1
2
```



```
// SAFE: cache partitioned by cloudId (tenant identifier)
const cache = {};

export async function handler(context) {
  const { cloudId } = context;

  if (cache[cloudId]?.currentUser) {
    return cache[cloudId].currentUser;
  }

  const response = await api.asUser().requestJira('/rest/api/3/myself');
  const user = await response.json();

  // Scope the cached value to this specific tenant
  if (!cache[cloudId]) {
    cache[cloudId] = {};
  }
  cache[cloudId].currentUser = user;

  return user;
}
```
```

Even with tenant-partitioned caches, cached data may become stale across
invocations. Consider adding a time-to-live (TTL) check or using
[Forge Storage](/platform/forge/storage/) for durable, cross-invocation data
that is automatically scoped per installation.

### Use Forge Storage for durable cross-invocation data

[Forge hosted storage capabilities](/platform/forge/storage/) ([Key-Value Store]{/platform/forge/storage-reference/kvs/},
[Custom Entity Store](/platform/forge/storage-reference/entities/),
[SQL](/platform/forge/storage-reference/sql/))
is **automatically scoped per app installation**, which means it is
inherently tenant-safe. Prefer storage over in-memory caches when you need data
to persist across invocations.

```
```
1
2
```



```
import { kvs } from '@forge/kvs';

// SAFE: Forge Storage is scoped per installation (per tenant)
export async function handler(context) {
  const cachedUser = await kvs.get('currentUser');
  if (cachedUser) {
    return cachedUser;
  }

  const response = await api.asUser().requestJira('/rest/api/3/myself');
  const user = await response.json();

  await kvs.set('currentUser', user);
  return user;
}
```
```

### Use read-only module-level constants

Module-level state that is **read-only** and **not tenant-specific** is safe.

```
```
1
2
```



```
// SAFE: read-only configuration constant - not tenant data
const MAX_RETRIES = 3;
const API_VERSION = 'v3';

export async function handler(context) {
  // MAX_RETRIES and API_VERSION are the same for all tenants
  // and are never modified
}
```
```

## Audit checklist

Use this checklist to review your Forge app for data isolation risks:

## Static analysis and linting

Forge does not currently provide built-in lint rules to detect unsafe global
state. However, you can configure your own ESLint rules to flag patterns that
are commonly associated with cross-tenant data leaks:

* Mutable `let` or `var` declarations at module scope.
* Assignments to `module`-level `const` objects (e.g., `cache[key] = value`).
* Use of `global` or `globalThis`.

Consider adding the
[`no-restricted-syntax`](https://eslint.org/docs/latest/rules/no-restricted-syntax)
ESLint rule or a custom plugin to catch these patterns during development.
