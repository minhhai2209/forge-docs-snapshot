# In-scope End-User Data

In-scope End-User Data (EUD) refers to data that must comply with
[data residency](/platform/forge/data-residency/) requirements. As a Forge developer, you are
responsible for defining, documenting, and communicating with your customers what data is in-scope
and out-of-scope for data residency for your app.

The `inScopeEUD` property in your app's `manifest.yml` file declares whether your app egresses
in-scope End-User Data through its external permissions. This property affects your app's:

## The `inScopeEUD` property

The `inScopeEUD` property is a boolean that you can set on
[egress permissions](/platform/forge/manifest-reference/permissions/#egress-permissions) and
[remotes](/platform/forge/manifest-reference/remotes/#data-residency) in your app's manifest file.

* **`inScopeEUD: true`** — The app egresses in-scope End-User Data to the specified address.
* **`inScopeEUD: false`** — The app does not egress in-scope End-User Data to the specified address.

If `inScopeEUD` is not specified, it defaults to `true`.

### Example

```
1
2
3
4
5
6
7
permissions:
  external:
    fetch:
      backend:
        - address: '*.example-analytics.com'
          category: analytics
          inScopeEUD: false
```

## Impact on data residency

Setting `inScopeEUD` determines whether your app can achieve `PINNED` status for
[data residency](/platform/forge/data-residency/#eligibility):

* If `inScopeEUD` is set to `true` on any egress permission, your app must use
  [Forge Remote data residency](/platform/forge/manifest-reference/remotes/#data-residency) with
  region-specific URLs to maintain eligibility for `PINNED` status.
* If `inScopeEUD` is set to `false` on all egress permissions, your app can be eligible for
  `PINNED` status without additional remote configuration.

For more information, see [Data residency eligibility](/platform/forge/data-residency/#eligibility).

## Impact on Runs on Atlassian

If `inScopeEUD` is set to `true` on any egress permission, the app is ineligible for the
[Runs on Atlassian](/platform/forge/runs-on-atlassian/) badge. To be eligible, your app must not
egress in-scope End-User Data. For more information, see
[Runs on Atlassian eligibility requirements](/platform/forge/runs-on-atlassian/#eligibility-requirements).

## Impact on app versioning

Changes to the `inScopeEUD` property can trigger either a major or minor
[version upgrade](/platform/forge/versions/) for your app:

* **Major version upgrade** — Changing `inScopeEUD` from `false` to `true` for the first time
  (that is, when no existing egress permission already has `inScopeEUD` set to `true`).
* **Minor version upgrade** — Changing `inScopeEUD` from `false` to `true` when another egress
  permission already has `inScopeEUD` set to `true`.

The following examples illustrate these scenarios.

### Example 1: Major version upgrade

This example shows a change to the `inScopeEUD` value from `false` to `true`.
This change leads to a major version upgrade.

```
```
1
2
```



```
permissions:
  external:
    fetch:
      backend:
        - address: '*.example-dev.com'
          category: analytics
          inScopeEUD: true # inScopeEUD value was previously false
```
```

### Example 2: Major version upgrade

This example shows a change to one of the `inScopeEUD` values, from `false` to `true`, where in the
previous version of the app, all `inScopeEUD` values were `false`. This change leads to a
major version upgrade.

```
```
1
2
```



```
permissions:
  external:
    fetch:
      backend:
        - address: '*.example-dev.com'
          category: analytics
          inScopeEUD: true # inScopeEUD value was previously false, with all values previously false
        - address: '*.example-prod.com'
          category: analytics
          inScopeEUD: false # no change in value
```
```

### Example 3: Minor version upgrade

This example shows a change to one of the `inScopeEUD` values, from `false` to `true`, where in the
previous version of the app, there is already an existing `inScopeEUD` value that's set to `true`.
Because the previous version is already egressing in-scope End-User Data, this change only leads
to a minor version upgrade.

```
```
1
2
```



```
permissions:
  external:
    fetch:
      backend:
        - address: '*.example-dev.com'
          category: analytics
          inScopeEUD: true # no change in value
        - address: '*.example-prod.com'
          category: analytics
          inScopeEUD: true # inScopeEUD value was previously false
```
```

## Defining in-scope data for your app

You are responsible for defining what data your app considers in-scope and out-of-scope for data
residency. You must publish this information in your own documentation so that admins can
understand your app's suitability and compliance with relevant data residency regulations.

You can also leverage the Atlassian Marketplace to advertise your app's support for data residency.
For more information, see
[Marketplace listing](/platform/forge/data-residency/#marketplace-listing).

## Related pages

* [Egress permissions](/platform/forge/manifest-reference/permissions/#egress-permissions)
  — Configure the `inScopeEUD` property in your manifest file
* [Data residency](/platform/forge/data-residency/)
  — Learn how data residency works for Forge apps
* [Runs on Atlassian](/platform/forge/runs-on-atlassian/)
  — Understand eligibility requirements for the Runs on Atlassian badge
* [Remotes](/platform/forge/manifest-reference/remotes/#data-residency)
  — Configure remote data residency with `inScopeEUD`
* [App versions](/platform/forge/versions/)
  — Understand how manifest changes affect app versioning
