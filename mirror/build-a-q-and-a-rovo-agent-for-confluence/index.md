# Build a Q&A Rovo Agent for Confluence

When you use Rovo APIs, you must comply with the [Atlassian Acceptable Use Policy](https://www.atlassian.com/legal/acceptable-use-policy#disruption), including the section titled “Artificial intelligence offerings and features.” For the protection of our customers, Atlassian performs safety screening on Agents at our sole discretion. If we identify any issues with your Agent, we may take protective actions, such as preventing the Agent from being deployed or suspending your use of Rovo APIs. Where possible we will notify you of the nature of the issue, and you must use reasonable commercial efforts to correct the issue before deploying your Agent again.

This tutorial explains how the Q&A Creator example Forge app works. If you are unfamiliar with Forge app development, you may want to visit [this introduction](https://developer.atlassian.com/platform/forge/).

The Q&A Creator app comprises an Agent and associated actions that provide custom capabilities that creates a list of questions and answers based on the Confluence content where the Agent is executing.

The source code of the app is available [here](https://go.atlassian.com/qanda-agent). Readers are recommended to review the code as they complete this tutorial.

## Before you begin

Before starting this tutorial, you may want to familiarise yourself with the [Forge Rovo module documentation](https://developer.atlassian.com/platform/forge/manifest-reference/modules/rovo-index/) and complete the [Build a Rovo Agent tutorial](https://developer.atlassian.com/platform/forge/build-a-hello-world-rovo-agent/#before-you-begin) to ensure you are familiar with the basics of creating, installing and viewing Rovo apps.

## Step 1: Clone the example app

Clone the [Forge Q&A Creator](https://bitbucket.org/atlassian/forge-q-and-a-creator/src/main/) app.

## Step 2: Understand the structure of the app

The app has the following structure:

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
10
11
├── src
    └── backend
        └── action.js
        └── confluenceUtil.js
        └── qandaUtil.js
        └── resolver.js
    └── frontend
        └── macro.jsx
    └── index.js
├── manifest.yml
├── package.json
```

`backend`: Most of the code is within the backend directory. All of the backend code runs in Forge’s functions as a service infrastructure.

frontend: The code in the frontend directory runs in the user’s browser, but it can make calls to the backend via the resolver. It comprises the implementation of a Confluence macro that provides a bespoke experience presenting a list of questions and answers.

`manifest`: a significant amount of logic is contained in the [app manifest](https://developer.atlassian.com/platform/forge/manifest/), manifest.yml. The manifest is where the app declares all the Forge capabilities it utilises. It’s also where the prompt of the apps Agent is defined.

### Q&A

**Q1**: Where is the app’s AI logic?

**A1**: The app’s AI logic is defined by the prompt in the app’s manifest plus the actions that run in the backend of the app.

**Q2**: What does the `resolver.js` do?

**A2**: The resolver defines operations in the backend that can be invoked by the macro which executes in the user’s browser.

**Q3**: What does the `action.js` do?

**Q3**: This code exports functions that implement the actions indirectly referenced by the prompt.

**Q4**: What does the `confluenceUtil.js` do?

**Q4**: This code implements generic Confluence related utilities needed by the app.

**Q5**: What does the `qandaUtil.js` do?

**Q5**: This code implements utilities specific to the Q&A logic needed by the app. Most of these utilities relate to the storage of questions and answers.

## Step 3: Understand the app manifest

The app manifest, manifest.yml, declares various modules:

```
```
1
2
```



```
modules:
  macro:
    - key: qanda-macro
      title: Q&A Quiz
      ...
  rovo:agent:
    - key: q-and-a
      ...
      actions:
        - fetch-content
        - register-q-and-a
        - insert-q-and-a
  action:
    - key: fetch-content
      ...
    - key: register-q-and-a
      ...
    - key: insert-q-and-a
      ...
  function:
    - key: fetchContent
      handler: index.fetchContent
    - key: registerQandA
      handler: index.registerQandA
    - key: insertQandAMacro
      handler: index.insertQandAMacro
    - key: macro-resolver
      handler: index.macroHandler
      ...
app:
  runtime:
    name: nodejs24.x
  id: ari:cloud:ecosystem::app/6452e1d8-c457-446a-82a7-d186ef150f15
permissions:
  scopes:
    - read:content.metadata:confluence
    - read:page:confluence
    - write:page:confluence
resources:
  - key: q-and-a-macro
    path: src/frontend/macro.jsx
  - key: static-resources
    path: static
```
```

Some modules are *wired* to other modules by referencing their keys. The function modules are *wired* to code by referencing *handlers*. In this tutorial we have used 3 modules:

The app declares one agent using the `rovo:agent` module and a Confluence macro using the `macro` module.

The `permissions` section declares the need for several scopes in order to invoke various Confluence APIs.

The `resources` section declares front end components such as the macro code and the location of icons.

### Q&A

**Q1**: When do actions run?

**A1**: Actions are triggered by the AI when conditions outlined by the prompt are met. For example, the fetch content action retrieves the content of the current Confluence page or blogpost or the selected text at the start of the AI processing.

**Q2**: Which types of modules relate specifically to AI capabilities?

**A2**: The `rovo:agent` and `action` modules relate specifically to AI capabilities.

## Step 4: Understand the prompt

The prompt defines how the AI should behave and can be thought of as a program in its own right, but instead of the programming language being Javascript or another traditional programming language, the prompt programming language is English.

The app declares a single Agent that instructs the AI how to generate a list of questions and answers. At a high level, the prompt defines the following logic:

1. Retrieve the text that the user wishes to generate questions and answers for.
2. Generate the list of questions and answers.
3. Register each question and answer pair with an action provided by the app.
4. Present the questions and answers in a specific format to the user.
5. Ask the user if they would like the Q&A Quiz macro inserted.
6. If the user accepts the offer, invoke an action to insert the Q&A Quiz macro.

The app’s prompt has the following outline:

```
```
1
2
```



```
Preamble
Workflow
Jobs
Templates
```
```

* **Preamble**: The preamble part of the prompt defines the role and rules that the AI should take on. The preamble also defines the structure and formatting of the remainder of the prompt. In this example app, see, [here](https://bitbucket.org/atlassian/forge-q-and-a-creator/src/8c7da73fe0fbc2dfefce450c394fb58110a0c5e0/manifest.yml#lines-16)
* **Workflow**: The workflow defines the overall workflow that the AI should follow. It is a series of steps that refers to jobs. In this example app, see, [here](https://bitbucket.org/atlassian/forge-q-and-a-creator/src/8c7da73fe0fbc2dfefce450c394fb58110a0c5e0/manifest.yml#lines-31).
* **Jobs**: The prompt is comprised of a number of jobs. Each job is comprised of a number of steps. Jobs may reference actions and templates by quoting their names. In this example, see, [here](https://bitbucket.org/atlassian/forge-q-and-a-creator/src/8c7da73fe0fbc2dfefce450c394fb58110a0c5e0/manifest.yml#lines-43).
* **Templates**: Templates define the format of responses to users that the AI should adhere to. In this example, see [here](https://bitbucket.org/atlassian/forge-q-and-a-creator/src/8c7da73fe0fbc2dfefce450c394fb58110a0c5e0/manifest.yml#lines-95).

Forge Rovo apps can define actions to augment the behavior of the AI. The following diagram illustrates the relationships between prompts, actions and the AI:

The Forge Q&A app’s prompt instructs the AI to delegate certain operations to three actions:

* `fetch-content`: The AI does not automatically operate with the current page or blog post in its context so this action is necessary to retrieve the content.
* `register-q-and-a`: After the AI has generated the list of questions and answers, it is instructed to register each question and answer with this action. The action stores the question and answer provided in a content property.
* `insert-q-and-a`: After presenting the generated questions and answers to the user, the AI also asks the user if they would like the Q&A Quiz macro to be inserted in order to provide a custom user experience to present the questions and answers.

### Q&A

**Q1**: Do all prompts need complicated structures?

**A1**: No, but increasing structure helps when prompts comprise considerable amounts of logic.

**Q2**: Must all prompts have the concepts of a workflow, jobs and templates.

**A2**: No, these abstractions are used by this apps prompt, but alternate abstractions may be used by other prompts.

**Q3**: How should a prompt reference a job to execute or a template to use?

**A3**: Jobs and templates are referenced by quoting their names.

## Step 5: Understand how actions work

Actions are routines that prompts can delegate to. More accurately, the AI delegates work to an action whilst the prompt defines the logic defining when the AI should delegate to an action.

Actions are defined in the app manifest. The definition of an action can define any number of parameters that the AI is expected to supply when invoking the action. Action parameters are provided by the AI in response to the context of the AI and instructions in the prompt.

Actions accept a payload parameter which contains a range of contextual information, including the parameters specified by the action.

A prompt may indicate that the information returned by the action should be used by subsequent AI processing.

View the [actions](https://developer.atlassian.com/platform/forge/manifest-reference/modules/rovo-action/) documentation for more details about actions.

### Q&A

**Q1**: What is an action?

**A1**: An action is an app function that the prompt can instruct the AI to invoke at certain stages and under certain conditions.

**Q2**: How many actions can an app define for a prompt.

**A2**: Any number. App prompts do not need any actions to be defined, but there is no limit to the number of actions allowed.

**Q3**: How do actions know what information to process?

**A3**: The definition of actions in the app manifest includes inputs that the AI invokes the action with.

## Step 6: Understand the fetch content action

The fetch content action is implemented by the `fetchContent` routine within `src/backend/action.js`. The action takes a single parameter;- `contentId`, the ID of the content that the AI is open against. The action first checks if the user is working against a section of the content by checking of the payload’s `highlightedText` field. If they are, then the `highlightedText` is returned. Otherwise, the content is fetched via a utility routine, `fetchPageOrBlogInfo` using the ID of the content that the AI passes in.

### Q&A

**Q1**: How does the AI know what value to provide for the `contentId` input parameter?

**A1**: The AI executes in a context such as Confluence page or blog post. The AI is aware of the context and able to retrieve information from it.

## Step 7: Understand the register Q&A action

The register Q&A action is implemented by the `registerQandA` routine within `src/backend/action.js`. It is invoked separately for each question and answer pair that the AI generates. The action takes three parameters:

* `contentId`: the ID of the content that the AI is open against;
* `question`: the AI generated question; and
* `answer`: the AI generated answer.

The register Q&A action demonstrates the ability to post process information returned by the AI. It assigns a score to each question and answer pair and it also stores the question and answer pair as a content property using the Confluence API. To achieve this, the routine performs the following steps:

1. Retrieve all the entity properties stored against the content.
2. Determine if question is already stored by matching it against the stored entity properties.
3. If the question has already been stored, store a new version of it and the answer just in case the answer has been updated.
4. If the question has not already been stored, store it and the answer.

Each question and answer pair are stored in JSON format to simplify parsing.

### Q&A

**Q1**: What is the purpose of the register Q&A action?

**A1**: The purpose of the register Q&A action is to post process each generated question and answer pair. It assigns a random score and stores the question and answer pair against the content which will be utilised by the Q&A Quiz macro.

## Step 8: Understand the insert Q&A Quiz macro action

The insert macro action is implemented by the `insertQandAMacro` routine within `src/backend/action.js`. The action takes a single `contentId` parameter.

To store the macro, the routine performs the following steps:

1. Retrieve the content and content meta data.
2. Format the macro in [Atlassian Document Format (ADF)](https://developer.atlassian.com/cloud/jira/platform/apis/document/structure/). The required format was determined by retrieving a page with the macro in it. Whilst not a format API, this format is stable.
3. Append the macro to the end of the content.
4. Update the current draft of the content to allow the user to continue editing the draft as necessary.

### Q&A

**Q1**: Why does the insert quiz macro update a draft of the content rather than publishing a new version of the content.

**A1**: Updating the draft provides the user with an opportunity to review and further edit the applied changes before publishing them.

## Debugging tips

As you can see, the prompt contains a considerable amount of logic. As with all types of programs, the prompt needs to be iteratively developed and the behavior of the AI needs to understood as changes are made. Traditional programming typically involves the ability the set breakpoints to stop the program and inspect the state of the program. Alternatively, programs can be debugged by logging output. Whilst you can’t set breakpoints in the AI, you can use the logging technique to debug it.

Whilst the prompt has been fully developed, it still includes some logging statements to illustrate the technique. Here is an excerpt showing logging statements:

```
```
1
2
```



```
4. DEBUG: Inform the user of the number of characters in the content.
5. If the length of the fecthed content is less than 200 characters, return a failure message to the user and abort further processing.
6. DEBUG: Provide the user with an explanation of how you fetched the text of the Confluence content.
7. DEBUG: Return up to the first 500 characters of the text of the Confluence content to the user.
8. DEBUG: Return the URL of the Confluence content to the user.
```
```

Note the “DEBUG: “ prefix and the following instruction in the preamble:

```
```
1
2
```



```
Some instructions begin with "DEBUG: ", indicating its purpose is to help 
debug the state. Debugging is enabled so perform these instructions.
```
```

To disable the debugging statements, change the last part of the preamble as follows:

```
```
1
2
```



```
Debugging is disabled so ignore these instructions.
```
```

### Q&A

**Q1**: Is is possible to set breakpoints in the AI.

**A1**: No, breakpoints can’t be set in the AI, but the AI can be debugged via logging instructions in the prompt.

**Q2**: How can the debugging output of the prompt be disabled.

**A2**: The debugging output of the prompt can be disabled by modifying the preamble part of the prompt to inform the AI that it should ignore the `DEBUG` instructions.

## Summing up

The app demonstrates the ability of a prompt to be defined which involves:

* Interactions between the AI and actions provided by the app;
* Interaction between the AI and the user to inform subsequent processing; and
* Debugging via instructing the AI to present state information to the user.

## Developing for Atlassian Government Cloud

This content is written with standard cloud development in mind. To learn about developing for Atlassian Government Cloud, go to our [Atlassian Government Cloud developer portal](https://developer.atlassian.com/platform/framework/agc/).
