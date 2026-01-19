# Create a quiz app using UI Kit

## Create a quiz app using UI Kit

This tutorial describes how you can use UI Kit layout components to make a playable quiz in Confluence.
You’ll be using [heading](/platform/forge/ui-kit/components/heading/),
[image](/platform/forge/ui-kit/components/image/), [button](/platform/forge/ui-kit/components/button),
[text](/platform/forge/ui-kit/components/text/), [inline](/platform/forge/ui-kit/components/inline/),
and [stack](/platform/forge/ui-kit/components/stack/) to build the user interface.
The purpose of this tutorial is to get familiar with using
[UI Kit components](/platform/forge/ui-kit/components/), so it is a purely frontend app.

![A gif is added to a Confluence page](https://dac-static.atlassian.com/platform/forge/images/quiz-app.gif?_v=1.5800.1777)

## Before you begin

This tutorial assumes you're already familiar with the basics of Forge development.
If this is your first time using Forge, see [Getting started](/platform/forge/getting-started/) first.

To complete this tutorial, you need the latest version of the Forge CLI. To update your CLI version, run `npm install -g @forge/cli@latest` on the command line.

### Set up a cloud developer site

An Atlassian cloud developer site lets you install and test your app on
Atlassian apps including Confluence and Jira. If you don't have one yet, set it up now:

1. Go to <http://go.atlassian.com/cloud-dev> and
   create a site using the email address associated with your Atlassian account.
2. Once your site is ready, log in and complete the setup wizard.

You can install your app to multiple Atlassian sites. However, app
data won't be shared between separate Atlassian apps, sites,
or Forge environments.

The limits on the numbers of users you can create are as follows:

* Confluence: 5 users
* Jira Service Management: 1 agent
* Jira Software and Jira Work Management: 5 users

## Step 1: Create your app

Create an app using a template.

1. Navigate to the directory where you want to create the app.
2. Create your app by running:
3. Enter a name for the app. For example, *quiz-app*.
4. Select the *UI Kit* category from the list.
5. Select the *confluence-global-page* template from the list.
6. Change to the app subdirectory to see the app files

## Step 2: Configure the app manifest

This app uses a Confluence `globalPage` module. The `confluence:globalPage` module displays content
in place of a Confluence page.

1. In the app’s top-level directory, open the `manifest.yml` file.
2. Change the `key` under `confluence:globalPage` to *quizapp-global-page*.
3. Change the `title` under `confluence:globalPage` to *QuizApp*.
4. Add [image egress permissions](/platform/forge/manifest-reference/permissions/#images)
   to whitelist a GIPHY image.

```
```
1
2
```



```
    permissions:
        external:
            images:
              - address: https://media.giphy.com
```
```

Your manifest file should look like this:

```
```
1
2
```



```
modules:
  confluence:globalPage:
    - key: quizapp-global-page
      resource: main
      render: native
      title: QuizApp
      route: global-page
resources:
  - key: main
    path: src/frontend/index.jsx
permissions:
  external:
    images:
      - address: https://media.giphy.com
app:
  id: ari:cloud:ecosystem::app/<YOUR_APP_ID>
```
```

See [Manifest](/platform/forge/manifest-reference/) to learn more about the manifest file.

## Step 3: Add a local questions data file

For the purposes of this tutorial, we will only be fetching questions locally from a `.js` file.
In the src directory, create the data folder, and then create questions.js under it. Your file structure should be,
`src/data/questions.js`. The question set will be an array of objects,
each having a `question`, `image?`, `options`, and optionally, a `correctAnswer` key if you also want
to add further notes to be displayed to the user.

```
```
1
2
```



```
export const QuestionSet = [
    {
      question: "What year was Atlassian Founded?",
      image: "https://media.giphy.com/media/dwtX3iozeZCoVcyBVu/giphy.gif",
      options:[
        { option: "1998", isCorrect: false },
        { option: "2000", isCorrect: false },
        { option: "2002", isCorrect: true },
        { option: "2004", isCorrect: false },
      ],
      correctAnswer: "2002",
    },
    {
      question: "How many office locations are there at Atlassian?",
      image: "https://media.giphy.com/media/xUOwGj1jwTZq5Kh3Ko/giphy.gif",
      options:[
        { option: "6", isCorrect: false },
        { option: "9", isCorrect: false },
        { option: "13", isCorrect: true },
        { option: "18", isCorrect: false },
      ],
      correctAnswer: "13. San Francisco, Austin, Mountain View, New York, Sydney x2, Bengaluru, Yokohama, Amsterdam, Taguig!",
    },
    {
      question: "How many major versions of Confluence are there?",
      options:[
        { option: "5", isCorrect: false },
        { option: "8", isCorrect: true },
        { option: "11", isCorrect: false },
        { option: "14", isCorrect: false },
      ],
      correctAnswer: "8. You can check out https://confluence.atlassian.com/doc/confluence-release-notes-327.html for all versions",
    },
  ];
```
```

## Step 4: Add a basic user interface

We are going to build a basic UI to layout our components. The layout of the app consists of a heading
(which shows the question), an associated image, buttons to display the four multi-choice options,
and a button to go to the next question.

![A diagram of the quiz app is added to a Confluence page](https://dac-static.atlassian.com/platform/forge/images/quiz-app-diagram.png?_v=1.5800.1777)

We are also going to use `Inline` and `Stack` components to layout our components:

![A diagram showing the inline and stack components is added to a Confluence page](https://dac-static.atlassian.com/platform/forge/images/quiz-app-diagram-inline-stack.png?_v=1.5800.1777)

Install the latest versions of the following packages in the top-level directory of the app:

* UI Kit: To update your version run `npm install @forge/react@latest --save` on the command line.

In `frontend/index.jsx`, we want to import our components from `@forge/react`, so update
the existing import statement to look like this:

```
```
1
2
```



```
import ForgeReconciler, { Heading, Image, Button, Text, Inline, Stack } from '@forge/react';
```
```

You can also remove the other unused imports.

In the `App` component, remove everything in there as we will be adding our own components and states.
Add our component stack inside `return()`.
Your `frontend/index.jsx` file should look like this:

```
```
1
2
```



```
import React from 'react';
import ForgeReconciler, { Heading, Image, Button, Text, Inline, Stack } from '@forge/react';

const App = () => {
  return (
    <>
      <Stack space="space.200" alignInline="center">
        <Heading as="h1">My Question</Heading>
        <Image src="https://media.giphy.com/media/xUOxfjsW9fWPqEWouI/giphy.gif" alt="Founders" size="xsmall" />
        <Inline space="space.200" alignBlock="center" alignInline="center">
          <Stack space="space.200" grow="hug">
            <Button appearance="primary" onClick={() => {}}>
              Option 1
            </Button>
            <Button appearance="primary" onClick={() => {}}>
              Option 3
            </Button>
          </Stack>
          <Stack space="space.200" grow="hug">
            <Button appearance="primary" onClick={() => {}}>
              Option 2
            </Button>
            <Button appearance="primary" onClick={() => {}}>
              Option 4
            </Button>
          </Stack>
        </Inline>
        <Text>Answer</Text>
        <Button appearance='default' onClick={() => {}}>Next question</Button>
        <Text>Question 1 out of 3</Text>
      </Stack>
    </>
  );
};

ForgeReconciler.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```
```

## Step 5: Install your app

Build, deploy, and install the app to see it in your Confluence site.

To use your app, it must be installed onto an Atlassian site. The
`forge deploy` command builds, compiles, and deploys your code; it'll also report any compilation errors.
The `forge install` command then installs the deployed app onto an Atlassian site with the
required API access.

You must run the `forge deploy` command before `forge install` because an installation
links your deployed app to an Atlassian site.

1. Navigate to the app's top-level directory and deploy your app by running:
2. Install your app by running:
3. Select your Atlassian context using the arrow keys and press the enter key.
4. Enter the URL for your development site. For example, *example.atlassian.net*.
   [View a list of your active sites at Atlassian administration](https://admin.atlassian.com/).

Once the *successful installation* message appears, your app is installed and ready
to use on the specified site.
You can always delete your app from the site by running the `forge uninstall` command.

The quiz app uses the `confluence:globalPage` template, which displays content in place of a Confluence page.
To view the quiz app:

1. Go the site where your app is installed.
2. Select the **Apps** tab on the top navigation bar and select your app to view.

![The app is inserted into a Confluence page](https://dac-static.atlassian.com/platform/forge/images/quiz-app-part-1.png?_v=1.5800.1777)

## Step 6: Importing questions and adding states

Import our question set from `questions.js`:

```
```
1
2
```



```
import { QuestionSet } from '../data/questions';
```
```

We are going to keep track of which question is displayed using a counter. We will track the question
using the `useState` hook and set the state when the user clicks `Next question`.

```
```
1
2
```



```
const [activeQuestion, setActiveQuestion] = useState(0);
```
```

We can now grab the next question using the `activeQuestion` index:

```
```
1
2
```



```
const { question, options, image } = QuestionSet[activeQuestion];
```
```

We will also create more states to track when to display the explanation and the result. You can try
to build it yourself, or replace your `frontend/index.jsx` with the following:

```
```
1
2
```



```
import React, { useState } from 'react';
import ForgeReconciler, { Heading, Image, Button, Text, Inline, Stack } from '@forge/react';
import { QuestionSet } from '../data/questions';

const App = () => {

  const [activeQuestion, setActiveQuestion] = useState(0);
  const [explanation, setExplanation] = useState('')
  const [showResult, setShowResult] = useState(false);

  const onClickHandler = (isCorrect) => {
    if (isCorrect) {
      setExplanation('You got it right!');
    } else {
      setExplanation('Incorrect, the correct answer is ' + `${QuestionSet[activeQuestion].correctAnswer}`);
    }

    setShowResult(true);
  }

  const onClickNext = () => {
    if (activeQuestion + 1 < QuestionSet.length) {
      setActiveQuestion(activeQuestion + 1);
      setShowResult(false);
    }
  }

  const { question, options, image } = QuestionSet[activeQuestion];

  return (
    <>
      <Stack space="space.200" alignInline="center">
        <Heading as="h1">{question}</Heading>
        <Image src={image ? image : "https://media.giphy.com/media/xUOxfjsW9fWPqEWouI/giphy.gif"} alt="Founders" size="xsmall" />
        <Inline space="space.200" alignBlock="center" alignInline="center">
          <Stack space="space.200" grow="hug">
            <Button appearance="primary" onClick={() => onClickHandler(options[0].isCorrect)} isDisabled={showResult ? true : false}>
              {options[0].option}
            </Button>
            <Button appearance="primary" onClick={() => onClickHandler(options[2].isCorrect)} isDisabled={showResult ? true : false}>
              {options[2].option}
            </Button>
          </Stack>
          <Stack space="space.200" grow="hug">
            <Button appearance="primary" onClick={() => onClickHandler(options[1].isCorrect)} isDisabled={showResult ? true : false}>
              {options[1].option}
            </Button>
            <Button appearance="primary" onClick={() => onClickHandler(options[3].isCorrect)} isDisabled={showResult ? true : false}>
              {options[3].option}
            </Button>
          </Stack>
        </Inline>
        <Text>{showResult ? explanation : null}</Text>
        <Button appearance='default' onClick={onClickNext} isDisabled={showResult ? false : true}>{ activeQuestion == QuestionSet.length-1 ? 'Finish' : 'Next Question'}</Button>
        <Text>Question {activeQuestion + 1} of {QuestionSet.length}</Text>
      </Stack>
    </>
  );
};

ForgeReconciler.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```
```

The user flow is that the answer will be checked as soon as the multi-choice option is clicked,
but it does not go to the next question immediately as we want to display a result plus the explanation.
Two more hooks are added to support this, `explanation` and `showResult`. `showResult` is a hook
that toggles whether to display the explanation.

Your app should now look like this and can be playable:

![A gif is added to a Confluence page](https://dac-static.atlassian.com/platform/forge/images/quiz-app-before-ending-screen.gif?_v=1.5800.1777)

## Step 7: Adding an ending screen

The quiz app also needs a simple scoring system and an end screen to display it. Using a new hook
`showResults`, we will keep track of `activeQuestion` and if it is the last question and next question
is clicked, the ending screen will be displayed.

The final `frontend/index.jsx` should look like this:

```
```
1
2
```



```
import React, { useState } from 'react';
import ForgeReconciler, { Heading, Image, Button, Text, Inline, Stack } from '@forge/react';
import { QuestionSet } from '../data/questions';

const App = () => {

  const [activeQuestion, setActiveQuestion] = useState(0);
  const [explanation, setExplanation] = useState('')
  const [showResult, setShowResult] = useState(false);
  const [showResults, setShowResults] = useState(false);
  const [score, setScore] = useState(0);

  const onClickHandler = (isCorrect) => {
    if (isCorrect) {
      setExplanation('You got it right!');
      setScore(score + 1);
    } else {
      setExplanation('Incorrect, the correct answer is ' + `${QuestionSet[activeQuestion].correctAnswer}`);
    }

    setShowResult(true);
  }

  const onClickNext = () => {
    if (activeQuestion + 1 < QuestionSet.length) {
      setActiveQuestion(activeQuestion + 1);
      setShowResult(false);
    } else {
      setShowResults(true);
    }
  }

  const onClickReplay = () => {
    setActiveQuestion(0);
    setShowResult(false);
    setScore(0);
    setExplanation('');
    setShowResults(false);
  }

  const { question, options, image } = QuestionSet[activeQuestion];

  return (
    <>
      { showResults ? (
        <Stack space="space.200" alignInline="center">
          <Heading as="h1">Final score: {score} out of {QuestionSet.length} </Heading>
          <Image src={"https://media.giphy.com/media/XROOE9NApITmCgF6dZ/giphy.gif"} alt='High-five' size = "small"/>
          <Button appearance="primary" onClick={onClickReplay}>
              Replay
          </Button>
        </Stack>
      ) : (
      <Stack space="space.200" alignInline="center">
        <Heading as="h1">{question}</Heading>
        <Image src={image ? image : "https://media.giphy.com/media/xUOxfjsW9fWPqEWouI/giphy.gif"} alt="Founders" size="xsmall" />
        <Inline space="space.200" alignBlock="center" alignInline="center">
          <Stack space="space.200" grow="hug">
            <Button appearance="primary" onClick={() => onClickHandler(options[0].isCorrect)} isDisabled={showResult ? true : false}>
              {options[0].option}
            </Button>
            <Button appearance="primary" onClick={() => onClickHandler(options[2].isCorrect)} isDisabled={showResult ? true : false}>
              {options[2].option}
            </Button>
          </Stack>
          <Stack space="space.200" grow="hug">
            <Button appearance="primary" onClick={() => onClickHandler(options[1].isCorrect)} isDisabled={showResult ? true : false}>
              {options[1].option}
            </Button>
            <Button appearance="primary" onClick={() => onClickHandler(options[3].isCorrect)} isDisabled={showResult ? true : false}>
              {options[3].option}
            </Button>
          </Stack>
        </Inline>
        <Text>{showResult ? explanation : null}</Text>
        <Button appearance='default' onClick={onClickNext} isDisabled={showResult ? false : true}>{ activeQuestion == QuestionSet.length-1 ? 'Finish' : 'Next Question'}</Button>
        <Text>Question {activeQuestion + 1} of {QuestionSet.length}</Text>
      </Stack> )
      }
    </>
  );
};

ForgeReconciler.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```
```

Ensure you deploy your app with `forge deploy`.

Congrats! Now you have a quiz app in Confluence.

## Next steps

Continue to one of the other tutorials or look through the reference pages to learn more.

See the [reference pages](/platform/forge/manifest-reference/) to learn what else you can do
with what you’ve learned.
