# Extending your app with a scheduled trigger

You can configure a scheduled trigger for your existing app to repeatedly invoke a function on a scheduled interval.

This guide assumes you have an app with a [function](/platform/forge/manifest-reference/modules/function)
that you would like to trigger on a schedule.
If you haven’t already created a function, see [Getting started](/platform/forge/getting-started/)
for step-by-step instructions on setting up Forge and creating your first app.

**Development Workflow**
Scheduled triggers are perfect for automation tasks like data synchronization, periodic cleanup, monitoring, and background processing. Consider your use case carefully as the shortest interval is 5 minutes.

## Add a web trigger

To develop your function, create a temporary web trigger to invoke your function manually while testing.
Add a [web trigger](/platform/forge/manifest-reference/modules/web-trigger/) module to your
`manifest.yml` as follows:

```
1
2
3
4
5
6
modules:
  webtrigger:
    - key: temporary-development-webtrigger
      function: '<your-function-key>'
      response:
        type: dynamic
```

**Web Trigger for Development**
Web triggers are essential during development as they allow you to test your function immediately without waiting for the scheduled interval. Keep this in mind when designing your function - avoid hardcoding scheduled-specific logic.

## Deploy and install your app

You'll need to redeploy your app to add the web trigger module. If this is the first
time you're deploying your app, you'll also need to install the app on an Atlassian site.

1. Navigate to the app's top-level directory and deploy your app by running:
2. Install your app by running:
3. Select your Atlassian context using the arrow keys and press the enter key.
4. Enter the URL for your development site. For example, *example.atlassian.net*.
   [View a list of your active sites at Atlassian administration](https://admin.atlassian.com/).

Once the *successful installation* message appears, your app is installed and ready
to use on the specified site.
You can always delete your app from the site by running the `forge uninstall` command.

## Develop your app using the web trigger

Iterate through your function’s development by invoking the function using the web trigger.

The `event` parameter does not have a value for scheduled triggers, so you should avoid referencing it
in your function.

1. Get the web trigger URL by running:

   1. Select the installation for the corresponding site, Atlassian app, and Forge environment.
   2. Select the web trigger function that you want the URL for. The options come from the manifest.

   You'll be provided with a URL that you can use to invoke the web trigger. See
   [webtrigger](/platform/forge/cli-reference/webtrigger/) for more information about
   the `forge webtrigger` command.

   By default, the URLs provided by `forge webtrigger` have no built-in authentication. As such, anyone can use the URL (and, by extension, invoke its related function) without providing an authentication token. You should keep these URLs secure.

   Alternatively, you can also implement authentication inside the trigger itself. For example, you can add a check for an `Authorization` header in the request and validate any provided token.
2. Start your app using the tunnel to get fast feedback without needing to redeploy.
   Run the following command:
3. Make a request to the URL provided by `forge webtrigger` in a web browser or using the `curl` utility.

`forge tunnel` is only available in the `development` environment. See the *environment restrictions*
on the [environments and versions](/platform/forge/environments-and-versions/#environment-restrictions)
page for details.

## Add a scheduled trigger and remove the web trigger

Once you have completed development of the function, you can add a scheduled trigger to your `manifest.yml`:

```
```
1
2
```



```
modules:
  scheduledTrigger:
    - key: my-scheduled-trigger
      function: '<your-function-key>'
      interval: hour
```
```

**Interval Selection & Deployment**
Choose your interval carefully - `fiveMinute` is the shortest available and should only be used for critical, lightweight operations. Remember that any changes to scheduled trigger modules will reset all triggers and their start times.

While debugging, you can keep using the web trigger and scheduled trigger. When you’re
done, you can remove the web trigger module from the manifest file.

To make your changes permanent, redeploy your app using the `forge deploy` command.

## Frequently asked questions

**Key Scheduled Trigger Facts**

* Maximum 5 scheduled triggers per app
* Starts ~5 minutes after deployment
* Supports intervals: 5min, 1hr, 1day, 1week
* Functions run without user context
* Errors don't trigger retries

**Q: What intervals are available for scheduled triggers?**
A: Scheduled triggers support four intervals: `fiveMinute`, `hour`, `day`, and `week`. Choose the interval that best fits your use case and performance requirements.

**Q: How many scheduled triggers can I have in my app?**
A: You can declare up to five scheduled triggers in your `manifest.yml` file.

**Q: When do scheduled triggers start running?**
A: Scheduled triggers start approximately 5 minutes after app deployment. Each trigger is scheduled to start shortly after it is created.

**Q: Can I change the interval of a scheduled trigger after deployment?**
A: Yes, but you'll need to redeploy your app. Note that any changes to scheduled trigger modules will reset all scheduled triggers and their start times.

### Development and testing

**Q: Why do I need a web trigger during development?**
A: Web triggers allow you to manually invoke your function for testing without waiting for the scheduled interval. This makes development and debugging much faster.

**Q: Can I keep both web trigger and scheduled trigger during development?**
A: Yes, you can use both simultaneously during development. Once you're satisfied with your function, you can remove the web trigger module from your manifest.

**Q: What happens if my function throws an error?**
A: If a scheduled trigger function throws an error, nothing will happen and the function will not be retried. The function will be invoked again at the next scheduled interval.

**Q: How do I set up a scheduled trigger for my Jira Forge app every 5 minutes?**
A: To set up a 5-minute scheduled trigger for your Jira Forge app, add the following to your `manifest.yml`:

```
```
1
2
```



```
modules:
  scheduledTrigger:
    - key: jira-five-minute-trigger
      function: 'your-function-key'
      interval: fiveMinute
  function:
    - key: your-function-key
      handler: index.handler
```
```

Make sure to replace `your-function-key` with the actual key of your function. The `fiveMinute` interval is the shortest available interval for scheduled triggers in Forge.

**Q: Can I set up a scheduled trigger for my Jira Forge app every 1 minute?**
A: No, Forge doesn't support 1-minute intervals. The shortest available interval is `fiveMinute`. If you need more frequent execution, consider these alternatives:

1. **Use the 5-minute interval** - This is the fastest option available
2. **Implement custom logic** - Use Forge storage to track time and execute logic conditionally within your 5-minute function. See the [forge-scheduler](https://github.com/kannonboy/forge-scheduler) example for a complete implementation
3. **Web triggers with external scheduling** - Use external services (like cron jobs) to call your web trigger endpoints
4. **Real-time events** - Consider using [Jira webhooks](/platform/forge/events-reference/jira/) or [event listeners](/platform/forge/events-reference/app-events/) for immediate responses instead of scheduled triggers

For most use cases, the 5-minute interval provides sufficient frequency while maintaining good performance and staying within platform limits.
