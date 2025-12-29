# Use a long-running function

By default, [async event consumers](/platform/forge/runtime-reference/async-events-api/#event-consumer) time out after 55 seconds. Use cases that required longer computation have previously had to rely on breaking the task into multiple steps or batches, and [queuing multiple events](/platform/forge/queue-events-with-async-events-api-to-import-assets) to do the work.

You can now configure a timeout of up to 900 seconds (15 minutes) which will allow many such use cases to be performed in a single invocation.

### Use Case: Generating Reports from Jira Data

Imagine you are developing an application that generates detailed reports from Jira issues. This process can be time-consuming, especially if you are aggregating data from multiple projects and applying complex calculations. The Long-Running Compute feature allows you to handle these tasks efficiently without running into timeout issues.

## Before you begin

This tutorial assumes you're already familiar with developing on [Forge](/platform/forge) and the [Async Events API](/platform/forge/runtime-reference/async-events-api/).

Before you start, ensure you have the following:

* An Atlassian account with access to Forge.
* The Forge CLI installed on your machine.
* Basic knowledge of JavaScript and Forge development.

## Step 1: Set Up Your Forge Application

1. **Create a new Forge app:**

   Follow the prompts to set up your application. Name your app and choose the template appropriate to the type of app you are creating. For the purposes of this tutorial, we will use the `blank` template. Select the following options:

   * `context: Show All`
   * `category: Show All`
   * scroll down and choose `blank`

   If you intend to extend this example to use UI to trigger a long-running function, or display the results of your long-running function to the front end, you can select a template from the UI Kit or Custom UI category.
2. **Navigate to your app directory:**
3. **Add necessary permissions:**
   Open `manifest.yml` and add the required permissions to access Jira data:

   ```
   ```
   1
   2
   ```



   ```
   permissions:
     scopes:
       - read:jira-work
   ```
   ```

   If you chose the `blank` template, the existing `function` module in the manifest can be removed, along with the sample `src/index.js` file.

## Step 2: Create an event consumer

All long-running functions must be invoked by an [async event consumer](/platform/forge/runtime-reference/async-events-api/#event-consumer). Update the `manifest.yml` file to include the required event consumer module and corresponding function module:

```
```
1
2
```



```
modules:
  consumer:
    - key: queue-consumer-key
      # Name of the queue for which this consumer will be invoked
      queue: queue-consumer-name
      # Function to be called with payload
      function: generate-report
  function:
    - key: generate-report
      handler: generateReport.handler
      timeoutSeconds: 900
```
```

### Notes

* The function `generateReport.handler` will be invoked by the queue each time an event is pushed to it.
* The consumer module uses a [function](https://developer.atlassian.com/platform/forge/function-reference/index/) which has function value `generate-report` and method value `generate-report-event-listener`. The function value must match the key under the `function` module. The function must be defined in `generateReport.js` for the consumer to invoke it. This will be visible in the following section.

## Step 3: Implement the long-running function

**Create a new long-running function**:
In the `src` directory, create a new file called `generateReport.js`. This is where the long-running function is defined. The below long-running function will take 5 seconds to execute, however it can take up to 900 seconds until it gets timed out:

```
```
1
2
```



```
import { AsyncEvent } from '@forge/events';

export const handler = async (event, context) => {
    try {
        console.log("The handler has been invoked");
        const ret = await processGenerate(event);
        console.log(`The handler returned with: ${JSON.stringify(ret)}`);
        return ret;
    } catch (error) {
        console.error('Error in generate-report-event-listener:', error);
        throw error;
    }
};

export const processGenerate = async (event) => {
    const { projectKey } = event;
    
    if (!projectKey) {
        throw new Error('Project key is required but not provided in event payload');
    }

    // Simulate a long-running task
    const reportData = await generateReport(projectKey);
    return {
        statusCode: 200,
        body: reportData,
    };
};

const generateReport = async (projectKey) => {
    const issues = await fetchIssuesFromJira(projectKey);
    // Perform complex calculations and aggregations
    return performCalculations(issues);
};

const createMockIssuesFromJira = (projectKey) => ([
    { id: 1, key: `${projectKey}-1`, fields: { status: { name: 'Done' }, customfield_10016: 5 } },
    { id: 2, key: `${projectKey}-2`, fields: { status: { name: 'In Progress' }, customfield_10016: 3 } },
]);

const fetchIssuesFromJira = async (projectKey) => {
    try {
        // Simulate a delay for fetching data from Jira API
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        // Fetch real data from Jira API
        const response = await api.asApp().requestJira(
            route`/rest/api/3/search?jql=project=${projectKey}&maxResults=100`
        );
        
        if (!response.ok) {
            console.log(`API request failed, using mock data. Status: ${response.status}`);
            // Fallback to mock data if API call fails
            return createMockIssuesFromJira(projectKey);
        }
        
        const data = await response.json();
        return data.issues || [];
    } catch (error) {
        console.error('Error fetching issues from Jira:', error);
        // Return mock data as fallback
        return createMockIssuesFromJira(projectKey);
    }
};

const performCalculations = (issues) => {
    // Aggregate data from real Jira issues
    const statusCounts = {};
    let totalStoryPoints = 0;
    let issuesWithPoints = 0;

    issues.forEach(issue => {
        const status = issue.fields?.status?.name || 'Unknown';
        statusCounts[status] = (statusCounts[status] || 0) + 1;
        
        // Story points are often in customfield_10016, but this varies by instance
        const storyPoints = issue.fields?.customfield_10016 || 0;
        if (storyPoints > 0) {
            totalStoryPoints += storyPoints;
            issuesWithPoints++;
        }
    });

    return {
        totalIssues: issues.length,
        statusBreakdown: statusCounts,
        totalStoryPoints,
        averageStoryPoints: issuesWithPoints > 0 ? 
            Math.round((totalStoryPoints / issuesWithPoints) * 100) / 100 : 0,
        reportGeneratedAt: new Date().toISOString()
    };
};
```
```

## Step 4: Create a trigger to invoke the long-running function

There are many ways to invoke a function which will push events to the consumer queue, however a simple one we will use is a [trigger](/platform/forge/manifest-reference/modules/trigger/#trigger).

1. Create a new file `src/pushToQueue.js` with the following code:

   ```
   ```
   1
   2
   ```



   ```
   import { Queue } from "@forge/events";

   export const handler = async (event, context) => {
       try {
           const queue = new Queue({key: "queue-consumer-name"});

           // Extract project key from the Jira issue update event
           const projectKey = event.issue?.fields?.project?.key;
           
           if (!projectKey) {
               console.error('No project key found in event payload');
               return {
                   statusCode: 400,
                   statusText: "Bad Request - No project key found"
               };
           }

           console.log(`Pushing an event to the queue for project: ${projectKey}`);
           const { jobId } = await queue.push({ 
               body: { 
                   projectKey: projectKey,
                   issueKey: event.issue?.key,
                   triggeredAt: new Date().toISOString()
               } 
           });
           console.log(`Queued job ${queue.key}#${jobId}`);

           return {
               statusCode: 200,
               statusText: "Success"
           };
       } catch (error) {
           console.error('Error in pushToQueue handler:', error);
           return {
               statusCode: 500,
               statusText: "Internal Server Error"
           };
       }
   }
   ```
   ```
2. Update `manifest.yml` to include a new trigger module, and extend the current function module. The event which will invoke the trigger is `avi:jira:updated:issue`. This means every time an issue is updated, the trigger is invoked and `pushToQueue.handler` is called. Your `manifest.yml` file should now look like this:

   ```
   ```
   1
   2
   ```



   ```
   modules:    
     consumer:
       - key: queue-consumer-key
         queue: queue-consumer-name
         function: generate-report
     trigger:
       - key: invoke-lrf-when-jira-issue-updated
         function: push-to-queue
         events:
           - avi:jira:updated:issue
     function:
       - key: generate-report
         handler: generateReport.handler
         timeoutSeconds: 900
       - key: push-to-queue
         handler: pushToQueue.handler
   ```
   ```

## Step 5: Deploy Your Application

1. **Install required dependencies:**
   Since in this tutorial the `blank` template was chosen, there are no pre-installed dependencies.

   ```
   ```
   1
   2
   ```



   ```
   npm install @forge/events
   ```
   ```
2. **Deploy your Forge app:**
3. **Install the app in your Jira instance:**

## Step 6: Invoke the Long-Running Function

Update any Jira issue to invoke the long-running function! The `console.log` statements executed can be seen in the terminal if running `forge tunnel` or in the developer console if not. You can also see them by running `forge logs`. To see the output of the long-running function on your frontend, build a UI Kit or [Custom UI](/platform/forge/build-a-custom-ui-app-in-jira/) app.

### **Expected output**

If you have an active `forge tunnel` running, the expected output is as follows:

```
```
1
2
```



```
invocation: ... pushToQueue.handler
INFO    14:30:01.146  ...  Pushing an event to the queue for project: DEMO
INFO    14:30:01.589  ...  Queued job queue-consumer-name#...

invocation: ... generateReport.handler
INFO    14:30:02.506  ...  The handler has been invoked
INFO    14:30:04.508  ...  The handler returned with: {"statusCode":200,"body":{"totalIssues":25,"statusBreakdown":{"Done":10,"In Progress":8,"To Do":7},"totalStoryPoints":42,"averageStoryPoints":3.5,"reportGeneratedAt":"2025-01-11T14:30:04.508Z"}}
```
```

The `...` replaces anywhere an id is used in the log output. Your output will have real values and may vary depending on your Jira project data.

## Conclusion

Long-running functions allow Forge developers to handle complex and time-consuming tasks efficiently. By following this tutorial, you have learned how to set up a realistic use case for generating reports from Jira data.
