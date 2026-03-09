# Forge Realtime (Preview)

Forge Realtime is now available as Preview capability. Preview capabilities are deemed stable; however, they remain under active development and may be subject to shorter deprecation windows. Preview capabilities are suitable for early adopters in production environments.

We release preview features so partners and developers can study, test, and integrate them prior to General Availability (GA). For more details, see [Forge EAP, Preview, and GA](/platform/forge/whats-coming/#preview).

Forge Realtime allows you to send events between different instances of your Forge app. This includes instances across different browsing contexts.

For example, you can broadcast realtime events to the multiple tabs that a user has opened. Or you can broadcast realtime events across multiple users that have your app open.

Forge Realtime capabilities include:

* Sending and receiving events between instances of your Forge frontend (Custom UI and UI Kit)
* Publishing events from your Forge backend to your Forge frontend, using the @forge/realtime package
* A secure-by-default yet flexible channel permissions context

  * Realtime channel contexts meet the same authentication and confidentiality standards as Atlassian app contexts. The Forge Realtime API also allows for fine-grained control over channel context - for example, restricting channels on a per-issue or per-project basis.

## Using Forge Realtime

References and guides on Realtime capabilities:

## Use cases

Some use cases for these capabilities:

* Create real-time status indicators showing when team members are viewing, editing, or working across the same Forge app context
* Implement collaborative activity feeds that broadcast project updates and team actions across all users viewing the same workspace context.

## Changes from EAP

### New features

* Realtime is now available in Jira and Confluence.
* The [contextOverrides](/platform/forge/realtime/authorizing-realtime-channels/#using-context-overrides) option now also accepts Confluence context properties.
* Event payloads can now be JSON-serializable objects without needing to be stringified first. String payloads are still supported.
