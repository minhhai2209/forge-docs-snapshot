# Forge changelog

The Forge bridge **invoke** method now supports an optional metadata argument. This allows you to receive additional information about an invocation, such as rate limiting details, alongside the response.

**What's changing**  
When you pass a **metadata** argument into the **invoke** function, it returns an object containing both a **body** field (the invocation response) and a **metadata** field. Any supported field set to **true** in the **metadata** argument will be returned within this **metadata** field.

Currently, **rateLimitProperties** is the only supported field in the metadata. This allows you to monitor rate limiting information for your invocations to better manage app performance and reliability.

**Example usage:**

`invoke('getText', { example: 'my-variable' }, { rateLimitProperties: true })
  .then(({ body, metadata }) => {
    
    console.log(JSON.stringify(metadata));
}`

**What you need to do**  
If you want to access invocation metadata, update your **invoke** calls to include the third **metadata** argument and handle the new response structure (**{ body, metadata }**).

Existing calls to **invoke** without the metadata argument remain unchanged and will continue to return the response body directly.

For more details, see the [Forge bridge invoke documentation](https://developer.atlassian.com/platform/forge/apis-reference/ui-api-bridge/invoke/ "https://developer.atlassian.com/platform/forge/apis-reference/ui-api-bridge/invoke/").
