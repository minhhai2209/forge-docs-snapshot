# Work item picker custom field in Jira

**[Go to sample code](https://bitbucket.org/atlassian/reference-architectures/src/main/forge-issue-picker-custom-field-type/)**

## Overview

This reference architecture demonstrates how to add a work item picker custom field in Jira using a Forge app.

Jira admins can configure a JQL filter to define the list of work items displayed in the field, either for the global context or for each space. Users can then search for work items using a type-ahead search—where suggestions appear as they type—directly within the custom field.

This custom field app leverages the `jira:customFieldType` Forge module, Forge's secure runtime, Forge UI Kit, and Jira REST APIs.

---

## Benefits

* **Key feature**: Adds a work item custom field to Jira, allowing users to easily search for and select relevant work items.
* **Configurable filtering**: Admins can tailor the field to any use case by specifying custom JQL queries on a per-space basis based on the context configuration.
* **Dynamic selection**: Users can search and select from filtered work items in real time, improving accuracy.
* **Rich context**: The picker displays key details (work item key, summary) for each work item. Additionally, the app can be modified to display additional information in each option for informed selection.
* **Consistent UI**: Built with UI Kit for a native Jira look and feel.

---

## How it works

The app is composed of three components:

### Work item view

Display view that shows the selected work item(s) on the Jira work item screen. It uses the `jira:customFieldType` Forge module to read the field value and render key details, such as work item key and summary, leveraging Jira REST APIs and UI Kit components for a native Jira look and feel.

![Work item view](https://dac-static.atlassian.com/platform/forge/images/work-item-view.svg?_v=1.5800.1777)

### Work item edit

Interactive view used when the user searches for and selects a work item. It powers the type-ahead work item picker: as the user types, it shows the work items that match the configured JQL so users can quickly search and select the right work item.

![Work item edit](https://dac-static.atlassian.com/platform/forge/images/work-item-edit.svg?_v=1.5800.1777)

### Context configuration

Admin configuration view for the `jira:customFieldType`. Jira admins can define a JQL filter per context to control which work items are available in the picker. The app provides the UI to enter, validate, and store the configuration as part of the context configuration.

![Context configuration](https://dac-static.atlassian.com/platform/forge/images/field-context-configuration.svg?_v=1.5800.1777)

---

## Best practices and considerations

* **Limit fields in work item GET requests**: In the view component, use the fields query parameter when fetching individual work items to reduce payload size and improve performance. For example, `/rest/api/3/issue/${issueKey}?fields=summary` returns only the summary field instead of all fields (default behavior). Only request the fields your UI actually renders—this reduces bandwidth usage and speeds up response times.
* **Request only required fields in JQL searches**: In the edit component, when calling `/rest/api/3/search/jql`, specify only necessary fields in the fields array within the request body (e.g., `fields: ['summary']`). The key field is always included automatically, so you don't need to declare it. This minimizes API response size, improves load times, and reduces bandwidth consumption. This is particularly important for type-ahead pickers and dropdown components if data is fetched on every keystroke.
* **Debounce type-ahead search input**: The edit component implements debouncing on `handleInputChange` to prevent excessive API calls while users type. A 400ms delay is applied using `setTimeout` and a `useRef` timer, which means each new keystroke cancels the previous timer before starting a new one. Without this debouncing, every keystroke would trigger a `/rest/api/3/search/jql` request, resulting in inefficient resource usage and reduced responsiveness. With debouncing in place, API calls are reduced from potentially dozens per search to just one or two, significantly improving user experience and rate limit compliance.
* **Validate JQL in context configuration**: The context configuration component should validate the JQL query before allowing admins to save it. When admins enter a JQL query in the configuration UI, use the `/rest/api/3/jql/parse` endpoint to verify the syntax is valid and display validation feedback. This prevents admins from saving broken JQL that causes the edit component to fail for all users, improves the configuration experience by catching errors early, and ensures the custom field works correctly when added to work item screens.

---

## Disclaimer

This solution is provided as a reference implementation. Before deploying in production, review and adapt the code for your organization's security, compliance, and operational requirements.
