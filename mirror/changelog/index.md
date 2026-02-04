# Forge changelog

Support for dynamically retrieving the list of supported models is now available in Forge LLMs. The new `list` function in the [@forge/llm SDK](https://www.npmjs.com/package/@forge/llm/v/0.3.0 "https://www.npmjs.com/package/@forge/llm/v/0.3.0") lets apps fetch the latest list of models, returning a response like:

`{
 "models": [
{
"model": "claude-sonnet-4-20250514",
"status": "active"
},
{
"model": "claude-opus-4-20250514",
"status": "deprecated"
}
]
}`

You can filter on the `status` field to ensure your app always uses an **active** model and avoid breaking changes when a model is removed.

Forge LLMs remain in Early Access (EAP). Due to high demand, participation is limited. To request access, join the waitlist [here](https://go.atlassian.com/signup-forge-llms "https://go.atlassian.com/signup-forge-llms").

For implementation details, refer to the documentation [here](https://developer.atlassian.com/platform/forge/runtime-reference/forge-llms-api/#node-js-sdk "https://developer.atlassian.com/platform/forge/runtime-reference/forge-llms-api/#node-js-sdk").
