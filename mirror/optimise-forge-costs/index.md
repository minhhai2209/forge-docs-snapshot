# Optimise Forge platform costs

This guide will help you keep your Forge app costs low — or avoid charges altogether — by showing you practical patterns that reduce billable usage without sacrificing functionality.

Forge's consumption-based pricing includes generous free monthly allowances, and many apps will never exceed them. But as your app scales or handles more events, function invocations, storage operations, and logging can push usage past the free tier. The techniques in this guide help you stay within those allowances — or minimise overage when you do exceed them.

## Understanding what drives Forge costs

Forge uses a **consumption-based pricing model** with generous free monthly allowances per app. Charges only apply when you exceed these thresholds. Understanding the billable capabilities helps you know where to focus your optimisation efforts.

See [Forge platform pricing](/platform/forge/forge-platform-pricing/) for the authoritative and up-to-date allowances and prices. A summary is included below for reference:

| Capability | Unit | Free usage allowance (monthly) | Overage price per unit ($USD) |
| --- | --- | --- | --- |
| Forge Functions: Duration | $/GB-seconds | 200,000 GB-seconds | 0.000025 |
| Key-Value Store: Reads | $/GB | 0.1 GB | 0.055 |
| Key-Value Store: Writes | $/GB | 0.1 GB | 1.090 |
| Logs: Writes | $/GB | 1 GB | 1.005 |
| SQL: Compute duration | $/hr | 1 hr | 0.143 |
| SQL: Compute requests | $/1M-requests | 100,000 requests | 1.929 |
| SQL: Data stored | $/GB-hours | 730 GB-hours | 0.00076850 |
| Object Store: Requests | $/1k-requests | 5,000 requests | 0.001353 |
| LLM: Input | $/credits | 0 credits | 0.0000001 |
| LLM: Output | $/credits | 0 credits | 0.0000005 |

Capabilities not listed above — including UI modules, Jira expressions, and Forge Remote — are **free** and do not contribute to your bill.

### Key cost drivers to watch

* **Function duration × memory = GB-seconds.** Compute cost is determined by how long your functions run multiplied by the memory allocated to them. Reducing either dimension reduces cost. The techniques in this guide primarily target reducing function duration — by reducing unnecessary invocations, cutting API call counts, and exiting early.
* **KVS reads and writes.** Key-Value Store operations are billed by data volume. Writes are ~20× more expensive than reads, so minimising unnecessary writes has an outsized impact on costs.
* **Logging.** Every call to `console.log()` contributes to log write volume. Avoid verbose logging in hot paths; use log levels and strip debug logs from production builds.
* **LLM input and output.** LLM usage is billed per credit with no free usage allowance. Input credits and output credits are charged at different rates ($0.0000001/credit for input, $0.0000005/credit for output).

You can monitor your app's usage and forecast costs in the [Developer Console](/platform/forge/monitor-usage-metrics/), and use the [Forge cost estimator](https://developer.atlassian.com/forge-cost-estimator) to preview potential charges.

## Frontend optimisations

Forge functions are invoked every time your UI needs data or the user performs an action. Moving logic into the browser — where it runs freely — is one of the highest-impact ways to reduce FaaS invocations.

### Shift logic to the frontend

Every call to a Forge function — even a simple one — incurs a FaaS invocation cost. A significant opportunity for cost reduction lies in moving logic that doesn't require server-side execution into your frontend UI component instead.

Forge's UI Kit and Custom UI frontends run entirely in the browser and are not subject to function invocation costs or limits. This makes the frontend an ideal place for:

* **Direct API calls via `requestJira()` / `requestConfluence()`** — both UI Kit and Custom UI can call Atlassian REST APIs directly from the browser using the Forge bridge, without invoking a backend function at all.
* **Data formatting and transformation** — sorting, filtering, grouping, or reformatting data — often it is more cost efficient to perform data intensive operations client-side.
* **Validation** — field validation rules for forms can run client-side before any resolver call is made.
* **Caching fetched data** — storing the result of a resolver call in component state and reusing it across interactions, rather than re-invoking the resolver on every render.

### Making API calls from the frontend

Both UI Kit and Custom UI apps can use [`requestJira()`](/platform/forge/apis-reference/ui-api-bridge/requestJira/) and [`requestConfluence()`](/platform/forge/apis-reference/ui-api-bridge/requestConfluence/) to call Atlassian REST APIs directly from the browser. This eliminates the round-trip through a Forge function for read-heavy operations like fetching issue details or page content.

```
```
1
2
```



```
// Both UI Kit and Custom UI — import from @forge/bridge
import { requestJira } from '@forge/bridge';

// ✅ Fetch issue data directly from the browser — no function invocation needed
async function loadIssue(issueKey) {
  const response = await requestJira(`/rest/api/3/issue/${issueKey}?fields=summary,status,assignee`);
  return response.json();
}
```
```

Note that API requests from the frontend are always authenticated as the context user. Secure operations, such as accessing Forge storage, can only be accessed via a resolver.

**When to keep logic in the backend:** Use Forge functions for operations that require secure access to Atlassian APIs, app storage, or secrets. Don't expose sensitive data or business logic to the client unless the context user is authorised to see it.

### Example: avoid calling a resolver on every render

A common anti-pattern is fetching data inside a component that re-renders frequently. Instead, fetch once and store the result:

```
```
1
2
```



```
// ❌ Anti-pattern: resolver called on every render
function MyPanel() {
  const result = useAction(() => invoke('getConfig'));
  return <Text>{result.data?.value}</Text>;
}

// ✅ Better: fetch once, store in state
function MyPanel() {
  const [config, setConfig] = useState(null);
  useEffect(() => {
    invoke('getConfig').then(setConfig);
  }, []); // empty dependency array = runs once on mount
  return <Text>{config?.value}</Text>;
}
```
```

**References:** [Forge UI Kit](/platform/forge/ui-kit/) | [Custom UI](/platform/forge/custom-ui/)

### Use `useProductContext()` / `view.getContext()` to avoid resolver invocations

A surprisingly common anti-pattern is invoking a Forge resolver to look up contextual metadata that is already available in the frontend context — for example, the current issue key, project key, or space key. Both UI Kit and Custom UI provide ways to access this context directly in the browser, with no function invocation required.

In both **UI Kit** and **Custom UI** you can use `view.getContext()` from `@forge/bridge`:

```
```
1
2
```



```
import { view } from '@forge/bridge';

async function getIssueKey() {
  const context = await view.getContext();
  return context.extension.issue.key;
}
```
```

Alternatively in **UI Kit**, you can also use the `useProductContext()` hook from `@forge/react`:

```
```
1
2
```



```
import { useProductContext } from '@forge/react';

function MyPanel() {
  const context = useProductContext();

  // context.extension.issue.key, context.extension.project.key, etc.
  // are all available here — no resolver call needed
  const issueKey = context?.extension?.issue?.key;

  return <Text>Issue: {issueKey}</Text>;
}
```
```

You can use the context values to decide *whether* to call a resolver (e.g. only fetch data if the issue is in a specific project), or to pass them as arguments to a resolver rather than having the resolver look them up itself.

**References:** [useProductContext hook](/platform/forge/ui-kit/hooks/use-product-context/) | [view.getContext() (Custom UI)](/platform/forge/custom-ui/iframe/#getcontext)

---

## Trigger & scheduling optimisations

Scheduled and event-driven triggers are one of the most common sources of unnecessary invocations. The goal is to invoke your function only when there is real work to do.

### Reduce scheduled trigger frequency

Scheduled triggers are one of the most common sources of unnecessary compute consumption. Each execution of a scheduled trigger invokes a Forge function — and if the trigger runs frequently but rarely has meaningful work to do, the invocations are wasted.

### Choose the right interval

Before setting a schedule, ask: *How often does this job actually need to run?* Common mistakes include:

* Running a sync job every 5 minutes when the data it reads only changes hourly.
* Running a cleanup job nightly when it could run weekly.
* Using a short interval "just to be safe" without profiling actual data change frequency.

In your `manifest.yml`, prefer longer intervals wherever possible:

```
```
1
2
```



```
modules:
  scheduledTrigger:
    - key: my-scheduled-trigger
      function: my-function
      interval: day   # Options: fiveMinutes, hour, day, week
```
```

### Use event-driven triggers instead of polling

If your scheduled trigger is polling for changes (e.g. checking whether issues have been updated), replace it with a **product event trigger** that fires only when the relevant event actually occurs. This eliminates unnecessary invocations entirely.

```
```
1
2
```



```
modules:
  trigger:
    - key: issue-updated-trigger
      function: my-function
      events:
        - avi:jira:updated:issue   # fires only when an issue is updated
```
```

### Use Forge Realtime instead of polling a resolver

When implementing map-reduce operations or integrating with external systems, a common pattern is to use a resolver to poll Forge storage until a certain value is updated. This can cause unnecessary compute usage and a lengthy wait for the user. A more efficient alternative is to use [Forge Realtime](/platform/forge/realtime/) to push events from your backend to your UI. Forge Realtime can also be used to send events between different instances of your UI (e.g. to keep multiple users in sync).

### Do a quick check before doing expensive work

If you must use a scheduled trigger, add a lightweight guard at the start of your function to check whether there is actually work to do before proceeding with expensive operations:

```
```
1
2
```



```
export async function run(event, context) {
  // Read a lightweight flag from storage before doing expensive work
  const lastProcessedAt = await storage.get('lastProcessedAt');
  const dataChangedAt = await getDataLastChangedTimestamp();

  if (dataChangedAt <= lastProcessedAt) {
    // Nothing has changed since last run — exit early
    return;
  }

  // Only now do the expensive processing
  await processData();
  await storage.set('lastProcessedAt', Date.now());
}
```
```

**References:** [Scheduled Trigger](/platform/forge/manifest-reference/modules/scheduled-trigger/) | [Product Events](/platform/forge/events-reference/product_events/)

### Filter trigger events effectively

When your app listens to product events (such as issue updated, page created, or sprint started), Forge invokes your function for *every matching event* across all users and content in the installed site. At scale, this can result in a large number of invocations — many of which your function will immediately discard because they don't meet your business criteria.

The key principle is: **reject irrelevant events as early and cheaply as possible.**

#### Use event filter conditions in the manifest

Where available, use [manifest-level filtering](/platform/forge/events-reference/product_events/#filter-out-atlassian-app-events) to prevent Forge from invoking your function at all for events you don't care about. This is the most cost-effective option because the function is never invoked:

```
```
1
2
```



```
modules:
  trigger:
    - key: issue-trigger
      function: handle-issue-event
      events:
        - avi:jira:updated:issue
      filter:
        # Only invoke the function for issues in a specific project
        expression: "event.issue.fields.project.key == 'MYPROJ'"
```
```

#### Exit early inside the function

When manifest-level filtering isn't sufficient, add a fast check at the very top of your function handler before any expensive operations:

```
```
1
2
```



```
export async function run(event, context) {
  const { issue } = event;

  // Exit early if this isn't an issue type we care about
  if (issue.fields.issuetype.name !== 'Bug') return;

  // Exit early if the priority isn't high enough
  if (!['Critical', 'Blocker'].includes(issue.fields.priority.name)) return;

  // Only now do expensive work
  await processHighPriorityBug(issue);
}
```
```

#### Ignore events generated by your own app

A common source of wasted invocations is an app that modifies a Jira entity (for example, updating an issue field) and then receives and processes the event that its own update generated. This creates unnecessary work and can even cause feedback loops.

Use the `ignoreSelf` filter property in your manifest to tell Forge to suppress events generated by your app's own actions:

```
```
1
2
```



```
modules:
  trigger:
    - key: issue-updated-trigger
      function: handle-issue-update
      events:
        - avi:jira:updated:issue
      filter:
        ignoreSelf: true   # Don't invoke this function for updates made by our own app
        expression: "event.issue.fields.project.key == 'MYPROJ'"
```
```

**Jira only:** `ignoreSelf` currently only works with [Jira events](/platform/forge/events-reference/jira/). It is not yet supported for Confluence or other product events.

**References:** [Product Events reference](/platform/forge/events-reference/product_events/) | [Trigger manifest reference](/platform/forge/manifest-reference/modules/trigger/)

### Use web triggers for inbound webhooks instead of polling

If your app periodically polls an external service to check for updates — for example, calling a third-party API every few minutes to see if anything has changed — consider replacing this pattern with a **Forge web trigger**.

A web trigger gives your app a publicly accessible HTTPS URL. You can register this URL with the external service as a webhook, so it calls *you* only when something actually changes. This eliminates all the empty polling invocations. Note that there is no flagfall cost or network charges for invoking web triggers, but the web trigger function runtime is still billed as compute.

```
```
1
2
```



```
modules:
  webtrigger:
    - key: my-inbound-webhook
      function: handle-webhook

functions:
  - key: handle-webhook
    handler: index.handleWebhook
```
```

```
```
1
2
```



```
// Your web trigger handler receives the inbound HTTP request
export async function handleWebhook(request) {
  const payload = JSON.parse(request.body);

  // Process the event from the external service
  await processExternalEvent(payload);

  return { statusCode: 200, body: 'OK' };
}
```
```

**References:** [Web Trigger](/platform/forge/runtime-reference/web-trigger/) | [Web Trigger manifest reference](/platform/forge/manifest-reference/modules/web-trigger/)

---

## Storage optimisations

Forge provides built-in storage options that can help you avoid redundant API calls and unnecessary function work. Understanding what's free and what's billed helps you use storage effectively without introducing new costs.

### Forge Storage (Key-Value Store and Custom Entities)

The [Forge Storage API](/platform/forge/runtime-reference/storage-api-basic-api/) provides a hosted key-value store available to all Forge apps. Note that **KVS reads and writes are billable above the free tier** (0.1 GB free per month for reads and writes respectively — see the pricing table above). That said, KVS storage does not incur function invocation costs, and storing data here can help you avoid redundant API calls to Atlassian products.

Good use cases for Forge Storage include:

* App configuration and settings
* Per-installation state (e.g. last sync timestamp)
* Cached results from expensive API calls (though be wary of using storage excessively for caching — write costs can add up over time!)
* Small datasets that change infrequently

```
```
1
2
```



```
import { storage } from '@forge/api';

// Cache an expensive API result for 1 hour
const CACHE_TTL_MS = 60 * 60 * 1000;

export async function getCachedData(key) {
  const cached = await storage.get(`cache:${key}`);
  if (cached && Date.now() - cached.timestamp < CACHE_TTL_MS) {
    return cached.value; // serve from cache — no extra API call needed
  }

  const freshData = await fetchExpensiveData(key);
  await storage.set(`cache:${key}`, { value: freshData, timestamp: Date.now() });
  return freshData;
}
```
```

### Entity properties

Jira and Confluence support [entity properties](https://developer.atlassian.com/cloud/jira/platform/jira-entity-properties/) (also called [content properties](https://developer.atlassian.com/cloud/confluence/content-properties/) in Confluence) — metadata storage attached directly to issues, projects, users, pages, and other entities. Entity properties are stored by the product itself, so they don't consume Forge Storage quota and are entirely free to use.

Good use cases for entity properties include:

* Storing small amounts of app-specific data against Jira issues or Confluence pages
* Flags or markers that need to be queryable (via JQL for Jira entity properties)
* Data that should travel with the entity (e.g. during export/import)

```
```
1
2
```



```
import { asApp, route } from '@forge/api';

// Store metadata against a Jira issue — uses product storage, not Forge storage
await asApp().requestJira(route`/rest/api/3/issue/${issueId}/properties/my-app-data`, {
  method: 'PUT',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ processedAt: Date.now(), status: 'done' }),
});
```
```

**Visibility:** Some entity property types are visible to other apps and end-users via the REST API, so they are **not suitable for storing sensitive or confidential data**. Use Forge Storage (with appropriate access controls) or Forge Remote with external storage for sensitive information.

**Size limits:** Entity properties have a maximum value size of 32 KB per property. For larger payloads, use Forge Storage or Forge Remote with external storage.

### Avoid excessive storage reads/writes

KVS reads and writes are billed by data volume once you exceed the free tier. Avoid patterns that perform dozens of individual storage reads/writes in a loop — batch your reads and writes where possible, and use the [Custom Entities API](/platform/forge/runtime-reference/custom-entities/) for structured querying rather than iterating over many keys.

**References:** [Storage API](/platform/forge/runtime-reference/storage-api-basic-api/) | [Jira entity properties](https://developer.atlassian.com/cloud/jira/platform/jira-entity-properties/) | [Confluence content properties](https://developer.atlassian.com/cloud/confluence/content-properties/)

### Cache app-level data with a TTL

Some data fetched via `asApp()` API calls is the same for all users and changes infrequently — for example, custom field IDs, project configurations, field schemes, or workflow statuses. Rather than making a live API call on every function invocation, cache this data in Forge Storage with a time-to-live (TTL) and serve subsequent invocations from the cache.

```
```
1
2
```



```
import { storage } from '@forge/api';

const CACHE_TTL_MS = 60 * 60 * 1000; // 1 hour

async function getCustomFieldId(fieldName) {
  const cacheKey = `field-id:${fieldName}`;
  const cached = await storage.get(cacheKey);

  if (cached && Date.now() - cached.cachedAt < CACHE_TTL_MS) {
    return cached.fieldId; // serve from cache — no API call needed
  }

  // Cache miss: fetch from API and store
  const fields = await fetchAllFields();
  const field = fields.find(f => f.name === fieldName);

  await storage.set(cacheKey, { fieldId: field.id, cachedAt: Date.now() });
  return field.id;
}
```
```

This pattern is particularly effective for data that is read on every invocation but updated rarely — the cache hit rate will be very high, and you'll typically make one API call per hour instead of one per invocation.

Because KVS writes are ~20× more expensive than reads, prefer longer TTLs where the data allows. A 1-hour TTL means 1 write per hour; a 1-minute TTL means 60 writes per hour — at 20× the cost.

**References:** [Storage API](/platform/forge/runtime-reference/storage-api-basic-api/)

### Use `storage.query()` instead of iterating over keys

When working with the Forge Storage Custom Entities API, avoid patterns that fetch all stored items into memory and then filter them in your function code. Instead, use `storage.query()` to push filtering, sorting, and pagination down to the storage layer — this reduces both the volume of data read (lowering KVS read costs) and the amount of work your function has to do.

```
```
1
2
```



```
import { storage, startsWith } from '@forge/api';

// ❌ Anti-pattern: fetch all items and filter in code
const allItems = await storage.query().getMany();
const activeItems = allItems.results.filter(item => item.value.status === 'active');

// ✅ Better: use index-based querying to fetch only what you need
// (requires defining an index on the 'status' field in your entity schema)
const activeItems = await storage.query()
  .index('by-status')
  .where('status', startsWith('active'))
  .limit(50)
  .getMany();
```
```

Even without custom indexes, always pass a `.limit()` to bound the maximum number of items returned per call, and use cursor-based pagination rather than loading all pages at once.

**References:** [Custom Entities API](/platform/forge/runtime-reference/storage-api-custom-entities/)

---

## API & data fetching optimisations

Every API call within a Forge function consumes time and contributes to function duration costs. Fetching only what you need, using bulk endpoints, and pre-filtering at the source are the most effective ways to reduce API-related costs.

### Use bulk APIs instead of individual request APIs

One of the most impactful performance and cost optimisations is replacing multiple individual API calls with a single bulk API call. Each API call within a Forge function consumes time (increasing function duration) and contributes to rate limit consumption. Reducing the number of API calls directly reduces the cost and risk of your function.

#### The N+1 problem

A classic anti-pattern is the "N+1 problem": fetching a list of items and then making a separate API call for each item to retrieve its details:

```
```
1
2
```



```
// ❌ Anti-pattern: N+1 API calls
const issues = await searchIssues('project = MYPROJ');
for (const issue of issues) {
  // This makes one API call per issue — very expensive!
  const details = await getIssue(issue.id);
  await process(details);
}
```
```

#### Use bulk endpoints

Many Atlassian APIs offer bulk endpoints that can fetch multiple resources in a single request. Use these wherever they exist. For example, when searching for issues, the [Jira Search API](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-search/#api-rest-api-3-search-post) returns full issue objects with all the fields you request — no need for follow-up calls:

```
```
1
2
```



```
// ✅ Better: fetch all details in one or a few bulk requests
const issues = await searchIssues('project = MYPROJ', {
  fields: ['summary', 'status', 'assignee', 'priority', 'description'],
  // Request all the fields you need upfront
});
// No additional per-issue calls needed — all fields already loaded
for (const issue of issues) {
  await process(issue);
}
```
```

#### Request only the fields you need

For search-style APIs that support field selection, always specify exactly the fields your function needs. This reduces response payload size, improving speed and reducing memory usage:

```
```
1
2
```



```
// ❌ Fetches every field — wastes bandwidth and memory
const response = await asApp().requestJira(route`/rest/api/3/search?jql=project=MYPROJ`);

// ✅ Request only the fields you'll actually use
const response = await asApp().requestJira(
  route`/rest/api/3/search?jql=project=MYPROJ&fields=summary,status,assignee`
);
```
```

#### Examples of bulk API capabilities

| Use case | Individual approach (avoid) | Bulk approach (prefer) |
| --- | --- | --- |
| Fetch multiple Jira issues | `GET /rest/api/3/issue/{issueId}` × N | [POST /rest/api/3/issue/bulkfetch](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issues/#api-rest-api-3-issue-bulkfetch-post) |
| Update multiple issue fields | `PUT /rest/api/3/issue/{issueId}` × N | [POST /rest/api/3/bulk/issues/fields/edit](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-bulk-operations/#api-rest-api-3-bulk-issues-fields-edit-post) |
| Fetch user details | `GET /rest/api/3/user?accountId=X` × N | [GET /rest/api/3/user/bulk](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-users/#api-rest-api-3-user-bulk-get) |
| Search issues with full details | Search then fetch each issue | `POST /rest/api/3/search` with `fields` parameter |
| Fetch multiple Confluence pages | `GET /wiki/api/v2/pages/{id}` × N | `GET /wiki/api/v2/pages?id=X&id=Y&...` |

#### Parallelise independent requests with Promise.all

When you genuinely need to make multiple independent API calls, use `Promise.all` to parallelise them rather than awaiting them sequentially. This reduces total function duration without increasing the number of invocations:

**Rate limits:** Parallelisation is more efficient up to a point, but sending too many concurrent requests can trigger rate limit errors (HTTP 429). Avoid parallelising large numbers of requests at once — send at most 5–10 concurrent requests and batch the rest. See the [Jira rate limiting documentation](https://developer.atlassian.com/cloud/jira/platform/rate-limiting/) for details.

```
```
1
2
```



```
// ❌ Sequential: duration = sum of all call durations
const issueData = await getIssue(issueId);
const userData = await getUser(userId);
const projectData = await getProject(projectId);

// ✅ Parallel: duration ≈ slowest single call
const [issueData, userData, projectData] = await Promise.all([
  getIssue(issueId),
  getUser(userId),
  getProject(projectId),
]);
```
```

**References:** [Jira Search API](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-search/#api-rest-api-3-search-post) | [Jira Bulk Issue Fetch](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issues/#api-rest-api-3-issue-bulkfetch-post) | [Confluence Pages API](https://developer.atlassian.com/cloud/confluence/rest/v2/api-group-page/#api-pages-get)

### Pre-filter bulk operations to reduce unnecessary work

Bulk operations — such as processing all issues in a project, all pages in a space, or all users in an organisation — can be extremely expensive in terms of function duration and API calls. Without good filtering, a single invocation can iterate over thousands of items unnecessarily, rapidly consuming compute quota.

The key principle is: **fetch only the items you actually need to process, not all items and then filter in code.** Spreading work across more invocations through batching may make each individual invocation cheaper, but the total compute consumed is the same — the real saving comes from doing less work in the first place.

#### Use JQL and API filters to pre-filter at the source

If your function iterates over a set of items, tests a condition on each, and then only acts on items that meet the condition, consider whether you can express that condition as a JQL query or API filter — so that only the relevant items are returned in the first place:

```
```
1
2
```



```
// ❌ Anti-pattern: fetch all issues, filter in code
const allIssues = await searchIssues('project = MYPROJ');
for (const issue of allIssues) {
  if (issue.fields.status.name === 'Done' && issue.fields.assignee === null) {
    await processIssue(issue); // only a small subset actually gets processed
  }
}

// ✅ Better: express the condition in JQL so only matching issues are returned
const targetIssues = await searchIssues(
  'project = MYPROJ AND status = Done AND assignee is EMPTY'
);
for (const issue of targetIssues) {
  await processIssue(issue); // every issue here needs processing
}
```
```

#### Use date-based filters to process only recent changes

For scheduled jobs that process "all items that need attention", use a timestamp filter to restrict the query to items that have changed since the last run:

```
```
1
2
```



```
export async function run(event, context) {
  const lastRunAt = await storage.get('lastRunAt') || '2000-01-01';

  // Only fetch issues updated since the last run
  const issues = await searchIssues(
    `project = MYPROJ AND updated >= "${lastRunAt}" ORDER BY updated ASC`
  );

  for (const issue of issues) {
    await processIssue(issue);
  }

  await storage.set('lastRunAt', new Date().toISOString().split('T')[0]);
}
```
```

**References:** [Jira Issue Search API](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-search/#api-rest-api-3-search-post) | [Async Events API](/platform/forge/runtime-reference/async-events-api/) | [Forge platform limits](/platform/forge/platform-quotas-and-limits/)

### Always specify `maxResults` on paginated API calls

Atlassian REST APIs that return paginated results will use a default page size when `maxResults` is not specified — often 50 or 100 items. If your function only needs the first few results, fetching the full default page wastes bandwidth, increases response payload size, and extends function duration (all of which increase compute cost).

Always pass an explicit `maxResults` limit matched to your actual need:

```
```
1
2
```



```
// ❌ Fetches up to 50 issues by default — wasteful if you only need 5
const response = await asApp().requestJira(
  route`/rest/api/3/search?jql=project=MYPROJ&orderby=created DESC`
);

// ✅ Fetch only as many items as you actually need
const response = await asApp().requestJira(
  route`/rest/api/3/search?jql=project=MYPROJ&orderby=created DESC&maxResults=5`
);
```
```

Conversely, when you *do* need all items, use the maximum allowed page size (typically 100 for Jira search) to minimise the number of paginated requests required — fewer requests means shorter function duration.

```
```
1
2
```



```
// ✅ Use maximum page size when fetching all results to minimise round trips
const response = await asApp().requestJira(
  route`/rest/api/3/search?jql=project=MYPROJ&maxResults=100`
);
```
```

**References:** [Jira Search API](https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-search/#api-rest-api-3-search-post) | [Confluence REST API v2](https://developer.atlassian.com/cloud/confluence/rest/v2/)

---

## Function & compute optimisations

Once you've reduced the number of invocations, the next lever is reducing the cost of each individual invocation — by tuning memory, reducing logging overhead, and offloading the heaviest work off-platform.

### Tune function memory allocation

Forge function compute costs are billed in **GB-seconds**: the amount of memory allocated to your function multiplied by how long it runs. This means memory is a direct cost lever — allocating more memory than your function needs wastes money, but allocating too little can slow execution (ironically increasing duration and therefore cost).

The default memory allocation for Forge functions is **512 MB**. You can adjust this per function in your `manifest.yml` using the `memoryMiB` property:

```
```
1
2
```



```
functions:
  - key: my-lightweight-function
    handler: index.run
    memoryMiB: 128   # Reduce for simple, low-memory functions

  - key: my-data-processing-function
    handler: processor.run
    memoryMiB: 1024   # Increase if the function processes large payloads
```
```

#### Finding the right memory setting

* **Start with the default (512 MB)** and observe actual memory usage in your function logs.
* **Reduce memory** for simple resolver functions that do light computation or a single API call — 128 MB is often sufficient.
* **Increase memory** for functions that process large JSON payloads, perform in-memory aggregations, or run data transformations. More memory can also improve CPU allocation, which may reduce duration enough to offset the higher per-second cost.
* **Avoid over-provisioning** — allocating 1024 MB to a function that only uses 100 MB wastes 4× the compute allowance per second of runtime.

The cost formula is: **GB-seconds = (memoryMiB ÷ 1024) × duration in seconds**. A function using 512 MB for 1 second costs the same as a function using 256 MB for 2 seconds — so reducing duration is just as valuable as reducing memory.

**References:** [Function manifest reference](/platform/forge/manifest-reference/modules/function/) | [Forge platform pricing](/platform/forge/forge-platform-pricing/)

### Right-size timeouts and avoid crashes

Set [`timeoutSeconds`](/platform/forge/manifest-reference/modules/function/) to the smallest value your function actually needs, rather than defaulting to the maximum. Beyond avoiding wasted runtime, this also makes your compute costs more predictable when a function crashes.

When a function runs out of memory or the runtime crashes, Forge may be unable to record a reliable execution time. In these cases you are billed for the **lower of** the function's configured timeout or the measured execution time including platform overhead. A tighter timeout therefore caps the cost of an invocation that fails this way. See [How are functions that crash or run out of memory billed?](/platform/forge/forge-platform-pricing/#crashed-functions-billing) for details.

To keep these costs down:

* **Right-size `timeoutSeconds`** to your function's realistic worst-case duration.
* **Avoid out-of-memory failures** by tuning `memoryMiB` (see above) and processing large datasets in batches rather than loading everything into memory at once.

**References:** [Function manifest reference](/platform/forge/manifest-reference/modules/function/) | [Forge platform pricing](/platform/forge/forge-platform-pricing/)

### Avoid verbose logging in high-frequency functions

Every call to `console.log()` contributes to billable log write volume. In functions that are invoked frequently — such as product event triggers or resolvers in widely-used apps — even routine debug logging can accumulate significant log volume.

#### Use conditional logging

Gate debug-level logging behind an environment variable or a Forge Storage flag, so it's only active when you explicitly need it:

```
```
1
2
```



```
const DEBUG = process.env.DEBUG_LOGGING === 'true';

export async function run(event, context) {
  if (DEBUG) console.log('Event received:', JSON.stringify(event));

  // ... function logic ...

  if (DEBUG) console.log('Processing complete');
}
```
```

#### Log exceptions and errors only

In production, restrict logging to errors and meaningful state changes. Avoid logging the full payload of every event or API response — these can be very large and are the primary driver of log volume:

```
```
1
2
```



```
// ❌ Logs the full event payload on every invocation — expensive at scale
console.log('Processing event:', JSON.stringify(event));

// ✅ Log only what you need for debugging production issues
console.log(`Processing issue ${event.issue?.key} (type: ${event.issue?.fields?.issuetype?.name})`);
```
```

**References:** [Forge platform pricing](/platform/forge/forge-platform-pricing/) | [Logging guidelines](/platform/forge/logging-guidelines/)

### Offload compute with Forge Remote

[Forge Remote](/platform/forge/remote/) allows your Forge app to delegate processing to an external backend service that you operate — such as a service running on AWS, GCP, Azure, or any HTTPS-accessible endpoint. This fundamentally changes the cost model: instead of consuming Forge FaaS invocations for compute-intensive work, that work is handled by your own infrastructure.

#### When to use Forge Remote

* **Compute-intensive operations** — machine learning inference, image processing, complex report generation, or data aggregation over large datasets.
* **Long-running operations** — tasks that would exceed Forge's function timeout (25 seconds for standard functions).
* **Existing backend services** — when you already have business logic running in your own infrastructure and don't want to duplicate it in Forge functions.
* **Large-scale storage needs** — offloading data to your own databases when Forge Storage limits are insufficient.

#### How it works

With Forge Remote, your `manifest.yml` declares a remote backend endpoint. Forge routes calls from your resolver to that endpoint, passing the Forge-managed auth token so your backend can verify the request:

```
```
1
2
```



```
remotes:
  - key: my-remote-backend
    baseUrl: https://my-backend.example.com

modules:
  jira:issuePanel:
    - key: my-panel
      resource: main
      resolver:
        function: remote-resolver
        endpoint: my-remote-backend
```
```

Your remote backend receives the invocation and handles it — your Forge function is not executed at all for these calls, saving FaaS invocations.

#### Offloading storage costs

Forge Remote also enables you to use your own databases, blob stores, or caches as a storage backend. This is particularly valuable for:

* Apps with large datasets that exceed Forge Storage limits
* Apps requiring relational queries or full-text search
* Apps needing cross-installation data aggregation

**Think carefully before adopting Forge Remote.** Using a remote backend means you become wholly responsible for operating, securing, scaling, and maintaining that infrastructure — including patching, uptime, and incident response. It also makes your app ineligible for **"Runs on Atlassian"** status, which may be important if you plan to distribute it on the Atlassian Marketplace.

For most teams building in-house tools or Marketplace apps, keeping compute and storage workloads on-platform is by far the simpler option. Forge Remote is best suited to cases where you have an existing backend you need to integrate with, or requirements that genuinely cannot be met by the on-platform capabilities.

**References:** [Forge Remote](/platform/forge/remote/)

---

## Final thoughts

We hope this guide has provided some useful tips for optimising your Forge app costs, and potentially also improving performance. But please take these tips with a grain of salt. As Donald Knuth said in 1974:

> "Programmers waste enormous amounts of time thinking about, or worrying about, the speed of noncritical parts of their programs, and these attempts at efficiency actually have a strong negative impact when debugging and maintenance are considered. We should forget about small efficiencies, say about 97% of the time: premature optimisation is the root of all evil. Yet we should not pass up our opportunities in that critical 3%."

This sage advice also applies to Forge apps.

Forge has a generous free tier. The vast majority of private apps developed by customers for use in a single site — even written naively without special regard for cost — will never exceed it. Some of the practices above are almost universally beneficial: filtering events, using bulk APIs, and writing effective queries will typically simplify app logic while also making it more efficient. Other patterns such as introducing caches, stripping log statements, and offloading compute and storage to Forge Remote introduce real complexity and should only be adopted when profiling shows a clear benefit.

Before making any changes, we recommend profiling your app and making careful observations of your [logs](/platform/forge/monitor-app-logs/) and [usage metrics](/platform/forge/monitor-usage-metrics/) to determine which areas would benefit from optimisation, and whether the complexity trade-off is worthwhile.

Happy forging!
