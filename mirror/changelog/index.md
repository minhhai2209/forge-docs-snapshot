# Forge changelog

**What’s changing**  
You can now build your [Rovo actions](https://developer.atlassian.com/platform/forge/manifest-reference/modules/rovo-action/ "https://developer.atlassian.com/platform/forge/manifest-reference/modules/rovo-action/") once and expose them as tools to both custom agents in Rovo Studio and third-party, MCP-enabled AI clients. This is made possible through the `rovo:mcp` module, which is now available in Preview.

With this capability, your Forge tools can reach users in external clients such as Claude Desktop, Codex, and Cursor. This allows you to bring Forge functionality into more AI-powered workflows without building separate integrations for every client. For example, a Rovo action that retrieves and summarizes Jira issues can now be made available in both Rovo Agents and external AI environments.

Admins remain in control of this connectivity:

* **Opt-in access**: External access is disabled by default and must be enabled separately for each app installation.
* **Unified control**: During Preview, enabling external access exposes all tools declared in the app’s `rovo:mcp` module.
* **Secure execution**: Users connect via OAuth, and every tool invocation respects their existing permissions on the Atlassian site.

**What you need to do**  
To start connecting your tools to external AI clients:

1. Define your tools in the `manifest.yml` file using the [rovo:mcp module](https://developer.atlassian.com/platform/forge/manifest-reference/modules/rovo-mcp/#connect-tools-to-third-party-ai-clients-eap "https://developer.atlassian.com/platform/forge/manifest-reference/modules/rovo-mcp/#connect-tools-to-third-party-ai-clients-eap").
2. Update your app to use the latest version of the Forge CLI to support the new module definitions.
3. Follow the [Build your first Rovo MCP tool](https://developer.atlassian.com/platform/forge/build-a-hello-world-rovo-mcp/#connect-to-a-third-party-ai-client-eap "https://developer.atlassian.com/platform/forge/build-a-hello-world-rovo-mcp/#connect-to-a-third-party-ai-client-eap") guide to set up the integration.
4. If you are building tools that interact with Jira data, refer to the [tutorial for reading Jira issues with MCP](https://developer.atlassian.com/platform/forge/read-jira-issues-with-a-rovo-mcp-tool/#connect-to-a-third-party-ai-client-eap "https://developer.atlassian.com/platform/forge/read-jira-issues-with-a-rovo-mcp-tool/#connect-to-a-third-party-ai-client-eap").
