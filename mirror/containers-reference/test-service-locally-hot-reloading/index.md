# Set up hot reloading for containerised services (EAP)

Forge Containers are now available through Forge's Early Access Program (EAP). To start testing this feature,
submit your app's ID to our team [through this link](https://ecosystem.atlassian.net/servicedesk/customer/portal/1040/create/18884).

EAPs are offered to selected users for testing and feedback purposes. APIs and features under EAP
are unsupported and subject to change without notice. APIs and features under EAP are not recommended
for use in production environments.

For more details, see [Forge EAP, Preview, and GA](/platform/forge/whats-coming/#eap).

The Forge CLI allows *hot reloading*, letting you make code changes without having to manually rebuild and restart your containers. With hot reloading, you won't need to restart the tunnel either.

To enable hot reloading for a container, add any of the following [Docker Compose](https://docs.docker.com/compose/) properties to the `tunnel.docker` configuration in your manifest:

| Property | Description |
| --- | --- |
| `command` | Override the container's startup command at tunnel time. |
| `develop.watch` | Tell Docker Compose what to do when files on the host machine change. Each watch entry supports the standard Compose `action` (for example, `sync`, `rebuild`, `sync+restart`), `path`, and `target` fields. |
| `volumes` | Mount host paths into the container. If you use `develop.watch` with `action: sync`, you may not need a volume for source files because Compose synchronizes changed files to the configured `target`. |
| `working_dir` | Override the container's working directory for the command that runs during tunneling. |
| `environment` | Set development-only environment variables, such as verbose logging or framework-specific dev settings. |
| `ports` | Expose development-only ports, such as a Node.js inspector port (`9229:9229`) for attaching a debugger from VS Code. |

For example:

```
```
1
2
```



```
services:
  - key: express-server-service
    containers:
      - key: express-server-container
        tunnel:
          docker:
            build:
              context: ./services/express-server
              dockerfile: Dockerfile.dev
            ports:
              - '8080:8080'
            develop:
              watch:
                - path: ./services/express-server
                  target: /app
                  action: sync
        tag: ${TAG}
        resources:
          cpu: '1'
          memory: '2Gi'
        health:
          type: http
          route:
            path: /health
```
```

If a container's `tunnel.docker` config does **not** include a `develop` block, that container will be started normally (without hot reloading enabled). This means that some services can have hot reloading enabled while others do not.

Hot reloading typically requires a language/framework-specific setup inside the container itself (for example `nodemon` for Node.js, `spring-boot-devtools` for Java, etc.). Docker Compose's `watch` feature only handles getting the changed files into the container - it's up to the application runtime to detect and apply them.

## Example: Node.js with `nodemon`

We recommend using a separate development Dockerfile for hot reloading. This lets the development image start under `nodemon` by default, without changing the command used by your production image. A minimal example (without adding `USER` config) of a development Dockerfile can be seen below:

Sample `services/express-server/Dockerfile.dev`:

```
```
1
2
```



```
FROM node:24-alpine

# Must match the `target` of the develop.watch entry in manifest.yml.
WORKDIR /app
COPY package*.json ./

# Installs all dependencies - including nodemon (devDependency)
RUN npm install
COPY . .

EXPOSE 8080

# Development default used while tunneling.
CMD ["npm", "run", "dev"]
```
```

Sample `services/express-server/package.json`:

```
```
1
2
```



```
{
  "name": "express-service",
  "type": "module",
  "main": "index.js",
  "scripts": {
    "start": "node index.js",
    "dev": "nodemon index.js"
  },
  "dependencies": {
    "express": "^4.18.2"
  },
  "devDependencies": {
    "nodemon": "^3.0.0"
  }
}
```
```

The end-to-end flow when you save a `.js` file on your host machine is:

1. The `.js` file is synced from the host machine into `/app` inside the container (per the `develop.watch` entry in your `manifest.yml`).
2. `nodemon` (already running as the container's main process from the development Dockerfile's `CMD`) sees the file modification time update.
3. `nodemon` kills the existing Node process and re-runs `index.js` with the new code.

No container restart is required - everything happens inside the running container, which makes the reload near-instant. To deploy to production, no changes are needed: `forge deploy` ignores the container `tunnel` config, including the development Dockerfile, so the production image continues to use its normal Dockerfile and `CMD`.
