# Understanding UI modifications

This is a primer on UI modifications, you should read this to understand the concepts behind this Forge module. If you are not sure what UI modifications are or what it can do for you, refer to the [module documentation](/platform/forge/manifest-reference/modules/jira-ui-modifications/) first.

## A unique way to modify Jira

UI modifications (UIM) give Forge app developers a low-level API to alter the behavior of the Jira user interface. For the time being, the *Global issue create* (GIC), *Issue view* and *Issue transition* can be customised.

The UIM module is unique - it requires more than just adding definitions to your Forge app manifest. Running `forge install` also isn't enough to get UIM to run on your dev instance or for the users of your app. You also need to [define the context](#uim-contexts) in which your UIM are going to be applied.

## Why is it different?

The purpose of UIM is to alter the user experience in Jira. To that end, the code you provide on the UIM module will run as the user interacts with Jira. So, it needs to be performant.

Thankfully, UIM are highly dependent on the context in which they run.

Different projects have different fields and different issue types, and Jira instances usually contain hundreds of those. With UIM you need to specify certain project and issue type combinations. We call those [contexts](#uim-contexts). That way if you have a lot of different customizations suitable for your workflow, Jira won’t load all of them every time you open the issue create form. UIM modules will only be loaded in relevant contexts and won’t hurt the performance of other users in other contexts.

What's more, UIM modules are not limited to extending the behavior of the [supported views](/platform/forge/manifest-reference/modules/jira-ui-modifications/#jira-ui-modifications). Any Forge app can include this module and expand the functionality of Jira in different ways. For example, you could surface information from your Forge app in the description of a supported field. UIM are built so that they can be used by dozens of apps installed on a single Jira instance. However right now only one app can run in a given [context](/platform/forge/understanding-ui-modifications/#uim-contexts).

## How to make it work

To get UIM working you need three pieces:

* Custom UI code in your Forge app, declared as a UIM module in the Forge manifest.
* A UIM entity, which may also contain [custom data](#uim-entities), created through the Jira REST API.
* Relations between [UIM entities](#uim-entities) and [UIM contexts](#uim-contexts). These you also create through the Jira REST API.

## UIM module code

UI modifications run as an invisible Custom UI app in the [supported views](/platform/forge/manifest-reference/modules/jira-ui-modifications/#jira-ui-modifications). Refer to the [Custom UI documentation](/platform/forge/custom-ui/) to learn about APIs you can use.

The interactions between your Custom UI code and the [supported views](/platform/forge/manifest-reference/modules/jira-ui-modifications/#jira-ui-modifications) happen through the [@forge/jira-bridge](/platform/forge/custom-ui-jira-bridge/bridge/) package, using the `uiModifications` API.

## UIM entities

They are app-specific - one Forge app cannot read UIM entities created for different Forge app.

The Forge app using UIM module will have access to all UIM entities assigned to a specific UIM context.

UIM entities let you store context-specific data the app can consume at runtime.

You can find the shape of [UIM entities in the module documentation](/platform/forge/manifest-reference/modules/jira-ui-modifications/#configure-the-ui-modification).

When creating the entity, the `data` parameter accepts a string. This data will be stored together with the context and passed as a parameter for the callbacks in your Forge app. Having this data attached on the execution of UIM allows enough flexibility without compromising on security and performance.

The idea is for apps to work with the data to make the UIM module robust and flexible. The app has complete control of what kind of data it stores - up to 50000 characters per entity.

Overall, the expectation is that apps will have multiple UIM entities, which contain different data, and will attach them to multiple contexts.

## UIM contexts

The final piece needed to make UIM work is the context.

Context is the delivery address for your UIM. It will connect your module code and data for the execution of UIM inside the GIC/Issue view.

Context is a combination of project, issue type and view type. This may be extended in the future.

From the execution perspective, your UIM module will run every time a context matches. That includes scenarios like:

### All supported views

### Global issue create

* when the user has checked the *Create another issue* checkbox and creates consecutive issues;
* or when the user switches between projects or issue types.

## UIM REST API

UIM modules are owned by the apps defining them. The same applies to their entities and contexts.

The only way to manage all of those is through the app itself. That implies the REST API for UIM is restricted to the apps. Users can't make calls to the REST API and alter any aspect of UIM, they are not authorized to do so. Apps also can't see or modify UIM entities from other apps.

We recommend to use our REST API to store any context-related data instead of other storage APIs. That way your app doesn't have to perform any extra requests - the data is provided to the app at render time. The main benefit here is the better performance for the end user.

Please refer to the [UIM REST API documentation](/cloud/jira/platform/rest/v3/api-group-ui-modifications--apps-/) for more details.

You must make all UIM-related requests to Jira with the `asApp()`. Keep in mind you can use `asApp()` only through [resolvers](/platform/forge/runtime-reference/custom-ui-resolver/).

## Scopes and permissions

Apps with UIM modules will have access to the information contained inside the supported view they apply to. This requires a set of scopes to work correctly. The specific scopes required are detailed in the [module reference](/platform/forge/manifest-reference/modules/jira-ui-modifications/#scopes).

## Avoiding UIM antipatterns

Before you jump into developing your Forge app using UIM module, you should be aware of some pitfalls.

#### Antipattern 1: The mega app

This pattern is not recommended if you are writing a multi-tenant app for the marketplace. It may be totally fine if you are building a tenant-specific app (in-house/internal).

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
