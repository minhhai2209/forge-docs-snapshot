# Billing models

Forge apps support two billing models for licensing on the Atlassian Marketplace:

* **Standard billing** — customers pay for all users in their Atlassian app instance, regardless of how many actually use the app.
* **User-based billing** — customers pay only for the users granted access to the app. Admins control who has access, so organizations are billed for a targeted subset of users rather than the entire instance.

You must choose one billing model per app. Both models cannot be active for the same app at the same time.

The following sections illustrate the key differences between the two billing models.

## Standard billing (all users)

With the standard billing model, customers pay for all users in their Atlassian app instance,
regardless of how many users actually use the Marketplace app.

### Example

An organization has a Jira instance with 500 users. An org admin installs an app that charges $2 per user per month under the standard billing model. The organization pays for all 500
users ($1,000/month), even if only 50 people actively use the app.

To enable standard billing, set `licensing.enabled` to `true` in your
[app manifest](/platform/forge/manifest-reference/#app):

```
1
2
3
4
app:
  id: ari:cloud:ecosystem::app/your-app-id
  licensing:
    enabled: true
```

## User-based billing (EAP)

User-based billing is currently available as an Early Access Program (EAP), allowing app developers
to build, deploy and test an app via Forge CLI on non-production environments.

Future EAP updates for user-based billing will enable app publishing, pricing setup,
app revision, and app approval to be available on Atlassian Marketplace.

With user-based billing, customers pay only for the users who are granted access to the app.
Admins control which users have access, and the organization is billed only for those users.

### Example

An organization has a Jira instance with 500 users. An org admin installs an app that charges $3 per user per month under the user-based billing model. The admin grants only 50 users access to the app. The organization pays for those 50 users ($150/month) instead of all 500.

To enable user-based billing, set both `licensing.enabled` and `access.userAccess` to `true` in your
[app manifest](/platform/forge/manifest-reference/#app):

```
```
1
2
```



```
app:
  id: ari:cloud:ecosystem::app/your-app-id
  licensing:
    enabled: true
  access:
    userAccess: true
```
```

For implementation details, see [User-based billing (EAP)](/platform/forge/adopt-user-based-billing/).

## Next steps
