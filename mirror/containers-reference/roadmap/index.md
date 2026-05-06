# Forge Containers roadmap (EAP)

Forge Containers are now available through Forge's Early Access Program (EAP). To start testing this feature,
submit your app's ID to our team [through this link](https://ecosystem.atlassian.net/servicedesk/customer/portal/1040/create/18884).

EAPs are offered to selected users for testing and feedback purposes. APIs and features under EAP
are unsupported and subject to change without notice. APIs and features under EAP are not recommended
for use in production environments.

For more details, see [Forge EAP, Preview, and GA](/platform/forge/whats-coming/#eap).

The current EAP release has a deliberately reduced scope and limited functionality. Its purpose is to create a usable containers environment where we can incrementally deliver new functionality and get your immediate feedback.

This release may not currently satisfy all your requirements. Going forward, we will be working with you to collect your feedback and evolve Forge Containers to meet your needs.

With this release, you can test and assess how to deploy a containerised service in Forge Containers. Service scaling, routing, deployment, and configuration options will be limited in this release, but we will be improving this over time.

Currently, Forge Containers has the following limitations:

## Region limitations

Pin your test site's location to **Germany** to avoid significant latency.

Forge Containers is currently deployed in `Germany` only. If your test tenant is provisioned in a different region, you may experience up to **100ms+ latency increases** when using [Forge storage APIs](/platform/forge/storage-reference/)
and [Atlassian app APIs](/platform/forge/apis-reference/product-rest-api-reference/). In some cases, this latency can also impact connection pool limits and query timeouts.

To avoid these issues, we strongly recommend that you pin your test site's data location to **Germany**.

Multi-region support for Forge Containers will be addressed in a future release.

## Integration limitations

* Forge Containers have not yet been fully tested against every single Forge module that supports an `endpoint` module as its implementation. Some rough edges may exist.
* Documentation for reading/writing from Forge Object Store (EAP) is not yet available.
* Apps can't process an async event within a container and provide a result back to the queue (async events processed by a container currently use a 'fire and forget' mechanism, and can't retry or assess success/failure of the event processing).
* Containers can't call the REST APIs of Bitbucket Cloud and Compass.

## Deployment limitations

* You can only build and run Forge Container services on Forge's `development` and custom [environments](https://developer.atlassian.com/platform/forge/environments-and-versions/#environments).
* An app can only have *one* containerised service, which can only have *one* defined container.
* To deploy a change to a container image, you'll need to run `forge deploy`.

## Lifecycle limitations

* Service instances are not automatically recycled. Therefore, while Forge Containers is under active development, you may be periodically required to re-deploy your container services (using `forge deploy`) to pick up breaking changes to platform components. This will be communicated via Slack and Confluence blogs when required.
* Service instances cannot be deleted. As such, deploying your app after editing your `services.key` in the manifest will fail, as apps are limited to only one containerised service during EAP.

## Resource and scaling limitations

* An app's service can only have *one* instance, and cannot scale.
* A service can have a maximum of 1000m CPU and 2048 Mi of memory allocated.

## Observability limitations

CPU and memory usage tracking in the Developer Console are not yet available.

## Pricing

Forge Containers are free to use during EAP. Pricing will apply from the point at which Forge Containers enters [Preview](/platform/forge/whats-coming/#forge-early-access-program--eap-).

Unlike other Forge capabilities that use a [consumption-based pricing model](/platform/forge/forge-platform-pricing/), Forge Containers use a **reservation-based pricing model**. You pay for the CPU and memory capacity reserved for each container instance, regardless of whether that instance is actively handling requests. This reflects the always-on nature of container services, which must remain running to serve traffic at any time.

See [Forge Containers pricing](/platform/forge/containers-reference/pricing/) for unit prices, cost examples, and optimization options.
