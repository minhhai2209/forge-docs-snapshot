# Dynamic Modules (EAP)

Forge Dynamic Modules is now available as part of Forge’s Early Access Program (EAP).
To start testing this, sign up [here](https://ecosystem.atlassian.net/servicedesk/customer/portal/3595).

EAP features and APIs are unsupported, and subject to change without notice. Apps that use dynamic modules should not be deployed to `production` environments.

All dynamic modules created during EAP will not be carried over to Preview. For more details, see [Forge EAP, Preview, and GA](/platform/forge/whats-coming/#eap).

In addition to declaring modules in your app manifest, Forge apps can register some modules dynamically at runtime. This capability
provides you with the flexibility to define an app's behaviour, and is useful for adding app features that are more responsive to
arbitrary user needs.

Dynamic modules are registered in the context of an app installation, which means that an app can register different modules for
each app installation.

## Limitations

This capability has the following limitations:

* Each app installation can register a maximum of 100 dynamic modules. Attempts to exceed this limit will result in a `422 Unprocessable` error response.
* [Remote](/platform/forge/remote/) backends can only use `asApp` calls for dynamic module operations; `asUser` calls are not allowed. This means your remote backend will only be able to call the Dynamic Modules API as a generic bot user.

## Available modules

For now, only the [Trigger](/platform/forge/manifest-reference/modules/trigger/) module can be declared as a dynamic module.
We are planning to add more in the future.

## Managing dynamic modules

Use the [Dynamic Modules API](/platform/forge/apis-reference/dynamic-modules-api/) to register, list, update, or delete dynamic modules.
Dynamic modules are registered on a *per-installation context*. Any functions or APIs that use the dynamic module only become enabled once
the module is registered.

## Migration from Connect

We have no plans to support a migration path for existing dynamic modules from Connect. This means that any dynamic modules registered in Connect
app installations will *not* be automatically migrated to Forge (even if a Forge version of that dynamic module becomes available). Forge apps can
only use dynamic modules registered through the [Dynamic Modules API](/platform/forge/apis-reference/dynamic-modules-api/).

If you are [incrementally migrating a Connect app](/platform/adopting-forge-from-connect/) that used Dynamic Modules, your app should
also remove any registered Connect dynamic modules. Then, those modules will need to be either declared as
[static modules in the Forge manifest](/platform/forge/manifest-reference/modules/) or as Forge dynamic modules.

To remove any registered Connect dynamic modules from an installation, your app should use the Connect API to:
