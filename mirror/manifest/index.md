# Manifest

The manifest is a YAML file (`manifest.yml`) that describes your Forge app. It includes the
[modules](/platform/forge/modules/) your app wants to use, the
[permissions](/platform/forge/manifest-reference/permissions/) required by your app,
and other information about your app.

It’s created when you run the `forge create` command in the Forge CLI.

For an introduction to the manifest, check out this video:

## Example

Here is an example `manifest.yml` file:

```
1app:
2  id: ari:cloud:ecosystem::app/baf12188-3db6-4ec9-aa26-f85cecb62d05
3modules:
4  confluence:contextMenu:
5    - key: dictionary
6      function: main
7      title: Define word
8  function:
9    - key: main
10      handler: index.run
11permissions:
12  scopes:
13    - read:content-details:confluence
14    - read:content.property:confluence
15    - write:content.property:confluence
16
```

## Reference documentation

To learn more, check out the manifest
[reference documentation](/platform/forge/manifest-reference/).
