# Building automations with Forge

The content on this page may refer to automation in various contexts, including:

* **Automation**, when we refer to the technology that's used to perform tasks with minimal
  human intervention.
* **Automation Platform**, when we discuss the
  [basic concepts and capabilities](https://support.atlassian.com/cloud-automation/docs/automation-basics/)
  provided by the [Atlassian Automation Platform](https://www.atlassian.com/platform/automation).
* **Automation in Forge**, when we discuss how apps built on Forge can be configured
  to automate certain tasks.

Forge unlocks automation possibilities that go beyond
[Automation Platform](https://support.atlassian.com/cloud-automation/docs/automation-basics/)
capabilities within Atlassian apps, like Jira and Confluence. This includes the ability
to implement complex logic and deeply integrate with external systems.

## Usage

In general, we recommend using Automation Platform capabilities where available, rather than
building identical functionality in an app. There are also existing
[Marketplace](https://marketplace.atlassian.com/) apps that provide automation capabilities
that could be considered before writing a bespoke app.

## Conceptual overview

There are several ways in which Forge apps can automate tasks. An app can leverage automation features
built into Atlassian apps, such as Jira, for example. Alternatively, an app can independently
implement automation capabilities. These methodologies can work independently or in concert
with each other, as shown below.

The integration between Forge apps and Automation Platform capabilities uses the generic
**Send web request** component.

## Patterns

There are four main patterns that define how automation can be built using Forge:

### Implementing automation entirely with Forge

Automation can be entirely implemented as a Forge app. In this pattern, the Automation Platform
capabilities are not used since Forge apps have the ability to subscribe to Atlassian app events
and can invoke Atlassian app APIs.

### Extending the Automation Platform with Forge

You can consider the following patterns to extend the Automation Platform with Forge:

#### Using webhooks and web requests

In this pattern, automation may be implemented with Automation Platform components that trigger
a Forge app to complete the automation.

#### Using the Forge Action module

The Forge Action module is now available in Preview. It opens yet another way
to extend automation rules within Atlassian apps.

See [Forge Automation modules](/platform/forge/manifest-reference/modules/automation-action/)
for more details.

In this pattern, you can define your own automation actions using the
Forge [Action](/platform/forge/manifest-reference/modules/automation-action/) module.
These actions appear as components in the Automation Platform rule builder. This allows users
to add your app’s logic directly to their rules.

### Triggering automation with Forge

A Forge app can respond to a Forge event, then perform some logic and conditionally invoke
an automation to perform additional actions. There are a range of different kinds of Forge events,
including Atlassian app events similar to those available to Automation Platform, as well as events
that are triggered by non-Atlassian app events.

### Injecting custom logic in automation

In some cases, it may make sense to incorporate Forge capabilities within Automation Platform
that start and end with Automation Platform capabilities.

## Example

The diagram below shows an example of a Forge app with Automation Platform capabilities
that integrate with automations created with Automation for Jira. There are three automations:
*add joke comment*, *add joke-added label*, and *add key labels*.

The *send web request* automation component is configured to invoke the app’s
[web trigger](/platform/forge/runtime-reference/web-trigger-api/#web-trigger-api),
which handles the condition evaluated by the first part of the automation (the assignee of an issue is a specific user).
The app then retrieves a joke from an external system, adds it as a comment to the issue, and invokes
and *add joke-added label* automation by calling its *incoming webhook* component.

The *add key labels* automation is wholly implemented by the same Forge app. The app listens for
comment added events. On receipt of an event, it checks the comment for certain keywords, and if detected,
adds labels to the issue that relate to the keywords found.

## Advanced considerations and tactics

* **Validating invocations from the send web request component**: If your Forge app has a web trigger
  that will be invoked by the send web request automation component, the send web request automation
  component can be configured to send a custom header that acts as a secret shared between
  the automation component and the app. On receipt of the web trigger event, the app should check
  the header value. Use an
  [environment variable](/platform/forge/environments-and-versions/#environment-variables)
  in your app to store the secret. The following code will validate the header:

```
```
1
2
```



```
const headers = webtriggerPayload.headers;
const headerSecretObject = headers['shared-secret'];
const headerSecret = headerSecretObject ? headerSecretObject[0] : undefined;
const validated = headerSecret && headerSecret === process.env.SHARED_SECRET;
```
```

* **Constraining automations to specific contexts**: It’s often the case that automation applies
  only to a specific context, such as a Jira project or Confluence space. Constraining Forge app automations
  to specific contexts can easily be achieved. When a Forge function is invoked outside of a user context,
  such as an Atlassian app trigger, the function receives a payload or parameter that contains context information.
  See the [Atlassian app events](/platform/forge/events-reference/product_events/#product-events)
  documentation for more details.
* **Avoid circular loops**: Be aware of the possibility of circular loops that result from multiple
  automations triggering from each other.
* **Permissions**: For an app to invoke an incoming webhook automation component, the app will need
  to request a backend external fetch permission as follows:

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
        - 'https://automation.atlassian.com'
```
```

* **Process-intensive operations**: If a Forge app needs to perform operations that will take
  significant computing power, time, or both, it may be necessary to implement in small processing chunks
  using the [async events API](/platform/forge/runtime-reference/async-events-api/#async-events-api).
  Doing this helps prevent the app from exceeding the Forge
  [function invocation timeout](/platform/forge/platform-quotas-and-limits/#invocation-limits).

## Detailed information

### Forge and Atlassian app triggers

#### Atlassian app triggers

Forge app functions can register to receive trigger events for a range of different kinds of
Atlassian app events that are similar to the different kinds of triggers available within the built-in
automation capabilities. When an app is invoked by an Atlassian app trigger, information is passed
to the app about the event causing the trigger, including contextual information, such as the project,
issue, or page relating to the event.

More details:

#### Ad-hoc Forge triggers

Forge app functions can be triggered in an ad-hoc manner. This is useful where the triggering event
occurs in an external system, and as explained above, having an Atlassian app automation invoke a Forge function.

More details:

#### Periodic Forge triggers

Forge app functions can be triggered in a periodic manner. This allows automations to execute on a scheduled basis.

More details:

#### Calling APIs from a Forge app

##### Calling Atlassian app APIs

Forge apps can invoke Atlassian app APIs without the app developer needing to manage Atlassian app credentials.

Import the Forge API package in your app, as follows:

```
```
1
2
```



```
import api, { route } from '@forge/api';
```
```

To check the status of a request, use status as shown below:

```
```
1
2
```



```
const result = await api
  .asApp()
  .[requestConfluence | requestJira](
    route`/rest/api/etc`
  );
const status = result.status;
```
```

More details:

##### Calling external APIs

Forge apps can also make authenticated requests to external APIs using the fetch operation as follows:

```
```
1
2
```



```
import api from '@forge/api';

const response = await api.asUser()
  .withProvider('google', 'google-apis')
  .fetch('/userinfo/v2/me');
```
```

More details:

#### Invoking an Atlassian app automation trigger

Invoking an Atlassian app automation trigger involves a simple fetch request:

```
```
1
2
```



```
const payload = {
  ...
}
const options = {
  method: 'POST',
  headers: {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(payload)
}
// Set this environment variable with forge variables set MY_WEBHOOK_URL https://automation.atlassian.com/[remainder of url of incoming webhook component]
const url = process.env.MYL_WEBHOOK_URL;
const response = await fetch(url, options);
```
```

More details:

## Additional guides

The following resources provide additional guidance that will help you get started building Forge automation apps:
