# Forge Containers pricing (EAP)

Forge Containers are now available through Forge's Early Access Program (EAP). To start testing this feature,
submit your app's ID to our team [through this link](https://ecosystem.atlassian.net/servicedesk/customer/portal/1040/create/18884).

EAPs are offered to selected users for testing and feedback purposes. APIs and features under EAP
are unsupported and subject to change without notice. APIs and features under EAP are not recommended
for use in production environments.

For more details, see [Forge EAP, Preview, and GA](/platform/forge/whats-coming/#eap).

Unlike other Forge capabilities that use a [consumption-based pricing model](/platform/forge/forge-platform-pricing/), Forge Containers use a **reservation-based pricing model**. You pay for the CPU and memory capacity reserved for each container instance, regardless of whether that instance is actively handling requests. This reflects the always-on nature of container services, which must remain running to serve traffic at any time.

Containers are free to use during EAP. Pricing will apply from the point at which Forge Containers enters [Preview](/platform/forge/whats-coming/#forge-early-access-program--eap-). During the current EAP phase, billing is not yet enabled.

**No free usage allowance:** Unlike other Forge capabilities, Forge Containers do not include a free monthly usage allowance. All reserved CPU and memory capacity is billed from the moment billing is enabled at Preview.

## Unit pricing

Forge Containers are billed based on two dimensions: compute (vCPU) and memory (GiB), measured per hour.

| Metric | Unit | Price (USD) |
| --- | --- | --- |
| Compute | vCPU-hour | $0.07177 |
| Memory | GiB-hour | $0.00786 |

Charges are calculated based on the CPU and memory values declared in your [service manifest](/platform/forge/containers-reference/ref-manifest/), not on actual runtime utilization. Although billing uses an hourly unit, consumption is sampled at **1-minute intervals** and aggregated into hourly totals.

## Multi-region deployment model

Forge Containers are deployed across multiple Atlassian regions to deliver adequate performance for your app's users and to support [data residency](/platform/forge/data-residency/) requirements. Because each region runs its own container instances, **your costs scale with the number of regions your service is deployed in**.

When Forge Containers enters Preview with billing enabled, your container services will be automatically deployed in the following 6 Atlassian regions:

| Region | Location |
| --- | --- |
| Asia Pacific | Singapore |
| Australia | Sydney |
| Europe | Dublin |
| Europe | Frankfurt |
| US East | North Virginia |
| US West | Oregon |

These 6 regions balance performance coverage for the widest range of customers against cost to app developers. This is a deliberate trade-off against deploying across all 12 Atlassian [data residency locations](https://support.atlassian.com/security-and-access-policies/docs/understand-data-residency/). Atlassian will monitor performance and may adjust the regional footprint over time if needed.

## Estimating your costs

To estimate your monthly costs, multiply the reserved CPU and memory per container instance by the unit prices above, then multiply by the number of instances per service (controlled by the `min`/`max` settings in your manifest), the number of active regions, and the hours in the month.

**Example:** A service configured with **0.5 vCPU** and **1 GiB** memory, a minimum of **1 instance** per region, running in all **6 regions** for a full **730-hour month**:

| Dimension | Calculation | Cost |
| --- | --- | --- |
| Compute | 0.5 vCPU × $0.07177 × 1 instance × 6 regions × 730 hrs | $157.18 |
| Memory | 1 GiB × $0.00786 × 1 instance × 6 regions × 730 hrs | $34.43 |
| **Total** |  | **$191.82/month** |

The cost optimizations described below can significantly reduce this figure for most apps — particularly for non-production environments and apps with a limited geographic footprint.

## Cost optimizations

The following optimizations help minimize running costs for Forge Container services. Some are applied automatically by the platform; others can be configured directly by you as the app developer.

### Scale-to-zero in non-production environments

Container services in **non-production environments** (development and staging) automatically scale to zero running instances when they are idle. This means you are not charged for non-production container instances when they are not actively processing requests.

For production environments, a minimum of **2 running container instances per service** is recommended to ensure high availability. Running fewer than 2 instances in production is not advised.

### No provisioning where there are no installations

Container services are **not deployed in regions where your app has no installations**. If your app has no users in a given region, no container instances will run there, and no costs will be incurred for that region.

Provisioning and de-provisioning happen **dynamically and automatically**: when the first installation in a region is added, the service is provisioned there; when the last installation in a region is removed, the service is de-provisioned. This requires no developer intervention and no new `forge deploy` operation.

### Per-environment and per-region scaling configuration

The vertical and horizontal scaling profile of Forge Container services can be customized **per environment** and **per region**. This allows you to:

* Provision larger instances in high-traffic regions and smaller instances in quieter ones
* Reduce resource reservations in staging and development environments
* Right-size your service footprint as your app grows
