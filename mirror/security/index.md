# Security for Forge apps

Atlassian customers and admins only install apps they can trust. A key part of building this trust is security, which involves operational excellence in key areas like:

* Authentication and authorization
* Software execution
* Data management

[Learn more about how customers evaluate trust in cloud](/platform/marketplace/customer-trust-in-cloud/)

## Security considerations

It's important to consider building a Forge app that is [secure by design](https://www.atlassian.com/blog/it-teams/secure-by-design-tips-and-benefits-for-app-developers). This means your app's infrastructure is ready to handle the security needs of your target customer.

When your app is secure by design, it will:

* Avoid app rejection due to missing security requirements.
* Appeal to a wider range of customers, including enterprise.
* Set yourself up to earn and retain [Marketplace trust badges](https://www.atlassian.com/trust/marketplace) that help customers identify the most trustworthy apps.

Before you build your app, consider any regulatory frameworks that it may need to comply with, such as:

## Forge security principles

Forge facilitates many of the trust features that customers look for through a [shared responsibility model](/platform/forge/shared-responsibility-model/), where security responsibilities are shared between you and Atlassian.

Atlassian is responsible for running the platform used by Forge applications.
This includes enforcing what applications **can** and **can't** do.

### What Forge apps can do

* Run without interaction. For example, on a schedule, or in response
  to Atlassian app events.
* Be invoked directly by a web trigger.
* Access the raw HTTP request in a web trigger.
* Read/write all user-generated content (UGC), depending on which
  scopes are requested and granted.

### What Forge apps can't do

* Without reapproval by
  the site admin, you cannot increase scopes, permissions, and egress domains in new versions of previously installed apps.
* App users' Atlassian login credentials or sessions cannot be accessed.
* Unless the required [scopes](/platform/forge/security/#oauth-scopes) are granted, you cannot access Atlassian APIs.
* Identity properties of app users (such as user permissions or passwords) cannot be changed.

### App runtime

Controlling the app runtime is critical to security. The Forge runtime isolates the apps
from the environment in which they execute. By running apps in isolated environments, the platform limits what apps can do. For example:

* Apps cannot interfere with or modify other running apps.
* Apps cannot make requests to the Internet except as defined by the egress permissions in the app manifest.

To understand how this works in detail, see the diagram and notes on the Forge app environment below:

![Forge app environment diagram](https://dac-static.atlassian.com/platform/forge/images/forge-app-environment-diagram.svg?_v=1.5800.1853)

* App bundle: The app bundle is the packaged app code.
* Forge runtime: Forge apps run in AWS as lambdas. [AWS Lambda](https://aws.amazon.com/lambda/features/)
  provides per-app isolation.
* Outbound proxy: All external requests from the runtime pass through an outbound proxy which enforces strict egress controls as defined in your app manifest.
* Forge AWS account: The Forge platform runs lambdas using multiple AWS accounts to distribute the load.
  All of these accounts are separate from the other Atlassian services. Using dedicated accounts to run
  apps enables Forge to minimize privileges. This means that if an app escapes its sandbox due to a
  vulnerability, then running it in a less privileged account limits what it can do.

### User impersonation

If there is a user actively using a Forge app, the app may impersonate the user using any of its declared API scopes. For some scopes which control
access to PII such as `read:me`, the user needs to grant the app permission to impersonate them first.

An app may also specify a subset of its scopes for use with offline user impersonation, in this case the app can impersonate any user within the
context where it is installed, with some restrictions:

* An app cannot use offline impersonation with any API with scopes that require permission, e.g. `read:me`.
* An app cannot impersonate another app's user, or a deactivated user.
* An app cannot impersonate any user that doesn't have access to the app. This means the app can only impersonate app contributors if the app is
  not being shared through the Marketplace or direct distribution.

There are also some limitations on the current implementation of offline user impersonation. Currently, this cannot be used to impersonate anonymous
users or customer accounts. This may change in future.

## Data management

The Forge platform enables secure data management through its architecture and the way it handles data.
This includes data isolation to prevent leaks as well as data handling policies for the Forge
environments.

### Data isolation

Data isolation for apps is necessary in a cloud environment. The Atlassian cloud apps are
multi-tenant, so apps need to be multi-tenant. However, this means that apps can potentially mix
customer data. For example, two customers use an app that uses a global object to cache data by
issue key. Issue keys are not globally unique, therefore data could leak from one customer to another.

It is the developer's responsibility to keep tenant data isolated. This can be achieved by not keeping data in memory or on disk after the invocation finishes, and partitioning any global caches to separate data by tenant. Refer to the [Shared responsibility model](/platform/forge/shared-responsibility-model/) for information about the responsibilities of developers and Forge in [keeping customer data safe](/platform/forge/shared-responsibility-model/#tenant-safety).

### Environments

Forge ensures that data is handled responsibly by providing different environments for app developers.

Access to user data depends on:

* Your app enviornment
* What Forge capabilities you use

An [environment](/platform/forge/environments-and-versions/) is a version of the app that has its own code, manifest,
modules, outbound auth container, environment variables, and installations.

When your app is created, Forge sets up three environments:

* `development`: This is your default environment. You can create and manage [additional development environments](/platform/forge/contributors/#custom-environments). You can read logs and
  use tunneling.
* `staging`: This environment is typically used for continuous deployment, rather than development.
  However, it is the same as `development` in terms of restrictions on reading data.
* `production`: This is the environment where apps should be installed for use with production Cloud sites.
  You cannot use tunneling. Site admins can disable your access to logs for a production site. For more detail, refer to the [Logging guidelines for Forge app developers](/platform/forge/logging-guidelines/).

## Simple and secure authentication

Authentication is a fundamental part of security, but it can be complicated to implement and can open up
the app to security vulnerabilities. Forge controls the app runtime, which enables it to provide managed
APIs that apps can use to make secure calls to REST APIs.

Using managed APIs means that third-party code is never trusted with user credentials. API calls are
automatically authenticated on behalf of the app by the surrounding Forge infrastructure. This also
means that making API calls is much simpler.

### OAuth scopes

Forge apps use [OAuth 2.0](https://oauth.net/2) protocols when authenticating with:

* Jira platform
* Jira Software
* Jira Service Management
* Confluence REST APIs
* Bitbucket REST APIs
* Compass GraphQL API

Scopes are an OAuth 2.0 mechanism that enables an app to access the data manipulated by a REST API
operation. To access an Atlassian app operation that uses OAuth 2.0 authentication, the app needs
to request the scopes required by the operation in the manifest file. Scopes then provide
administrators and users information about the data an app accesses. This enables administrators
and users to decide whether they want to install the app. See
[Add scopes to call an Atlassian REST API](/platform/forge/add-scopes-to-call-an-atlassian-rest-api/)
for details.

If an app doesn't request any scopes, the app doesn't have access to OAuth 2.0 protected
resources. This follows the principle of least privilege and helps to retain the trust of your users.

### External providers

Beyond authentication with Atlassian APIs, Forge supports managed OAuth 2.0 authentication
with external identity providers that support
[OAuth 2.0 authorization code grants](https://tools.ietf.org/html/rfc6749#section-4.1),
such as Google or Slack.

When using external providers, Forge apps act as the OAuth 2.0 client connecting to an
external resource. This enables a Forge app to request information from third-party services
securely using the familiar fetch function, while the platform handles getting and rotating
OAuth 2.0 tokens automatically.

An app using external authentication provides a connection across multiple Atlassian apps
with shared authentication handled by the Forge platform. However, apps never have direct
access to the OAuth 2.0 tokens. Instead, apps use the `withProvider` method to have the Forge
platform automatically send tokens with each request.

[Learn how to integrate with an external provider](/platform/forge/use-an-external-oauth-2.0-api-with-fetch/)

## More trust resources for Forge apps

For more trust resources, check out:

## Developing for Atlassian Government Cloud

This content is written with standard cloud development in mind. To learn about developing for Atlassian Government Cloud, go to our [Atlassian Government Cloud developer portal](https://developer.atlassian.com/platform/framework/agc/).
