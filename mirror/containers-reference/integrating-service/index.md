# Integrating containerised services (EAP)

Forge Containers are now available through Forge's Early Access Program (EAP). To start testing this feature,
submit your app's ID to our team [through this link](https://ecosystem.atlassian.net/servicedesk/customer/portal/1040/create/18884).

EAPs are offered to selected users for testing and feedback purposes. APIs and features under EAP
are unsupported and subject to change without notice. APIs and features under EAP are not recommended
for use in production environments.

For more details, see [Forge EAP, Preview, and GA](/platform/forge/whats-coming/#eap).

To enable invocations, your container service must have an exposed API. You can invoke this API from an *event,* the app’s front end, or the app’s back end.

## Define endpoints

To invoke your container service from an event or front end invocation, you’ll need to first define an *endpoint* module for your container service.

You can define multiple endpoint modules for your container services, with each one mapped to a specific HTTP URL path. Use the endpoint’s `route:path` property to define the path; it will be appended to the service’s base URL to call the desired endpoint.

For example:

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
16
17
18
19
services:
  - key: java-service
    containers:
      - key: java-container
        tag: ${TAG}
        resources:
          cpu: "1"
          memory: "2Gi"
        health:
          type: http
          route:
            path: /health

modules:
  endpoint:
    - key: event-invocation
      service: java-service
      route:
        path: /event-invocation
```

App components such as such as events, webtriggers, and `invokeService` can then invoke your app’s API through these endpoints.

## Build service integration

After defining your containerised service's endpoints, you can now build invocations to or from other capabilities:

## Test invocation locally

You can use `forge tunnel` to test your containerised service locally before pushing its image to Forge. See [Test service locally](/platform/forge/containers-reference/test-service-locally/) for information on how to set this up.

## View container logs

You can view logs for service invocations using the `forge logs --containers` command.
