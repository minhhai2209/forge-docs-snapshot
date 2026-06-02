# Container image security guidelines (EAP)

Forge Containers are now available through Forge's Early Access Program (EAP). To start testing this feature,
submit your app's ID to our team [through this link](https://ecosystem.atlassian.net/servicedesk/customer/portal/1040/create/18884).

EAPs are offered to selected users for testing and feedback purposes. APIs and features under EAP
are unsupported and subject to change without notice. APIs and features under EAP are not recommended
for use in production environments.

For more details, see [Forge EAP, Preview, and GA](/platform/forge/whats-coming/#eap).

This page sets out the mandatory security **requirements** and strongly recommended **recommendations** for building container images used by your app. Following these guidelines ensures your app is hardened against infrastructure attacks, maintains [strict tenant isolation](/platform/forge/tenant-data-isolation/), and meets the transparency standards required for Marketplace approval.

During the [Marketplace approval process](/platform/marketplace/app-approval-guidelines/), we also review the images used by your app for compliance with these guidelines.

## Summary

These guidelines complement the platform-level controls described in [Forge Containers overview: Security](/platform/forge/containers-reference/#security). They map to controls in the [NIST SP 800-190 Container Security Guide](https://nvlpubs.nist.gov/nistpubs/specialpublications/nist.sp.800-190.pdf).

| Requirement | Summary | NIST SP 800-190 reference |
| --- | --- | --- |
| [Privilege level](#privilege-level) | Run as non-root (`UID 1000`, `GID 1000`). | 4.4.4 (App vulnerabilities) |
| [Maintenance](#maintenance) | Rebuild images at least every 180 days. | 4.2.2 (Stale images in registries) |
| [Data privacy and tenant scoping](#data-privacy-and-tenant-scoping) | Scope requests per installation; remain stateless. | 3.5.1 (Data privacy/integrity) |
| [Data egress](#data-egress) | Route outbound traffic via `FORGE_EGRESS_PROXY_URL`; listen only on `SERVER_PORT`. | 3.4.2 and 4.4.2 (Unbounded network access from containers) |
| [Secret management](#secret-management) | No hardcoded credentials; inject secrets as encrypted environment variables or via the Forge KVS secret store. | 3.1.4 (Embedded clear text secrets); 4.1.4 (Dynamic injection) |

| Recommendation | Summary | NIST SP 800-190 reference |
| --- | --- | --- |
| [Base image](#base-image) | Use distroless or minimal base images. | 3.1.1 (Image vulnerabilities) |
| [Dependencies](#dependencies) | Use multi-stage builds; strip shells and build tools. | 2.3.1 (Image creation, testing, and accreditation) |

## Requirements

This section lists *mandatory* requirements for images.
If non-compliant images are pushed to the Forge Container registry and used by your app, vulnerabilities will be assigned in accordance with the [Marketplace Security Bugfix policy](https://developer.atlassian.com/platform/marketplace/security-bugfix-policy).

### Privilege level

**Non-root execution.** Running containers with elevated privileges is a primary vector for host-to-container escapes.

* Processes must run as a non-privileged user with `UID 1000` and `GID 1000`. Root-owned processes will fail to deploy.

For more details, see [Managing a service](/platform/forge/containers-reference/managing-service/).

*NIST SP 800-190 reference: 4.4.4 (App vulnerabilities).*

### Maintenance

**Lifecycle rule.** Stale container images pose a significant security risk because they contain outdated libraries and OS packages with known vulnerabilities (CVEs) that have been discovered since the image was last built.

* Images built more than **180 days ago** are considered stale and will be blocked from production deployment.

*NIST SP 800-190 reference: 4.2.2 (Stale images in registries).*

### Data privacy and tenant scoping

**Strict tenant isolation.** App developers must ensure that customer data is handled with care, and in accordance with the [Forge shared responsibility model](/platform/forge/shared-responsibility-model). Detailed best practices are available on our [Data privacy guidelines for developers](https://developer.atlassian.com/platform/marketplace/data-privacy-guidelines). In particular, apps utilising Forge containers should observe tenant isolation best practices:

* **Scoped requests:** Ensure that every request to an Atlassian-controlled service or endpoint is correctly scoped to an installation or invocation. While Forge handles much of this, any remote API calls that egress tenant-specific data must be disclosed in your Marketplace listing.
* **Statelessness:** Treat containers as ephemeral. Don't store durable customer data on the local disk; use Forge hosted storage ([Forge KVS](/platform/forge/storage-reference/kvs/), [Forge Custom Entities](/platform/forge/storage-reference/entities/), [Forge SQL](/platform/forge/storage-reference/sql/), or the [Object Store](/platform/forge/storage-reference/object-store/)) or remotes instead.

For more details, see [Tenant data isolation](/platform/forge/tenant-data-isolation/) and [Storage overview](/platform/forge/storage-reference/).

*NIST SP 800-190 reference: 3.5.1 (Data privacy/integrity).*

### Data egress

**Deny-by-default.** The Forge Containers environment always operates under a deny-by-default network architecture.

* **Egress proxy:** All outbound traffic must be routed through the `FORGE_EGRESS_PROXY_URL` environment variable. Connections that bypass the proxy will be blocked.
* **Inbound traffic:** Your app must listen **only** on the port specified by the `SERVER_PORT` environment variable.

For more details, see [API contract](/platform/forge/containers-reference/ref-api/) and [Runtime egress permissions](/platform/forge/runtime-egress-permissions/).

*NIST SP 800-190 reference: 3.4.2 and 4.4.2 (Unbounded network access from containers).*

### Secret management

**No hardcoded credentials.** Hardcoded credentials are a major security risk.

API keys, tokens and other app secrets must not be stored staticaly in the image definition. Secrets and credentials can be injected as [encrypted environment variables at build time](/platform/forge/environments-and-versions/#environment-variables) or the [Forge KVS secret store](/platform/forge/storage-reference/kvs-api-secret/) at runtime.

For more details, see [Manage environment variables with the Forge CLI](/platform/forge/cli-reference/variables/).

*NIST SP 800-190 references: 3.1.4 (Embedded clear text secrets); 4.1.4 (Dynamic injection).*

## Recommendations

This section lists strongly recommended best practices. Any deviations from these recommendations may be flagged during app review.

### Base image

**Minimalist footprint.** To reduce the attack surface, use base images that include only the libraries essential to your app's operation.

* Use *distroless* or minimal OS base images (for example, Alpine).
* Images that contain package managers (such as `apt` or `yum`) or full OS suites are discouraged.

*NIST SP 800-190 reference: 3.1.1 (Image vulnerabilities).*

### Dependencies

**Multi-stage builds.** The final production image should be a clean runtime that does not contain the build tools used during development. Multi-stage builds let you use one image for building (with all the heavy compilers and tools) and a separate, clean image for production.

* Strip all compilers, build tools, and shells from the final runtime image. If a tool is not required for the app binary to run, remove it.
* Replace shell scripts with equivalent entrypoint binaries, or explicitly include a shell only when needed.
* Use [Docker Debug](https://docs.docker.com/reference/cli/docker/debug/) to temporarily inspect or troubleshoot containers without altering the base image.

If your app requires a shell or a specific system utility to function, you must provide a documented use case during the app review process.

**Approval criteria:**

* **Review:** Atlassian evaluates the tool's necessity against the requested functionality.
* **Decision:** Use cases that can be achieved using native language libraries (for example, `axios` or `fetch` instead of `curl`) are rejected.
* **Exemption:** If the tool is a hard dependency for a core binary and no library alternative exists, it may be approved subject to additional static image scanning and hardening verification.

**Best practice:** Favour static binaries and library-based implementations to ensure your app passes the automated static image scan without requiring manual intervention.

*NIST SP 800-190 reference: 2.3.1 (Image creation, testing, and accreditation).*
