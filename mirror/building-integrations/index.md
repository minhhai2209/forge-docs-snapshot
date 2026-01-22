# Building integrations with Forge

Forge allows you to build integrations from Atlassian apps - like Jira and Confluence - to external (or third-party) systems. For example, Jira work items can capture data about work and manage its workflow whilst an external system can capture or display related specialty data such as test information, customer feedback, geospatial data, etc.

Discover the capabilities and benefits of building custom integrations that streamline workflows and improve user experiences.

## Using Forge as a bridge

To integrate an third-party system with one or more Atlassian apps such as Jira, a Forge app can be created that acts as a bridge. The Forge app allows the third-party system to invoke Atlassian APIs and it also allows the third-party system to receive events from Atlassian apps.

![Forge integration bridge architecture](https://dac-static.atlassian.com/platform/forge/images/integrations/forge-bridge-architecture.png?_v=1.5800.1794)

### Invoke Atlassian APIs from an external system

A third-party system can invoke Atlassian app APIs in order to:

* Push data to an Atlassian app
* Retrieve state and data from an Atlassian app

The Forge [web trigger](/platform/forge/events-reference/web-trigger/) capability allows an app to receive API calls from a third-party system. After receiving a request, the Forge app can then invoke an Atlassian app API using the [Atlassian app fetch API](/platform/forge/apis-reference/product-rest-api-reference/#atlassian-app-fetch-api).

![Web trigger integration flow](https://dac-static.atlassian.com/platform/forge/images/integrations/web-trigger-flow.png?_v=1.5800.1794)

**Next step**: Review the [Forge integration tutorial's](/platform/forge/build-a-feedback-integration-app/) explanation of implementing a webtrigger to allow an external web application to utilise Jira to implement capabilities.

### Receive Atlassian app events

A third-party system can receive events from Atlassian apps by registering for [Atlassian app events](/platform/forge/events-reference/product_events/). For example, a Forge app can register to receive notifications whenever a Jira work item is created or when a Confluence page is updated. Upon receiving such an event, the Forge app can invoke a third-party system using the [basic fetch API](/platform/forge/runtime-reference/fetch-api.basic/) or the [external authentication API](/platform/forge/runtime-reference/external-fetch-api/) with the event information and potentially additional information. The [Forge trigger module](/platform/forge/manifest-reference/modules/trigger/) is used to register for Atlassian app events.

For more complex event-driven workflows and automation patterns, see [Automation with Forge](/platform/forge/automation-with-forge/).

It's important to authenticate web trigger requests. A simple way to achieve this is by requiring requests be sent with a header that includes a key that is private to your app and the client invoking the web trigger.

![Event trigger integration flow](https://dac-static.atlassian.com/platform/forge/images/integrations/event-trigger-flow.png?_v=1.5800.1794)

**Next step**: Review how the [Forge integration tutorial](/platform/forge/build-a-feedback-integration-app) explains how to listen to Jira work item events in order to relay feedback captured directly in Jira to the Feedback web app. For details, see the section below about the Forge Feedback example app.

## Forge Remotes

Forge has a feature named *Remotes* whereby functionality can be more directly implemented in third-party systems. For example, in the case of receiving Atlassian app events, the Forge app can specify that the third-party system can directly receive events. The Forge app can also specify that the event should convey a token that allows the third-party system to invoke Atlassian APIs in response to the event. Forge Remotes is a powerful way to integrate third-party systems with Atlassian apps. Forge Remotes is typically used when an external system such as a SaaS application has already been established, or if the system needs to utilise technologies such as programming languages, libraries, specialty databases or infrastructure that is unrealistic to implement in Forge.

![Forge Remotes architecture](https://dac-static.atlassian.com/platform/forge/images/integrations/forge-remotes-architecture.png?_v=1.5800.1794)

**Next step**: Review the [Forge Remotes documentation](/platform/forge/remote/).

## Surface external data in Atlassian apps

It's often very useful to have third-party app data appearing in Atlassian apps. Here are examples for both Jira and Confluence:

### Jira integration example

Let's say a third-party system monitors the health of equipment that is represented as Jira work items. For such a system, it would be useful to display the current health status in the work item. To achieve this, the third-party system can invoke the Jira APIs to store properties against work items. For this case, the Forge app that provides the bridging functionality can also provide one or more [Jira custom fields](/platform/forge/manifest-reference/modules/jira-custom-field/) that displays the data within the work item view.

### Confluence integration example

Consider a documentation system where technical specifications are stored in an external engineering database. A Forge app can create a [Confluence macro](/platform/forge/manifest-reference/modules/macro/) that displays real-time data from the engineering system directly within Confluence pages. When engineers update specifications in their specialized tools, the documentation in Confluence automatically reflects these changes, ensuring teams always have access to the latest information without manual updates.

There are many other ways to surface data in Atlassian apps using various [Forge modules](/platform/forge/manifest-reference/modules/).

**Next step**: Read about [Jira entity properties](https://developer.atlassian.com/cloud/jira/platform/jira-entity-properties/) and [Confluence entity properties](https://developer.atlassian.com/cloud/confluence/confluence-entity-properties/) since entity properties are a good way for a Forge app to store data that is associated with Atlassian app entities. Review the various [Forge modules](/platform/forge/manifest-reference/modules/) that can be used to surface data to users.

## Forge Feedback example app

The [Forge integration tutorial](/platform/forge/build-a-feedback-integration-app) shows how to use Forge to integrate a web app with Jira. In this example, the integration exchanges feedback between a web app and Jira, but you can apply the same pattern to many types of data.

![Forge Feedback integration example](https://dac-static.atlassian.com/platform/forge/images/integrations/forge-feedback-example.png?_v=1.5800.1794)

The feedback integration could be useful for a web app that a company uses to manage training. For example, the training web app could let students provide feedback about training sessions, stored in a Jira space, to take advantage of Jira’s workflow capabilities. Teachers can also capture feedback directly in the Jira project and the training web app will reflect this feedback in its system. The Forge Feedback app provides a two-way bridge between the training web app and Jira.

## Next steps

Ready to start building? Here are practical next steps to implement integration patterns:

### Advanced integration topics
