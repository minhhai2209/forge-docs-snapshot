# Packaging

This is an experimental [Early Access Program (EAP)](/platform/forge/whats-coming/#eap) feature, offered to selected users for testing
and feedback purposes. EAP features are unsupported, not usable in production environments, and subject to change without notice.

# Packaging

By default, Forge packages your application code before uploading by compiling
TypeScript and bundling the application dependencies using Webpack.

To use a different compiler, bundling solution, or configuration, you can switch
your application to manual packaging.

You can use manual packaging to let Forge CLI upload the code from the specified
directory without modifications. This allows you to:

* Use a different compiler or TypeScript version
* Change Webpack configuration, use no bundler or a different bundler
* Include and call WebAssembly in your application
* Require data files, or depend on packages that do

Manually packaging the application can also reduce the application size when it
has many dependencies used across multiple functions.

Manual packaging is available for the Forge functions as well as UI Kit.

When using manual packaging, Forge CLI does not process the code to upload.
Therefore, it does not catch errors related to wrong types, missing variables, or
dependencies. These errors will instead cause the application to crash or
misbehave when it runs.

## Functions

To use manual packaging for the [functions](/platform/forge/function-reference/),
set the following `app.package` properties in the manifest:

```
```
1
2
```



```
app:
  package:
    bundler: manual@2026
    path: out  # target directory with files to upload
```
```

Put the application backend code into the target directory (`out` above).

All the application's functions will be manually packaged. You cannot
selectively keep the automatic packaging behavior for a subset of them.

Manual packaging for the Forge functions requires the dependencies of the
application, typically in `node_modules`, to be available in the directory to be
uploaded as well, unless the dependency code is bundled together with the
application code into a single file. Ensure the required dependencies are
present in the target directory so they can be imported from the application
code.

See the [standard](/platform/forge/manifest-reference/packaging/standard/#functions)
for the full requirements to package the functions.

## UI Kit

To use manual packaging for a [UI Kit](/platform/forge/ui-kit/) resource, add the
`bundler` property to the individual resource and set `path` to a directory
containing the assets.

```
```
1
2
```



```
resources:
  - key: broccoli
    bundler: manual@2026
    path: frontend/broccoli/out
```
```

See the [standard](/platform/forge/manifest-reference/packaging/standard/#ui-kit)
for the full requirements to package the UI Kit resources.

## Tunneling

`forge tunnel` watches the target directory for changes, not the application
code. While tunneling, you need to run your own build process in watch mode
alongside Forge CLI to see changes reflected in the running application.

## Examples

### Plain TypeScript on the backend

To use the TypeScript compiler on the backend without Webpack:

1. In an existing Forge app, change `tsconfig.json` to output the compiled code
   to the `dist` directory:

```
```
1
2
```



```
{
  // ...
  "compilerOptions": {
    // ...
    "outDir": "./dist"
  }
}
```
```

2. Enable manual packaging in `manifest.yml`:

```
```
1
2
```



```
# ...
app:
  # ...
  package:
    bundler: manual@2026
    path: dist
```
```

3. Create scripts to package the application and its dependencies in
   `package.json`:

```
```
1
2
```



```
{
  // ...
  "scripts": {
    // ...
    // Install production dependencies into the target directory
    "build:dependencies": "yarn install --production --modules-folder ./dist/node_modules",
    // Compile the application
    "build": "tsc --project ./tsconfig.json"
  }
}
```
```

4. Run `yarn build:dependencies` whenever dependencies change, and `yarn build`
   before deploying the application, for example, on CI:

```
```
1
2
```



```
yarn build:dependencies
yarn build
forge deploy
```
```

5. For local testing via Forge tunnel, run the compiler in watch mode:

```
```
1
2
```



```
yarn build --watch
# separately (for example, in another terminal)
forge tunnel
```
```

### Bundling multi-entry frontend with Vite

The following example app with a custom Vite bundler has the structure:

```
```
1
2
```



```
.
├── manifest.yml
├── package.json
├── tsconfig.json
├── src
│   ├── index.ts
│   ├── resolvers/
│   └── frontend/
│       ├── package.json
│       ├── tsconfig.json
│       ├── vite.config.ts
│       ├── home.html
│       ├── settings.html
│       └── src
│           ├── Home.tsx
│           └── Settings.tsx
```
```

The `frontend` directory contains the frontend resource files, including the bundler config (Vite in this example), the HTML shells for each entry point, and the UI Kit files in the `src` directory. This resource has two entry points: `home` and `settings`.

To produce a frontend bundle with Vite:

1. In an existing Forge app, enable manual packaging for a UI Kit resource in `manifest.yml`:

```
```
1
2
```



```
resources:
  - key: prebuilt-multi
    path: prebuilt-multi/dist # output directory with compiled code
    bundler: manual@2026 # enable manual packaging
    entry:
      home: home.html
      settings: settings.html
    tunnel:
      port: 3000
```
```

2. Add HTML files that load a UI Kit file for each entry point.

**home.html**

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
    <script type="module" src="./src/Home.tsx"></script>
  </body>
</html>
```
```

**src/Home.tsx**

```
```
1
2
```



```
import React, { useEffect, useState } from 'react';
import ForgeReconciler from '@forge/react';
import { Text } from '@forge/react';
import { invoke } from '@forge/bridge';

export const Home = ({ title }: { title: string }) => {
  const [data, setData] = useState<string | null>(null);

  useEffect(() => {
    invoke('getText', { example: 'my-invoke-variable' }).then((response) => {
      setData(response as unknown as string);
    });
  }, []);

  return (
    <>
      <Text>{title}</Text>
      <Text>{data ?? 'Loading...'}</Text>
    </>
  );
};

ForgeReconciler.render(
  <React.StrictMode>
    <Home title="Hello from the Home page!" />
  </React.StrictMode>
);
```
```

3. Add a Vite config file `vite.config.ts`. The config sets the `base` path to be relative to the root, and configures build settings for the output bundle that is referenced by the resource in the manifest. It also configures a local development server to be used when tunneling the app.

```
```
1
2
```



```
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { resolve } from 'path';

export default defineConfig({
  root: resolve(__dirname),
  plugins: [react()],
  base: './',
  build: {
    outDir: resolve(__dirname, 'dist'),
    emptyOutDir: true,
    rollupOptions: {
      input: {
        home: resolve(__dirname, 'home.html'),
        settings: resolve(__dirname, 'settings.html')
      }
    }
  },
  server: {
    // Port specified as the tunnel port for the deployed resource
    port: Number(process.env.DEV_SERVER_PORT) || 3000,
    strictPort: true,
    host: 'localhost'
  }
});
```
```

4. Create scripts to package the application and its dependencies in
   `package.json`:

```
```
1
2
```



```
{
  // ...
  "scripts": {
    // compile app into dist directory
    "build": "vite build --config vite.config.ts",
    // start dev server for tunneling
    "dev": "vite --config vite.config.ts"
  }
}
```
```

5. Run `yarn build` before deploying the application, for example, on CI:

```
```
1
2
```



```
yarn build
forge deploy
```
```

6. For local testing via Forge tunnel, run the development server on the port specified in `manifest.yml` as the tunnel port for the resource. Then run the Forge tunnel in another terminal:

```
```
1
2
```



```
yarn dev
# separately (for example, in another terminal)
forge tunnel
```
```
