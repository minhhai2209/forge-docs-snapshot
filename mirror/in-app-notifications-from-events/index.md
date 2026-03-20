# In-app notifications from events

**[Go to sample code](https://bitbucket.org/atlassian/reference-architectures/src/main/forge-in-app-notifications-from-events/)**

## Overview

This reference architecture demonstrates how to use a Forge app to react to [events](https://developer.atlassian.com/platform/forge/events/) in Jira and Confluence to show in-app notifications. The app listens to events (for example, Jira work item events or Confluence page events), runs backend logic to decide whether to notify users, and then uses Forge UI capabilities to show notifications directly in the app interface.

This approach can be reused for many scenarios, such as:

* Informing users when an automated rule changes or reverts their action
* Surfacing warnings when content doesn’t meet a policy
* Confirming that a background process has completed or failed

It relies on events, Forge realtime events APIs, Forge background scripts, and the Forge bridge APIs.

---

## Benefits

* **Key feature**: in-app notifications that instantly inform users of important backend events (such as governance enforcement or remote content changes) with native UI notification experiences, ensuring users are always aware of relevant actions as they happen.
* **Efficiency**: Thanks to the Forge Realtime solution, there is no need to perform any polling or store information between the backend and the frontend. The realtime event payload contains all the information required, eliminating unnecessary API calls and ensuring the frontend always receives up-to-date context without additional state management.
* **Actionable user experience**: Notifications can include inline actions, such as navigating to related documentation or pages, performing additional actions via REST APIs, or refreshing the current view. This allows users to respond immediately without leaving the app.
* **Broad event support**: The app can listen to a wide range of Forge [events](https://developer.atlassian.com/platform/forge/events/), making it adaptable to many use cases across Jira and Confluence.
* **Secure and context-aware delivery**: Notifications are scoped to the relevant user and context, ensuring that only the appropriate users receive the right information at the right time.
* **Seamless user experience**: Uses native flag/pop-up banners that integrate naturally into the app interface, delivering essential information while allowing users to stay focused on their workflow.

---

## How it works

The app is composed of triggers, a secure [realtime channel](https://developer.atlassian.com/platform/forge/runtime-reference/realtime-events-api/), and a [Jira issue view background script](https://developer.atlassian.com/platform/forge/manifest-reference/modules/jira-issue-view-background-script/) that work together to deliver timely, context-aware notifications to users:

![In-app notifications from events](https://dac-static.atlassian.com/platform/forge/images/in-app-notifications-from-events.svg?_v=1.5800.1927)

This architecture leverages Forge triggers, background scripts, realtime channels, and bridge APIs to provide a seamless, secure, and highly targeted notification experience directly within Jira or Confluence.

---

## Best practices and considerations

* **Leverage manifest filters for efficiency**: the `ignoreSelf: true` filter in `manifest.yml` prevents the app from responding to its own actions, avoiding redundant processing. The manifest `expression` filter further narrows down which events your triggers respond to, so the app only processes relevant changes and reduces unnecessary executions.
* **Choose the right background script module for your use case**: This architecture uses the [Jira issue view background script](https://developer.atlassian.com/platform/forge/manifest-reference/modules/jira-issue-view-background-script/), but other module types may be a better fit depending on where notifications should appear, such as the [Jira global background script](https://developer.atlassian.com/platform/forge/manifest-reference/modules/jira-global-background-script/) or the [Jira dashboard background script](https://developer.atlassian.com/platform/forge/manifest-reference/modules/jira-dashboard-background-script/).
* **User availability when responding to app events**: When responding to events, the app code runs under the identity of the app system user, not an Atlassian interactive user account. As a result, the app cannot perform actions as the user (`asUser()`) in this context, and should use `asApp()` for REST API calls in event handlers. If you need to attribute an action to a specific user (for example, deleting a disallowed work item link as the user who created it), you can use offline user impersonation with `asUser(accountId)`, provided the relevant scopes in `manifest.yml` are declared with `allowImpersonation: true`—and only on the scopes that require it.
* **Scope notifications precisely**: Always sign and scope real-time tokens to the specific user and context (such as work item, space, or page) to ensure only the intended recipients receive notifications. This enhances both security and relevance.
* **Design useful, informative, and actionable notifications**: Ensure notifications provide clear and relevant information to help users understand what happened and why. Where appropriate, include contextual actions—such as links to documentation, REST API actions, or refresh options—so users can easily resolve issues or learn more without leaving the app.

---

## Disclaimer

This solution is provided as a reference implementation. Before deploying in production, review and adapt the code for your organization's security, compliance, and operational requirements.
