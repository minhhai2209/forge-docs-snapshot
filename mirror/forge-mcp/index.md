# Get started with the Forge MCP Server (preview)

This section describes a Forge *preview* feature. Preview features are deemed stable;
however, they remain under active development and may be subject to shorter deprecation
windows. Preview features are suitable for early adopters in production environments.

We release preview features so partners and developers can study, test, and integrate
them prior to General Availability (GA). For more information,
see [Forge release phases: EAP, Preview, and GA](/platform/forge/whats-coming/#preview).

The Forge MCP Server is a remote Model Context Protocol (MCP) server that exposes authoritative Forge and Atlassian Cloud knowledge to coding agents and AI-powered IDEs. It’s designed to help developers using tools like Cursor, VS Code, or Rovo Dev CLI get grounded, detailed, searchable context for their developer agents.

## What is the Forge MCP Server?

The Forge MCP Server provides Forge-specific knowledge and search as APIs, making it easy for AI coding agents to access:

* **How-to guides**: Provide information about building Forge apps and code snippets for common Forge tasks.
* **Module catalogs**: Recommend the right modules, manifest shapes, scopes, and backend patterns for your use case.
* **Manifest guidance**: Help with manifest structure, scopes, and permissions.
* **Forge document search**: Answer technical questions about Forge and Atlassian Cloud APIs using up-to-date knowledge bases.
* **Agent-friendly APIs**: Structure results so agents can turn guidance into working code.

Unlike general-purpose APIs, this server is aimed at developers working in AI-powered IDEs and code editors, not conversational AI chat platforms.

## Who is it for?

* Developers building Forge apps in IDEs like Cursor or VS Code.
* Teams using AI-powered coding assistants that support the MCP protocol like Rovo Dev CLI.
* Anyone who wants to accelerate Forge app development with reliable, context-aware guidance.

## What’s not included

* The Forge MCP server does not replace the Forge CLI. You’ll still use the CLI for tasks like tunneling, bundling, and deploying your app.
* It does not perform local file system actions or run CLI commands on your behalf.

## Prerequisites

Before you start, make sure you have:

* Node.js v18+ installed (for running the MCP proxy if needed).
* A supported AI-powered IDE (for example, Rovo Dev CLI, Cursor, VS Code) or another MCP-compatible client.

## Connecting your IDE to the Forge MCP server

### Rovo Dev CLI

To connect Rovo Dev CLI to the Forge MCP server, follow the [instructions in our support documentation](https://support.atlassian.com/rovo/docs/connect-to-an-mcp-server-in-rovo-dev-cli/).

Add the following configuration to your `~/.rovodev/mcp.json` file:

```
```
1
2
```



```
{
  "mcpServers": {
    "forge-knowledge": {
      "url": "https://mcp.atlassian.com/v1/forge/mcp",
      "transport": "http"
    }
  }
}
```
```

### Cursor

1. Open Cursor’s MCP settings panel.
2. Add the following configuration:

```
```
1
2
```



```
{
  "mcpServers": {
    "forge-knowledge": {
      "url": "https://mcp.atlassian.com/v1/forge/mcp"
    }
  }
}
```
```

For older versions of Cursor, you may need to use a command-based configuration. See the [Cursor MCP documentation](https://docs.cursor.com/en/context/mcp) for details.

3. Save and restart Cursor’s AI assistant or tools pane.

### VS Code

Add a `mcp.json` file manually:

* Create a `mcp.json` file in your workspace or home directory:

```
```
1
2
```



```
{
  "servers": {
    "forge-knowledge": {
      "url": "https://mcp.atlassian.com/v1/forge/mcp",
      "type": "http"
    }
  },
  "inputs": []
}
```
```

For the latest setup instructions, see the [VS Code MCP documentation](https://code.visualstudio.com/docs/copilot/chat/mcp-servers).

### Other IDEs or custom clients

If your IDE supports MCP via a proxy, you can use the `mcp-remote` tool:

1. Open your terminal.
2. Run:

```
```
1
2
```



```
npx -y mcp-remote https://mcp.atlassian.com/v1/forge/mcp
```
```

If you encounter issues, try specifying an older version:

```
```
1
2
```



```
npx -y mcp-remote@0.1.13 https://mcp.atlassian.com/v1/forge/mcp
```
```

3. Configure your client to connect to the local proxy as per its documentation.

## Example development flow

When working with AI coding agents, it’s important to explicitly instruct them to use the Forge-related tools provided by the MCP server. This ensures their work is based on the most up-to-date Forge knowledge, as some agents may not use these tools unless prompted and might otherwise attempt to build your app without referencing the latest documentation or guidance.

1. Prompt your agent: “Create a Confluence macro that shows a pie chart of Jira issues by status. Use the Forge MCP tools to ensure your solution is based on the latest Forge documentation.”
2. Agent plans the task: Calls the `forge-howto` guide for a high-level context.
3. Agent gathers details: Uses guides like `ui-kit-guide`, `forge-modules-list`, and `app-manifest-guide` as needed.
4. Agent queries documentation: Searches for specific components or API usage using `search-forge-docs` or `query-cloud-platform-knowledge-fragments`.
5. You build and test: Use the Forge CLI to lint, deploy, and install your app. The agent can help troubleshoot errors by querying the MCP server for relevant documentation.

## Security and access

* The Forge MCP server only provides publicly available information; no authentication is required.
* All data is sourced from <https://developer.atlassian.com/>.
* Rate limiting may be applied to prevent abuse.
* Risk: The information returned by the MCP server may become out-of-date if the knowledge index is not refreshed regularly as Forge evolves. Always verify critical details against the latest official Forge documentation.
