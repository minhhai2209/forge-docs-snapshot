# Use Async Events API to queue jobs to import objects into Assets

This tutorial describes how to divide your Assets import data into smaller submission chunks to avoid hitting the async events invocation runtime limit of Forge. Refer to forge documentation for more details on the [invocation limits](/platform/forge/platform-quotas-and-limits/#invocation-limits). The app you will create as a part of this tutorial uses the Async Events API to queue events that fetch and send data to Assets via the Imports REST API. You will also get exposed to the Forge Storage API through this tutorial.

## Before you begin

This tutorial assumes you're already familiar with developing an Assets Import app on Forge and the Imports REST API for Assets. If not, see [Import third party data into Assets](/platform/forge/assets-import-app/) and [Imports REST API Guide](/cloud/assets/imports-rest-api-guide/workflow/).

### Understanding the approach

In this app, we are focusing on how to import data into Assets without being bound by the invocation time limit. To overcome this, the import job needs to be divided into smaller tasks that take less than the time limit to finish and we leverage the Forge events package to queue and execute these tasks.

For example, if the third-party service contains 100 objects to be imported into Assets and the third-party API only returns a paginated response of 10 objects per read request, the Forge app in this tutorial will divide the import job into 10 tasks that will be handled by the Forge events package. Each of the tasks will:

1. Fetch 10 objects from the source (the third-party service API).
2. Transform the 10 objects into the shape that Assets expects.
3. Submit the 10 transformed objects to Assets using the Imports REST API.
4. Queue another event to execute the same task to handle the next 10 objects until all 100 objects are consumed.

![Sequence diagram to explain the approach.](https://dac-static.atlassian.com/platform/forge/images/jsm-assets-import/queues-diagram.png?_v=1.5800.1783)

### Known platform limitations

Since we are mainly leveraging the Forge Async Events API, there are platform limitations around this library that we should be aware of. To view the full list, see [Platform quotas and limit](/platform/forge/platform-quotas-and-limits/).

The most notable limitation of the Async Events API in our use case is the 1000-depth limit for cyclic invocations.

A cyclic invocation is when an event resolver pushes a new event into the queue and thus creating a cycle, which is what we are implementing in this guide.

If your use case requires the cyclic invocation limit to be increased, you can visit the [Platform quotas and limit - Apps exceeding quotas or limits](/platform/forge/platform-quotas-and-limits/#apps-exceeding-quotas-or-limits) for more details on how to request for the limit for your app to be raised.

Async events also have a higher invocation time limit than other types of invocations. For more details, see [Forge invocation limits](/platform/forge/platform-quotas-and-limits/#invocation-limits).

## Create your app

1. Navigate to the directory where you want to create the app.
2. Create your app by running:
3. Enter a name for the app. For example, *assets-import-app*.
4. Select the *UI Kit* category, and then the *Jira Service Management* Atlassian app.
5. Select the *jira-service-management-assets-import-type* template from the list.
6. Navigate to the top-level of your app directory and install the packages for Forge UI, Forge events and Forge resolvers:

   ```
   ```
   1
   2
   ```



   ```
   npm install @forge/react@latest @forge/events@latest @forge/resolver@latest @forge/bridge@latest @forge/kvs@latest --save
   ```
   ```

## Update the manifest

Since this app uses [Forge Storage API](/platform/forge/runtime-reference/storage-api/), we will need to update the manifest to include the following scope:

```
```
1
2
```



```
permissions:
  scopes:
    - import:import-configuration:cmdb
    - storage:app # scope required to use Forge Storage
```
```

We also need to set up the queues that will submit the data to Assets and mark the data submission process as completed following [Forge's guide on how to use Async Events API](/platform/forge/runtime-reference/async-events-api/).

```
```
1
2
```



```
modules:
  jiraServiceManagement:assetsImportType:
    ...

  consumer:
    - key: submit-data-chunk-queue-consumer
      queue: submit-data-chunk-queue
      resolver:
        function: processImportQueue
        method: submit-data-chunk-queue-listener
    - key: import-completed-queue-consumer
      queue: import-completed-queue
      resolver:
        function: importCompletedHandler
        method: import-completed-queue-listener

  function:
    - key: processImportQueue
      handler: index.processQueue
      timeoutSeconds: 900
    - key: importCompletedHandler
      handler: index.processQueue
      timeoutSeconds: 900
    ...
```
```

We are making API requests to external services that are not a part of Atlassian. The `permissions` property in the manifest needs to be extended to include egress control, defining the external domains our app sends requests to and reads data from.

```
```
1
2
```



```
permissions:
  scopes:
    ...

  external:
    fetch:
      backend:
        - "example.com" # replace this URL with that of your third-party service
```
```

## Create a new mapping for the import on app configuration submission

Imports REST workflow requires the user to define a mapping between the data source fields and the destination object type attributes in Assets.

We can make a request to Assets to create a new mapping for the import when the user finishes configuring the Forge app.

To do this, navigate to the `src/frontend/index.jsx` file and change the `onSubmit` function in the `App` component.

```
```
1
2
```



```
import { requestJira } from '@forge/bridge';
import { useForm, Form, Button, FormSection, FormFooter } from "@forge/react";
import { FullContext } from '@forge/bridge/out/types';
  ...
const App = () => {
  ...
  const [context, setContext] = useState<FullContext | undefined>(undefined);
  useEffect(() => {
        if (!context) {
            view.getContext().then(setContext);
        }
    }, [context]);

  const { handleSubmit } = useForm()
  const onSubmit = async () => {
    const {
        extension: { workspaceId, importId },
    } = context;
    await requestJira(`/jsm/assets/workspace/${workspaceId}/v1/importsource/${importId}/mapping`,
        {
          method: "PUT",
          body: JSON.stringify(/* TODO provide your mapping here */),
          headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
          },
        }
      );

      // should capture error, throw Error and handle error state here if required.
  };

    return (
    <Form onSubmit={handleSubmit(onSubmit)}>
      <FormSection>
        ...
      </FormSection>
      <FormFooter>
        <Button appearance="primary" type="submit">
          Save configuration
        </Button>
      </FormFooter>
    </Form>
  );
};
```
```

## Submit data to Assets using Forge events

In Step 2, we have defined in the manifest file the queues to which we will push the events.

To consume the queue events, we now need to define the resolver.

Navigate to `src/resolvers/index.js` and instantiate the queues like below.

```
```
1
2
```



```
export const importQueue = new Queue({ key: "submit-data-chunk-queue" });
export const importCompletedQueue = new Queue({
  key: "import-completed-queue",
});
```
```

Navigate to the `startImport` function in `src/resolvers/index.jsx` and add the following logic.

```
```
1
2
```



```
const getImportQueueJobsStorageKey = (importId) =>
  "import-" + importId + "_import-queue_jobs";

const startImport = async (context) => {
  // create a new execution
  const newlyCreatedExecution = await api
    .asUser()
    .requestJira(
      route`/jsm/assets/workspace/${context.workspaceId}/v1/importsource/${context.importId}/executions`,
      {
        method: "POST",
      }
    );

  const newlyCreatedExecutionJson = await newlyCreatedExecution.json();

  // the response is a set of links which contain a UUID that represents the execution
  // hence, we need to extract it
  const executionId = extractExecutionId(
    newlyCreatedExecutionJson.links.submitResults
  );

  // Set up our queue jobs tracker
  await kvs.set(getImportQueueJobsStorageKey(importId, 0), []);

  // Push a single event with JSON payload
  const jobId = await importQueue.push({ body: {
    workspaceId,
    importId,
    executionId,
    start: 0,
    end: apiPageLimit,
  } });

  return {
    result: "start import",
  };
};
```
```

Now that we have successfully queued our first job, we need to implement the resolver for that job. Go back to the `src/resolvers/index.js` file created at the beginning and add the following code.

```
```
1
2
```



```
const getImportQueueJobsStorageKey = (importId) =>
  "import-" + importId + "_import-queue_jobs";

resolver.define(
  "submit-data-chunk-queue-listener",
  async ({ payload, context }) => {
    const { workspaceId, importId, executionId, start, end } = payload;

    // keep track of all the jobs we have queued so far so we can check if they have finished successfully later
    // when we need to mark the execution as completed
    const jobs =
      (await kvs.get(getImportQueueJobsStorageKey(importId))) || [];
    const newJobs = jobs.concat(context.jobId);
    await kvs.set(getImportQueueJobsStorageKey(importId), newJobs);

    // fetch paged response for objects to import from 3rd party source
    const options = {
      method: "GET",
      headers: { "Content-Type": "application/json" },
    };
    const get3rdPartyDataResponse = await api.fetch(
      "https://example.com/GET", // TODO replace this with your 3rd party API
      options
    );

    // calculate the payload for the next job to be queued
    const nextJobPayload = {
      workspaceId,
      importId,
      executionId,
      start: end + 1,
      end: end + /* TODO insert number of objects per paginated request */, 
    };

    if (get3rdPartyDataResponse.hasNext) {
      // trigger this event listener again
      importQueue.push({ body: nextJobPayload });
    } else {
      // all jobs have finished and mark import as done
      // the details of this queue will be answered in Step 5
      importCompletedQueue.push({ body: { workspaceId, importId, executionId } });
    }

    const transformedData = transform3rdPartyData(get3rdPartyDataResponse.data); /* TODO transform3rdPartyData will need to be implemented by you */

    // send data chunk to Assets
    await api
      .asApp()
      .requestJira(
        route`/jsm/assets/workspace/${workspaceId}/v1/importsource/${importId}/executions/${executionId}/data`,
        {
          method: "POST",
          body: JSON.stringify({
            data: { /* TODO insert your transformed third-party data here */ },
          }),
          headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
          },
        }
      );
  }
);
```
```

## Mark data submission as completed

Once all the data chunks have been submitted (i.e. `get3rdPartyDataResponse.hasNext` should be `false`), we push a new event to the `importCompletedQueue` or Queue 2 in the diagram. This is to mark the data submission as completed so that Assets knows to start processing the data, reading and writing it to our database.

In the same `src/resolvers/index.js` file, we add another resolver to handle marking our data submission as completed.

```
```
1
2
```



```
resolver.define(
  "import-completed-queue-listener",
  async ({ payload, context }) => {
    const { workspaceId, importId, executionId } = payload;

    // Check if all jobs have finished successfully
    const jobs = await kvs.get(getImportQueueJobsStorageKey(importId));
    let allJobsSucceed = true;

    for (i = 0; i < jobs.length; i++) {
      const jobId = jobs[i];
      const jobProgress = importQueue.getJob(jobId);
      const { success, inProgress, failed } = await jobProgress.getStats();

      // If a job to submit data to Assets is still in progress, we continue to wait
      // by pushing a new event to the same queue
      if (inProgress) {
        allJobsSucceed = false;
        // we can add how long to wait until this event is picked up by the resolver
        importCompletedQueue.push({ body: { workspaceId, importId, executionId }, delayInSeconds: /* TODO insert the amount of time to wait*/ });

        break;
      }

      if (failed) {
        // TODO we can handle the case that a data submission for some reason failed here...
      }
    }

    if (allJobsSucceed) {
      console.log("All jobs have succeeded, marking import as COMPLETED...");
      // If all jobs have finished, mark data chunk submission as completed
      const submitResponse = await api
      .asApp()
      .requestJira(
        route`/jsm/assets/workspace/${workspaceId}/v1/importsource/${importId}/executions/${executionId}/data`,
        {
          method: "POST",
          body: JSON.stringify({
            completed: true
          }),
          headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
          },
        }
      );
    }
  }
);
```
```

## Test and deploy your app

That’s it! All of the pieces of code required for the import queues to work are in place. It’s time to deploy and test our changes!

You can run the app on your local machine and see logs in real time via the terminal using:

Once you have tested that all the functionality is working as intended, you can deploy your app by running:

Now you have a working Assets Import app that can handle a larger number of import records because they have been broken down into smaller chunks!

![Assets import app backed by Forge Async Events runs when an user click 'Start Import' in Import tab.](https://dac-static.atlassian.com/platform/forge/images/jsm-assets-import/import-app-running.gif?_v=1.5800.1783)

## Developing for Atlassian Government Cloud

This content is written with standard cloud development in mind. To learn about developing for Atlassian Government Cloud, go to our [Atlassian Government Cloud developer portal](https://developer.atlassian.com/platform/framework/agc/).
