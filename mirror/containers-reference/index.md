# Forge Container services overview (Preview)

Forge Container services is now in Preview, and therefore fully supported. However, it remains under active development and may be subject to shorter deprecation windows. Preview features are suitable for early adopters in production environments.

We release preview features so partners and developers can study, test, and integrate them prior to General Availability (GA). For more details, see [Forge EAP, Preview, and GA](/platform/forge/whats-coming/#forge-preview).

Forge Container services are a set of tools and capabilities for managing containerised services for Forge apps. You can use Forge Container services to package a service’s code and dependencies, opening up a wider range of programming languages and frameworks.

With Forge Container services, you can run services from container images directly on Forge infrastructure. You can update, launch, scale, and otherwise manage the lifecycle of these services using Forge Container tools. In addition, hosted container services unblock important use cases like long-running compute, which were previously not possible with [Forge functions](/platform/forge/function-reference/).

## Implementation

Functions, events, UI elements, and triggers from your app can invoke endpoints exposed by your containerised service. Conversely, you can build containerised services that invoke Atlassian product APIs or any Forge capability (for example, hosted storage).

This implementation is similar to how Forge apps can integrate with your remote services via [Forge Remote](/platform/forge/remote/#forge-remote). The key difference is that Forge Container services let you host services directly on Atlassian-hosted compute. This lets you build microservice-based apps that can also leverage platform features like [data residency](/platform/forge/data-residency/#data-residency) and the [Runs on Atlassian](/platform/forge/runs-on-atlassian/) badge.

### Deployments

Forge Container services uses a *canary deployment strategy* to validate each deployment before it takes effect.

During deployment, Forge runs a series of health checks before rolling the update out to provisioned instances. If the health checks fail, the deployment is rolled back.

Container service instances are provisioned based on app installations: when your app is installed on a site, the infrastructure is provisioned for that site's region. On the first deployment with no existing installations, the canary validation still runs but no persistent service instances are provisioned — the canary is cleaned up automatically. See [Managing containerised services](/platform/forge/containers-reference/managing-service/) for more details on provisioning.

During the canary validation phase, the new container version may run alongside existing instances. For this reason, your app's startup logic should be *defensive* — avoid performing destructive operations (such as schema migrations or cache invalidation) on startup, as the deployment may be rolled back if health checks fail.

The patch version of your app will be incremented automatically during the first installation (either via new installation or existing upgrade) for a new major version in a region. This is an internal versioning mechanism and does not affect your app's major or minor version.

### Security

Forge Container services follows the Kubernetes *Restricted* policy for security standards.
This ensures a more secure approach to running service and container instances.

For more details about this standard, refer to the [Kubernetes documentation](https://kubernetes.io/docs/concepts/security/pod-security-standards/#restricted).

In addition to this standard, Forge Container services deploys all container instances with restricted file system permissions.
Each instance mounts a *read-only* root file system, except for the following directories (which remain writeable):

Images used by your apps are subject to our [image security guidelines](/platform/forge/containers-reference/ref-image-security/). These guidelines describe the hardening, egress, and tenant-isolation requirements that apply during Marketplace approval.

## Constraints

Forge Container services aims to enable use cases that wouldn't be possible otherwise without container support. However, our goal is not to provide a general-purpose container management platform. As such, Forge Container services is subject to the following constraints:

* **Forge Container services is *stateless*.** This allows us to focus on scalability, rapid deployment, and cost efficiency. Container services are not designed to support persistent storage and should never be used for that purpose. If your app has persistent storage needs, use Forge's available [hosted storage capabilities](/platform/forge/storage-reference/).
* **Each container is tied to one app.** Every service hosted by Forge Container services must be owned by only one app. Each service and its containers can only be configured in a Forge app’s manifest.
* **Containers are effectively headless.** Containers hosted and launched via Forge Container services cannot be accessed via SSH or other forms of remote login.
* **Containers are deployed and run independent of app version.**
  Running container instances are shared across all app versions. If you have multiple installations of your app with different major versions, only a *single* container service is run. Your code may need to defensively handle situations where an installation does not have grants for scopes added in newer major versions. To access additional details of a single installation, see [Query a single installation](/platform/forge/containers-reference/int-installbased/#query-a-single-installation).
* **Access to Forge hosted services is only via REST API.** Containers won’t support `@forge/*` SDK packages (such as `@forge/api`, `@forge/kvs`, and `@forge/sql`).
* **Tags are immutable.**
  Image tags like `latest` won't work; we recommend using environment variables on your tagging scheme.
* **Runtime commands cannot be executed by *root*.**
  The Forge Container services [security](/platform/forge/containers-reference/#security) standard only allows *non-root* users with a UID and GID of `1000`
  to execute container runtime commands.
* **Service deployments are tied to app deployments.** Containerised services can only be launched and recycled as part of `forge deploy`. This means you won't be able to stop a containerised service manually.
* **Forge CLI won't scan images**. Specifically, the `forge lint` or `forge deploy` commands won't scan images for any problems or validation errors.
* **Adding a container service triggers a major version upgrade.** When you add a `services` definition to an existing app's manifest for the first time, the next deployment creates a new major version of your app.
* **Service deletion and renaming are not self-service.** You cannot delete or rename a container service through the CLI or developer console. To delete or rename a service, [open a support ticket](https://support.atlassian.com/).
* **Service name length is limited.** Your service `key` is limited to 19 characters due to infrastructure constraints. Choose concise service key names to avoid deployment failures.
* **Service definition changes require the latest major version.** Changes to the provisioned service definition (such as resource allocation or scaling configuration) can only be made via deployments to the latest major version of your app. Attempts to deploy changes to the service definition in an older major version will block the deployment.

## Preview limitations

Forge Container services is now in [Preview](/platform/forge/whats-coming/#forge-preview). Preview features are fully supported but remain under active development and may be subject to shorter deprecation windows.

See [Forge Container services roadmap](https://ecosystem.atlassian.net/browse/ROADMAP-228) for more details about current limitations and our plans to address them in upcoming milestones.

## Observability

Forge Container services provides built-in observability features to help you monitor the health and performance of your containerised services:

* **[Service Health metrics](/platform/forge/monitor-service-health/)**: View real-time CPU usage, memory usage, service availability, and instance counts in the developer console.
* **[Invocation metrics](/platform/forge/monitor-invocation-metrics/)**: Monitor container invocation response times.
* **[Logs](/platform/forge/monitor-app-logs/)**: View logs for your container services.
* **[Export metrics](/platform/forge/export-app-metrics/)**: Export container metrics to third-party observability tools using the App metrics API.

## Learning resources

**GLOSSARY**

The implementation of Forge Container services varies slightly from how traditional containerised services work. Refer to the following
[Glossary](/platform/forge/containers-reference/ref-glossary/) to understand how specific terms are used in Forge Container services.
