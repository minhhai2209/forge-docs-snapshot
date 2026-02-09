# Testing a containerised service locally (EAP)

Forge Containers are now available through Forge's Early Access Program (EAP). To start testing this feature,
submit your app's ID to our team [through this link](https://ecosystem.atlassian.net/servicedesk/customer/portal/1040/create/18884).

EAPs are offered to selected users for testing and feedback purposes. APIs and features under EAP
are unsupported and subject to change without notice. APIs and features under EAP are not recommended
for use in production environments.

For more details, see [Forge EAP, Preview, and GA](/platform/forge/whats-coming/#eap).

After [defining a containerised service](/platform/forge/containers-reference/managing-service), you can test it locally before you push its image to your container’s repository. You can then use `forge tunnel` to redirect app invocations from your development site to your local instance of the service.

To launch and run a service locally, you must have a docker engine installed.

## Set up docker compose for a local instance

To launch a container locally, you’ll need to set up its docker compose configuration. You can do this in the manifest through the container’s `tunnel` property, which follows the same syntax as a standard docker compose file.

Either `build` or `image` should be defined, but not both. All other `tunnel` fields are required, except for `environment`.

**`build` is defined**

Use `build` if you want to rebuild the image each time the tunnel is started. For example:

```
1
2
3
4
5
6
7
tunnel:
  docker:
    build:
      context: ./services/java-spring-server
      dockerfile: Dockerfile
    ports:
      - "8080:8080"
```

**`image` is defined**

Use `image` to define a pre-built image for the tunnel instead. For example:

```
```
1
2
```



```
tunnel:
  docker:
    image: java-service:${TAG}
    ports:
      - "8080:8080"
```
```

Running `forge tunnel` will then create a docker compose stack using the container’s `tunnel` configuration and the latest Forge Containers proxy sidecar. Terminating the tunnel will also clean up the compose stack.

You can add `tunnel` configurations for only a subset of containers. This lets you test and run some containers locally without the overhead of starting up all containers.
If you do this, however, any invocations to containers that *don’t* have a `tunnel` configuration set up will fail. We’re working on addressing this in a future milestone: <https://ecosystem.atlassian.net/browse/OIC-192>

## Optional: Set up a docker compose manually

Alternatively, you can manually set up the docker compose stack for one or more containers. This however, means you can’t include `tunnel` configurations for any containers in the manifest.

You can refer to our sample app for an implementation that uses this approach:

* The [docker-compose.yml](https://bitbucket.org/atlassian/forge-containers-app/src/main/docker-compose.yml) file configures the stack for the container that should be run locally.
* The [dev-loop.sh](https://bitbucket.org/atlassian/forge-containers-app/src/main/dev-loop.sh) script runs all the necessary steps to set up the tunnel. These include exporting the necessary environment variables, pulling the latest sidecar image, and launching `forge tunnel`.

To start, download the Forge Containers platform sidecar, available from the following repository: `forge-ecr.services.atlassian.com/forge-platform/proxy-sidecar:latest`

For example, to use `docker pull` (you may need to re-authenticate the Docker CLI first):

```
```
1
2
```



```
forge containers docker-login
docker pull forge-ecr.services.atlassian.com/forge-platform/proxy-sidecar:latest
```
```

After downloading the sidecar, you’ll need to launch it as a separate service to run locally. We recommend defining it as a separate containerised service dependent on the service you’re testing. This will allow you to build and launch both services together.
After configuring the sidecar and your service, build its image locally and launch it in the background. For example, using `docker compose`:

```
```
1
2
```



```
docker compose up --build -d
```
```

Once the docker compose is stack is created, you can now run `forge tunnel -e <environment>`.
