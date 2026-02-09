# Forge Containers overview (EAP)

Forge Containers are now available through Forge's Early Access Program (EAP). To start testing this feature,
submit your app's ID to our team [through this link](https://ecosystem.atlassian.net/servicedesk/customer/portal/1040/create/18884).

EAPs are offered to selected users for testing and feedback purposes. APIs and features under EAP
are unsupported and subject to change without notice. APIs and features under EAP are not recommended
for use in production environments.

For more details, see [Forge EAP, Preview, and GA](/platform/forge/whats-coming/#eap).

Forge Containers are a [set of tools and capabilities](/platform/forge/containers-reference/) for managing containerised services for Forge apps. You can use Forge Containers to package a service’s code and dependencies, opening up a wider range of programming languages and frameworks.

With Forge Containers, you can run services from container images directly on Forge infrastructure. You can update, launch, scale, and otherwise manage the lifecycle of these services using Forge Container tools. In addition, hosted container services unblock important use cases like long-running compute, which were previously not possible with [Forge functions](/platform/forge/function-reference/).

## Implementation

Functions, events, UI elements, and triggers from your app can invoke endpoints exposed by your containerised service. Conversely, you can build containerised services that invoke Atlassian product APIs or any Forge capability (for example, hosted storage).

This implementation is similar to how Forge apps can integrate with your remote services via [Forge Remote](/platform/forge/remote/#forge-remote). The key difference is that Forge Containers let you host services directly on Atlassian-hosted compute. This lets you build microservice-based apps that can also leverage platform features like [data residency](/platform/forge/data-residency/#data-residency) and the [Runs on Atlassian](/platform/forge/runs-on-atlassian/) badge.

### Deployments

Forge Containers use a *blue/green deployment strategy* between stable and canary versions to help ensure zero downtime.

### Security

Forge Containers follow the Kubernetes *Restricted* policy for security standards.
This ensures a more secure approach to running service and container instances.

For more details about this standard, refer to the [Kubernetes documentation](https://kubernetes.io/docs/concepts/security/pod-security-standards/#restricted).

In addition to this standard, Forge Containers will deploy all container instances with restricted file system permissions.
Each instance will mount a *read-only* root file system, except for the following directories (which will continue to be writeable):

## Constraints

Forge Containers aims to enable use cases that wouldn't be possible otherwise without container support. However, our goal is not to provide a general-purpose container management platform. As such, Forge Containers will be implemented with the following constraints:

* **Forge Containers will be *stateless*.** This allows us to focus on scalability, rapid deployment, and cost efficiency. For your persistent storage needs, we recommend you use Forge’s available [hosted storage capabilities](/platform/forge/runtime-reference/storage-api/).
* **Each container is tied to one app.** Every service hosted by Forge Containers must be owned by only one app. Each service and its containers can only be configured in a Forge app’s manifest.
* **Containers are effectively headless.** Containers hosted and launched via Forge Containers cannot be accessed via SSH or other forms of remote login.
* **Containers are deployed and run independent of app version.**
  Running container instances are shared across all app versions. If you have multiple installations of your app with different major versions, only a *single* container service is run. Your code may need to defensively handle situations where an installation does not have grants for scopes added in newer major versions.
* **Access to Forge hosted services will only be via REST API.** Containers won’t support `@forge/*` SDK packages (such as `@forge/api`, `@forge/kvs`, and `@forge/sql`).
* **Tags are immutable.**
  Image tags like `latest` won't work; we recommend using environment variables on your tagging scheme.
* **Runtime commands cannot be executed by *root*.**
  The Forge Containers [security](/platform/forge/containers-reference/#security) standard only allows *non-root* users with a UID and GID of `1000`
  to execute container runtime commands.
* **Service deployments are tied to app deployments.** Containerised services can only be launched and recycled as part of `forge deploy`. This means you won't be able to stop a containerised service manually.
* **Forge CLI won't scan images**. Specifically, the `forge lint` or `forge deploy` commands won't scan images for any problems or validation errors.

## EAP limitations

Forge Containers is provided as part of the [Forge Early Access Program (EAP)](/platform/forge/whats-coming/#forge-early-access-program--eap-). This means you can use Forge Containers to build containerised services for your apps on non-production environments.

Specifically, with this release, you can only build and run Forge Container services on Forge’s `development` and custom [environments](/platform/forge/environments-and-versions/#environments).

See [Forge Containers roadmap](/platform/forge/containers-reference/roadmap) for more details about current limitations and our plans to address them in upcoming milestones.

## Learning resources

**GLOSSARY**

The implementation of Forge Containers varies slightly from how traditional containerised services work. Refer to the following
[Glossary](/platform/forge/containers-reference/ref-glossary/) to understand how specific terms are used in Forge Containers.
