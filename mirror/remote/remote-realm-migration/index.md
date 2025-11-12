# Support data residency realm migrations for Forge Remote

The realm `migration` module is for Forge apps using remotes that need to align with the customer's Atlassian app region. While Forge automatically manages hosting, pinning, and migration for apps using Forge-hosted storage solutions like [Key-Value Store](/platform/forge/runtime-reference/storage-api-basic/) and [Custom Entity Store](/platform/forge/storage-reference/storage-api-custom-entities/), apps with remotes must actively manage data location through realm pinning and migration.

Customers may request a migration if a Forge app was originally installed in a global location due to missing region-specific `baseUrl` settings or if the Forge app did not support the host Atlassian app's region.

Even if a Forge app supported a region-specific `baseUrl` at installation, customers might later move their Atlassian app to a different region to meet data residency requirements. In these cases, they can request a Forge app data migration through the customer-facing UI.

To support migrations for Forge Remote, apps must implement the data residency migration hook in the `modules` field of the manifest and handle the required lifecycle hooks to complete the migration process.

A migration module can be specified as follows:

```
1
2
3
4
5
6
modules:
  migration:dataResidency:
    key: dare
    remote: remote-backend
    path: /migration
    maxMigrationDurationHours: 6
```

This makes your Forge app eligible to receive the following compulsory hooks:

* `/schedule`
* `/start`
* `/status`
* `/commit`
* `/rollback`

The related hook URL is appended to the remote and path defined in your migration module within the manifest. For example, if your module specifies `/migration`, the hook URL will follow this structure: `{remote}/migration/schedule`.

These lifecycles don't come from the Atlassian app. Instead, they come from a different service. This is to facilitate the migration process while the Atlassian app is down.

The service will continue to communicate with apps by including a Forge Invocation Token (FIT) as a bearer token in the authorization header. The FIT contains key details about the invocation context and should be used to [verify that the request originates from Atlassian](/platform/forge/remote/essentials/#verifying-remote-requests) and is intended for your Forge app.

## Data residency migrations hooks

### POST `/schedule`

When an Atlassian app admin schedules a migration, the service will notify eligible apps via this endpoint to schedule a migration. Use this to do any preparatory work prior to the migration.

**Request payload**

```
```
1
2
```



```
{
“startTime”: “2021-12-26T00:00:00.000Z”, 
“endTime”: “2021-12-27T00:00:00.000Z”, 
“location”: “EU”,
“migrationId”: 57500
}
```
```

**Response**

If your Forge app returns a non-2xx response without an [errorResponseCode](#error-codes), we will [retry up to two times](#retries). If these attempts are unsuccessful, the app migration is marked as a failure, and a rollback hook will be dispatched. The app will then continue to communicate with the original region.

### POST `/start`

Once the site is taken offline, the service will notify eligible apps that have successfully responded to the schedule hook via this endpoint to begin the migration.

**Request payload**

```
```
1
2
```



```
{
 “startTime”: “2021-12-26T00:00:00.000Z”,
 “endTime”: “2021-12-27T00:00:00.000Z”,
 “location”: “EU”,
 “migrationId”: 57500
}
```
```

**Response**

If your Forge app returns a non-2xx response without an [errorResponseCode](#error-codes), we will [retry up to two times](#retries). If these attempts are unsuccessful, the Forge app migration is marked as a failure, and a rollback hook will be dispatched. The Forge app will then continue to communicate with the original region.

### GET `/status`

This endpoint will be called by the service to fetch the status of an ongoing migration. The request can include `migrationId` as a query parameter:

```
```
1
2
```



```
GET /status?migrationId=57500
```
```

This endpoint should not expect a payload in the request.

The statuses the service will specifically be looking for are:

For `failed`, there will be a series of `errorResponseCodes` you may wish to report back with to provide more insight into the failure reason. This is described further under the Error Codes heading.

A `ready-to-commit` will mean that the Forge app has finished its migration and is awaiting a `/commit` lifecycle upon completion.

Beyond that, you can use any statuses you wish. However, upon completion, any status that isn't `ready-to-commit` will receive a rollback hook.

Once the migration starts, we'll also be regularly polling the apps for their status. If all apps have either `failed` or are `ready-to-commit`, then the migration can end, and the site can be brought back online.

**Response**

Failed status - service will update the Forge app migration's status to failed:

```
```
1
2
```



```
{
“status”: “failed”,
“errorResponseCode”: “E0004”
}
```
```

App is awaiting a `/commit` hook. The service, once the migration ends, will send a `/commit`hook:

```
```
1
2
```



```
{
“status”: “ready-to-commit”
}
```
```

### POST `/commit`

Once the site is brought back online, the service will query the status of each Forge app that has started the migration.

The service will ask apps to commit via this endpoint if they’ve reported that they're `ready-to-commit`.

Specifically, this is to commit the copied data to the new region.

**Request payload**

```
```
1
2
```



```
{
“migrationId”: 57500
}
```
```

**Response**

If your Forge app returns a non-2xx response without an [errorResponseCode](#error-codes), we will [retry up to two times](#retries). If these attempts are unsuccessful, the Forge app migration is marked as a failure, and a rollback hook will be dispatched. The Forge app will then continue to communicate with the original region.

### POST `/rollback`

There are various use cases for this endpoint:

1. Migration cancelled by the user via the UI
2. No report of `ready-to-commit` by the Forge app. Once the site is brought back online, the service will query the status of each Forge app which has started the migration.

The service will ask apps to roll back via this endpoint if they’ve reported that they aren't `ready-to-commit`.

Specifically, this is intended to roll back the non-destructive copy operation to the new region.

**Request payload**

```
```
1
2
```



```
{
“migrationId”: 57500
}
```
```

**Response**

Not applicable.

## Retries

The migration hooks use a retry mechanism to handle transient errors and increase the chances of a successful migration. The hooks are retried up to 2 times after the initial call. The exemption is the `status` hook which is dispatched every 5 minutes.

A retry is triggered when the Forge app responds with a non-2xx code and no `errorResponseCode`. If an `errorResponseCode` is received, it signals a failure, stopping further retries.

There is a 5 second pause between retries.

## Error codes

To help diagnose problems with migrations, we have a set of standardized error codes that your Forge app can report back to us with when you're reporting back with a non-2xx to the hooks or the status retrieval.

Any non-2xx response to any of the lifecycle events can optionally include any of the below error codes in its response to assist the user in understanding why the migration may have failed.

```
```
1
2
```



```
{
 “errorResponseCode”: “E0004”
}
```
```

| Error code | Reason |
| --- | --- |
| `E0001` | The migration was not scheduled. |
| `E0002` | The Forge app does not support the target region (versioning issues). |
| `E0003` | The Forge app does not support migrations (versioning issues). |
| `E0004` | The Forge app has too many concurrent migrations. |
| `E9999` | Generic failure code. |

## Considerations

When deciding whether to support data residency migrations for your Forge app, keep the following in mind:

* Migrations occur during site downtime – Forge apps will be migrated while the site is temporarily unavailable.
* Migrations apply at the Atlassian app level – Customers cannot migrate individual apps; all eligible Forge apps move together with the Atlassian app.
* 24-hour migration window – Eligible apps must complete their data migration within 24 hours.
* Eligibility is determined at scheduling – A Forge app's ability to migrate is assessed when the migration is scheduled.
* Eligible to move with the Atlassian app, without requiring three-day lead time - Forge apps that do not declare a `maxMigrationDuration` or is set to 90 minutes or less may be eligible to move immediately alongside the Atlassian app.

## Lifecycle of a Forge Remote data residency migration

1. The Atlassian app admin will schedule a migration of eligible apps via AdminHub.
2. Our service will notify eligible apps via the `/schedule` endpoint.
3. The site will be unavailable at the scheduled time.
4. Our service will notify apps that successfully responded to the `/schedule` endpoint to begin the migration via the `/start` endpoint.
5. The site will be brought live at the specified end time or once all app migrations are complete.
   * If the migration window is over, our service will query the apps that successfully started the migration for their status via `/status`.`
     * If the status is `ready-to-commit`, our service will send a `/commit` hook.
     * If the status is anything else, our service will send a `/rollback` hook.
   * If all app migrations have completed (i.e. responded `failed` or `ready-to-commit` when polled or reported back early):
     * If the status is `ready-to-commit`, our service will send a `/commit` hook.
     * If the status is anything else, our service will send a `/rollback` hook.
6. Forge will then update the installed region of the apps that have finished the migration process in the specified window.

## Declaring maximum downtime

Planning a migration downtime is challenging for enterprise customers, therefore a shorter app migration window encourages customers to migrate their apps. The app descriptor supports a `maxMigrationDurationHours` property, allowing partners to specify the maximum migration window. If this property is not declared, the maximum migration window will default to 1.5 hours. Apps that complete migration in 90 minutes or less will move immediately alongside the Atlassian app, without requiring a three-day lead time.

* Shorten to optimize the customer experience. Partners are encouraged to use the shortest possible migration duration they are able to support
* Extend for up to 24 hours if a longer migration duration if required
* Restrictions:
  * Max: `24`
  * Min: `0.5`
  * Increments of `0.5` only. i.e. `1`, `1.5`, `2` (`0.7` for example would be invalid)

```
```
1
2
```



```
  ...
  maxMigrationDurationHours: 0.5
  ...
```
```

If a Forge app fails to migrate within the specified `maxMigrationDuration` window, the `/rollback` hook will be sent.

## Realm persistence in Forge

Realm persistence is a default capability that ensures apps retain their previously assigned region when reinstalled within 30 days following uninstallation. This helps ensure consistency in data residency, preventing apps from being reassigned to a different region upon reinstallation, provided the reinstallation occurs with the 30 day window.

If a customer uninstalls and later reinstalls an app within 30 days, their remote traffic will be redirected back to existing regions. If their reinstallation occurs after 30 days, the remote region will be determined based upon the current Atlassian app region which may differ from the originally assigned region.
