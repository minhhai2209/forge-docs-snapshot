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
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
app:
  id: ari:cloud:ecosystem::app/baf12188-3db6-4ec9-aa26-f85cecb62d05
modules:
  confluence:contextMenu:
    - key: dictionary
      function: main
      title: Define word
  function:
    - key: main
      handler: index.run
permissions:
  scopes:
    - read:content-details:confluence
    - read:content.property:confluence
    - write:content.property:confluence
```

## Reference documentation

To learn more, check out the manifest
[reference documentation](/platform/forge/manifest-reference/).
