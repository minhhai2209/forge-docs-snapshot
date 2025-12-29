# Understanding UI modifications

This guide introduces you to the key concepts behind UI modifications (UIM) for Forge apps. By the end, you'll understand how UIM works and how to use it effectively in your Jira and Jira Service Management apps.

If you're ready to start building, check out the [Build a Jira UI modifications app](/platform/forge/build-a-jira-uim-app/) tutorial. For complete technical details, see the [Jira UI modifications module](/platform/forge/manifest-reference/modules/jira-ui-modifications/) and [Jira Service Management UI modifications module](/platform/forge/manifest-reference/modules/jira-service-management-ui-modifications/).

## What is UIM

**UI modifications** (UIM) is a runtime extension that gives Forge app developers a low-level API to alter the behavior of the Jira and Jira Service Management user interface. For the time being, in Jira *Global issue create* (GIC), *Issue view* and *Issue transition* can be customised and in Jira Service Management *Request create portal* can be customised.

The UI is modified using the **UIM JS API** in Forge applications in the **UIM Forge module**. You can manage the available **UI modifications** and their contexts using the **UIM REST API**. Applications can store additional data related to **UI modifications** as **UIM data**, which is also managed by the **UIM REST API**. Each **UI modification** is backed by a **UIM entity** which represents it on the back-end and is delivered to the front-end in **UIM data**.

## Key terminology

Below are some key terms you need to learn to understand UIM better:

| Term | Description |
| --- | --- |
| UIM app | An Atlassian Forge application which uses the UIM Forge module. A single UIM app can declare only one UIM Forge module. |
| UIM app invocation context | Provided to the UIM app by Jira.  **Jira:** For Jira, it consists of a `project`, `issueType`, and `uiModifications` (UIM data).  **Jira Service Management:** For Jira Service Management, it consists of a `portal`, `requestType`, and `uiModifications` (UIM data). |
| UIM app mounting context | **Jira:** A combination of a `project`, `issueType`, and `viewType`. UIM supports the following view types:   * Global issue create * Issue view * Issue transition     **Jira Service Management:** A combination of a `portal`, `requestType`, and `viewType`. UIM supports the following view types: |
| UIM data | An array of UIM entities for a given UIM app invocation context. The interpretation of UIM data is the responsibility of the UIM app. UIM data can be accessed through the invocation argument within the `initCallback` and the `changeCallback`. |
| UIM entity | A single mapping of custom textual data and a UIM app mounting context. It can be created and obtained using the UIM REST API. |
| UIM Forge bridge API | The API provided to the UIM app through the `@forge/jira-bridge` module. For more details, see the [documentation](http://localhost:9191/platform/forge/custom-ui-jira-bridge/uiModifications/). |
| UIM Forge module | A UI modifications Forge module (`jira:uiModifications`) declared in the manifest. |
| UIM REST API | The back-end REST API used to assign and retrieve specific data (related to `project`, `issueType`,`portal`,`requestType` and `viewType`) to be consumed by the UIM app through the UIM app invocation context. For more details, see the [API documentation](http://localhost:9191/cloud/jira/platform/rest/v3/api-group-ui-modifications--apps-/). |

## Why is it different?

The purpose of UIM is to alter the user experience in Jira and Jira Service Management. To that end,
the code you provide on the UIM module will run as the user interacts with Jira and Jira Service
Management. So, it needs to be performant.

Thankfully, UIM are highly dependent on the context in which they run.

Different projects have different fields and different issue types, and Jira instances usually contain
hundreds of those. With UIM you need to specify certain project and issue type combinations. We call
those [contexts](#uim-contexts). That way if you have a lot of different customizations suitable for
your workflow, Jira won’t load all of them every time you open the issue create form. UIM modules
will only be loaded in relevant contexts and won’t hurt the performance of other users in other contexts.

Similarly, Jira Service Management portals have different fields and request types. When using UIM,
you specify a particular portal and request-type combination to define the [contexts](#uim-context).
This ensures that UIM modules load only in the relevant Jira Service Management request creation
experience and do not affect performance for users in other contexts.

What's more, UIM modules are not limited to extending the behavior of the [supported views](/platform/forge/manifest-reference/modules/jira-ui-modifications/#jira-ui-modifications) in Jira and supported views in Jira Service Management[supported views](/platform/forge/manifest-reference/modules/jira-service-management-ui-modifications/#jira-ui-modifications). Any Forge app can include this module and expand the functionality of Jira in different ways. For example, you could surface information from your Forge app in the description of a supported field. UIM are built so that they can be used by dozens of apps installed on a single Jira and Jira Service Management instance. However right now only one app can run in a given [context](/platform/forge/understanding-ui-modifications/#uim-contexts).

## How to make it work

To get UIM working you need three pieces:

* Custom UI code in your Forge app, declared as a UIM module in the Forge manifest.
* A UIM entity, which may also contain [custom data](#uim-entities), created through the Jira REST API.
* Relations between [UIM entities](#uim-entities) and [UIM contexts](#uim-contexts). These you also create through the Jira REST API.

## UIM module code

UI modifications run as an invisible Custom UI app in the [supported views](/platform/forge/manifest-reference/modules/jira-ui-modifications/#jira-ui-modifications) of Jira and [supported views](/platform/forge/manifest-reference/modules/jira-service-management-ui-modifications/#jira-ui-modifications) of Jira Service Management. Refer to the [Custom UI documentation](/platform/forge/custom-ui/) to learn about APIs you can use.

The interactions between your Custom UI code and the [supported views](/platform/forge/manifest-reference/modules/jira-ui-modifications/#jira-ui-modifications) of Jira and [supported views](/platform/forge/manifest-reference/modules/jira-service-management-ui-modifications/#jira-ui-modifications) of Jira Service Management happen through the [@forge/jira-bridge](/platform/forge/custom-ui-jira-bridge/bridge/) package, using the `uiModifications` API.

## UIM entities

UIM entities are app-specific. One Forge app cannot read UIM entities created by another Forge app.

The Forge app that uses a UIM module can access all UIM entities assigned to a given UIM context.
UIM entities let you store context-specific data that your app can consume at runtime.

When creating an entity, the `data` parameter accepts a string. This value is stored together with the
context and passed as a parameter to your Forge app’s callbacks. Attaching this data at UIM execution
time provides flexibility without compromising security or performance.

The intent is for apps to use this data to make UIM modules robust and flexible. Your app has
complete control over what data it stores, up to 50,000 characters per entity. In practice, most
apps will create multiple UIM entities with different data and attach them to multiple contexts.

## UIM contexts

The final piece needed to make UIM work is the context.

A context is the delivery address for your UIM. It connects your module code and data to the place where the UIM runs in the UI.

The final piece needed to make UIM work is the context.

Context is the delivery address for your UIM. It will connect your module code and data for the execution of UIM inside the view.

* For Jira context is a combination of project, issue type and view type. This may be extended in the future.
* For Jira service management request create portal context is a combination of portal, request type and view type. This may be extended in the future.

From an execution perspective, your UIM module runs every time a context matches. That includes scenarios like:

* **Jira issue view and issue transition:** When a user opens any of the [supported views](/platform/forge/manifest-reference/modules/jira-ui-modifications/#jira-ui-modifications)
  from a supported trigger point that matches the context.
* **Jira global issue create:** When the user has selected the *Create another issue* checkbox and creates consecutive issues that match the context, or when the user switches between projects or issue types in the global create dialog and the new selection matches the context.
* **Jira Service Management request create portal:** When a user opens any of the [supported views](/platform/forge/manifest-reference/modules/jira-service-management-ui-modifications/#jira-ui-modifications) from a supported trigger point that matches the context.

## UIM REST API

UIM modules are owned by the apps defining them. The same applies to their entities and contexts.

The only way to manage all of those is through the app itself. That implies the REST API for UIM is restricted to the apps. Users can't make calls to the REST API and alter any aspect of UIM, they are not authorized to do so. Apps also can't see or modify UIM entities from other apps.

We recommend to use our REST API to store any context-related data instead of other storage APIs. That way your app doesn't have to perform any extra requests - the data is provided to the app at render time. The main benefit here is the better performance for the end user.

Please refer to the [UIM REST API documentation](/cloud/jira/platform/rest/v3/api-group-ui-modifications--apps-/) for more details.

You must make all UIM-related requests to Jira with the `asApp()`. Keep in mind you can use `asApp()` only through [resolvers](/platform/forge/runtime-reference/custom-ui-resolver/).

## Scopes and permissions

Apps with UIM modules will have access to the information contained inside the supported view they
apply to. This requires a set of scopes to work correctly:

## Avoiding UIM antipatterns

Before you jump into developing your Forge app using UIM module, you should be aware of some pitfalls.

#### Antipattern 1: The mega app

This pattern is not recommended if you are writing a multi-tenant app for the Marketplace. It may be fine if you are building a tenant-specific app (in-house/internal).

Given the nature of the UIM API, and the limitation of a single UIM module for your Forge app, it's tempting to hard-code project IDs in your app:

```
```
1
2
```



```
// Pseudocode
if (project === 1) {
    summary.hidden()
}

if (project === 2) {
    priority.hidden()
}
```
```

or hard-code tenant IDs:

```
```
1
2
```



```
// Pseudocode
switch (jiraTenantId) {
    case "alpha.atlassian.net":
        alphaModifications();
        break;
    case "beta.atlassian.net":
        betaModifications();
        break;
    // ...
}
```
```

This is an antipattern because this code is going to grow in size every time a new context needs to be matched. It also requires an app update every time there's a change in any of the behaviors. Remember, UIM uses the single module and code defined in the app manifest for all the contexts it's matched to.

#### Antipattern 2: Extreme flexibility

On the opposite extreme of defining every matching context in code with the desired modifications is proxying the whole UIM API to the data inside the UIM entity.

```
```
1
2
```



```
// Pseudocode
onInit(({api, uiModifications}) => {
    // Variant 1 (NOT RECOMMENDED): Running UIM entity data as code
    eval(uiModifications[0].data);
    // Variant 2 (NOT RECOMMENDED): Using UIM entity data as content of an extra iframe
    iframe.srcdoc = uiModifications[0].data;
})
```
```

Variant 1 would allow UIM entity data to be executed as JavaScript code with the full access to UIM API. This solution trades maintainability for flexibility since it strictly depends on the data being a syntactically correct JavaScript.

Variant 2 would result in wasting the users' time when loading and using the UIM applied view.

The UIM already provide a low-level API and Forge apps run inside iframes. UIM uses the Forge platform to build safe and performant apps. We designed it to allow developers to deliver a great experience to Jira users while keeping a balance of flexibility, safety and performance. Users of proxy apps would be better off writing their own UIM modules and apps.

### Writing UIM modules the right way

The point where the two extremes described above meet is where we intend app developers to write their UIM modules. Forge apps should not require an update every time a user needs customization, as in the mega app antipattern above.

The desired path is one where app developers utilize the `data` parameter, which is available when running the UIM and defined from within the app when creating a new UIM entity.

## Summing up

In short, a Forge app using the UIM module will handle multiple entities, each referring to its own data. This data will be shaped up according to the internal mechanics of each app.

Those entities will be then linked to contexts, as many as desired, so they can be executed in the supported view when the user's action matches them.

Given the overhead of managing entities and the low-level nature of the UIM API, UIM modules were designed to be used together with other modules (eg. admin page) which will actually manage the UIM entities and contexts, either as a side-effect of other functionalities from the app or explicitly.

To see in practice how your app can handle the management of UIM entities and contexts, look at the admin page module in [the example app](https://bitbucket.org/atlassian/forge-ui-modifications-example).
