# Packaging standard

This is an experimental [Early Access Program (EAP)](/platform/forge/whats-coming/#eap) feature, offered to selected users for testing
and feedback purposes. EAP features are unsupported, not usable in production environments, and subject to change without notice.

When using [manual packaging](/platform/forge/manifest-reference/packaging/), you must package the application code in a
format suitable for the Forge platform. This page describes these requirements
for both functions and UI Kit resources.

## Functions

The packaged directory (`app.package.path`) must contain all handlers referenced
by function modules in the app manifest.

For every function module with a handler `<path>.<export>`, there must be an
exported function `<export>` in a CommonJS module file `<path>.js` (or the same
path with a different extension that Node.js can load) inside the output
directory.

The handler string is `<path>.<export>`, where the two segments separated by the
dot are the relative file path (without extension) and the export name.

The export must be a function. Both a named export and a declaration like
`module.exports.<export>` satisfy this.

For example, the following manifest excerpt:

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
modules:
  trigger:
    - key: pickle
      function: main
      events:
        - avi:jira:updated:issue
  function:
    - key: main
      handler: cucumber/two.handler
app:
  package:
    bundler: manual@2026
    path: backend/dist
```

can be satisfied by having `backend/dist/cucumber/two.js` export a function
named `handler`.

File and directory names starting with double underscore, such as `__durian.js`,
are reserved and cannot be used by handlers.

## UI Kit

A UI Kit resource with manual packaging points via `path` at a target directory
containing the resource bundle. The directory must contain HTML files (see name
requirements below) and JavaScript files with the UI Kit code and assets
required by them.

For a single-entry resource, the HTML must be named `index.html`. For a
multi-entry resource, provide one HTML file per entry, named as declared in the
entry map. For example:

```
```
1
2
```



```
resources:
  - key: eggplant
    bundler: manual@2026
    path: frontend/eggplant/build  # must contain global.html and settings.html
    entry:
      global: global.html
      settings: settings.html
  - key: feijoa
    bundler: manual@2026
    path: frontend/feijoa/build  # must contain index.html
```
```

The HTML files must contain only the script references needed for the
particular resource in the body, using relative paths. For example,
`frontend/feijoa/build/index.html` could look like:

```
```
1
2
```



```
<!doctype html>
<html>
  <head></head>
  <body>
    <script type="module" src="./index.js"></script>
  </body>
</html>
```
```

The JavaScript files must:

* Not contain any JSX syntax; JSX must be transformed already using
  `React.createElement` pragma (for example, Vite `@vitejs/plugin-react`, Rollup
  `@rollup/plugin-babel`, or esbuild `--jsx-factory=React.createElement`).
* Define the application component according to UI Kit documentation in exactly
  one JavaScript file per resource.
* Use asset paths relative to the resource root. This is non-default for some
  tools; for example, Webpack and Vite default to an absolute `/` base and
  need `base: './'`.

File and directory names starting with double underscore, such as `__garlic.js`,
are reserved and cannot appear in the output directory.
