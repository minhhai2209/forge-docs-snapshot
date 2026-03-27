# Core concepts

This page explains the ideas behind feature flags and how they work in Forge. It's background reading — you don't need to read it before getting started, but it's useful for understanding why things work the way they do.

## What are feature flags?

Feature flags (also known as feature toggles or feature switches) separate two things that are usually coupled: **deploying code** and **activating features**.

Normally, when you deploy code, it's live immediately. Feature flags break that coupling. You deploy code with the new feature wrapped in a flag check. The feature stays dormant until you flip the flag on — which you do from Developer Console, not from a deployment.

This separation has a few practical consequences:

* You can merge unfinished features into your main branch without exposing them to users
* You can activate a feature for some users before all users
* You can disable a feature immediately if something goes wrong, without a rollback

## How flag evaluation works

When your Forge app calls `checkFlag`, the SDK doesn't make a network request. Instead, it evaluates the flag against a configuration that was downloaded and cached when the SDK was initialized.

The server-side SDK (`@forge/feature-flags`) downloads configuration on initialization and polls for updates every 60 seconds. The client SDK (`@forge/bridge`) downloads configuration on initialization.

This means evaluations are fast — typically sub-millisecond — and your app stays functional even if there's a temporary connectivity issue.

## The flag lifecycle

A feature flag moves through four stages:

**1. Creation** — You define the flag in Developer Console: give it a name, a flag ID, and an ID type. The flag ID is what you use in code. It's generated from the name you provide.

**2. Configuration** — You set targeting rules: which percentage of users see the flag as enabled, and any attribute-based conditions (license tier, account ID, etc.).

**3. Evaluation** — At runtime, your app calls `checkFlag(user, flagId)`. The SDK applies the configured rules against the user object you provide and returns `true` or `false`.

**4. Cleanup** — When a flag is permanently enabled or removed, you remove the `checkFlag` call from your code and delete the flag from Developer Console. Leaving dormant flags in code creates maintenance debt.

## ID types: the scope of evaluation

The **ID type** you choose when creating a flag determines what unit of targeting the flag operates on. This is one of the most important decisions when setting up a flag.

### installContext

`installContext` targets at the app installation level — a specific Jira site or Confluence site where your app is installed.

Use `installContext` when the feature decision is about an organization, not a person. For example: "Enable the advanced reporting dashboard for Acme Corp." All users within that installation see the same result.

### accountId

`accountId` targets at the individual user level using Atlassian account IDs.

Use `accountId` when the feature decision is about a specific person. For example: "Enable the beta UI for these 50 named users." Different users within the same installation can see different results.

### Choosing between them

The practical question is: should the feature decision be the same for everyone in an organization, or can it differ per person?

* Rolling out to a percentage of **sites**? Use `installContext`
* Rolling out to a percentage of **users** within a site? Use `accountId`
* Enabling a feature for a specific **customer**? Use `installContext`
* Enabling a feature for a specific **person** (admin, beta tester)? Use `accountId`

See [Target specific users or organizations](/platform/forge/feature-flags/how-to-target-users) for implementation examples.

## Attributes

Attributes let you apply rules based on properties of the app context, beyond just who the user is. For example: "Enable this feature only for apps on an ACTIVE license."

Predefined attributes include `installContext`, `accountId`, `appVersion`, `license`, and `capabilitySet`. You can also define custom attributes for any numeric or string property you expose in your user object.

Attribute values are set in your code when you construct the user object. Rules against those values are configured in Developer Console. See the [server-side SDK reference](/platform/forge/feature-flags/feature-flags-sdk) for the full user object interface.

## Flags and environments

Each flag is configured independently per environment: development, staging, and production. A flag enabled at 100% in development doesn't affect staging or production.

In your code, you pass the environment by reading `environmentType` from the Forge context:

```
```
1
2
```



```
const { environmentType } = context;
await featureFlags.initialize({
  environment: environmentType?.toLowerCase() || "development"
});
```
```

This means the same code automatically evaluates the flag differently based on where your app is running.

## What feature flags are not

Feature flags in Forge are boolean — a flag is either enabled or disabled for a given user. They don't support multi-variate flags (returning A, B, or C) or numeric values.

They are also not a configuration system. If you need to pass arbitrary data to your app at runtime, feature flags are not the right tool.

## Further reading
