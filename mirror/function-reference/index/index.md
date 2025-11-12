# Functions overview

Serverless functions are an integral part of the Forge platform, enabling developers to create custom, scalable applications that interact and extend seamlessly with Atlassian's suite of apps. Functions underpin many other foundational capabilities of the platform, including UI backend resolvers, Atlassian app events, and more.

## Platform pricing resources

Learn more about Forge’s pricing structure, allowances, and billing by visiting [Forge platform pricing](/platform/forge/forge-platform-pricing/).

Estimate your app’s monthly costs using the [cost estimator](https://developer.atlassian.com/forge-cost-estimator), which lets you model usage and see potential charges.

## Basic usage

### Creating a function

#### Dependencies

The following dependency should be installed at the top-level directory of your app:

```
1
npm i @forge/api@latest
```

#### File structure

The following directory and function entry point file should be added to your app `/src` folder:

```
1
2
3
/src
  /backend
    /index.js
```

#### Handler

The following function handler should be defined in the `/src/backend/index.js` file:

```
```
1
2
```



```
export const handler = (...args) => {
  console.log(args);
  // Do something
}
```
```

See [Arguments](/platform/forge/function-reference/arguments) for the schema of `...args`.

#### Manifest definition

The following [function](/platform/forge/manifest-reference/modules/function/) should be declared in the [app manifest](/platform/forge/manifest-reference/):

```
```
1
2
```



```
modules:
  function:
    - key: backend
      handler: index.handler
```
```

### Attaching a function to a module

To enable your function to run, it needs to be attached to a [module](/platform/forge/manifest-reference/modules/) via the [app manifest](/platform/forge/manifest-reference/). For example, a [scheduled trigger](/platform/forge/manifest-reference/modules/scheduled-trigger/):

```
```
1
2
```



```
modules:
  scheduledTrigger:
    - key: example
      function: backend
      interval: hour # Runs hourly
```
```

See [common modules](/platform/forge/manifest-reference/modules/index-common/) for a complete list of backend entry points.
