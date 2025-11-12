# Platform quotas and limits

We’re excited to kickstart the Forge journey by extending free use of the
Forge platform through 2025. We know the value that apps bring to our customers,
and want to support our developer ecosystem in getting started with Forge,
whether the app is for your organization, your customers, or for the
Atlassian Marketplace.

Forge apps can consume resources up to the quotas or limits outlined below.
The Function as a Service (FaaS) and storage quotas scale with your apps
install base. The larger the install base (number of seats), the higher the
FaaS and storage quotas are. Resource update quotas are applied on a per app
basis.

If your app consistently exceeds the quotas or limits, we will contact you.
You can also contact us if you think your app needs higher quotas or limits.
[Learn more about exceeding Forge limits and quotas](#apps-exceeding-quotas-or-limits).

These guidelines apply until the end of December 2024.

In addition to platform quotas and limits, Forge apps may also be affected by Atlassian
app-specific rate limits, such as when making REST API calls to
[Jira](https://developer.atlassian.com/cloud/jira/platform/rate-limiting/)
or [Confluence](https://developer.atlassian.com/cloud/confluence/rate-limiting/).

## Usage-based quotas

The FaaS and storage quotas are provided on a per app, per seat basis. For a
private app, this is the number of Jira Software and/or Confluence seats
that you have licensed. For a free or paid Marketplace app, this is the
total number of seats that all your app’s customers have licensed,
including evaluations.

As you estimate your app's usage relative to the quotas and limits below,
remember that the number of active users at any given point in time will
likely be lower than the number of licensed seats for an installation,
which would give your app some headroom.

### Jira issue panel app example

In this example, a paid Marketplace Forge app has 10 500-seat customers,
and five 10-seat customers, which is a total of 5,050 seats. The Forge app's weekly quota
is shown below.

| FaaS | | |
| --- | --- | --- |
| Invocations (seats) | Runtime (weekly) | Data returned (weekly) |
| 5,050,000 invocations | 20,200 minutes | 99 GB |
| Storage | | |
| --- | --- | --- |
| Storage capacity (seats) | Reads (weekly) | Writes (weekly) |
| 40,400 MB | 80,800 MB | 20,200 MB |
| Resource updates | | |
| --- | --- | --- |
| File upload (weekly) | File uploads (weekly) |  |
| 150 MB | 500 uploads |  |

To estimate how much of the quota the app will use, assume that all of your
users are on the standard edition of Jira Software.

The app has two modules that consume FaaS resources: a Jira issue activity
panel using Custom UI and an Atlassian app trigger that's listening to the issue
created event.

#### Calculate FaaS usage

The Jira issue activity panel loads whenever an issue is viewed, and invokes
its resolver function once. The resolver takes an average of 500 ms to
run, and returns an average of 32 KB to the client. In other words, the app
will consume one FaaS invocation, 500 ms of FaaS runtime, and 32 KB of FaaS
data returned every time a user views an issue in Jira.

In this example, the view issue event has 70 issue views per seat, per week,
for the app’s 10-seat licenses, and 25 issue views per seat for the 500-seat
licenses. The app has an estimated 3,500 issue views across the app’s 10-seat
licenses and 125,000 issue views across the 500-seat licenses, or 128,500
issue views per week in total.

```
```
1
2
```



```
 (70 * 50) + (25 * 5000) = 128,500 weekly invocations
 (128,500 * 500 ms)/1000/60 = 1,071 minutes
 (128,500 * 32 KB)/1000/1000 = 3.9 GB
```
```

The Atlassian app trigger fires whenever a Jira issue is created, and takes an
average of 2000 ms to run. Note that triggers don't return data, and therefore
don't consume the FaaS data quota.

In this example, the create issue event has three issues created per seat for
the app’s 10-seat licenses, and one issue created per seat for the 500-seat
licenses. The app has an estimated 150 issues created across the app’s 10-seat
licenses and 5,000 issues created across the 500-seat licenses, or 5,150
issues created per week total.

```
```
1
2
```



```
(3 * 50) + (1 * 5000) = 5,150 weekly issues
(5,150 * 2000 ms)/1000/60 = 172 minutes
```
```

Add the totals from the Jira issue panel and Atlassian app trigger together to get
the total FaaS usage of for the app, and calculate the percentage of the
quota that you’ll likely use:

```
```
1
2
```



```
128,500 + 5,150 = 133,650 invocations (2.6% of our quota of 5,050,000)
1,071 + 172 = 1,243 minutes (6.2% of our quota of 20,200)
4 GB data returned (4.1% of our quota of 99 GB)
```
```

#### Calculate resources usage

The Jira issue activity panel app uses Custom UI, and bundles some static
resources that are served to users when they use the app. Note that only
resources used in Custom UI have quotas applied. Forge JavaScript functions and
dependencies are not counted towards the app’s quota. Only deployments to
the production environment count towards the quota. Deployments to the
development and staging environments do not count towards the quota.

In this example, the static resources include an HTML file (1 MB), a
JavaScript file (1 MB), a CSS file (1 MB), a PNG file (1 MB), and a
GIF (1 MB); which is a total of 5 files and 5 MB.

Each time the app is deployed, the following quota is consumed:

```
```
1
2
```



```
5 * 1 MB = 5 MB uploaded (3% of the 150 MB quota)
5 files uploaded (1% of the 500 files quota)
```
```

This app consumes the weekly “File uploads (MB)” resource quota at a greater rate
than our “File uploads (file count)” resource quota. Divide the total quota
by the MB consumed per deploy to determine how many times the app can be
deployed weekly before exceeding the quota.

```
```
1
2
```



```
150 MB quota per week / 5 MB deployment size = 30 production deployments per week
```
```

If the app consumes the “File uploads (file count)” quota faster than
the “File uploads (MB)” quota, the number of files being deployed is the
limiting factor in how many deployments can be performed in a given week.

## Installation quotas

The quotas listed below apply to an app installation; E.g. the
*example* app, installed on *example.atlassian.net* in the *production* environment.

There are three tiers for quotas, depending on how your app is deployed:

* Paid apps - Apps listed on the Atlassian Marketplace with a paid license.
* Free apps - Apps listed on the Atlassian Marketplace with a free license.
* Distributed apps - Apps distributed via the developer console.

## Function as a Service quotas

The FaaS quotas are consumed when the function is invoked in any environment,
and scale with the number of seats in your app’s install base. Runtime is
metered by millisecond or part thereof. Data returned is metered by KB
or part thereof. These quotas are refreshed weekly.

|  | Paid apps | | Free apps | | Distributed apps | |
| --- | --- | --- | --- | --- | --- | --- |
|  | First 100 seats, total | Per seat thereafter | Up to 100 seats, total | Per seat thereafter | Up to 100 seats, total | Per seat thereafter |
| Invocations (weekly) | 100,000 invocations | 1,000 invocations | 50,000 invocations | 500 invocations | 50,000 invocations | 500 invocations |
| Runtime (weekly) | 400 minutes | 4 minutes | 200 minutes | 2 minutes | 200 minutes | 2 minutes |
| Data returned (weekly) | 2,000 MB | 20 MB | 1,000 MB | 10 MB | 1,000 MB | 10 MB |

## Resource update quotas

These quotas apply to the static resources packaged with your app that are
used by Custom UI functions. Note that Forge JavaScript functions and
dependencies are not counted towards the app’s quota.
Resource quotas are consumed per deployment to your production environment;
deployments to development and staging environments are unmetered. These quotas are
refreshed weekly.

|  | Paid apps | Free apps | Distributed apps |
| --- | --- | --- | --- |
|  | Per app | Per app | Per app |
| File capacity (weekly) | 150 MB | 75 MB | 75 MB |
| Files uploaded (weekly) | 500 files | 250 files | 250 files |

## KVS and Custom Entity Store quotas

These quotas apply to the use of [Key-Value Store (KVS)](/platform/forge/runtime-reference/storage-api-basic/) and [Custom Entity Store](/platform/forge/storage-reference/storage-api-custom-entities/)
in any environment, and scale with the number of seats in your app's install base.

If an installation decreases its seat count, quotas will currently *not* decrease
accordingly. This may change in the future, at which point we will provide guidance
on how to react to these events. Meanwhile, follow [your GDPR responsibilities with respect to storing, reporting and erasing user data](/platform/forge/user-privacy-guidelines/).

As with all quotas and limits, if you suspect our KVS and Custom Entity Store quotas will prevent
you from implementing your Forge app, [contact us to discuss your use case](#apps-exceeding-quotas-or-limits).

### Total storage capacity quota

Storage capacity (MB) is the total amount of storage provisioned per seat for each
installation of your app. These quotas are tracked in terms of raw format size.

The KVS [provides a way to store sensitive credentials (secrets)](/platform/forge/runtime-reference/storage-api-secret/),
which is subject to a separate total storage quota from general storage.

|  | Paid apps | | Free apps | | Distributed apps | |
| --- | --- | --- | --- | --- | --- | --- |
|  | First 100 seats, total | Per seat thereafter | Up to 100 seats, total | Per seat thereafter | Up to 100 seats, total | Per seat thereafter |
| Storage capacity | 1200 MB | 12 MB | 600 MB | 6 MB | 600 MB | 6 MB |
| Secret storage capacity | 200 MB | 2 MB | 100 MB | 1 MB | 100 MB | 1 MB |

### Weekly storage transfer capacity quotas

Read and write capacity quotas are the amount of data that can be transferred
in or out of hosted storage each week, per seat. These quotas are refreshed
weekly, and are tracked in terms of raw format size.

|  | Paid apps | | Free apps | | Distributed apps | |
| --- | --- | --- | --- | --- | --- | --- |
|  | First 100 seats, total | Per seat thereafter | Up to 100 seats, total | Per seat thereafter | Up to 100 seats, total | Per seat thereafter |
| Read capacity per week | 2400 MB | 24 MB | 1200 MB | 12 MB | 1200 MB | 12 MB |
| Write capacity per week | 600 MB | 6 MB | 300 MB | 3 MB | 300 MB | 3 MB |

## Platform limits

The Forge platform has additional limits that cannot be scaled with your app's usage.
To prevent your app from exceeding these limits, you may need to tune your app or remove some
resources. [Learn more about exceeding Forge limits and quotas](#apps-exceeding-quotas-or-limits).

## Invocation limits

An app can be invoked by users, webtriggers, or scheduled triggers. The following limits apply to all three:

| Resource | Limit | Description |
| --- | --- | --- |
| Invocation rate limit | 1,200 | Maximum number of invocations per one minute *sliding window*. That is, an app reaches this limit when it is invoked 1,200 times *within the last 60 seconds*. |
| Runtime seconds  (also includes UI modules invoked by Forge Remote) | 25 | Maximum runtime permitted before the app is stopped. |
| Runtime seconds  (events invoked by Forge Remote) | 5 | Maximum runtime permitted before the app is stopped. This applies to remote back ends receiving events from the Atlassian platform. |
| Runtime seconds (async events and scheduled trigger module) | 900 | This applies to function modules that are only referenced by consumer or scheduled trigger modules. Default timeout is 55 seconds. Use [timeoutSeconds](/platform/forge/manifest-reference/modules/function/) to extend it. |
| Runtime seconds  (web-triggers) | 55 | Maximum runtime permitted before the app is stopped. |
| Single outbound request timeout (async events) | 180 | Maximum time a single outbound request can take before being terminated. Outbound requests refer to fetch requests, including both Atlassian app REST API and external API requests. This limit can only be reached using [long-running functions](/platform/forge/use-a-long-running-function/). |
| Log lines per invocation | 100 per runtime minute (rounded up) | Maximum number of log entries for an invocation. The limit is calculated based on the function timeout, specified by `timeoutSeconds`, rounded up per minute.  * A function without a timeout declared is limited to 100 log lines. * A function with `timeoutSeconds: 90` (a minute and a half) is limited to 200 log lines. |
| Log size per invocation | 200 KB | Maximum size of all log line data generated per invocation. |
| Log file size per download | 100 MB | Maximum file size of filtered logs per download. |
| Log lines per download | 96,000 | Maximum number of log entries per download. |
| Egress requests | 100 per runtime minute (rounded up) | Number of network requests per invocation, excluding those made using `requestJira` or `requestConfluence`. The limit is calculated based on the function timeout, specified by `timeoutSeconds`, rounded up per minute.  * A function without a timeout declared is limited to 100 requests. * A function with `timeoutSeconds: 90` (a minute and a half) is limited to 200 requests. |
| Egress requests | 50,000 requests per minute, per app for egress calls | The maximum number of requests per minute that an app can make for egress calls, excluding those made using `requestJira` or `requestConfluence`. |
| Network requests | 3,000,000 requests per minute, per app and 100,000 requests per minute, per app, per tenant | The maximum number of requests per minute that an app can make for network calls, including those made using `requestJira` or `requestConfluence`. |
| Memory | 1,024MB | Available memory per invocation. |
| Front-end invocation request payload size | 500KB | The maximum request payload size for a front-end invocation (for example, `invoke` and `invokeRemote` via `@forge/bridge`). |
| Front-end invocation response payload size | 5MB | The maximum response payload size from a front-end invocation (for example, `invoke` and `invokeRemote` via `@forge/bridge`). |

If your app is still running on the previous runtime version, it only has 128MB of available memory per invocation.

We strongly recommend all Forge developers to use the current runtime. For details about the previous runtime (including instructions for migration), see
[Upgrading from legacy runtime](/platform/forge/runtime-reference/legacy-runtime-migrating/).

## Resource limits

There are limits on the number and size of static [resources](https://developer.atlassian.com/platform/forge/manifest-reference/resources/) that can be bundled with your app if you use Custom UI or UI Kit. The following limits apply:

| Category | Resource | Limit | Description |
| --- | --- | --- | --- |
| Custom UI | Bundle files | 5000 | Maximum number of files declared in a single resource bundle. |
| Bundle size | 50 | Maximum bundle size in megabytes (MB) for a resource. |
| Bundle count | 50 | Maximum number of resources per app. |
| UI Kit | Bundle files | 5000 | Maximum number of files declared in a single bundle. |
| Bundle size | 50 | Maximum bundle size in megabytes (MB) for a resource. |
| Bundle count | 50 | Maximum number of resources per app. |

## KVS and Custom Entity Store limits

When using the KVS and Custom Entity Store, we strongly recommend that you:

The Atlassian Cloud backs up the entire hosted storage for disaster recovery.
This includes content stored from the Forge storage API.

### Operation limits per installation

If an installation of your app exceeds these limits due to bulk processing
(for example, triggered by a bulk issue update in Jira), consider using
the [Async events API](/platform/forge/runtime-reference/async-events-api/)
to queue your app's interactions with the KVS and Custom Entity Store. See
[Queue app interactions with storage API](/platform/forge/storage-api-limit-handling/) for guidance. While the new limits are designed to fit the majority of apps, partners with data-heavy apps can reach out to Atlassian support and ask for extended limits.

The limits listed below apply to the [Key-Value Store or Custom Entity Store](/platform/forge/runtime-reference/storage-api/)
for *each installation* of your app.

#### Current limits (deprecated)

**Important update:** Starting from **November 16, 2025**, the current Forge KVS and Custom Entity Store limits will be **deprecated** and replaced with new limits focused on data consumption. Read more about the changes and how to adapt in [our changelog](/platform/forge/changelog/#CHANGE-2538).

| Resource | Limit | Description |
| --- | --- | --- |
| Delete operations | 400 | Maximum number of delete operations per 20 seconds |
| Query operations | 200 | Maximum number of query operations per 20 seconds |
| Read operations | 1000 | Maximum number of read operations per 20 seconds |
| Update operations | 1000 | Maximum number of update operations per 20 seconds |

### Future limits

| Parameter | Limit |
| --- | --- |
| Request rate (RPS) | 1000 |
| Read (10KB request per min)\* | 4000 |
| Write (10KB request per min)\* | 4000 |

\* Request sizes are rounded up to the nearest 10KB. Requests that are 10KB or smaller are counted as 1 request. For sizes between 10KB and 20KB, they are counted as 2 requests. For example, a request with a payload of 65KB will be rounded up to 70KB, resulting in a count of 7 requests.

The new limits, compared to the current rigid per-operation limits, allow apps to distribute their usage dynamically.

### Key and object size limits

The KVS and Custom Entity Store have the following limits on keys and values.

You don't need to include any identifiers for apps or installations in your key.

Internally, Forge automatically prepends an identifier to every key, mapping it to
the right app and installation. This lets you use the full key length without risking
conflicts across apps or installations.

| Resource | Limit | Description |
| --- | --- | --- |
| Key length | 500 | Maximum length of a key |
| Key format | `/^(?!\s+$)[a-zA-Z0-9:._\s-#]+$/` | Keys must match the regex |
| Value size | 240 KiB | Maximum size of a single persisted value (in RAW) |
| Object depth | 31 | Maximum object depth permitted |
| Reads | 12 MB/s per key | Maximum reads permitted per second for keys |
| Writes | 1 MB/s per key | Maximum writes permitted per second for keys |
| Query | 24 MB/s per index value | Maximum queries permitted per second for index values |

### Transaction limits

The KVS and Custom Entity Store also let you package multiple operations into one transaction. Transactions are subject to the following limits:

| Category | Limit |
| --- | --- |
| Rate limit | Transactions are treated as a single **Write** operation, subject to the rate limits defined in [KVS and Custom Entity Store limits - Future Limits](/platform/forge/platform-quotas-and-limits/#future-limits). The transaction will fail if it exceeds these limits, returning a `TOO_MANY_REQUESTS` error. |
| Quota | The `transaction.set` operation is subject to the quota limits defined in [KVS and Custom Entity Store quotas](/platform/forge/platform-quotas-and-limits/#kvs-and-custom-entity-store-quotas). |
| Transaction operations | Each transaction can contain a maximum of 25 operations. |
| Unique keys | Each key can only be used once in a transaction. |
| Payload | Each transaction is limited to a payload size of 4MB. |

We are currently working on addressing a bug that is incorrectly limiting request payloads for Transactions and Batch operations
to 1MB instead of 4MB. See [FRGE-1916](https://ecosystem.atlassian.net/browse/FRGE-1916) for additional details.

### Custom Entity Store limits

Custom entities (used for [complex queries](/platform/forge/runtime-reference/storage-api-query-complex/)) are subject to the following additional limits:

| Category | Requirements | Limits |
| --- | --- | --- |
| Entity | Entity names:   * Must only consist of the following characters `a-z0-9:-_.` * Must follow the regex pattern `[_a-z0-9:-.]` * Cannot start with `-` or `_` * Must not begin or end with a `.` * Must not contain the sequence `..`   In addition, an app must not have duplicate entity names. | * An app can have a maximum of 20 entities * Each entity can have a maximum of 7 custom indexes and 50 attributes * Objects that can be stored as custom entities have a maximum depth of 31 and a maximum size of 240KiB (RAW) per object * Entity names cannot be shorter than 3 characters or longer than 60 characters in length |
| Attribute | Attribute names must follow the regex `[_A-Za-z][_0-9A-Za-z]*`. | Attribute names have a maximum length of 64 characters. |
| Index | Index names must contain only the following characters `a-zA-Z0-9:-_.`, and must adhere to the following requirements:   * Must not begin or end with a `.` * Must not contain the sequence `..` * Must not be empty   In addition, each index name within an entity must be unique. | * Each entity can have a maximum of 7 custom indexes * The size of combined values for all   [range](/platform/forge/runtime-reference/custom-entities/#index-types)   attributes on any defined index cannot exceed 900 bytes * The size of combined values for all   [partition](/platform/forge/runtime-reference/custom-entities/#index-types)   attributes on any defined index cannot exceed 1700 bytes * Index names cannot be shorter than 3 characters or longer than 50 characters in length. |
| Keys | A key should:   * Follow the regex pattern `/^(?!\s+$)[a-zA-Z0-9:._\s-#]+$/` * Contain at least 1 character * Not be empty * Not contain only blank space(s) | A key can contain a maximum of 500 characters. |

In addition, each [complex query](/platform/forge/runtime-reference/storage-api-query-complex/)
can only have a maximum of 100 conditions
(for example, `beginsWith`, `contains`, and `isGreaterThan`). This limit applies to conditions used in
[where](/platform/forge/runtime-reference/storage-api-query-complex/#where),
[andFilter](/platform/forge/runtime-reference/storage-api-query-complex/#andfilter---orfilter), and
[orFilter](/platform/forge/runtime-reference/storage-api-query-complex/#andfilter---orfilter) filters.

### Forge SQL limits

Forge SQL offers a multi-tenant SQL solution offering tenant isolation and stable query performance. To do so, we add a few constraints over and above TiDB's limitations:

* Foreign keys are not supported. You can still perform `JOIN` operations, but `DELETE` operations will not be cascaded.
* Each SQL statement can only contain a single query.

The following limits also apply:

### Per-install limits

The following limits are applied to your app's Forge SQL usage on a per-install basis:

| Resource | Limit |
| --- | --- |
| Total stored data | 1 GiB (`production` installs) |
| 256 MiB (`staging` installs) |
| 128 MiB (`development` or custom environment installs) |
| Number of tables | 200 |
| DML Requests per second (RPS) | 150 |
| DDL Requests per minute (RPM) | 25 |
| Size per row | 6Mib |
| Total query execution time for all current invocations | 62.5 seconds (within each minute) |

App databases provisioned and managed via Forge SQL are backed up periodically.

### Query and response limits

The following limits apply to each query sent and response received by your app's Forge SQL database functions:

| Resource | Limit |
| --- | --- |
| Memory usage per query | 16 MiB |
| Query time per minute (s/minute) | 62.5 seconds |
| Request size | 1 MiB |
| Response size | 4 MiB |
| Per-connection timeout for `SELECT` queries | 5 seconds |
| Per-connection timeout for `INSERT`, `UPDATE`, and `DELETE` queries | 10 seconds |
| Per-connection query timeoutfor [DDL queries](/platform/forge/storage-reference/sql-api-schema/#manage-your-database-schema) | 20 seconds |

### SOC2 and ISO compliance

Forge SQL has not yet undergone external assessment for SOC 2 or ISO certification. As we continue development on Forge SQL, we will aim to include it in our standard audit certification reporting cycle.

### Versioning

If you add Forge SQL to an existing app, admins of that app's current installations must review and consent before updating.

As such, adding Forge SQL to an existing app will require a [major version upgrade](/platform/forge/versions/#major-version-upgrades). This will be triggered through the `sql` module (which is required to enable Forge SQL on an app).

## Web Trigger

Rate limits on web trigger GraphQL operations

| Operation | Limit |
| --- | --- |
| Get | 1,000 requests per minute per `app, env, context` |
| Delete | 500 requests per minute, web trigger ID |
| Create | 500 requests per minute per `app, env, context` |

## Async events limits

The limits listed below apply to the [Async events API](/platform/forge/runtime-reference/async-events-api/) for each installation of your app.

| Resource | Limit | Description |
| --- | --- | --- |
| Event per request | 50 | Maximum number of events pushed in a single request. |
| Event per minute | 500 | Maximum number of events pushed in one minute. |
| Payload size | 200 KB | Maximum combined payload size of events in single request. |
| Retry data size | 4 KB | Maximum size of `retryData`.  This will be enforced from `Nov 13, 2025`. See [CHANGE-2508](/platform/forge/changelog/#CHANGE-2508) for more details. |
| Payload size for long running functions | 100 KB | Maximum size of an *individual* event.  This limit only applies to functions specifying a timeout greater than 55 seconds. |
| Retry data size for long running functions | 4 KB | Maximum size of `retryData`.  This limit only applies to functions specifying a timeout greater than 55 seconds. |
| Cyclic invocation limit | 1000 | An event resolver can push more events to the queue thus creating a cycle. This limit applies to the maximum cyclic depth up to which events resolver can push more events to the queue. |

### App limits

The limits listed below apply to an app.

| Resource | Limit | Description |
| --- | --- | --- |
| App description | 1,000 | Maximum number of characters that the app `description` can have. |
| App name | 1 to 60 | The app `name` must be between the character limits. |
| App size | 100 | Maximum app size in megabytes (MB). |
| Base URL | 2,048 | Maximum number of characters that the app `baseUrl` can have. |
| Modules per app | 100 | Maximum number of unique modules that can be declared in a single app manifest. |
| Resources per app | 10 | Maximum number of unique resources that can be declared in a single app manifest. |
| Environments per app | 25 | Maximum number of environments in a single app. |
| Alerts per app | 5 | Maximum number of alerts that can be created for a single app. |

### Developer limits

The limits listed below apply to a developer's account.

| Resource | Limit | Description |
| --- | --- | --- |
| Apps | 100 | Maximum number of apps that can be created or owned by a single developer. |

## Scheduled trigger limits

The following limits apply to the [scheduled trigger module](/platform/forge/manifest-reference/modules/scheduled-trigger/) in an app.

| Description | Limit |
| --- | --- |
| Total number of scheduled trigger modules in an app | 5 |
| Total number of scheduled trigger modules with `fiveMinute` intervals in an app | 1 |

## Apps exceeding quotas or limits

If your app exceeds any quotas or limits, you can often fix the issue yourself:

* Most app limits are enforced through Forge CLI validation, where
  you'll immediately receive an error. Most errors have trivial fixes, such as shortening
  your app's name.
* For resource-bound limit errors (such as the total number of apps), you need to
  remove the relevant resources. You can uninstall an app with the `forge uninstall` command.
  Once you remove all installations of an app, delete it from the
  [developer console](https://developer.atlassian.com/apps/).

We understand that some quotas can be hard to monitor; as such, we are working on
better monitoring tools for future releases.
Meanwhile, if we detect that your app consistently exceeds our quotas or limits, we'll
first contact you to understand why. If your app needs higher storage capacity or a higher cyclic invocation limit, you can contact
us through [Developer and Marketplace support](https://developer.atlassian.com/support).
If your app needs an increase in other quotas or limits, please let us know through the
[Forge Jira Project](https://ecosystem.atlassian.net/jira/software/c/projects/FRGE/issues/).

We aim to unblock reasonable use cases, and we will work with you to achieve this.
However, repeated or prolonged failure to address requests to comply with quotas may result in
further action being taken (such as app suspension).

## Suspended apps

An app may be temporarily suspended if it negatively impacts the Forge
platform, regardless of whether it’s in breach of any quotas or limits.

Suspended apps cannot be:

* **Invoked**: Suspended apps cannot be invoked by any existing installations. Invoking
  a suspended app will return an `App is currently unavailable, please try again later` error.
* **Installed**: Attempting to install a suspended app will return an
  `App installation is not available while the app is suspended` error.
* **Deployed**: Running `forge deploy` command on a suspended app will return an
  `App management is unavailable while the app is suspended` error.

If your app is suspended, we'll submit a ticket through
[Developer and Marketplace support](https://developer.atlassian.com/support)
and mention you, so that you can help us fix the issue as soon as possible.

If you're not a Jira user, we’ll email you a link to the issue.

If have an issue with quotas or limits but haven't been contacted by our team, you
can seek assistance from the
[Forge developer community](https://community.developer.atlassian.com/c/forge).

See the [Forge Terms](/platform/forge/developer-terms/) for more information.
