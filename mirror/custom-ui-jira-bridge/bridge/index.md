# Jira UI bridge

The Jira UI bridge is a JavaScript API that enables [UI Kit](/platform/forge/ui-kit) and [Custom UI](/platform/forge/custom-ui) apps to securely integrate with Jira.

Install the Jira UI bridge using the
[@forge/jira-bridge](https://www.npmjs.com/package/@forge/jira-bridge) npm package.
Import `@forge/jira-bridge` using a bundler, such as [Webpack](https://webpack.js.org/).

You can start by creating a new app from one of the Custom UI templates.
In the `static/hello-world` directory, run `npm install && npm build` to bundle the
static web application template with the Jira UI bridge into the `static/hello-world/build`
directory. Use this directory as the resource path in the Forge app's `manifest.yml`.

In the template, use the bridge in `static/hello-world/src/App.js` like this:

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
import { ViewIssueModal } from '@forge/jira-bridge';

const viewIssueModal = new ViewIssueModal({
  context: {
    issueKey: 'CS-15',
  },
});

viewIssueModal.open();
```
