# Create a question generator app in multiple languages using i18n

This tutorial demonstrates how you can use [internationalization](/platform/forge/internationalization/)
and [UI Kit](/platform/forge/ui-kit/) to create a question generator Confluence macro. It shows how
to configure your manifest and setup translation functions to resolve translation keys in your app
code. This enables the app to adapt based on a user’s language. Additionally, this tutorial
demonstrates how to configure translation [fallbacks](/platform/forge/internationalization/#fallback-configurations)
which are used if a user’s locale is not supported.

## Before you begin

This tutorial assumes you're already familiar with the basics of Forge development.
If this is your first time using Forge, see [Getting started](/platform/forge/getting-started/) first.

You must also update to the latest Forge CLI version. To do this:

1. Install the Forge CLI globally by running:

   ```
   1
   npm install -g @forge/cli@latest
   ```
2. Verify that the CLI is installed correctly by running:

   You should be on version `11.3.0` or higher.

Additionally, ensure that you are using the latest version of `@forge/bridge` and `@forge/react`:

1. Install the latest `@forge/bridge` package to the project by running:

   ```
   1
   npm install @forge/bridge@latest
   ```
2. Install the latest `@forge/react` package to the project by running:

   ```
   1
   npm install @forge/react@latest
   ```

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
3. Enter a name for the app. For example, *forge-i18n-question-generator-app-ui-kit*.
4. Select the *UI Kit* category from the list.
5. Select the *confluence-macro* template from the list.
6. Change to the app subdirectory to see the app files:

   ```
   ```
   1
   2
   ```



   ```
   cd forge-i18n-question-generator-app-ui-kit
   ```
   ```

## Step 2: Create the translation files for your app

This app supports German, English (US), English (UK), Spanish, French, Chinese (Simplified, People's
Republic of China), and Chinese (Traditional, Taiwan). To begin, you need to create translation
files for each of those languages. These files contain the translation keys and their corresponding
translated strings, which are used by Forge to execute the translation.

For this example, you can use the existing translation JSON files in the `/locales` directory from
the [example app](https://bitbucket.org/atlassian/question-generator-app-i18n-for-ui-kit/src/master/locales/). In this example, we are defining the translation key for the title as `app.title` and the translation key for the description
as `app.description`.

```
```
1
2
```



```
"app": {
    "title": "Quizfragen-generator - i18n für UI Kit",
    "description": "Eine demo-anwendung, die quizfragen anzeigt. Die Forge-Anwendung wurde mit UI Kit erstellt, um die i18n-Unterstützung in Forge zu demonstrieren [de-DE]"
    ...
},
```
```

In this example, not all languages have every translation key defined. This is to demonstrate how the
fallback configurations work.

## Step 3: Configure your manifest

In the app's `manifest.yml` file, create a new section called `translations`. Under `translations.resources`, specify each locale in the `/locales` directory along with their corresponding translation file path. As you expand your language offering, you can add more translation resources.

```
```
1
2
```



```
translations:
  resources:
    - key: en-US
      path: locales/en-US.json
    - key: en-GB
      path: locales/en-GB.json
    - key: zh-CN
      path: locales/zh-CN.json
    - key: zh-TW
      path: locales/zh-TW.json
    - key: fr-FR
      path: locales/fr-FR.json
    - key: de-DE
      path: locales/de-DE.json
    - key: es-ES
      path: locales/es-ES.json
```
```

Nested within `translations`, you also have to define the fallback configurations for your app.
Configuring a default fallback is mandatory, and you also have the option to add locale-specific fallback
configurations. To learn more, see [Fallback configurations](/platform/forge/internationalization/#fallback-configurations).

In this example, the default fallback is `en-US`. The locale-specific fallback configurations are as follows:

* The fallback for `zh-TW` is `zh-CN`.
* The fallback for both `de-DE` and `en-ES` is `en-GB`.

```
```
1
2
```



```
  fallback:
    default: en-US
    zh-TW:
      - zh-CN
    de-DE:
      - en-GB
    es-ES:
      - en-GB
```
```

When resolving a translation, the app first attempts to find a translation for the user's specific
locale. If this translation is not available, the app will look for a translation in a locale-specific
fallback, if one is configured. If neither is found, the app will use the default fallback translation.

## Step 3: Add translatable keys to the module properties

Within your `manifest.yml` file, add the `i18n object` to any of the module properties that you want
to be translated. This instructs your app to find the corresponding value in the translation files
using the given key.

In this example, we are adding an `i18n object` to the `modules.macro.title`.

```
```
1
2
```



```
modules:
  macro:
    - key: forge-i18n-question-generator-app-ui-kit
      resource: main
      render: native
      resolver:
        function: resolver
      title:
        i18n: app.title
```
```

Now, based on the user’s locale, the app fetches the relevant translation file and loads the
translated strings for any properties with the `i18n object`. In the case it can't find the
translation file or the `app.title` key for the given locale, it goes to the corresponding
translation file of the locale-specific fallback or the default fallback.

## Step 4: Add translatable keys to your app frontend

Next, we will demonstrate how to translate the content in your frontend app code by adding the
internationalization APIs and functions.

Import the function `useTranslation()` and the React Context Provider `I18nProvider` in `src/frontend/index.jsx`. For more information, see [useTranslation](/platform/forge/ui-kit/hooks/use-translation/).

```
```
1
2
```



```
import { useTranslation, I18nProvider } from '@forge/react';
```
```

Wrap the `I18nProvider` around your `App` component. The `I18nProvider` initializes and provides an i18n context, which includes the user’s locale and the translation function. It makes these accessible to any components that consume this context.

```
```
1
2
```



```
ForgeReconciler.render(
  <React.StrictMode>
    <I18nProvider>
      <App />
    </I18nProvider>
  </React.StrictMode>
);
```
```

Next, we will create the `QuestionContent` component.

Create the file `src/frontend/QuestionContent.jsx` and copy the code below. The current question index, stored as `questionKey`, is passed as a prop to `QuestionContent`. This will be used to construct the translation key, `question.${questionKey}`.

```
```
1
2
```



```
import React from 'react';
import {
  useTranslation,
  Text,
  SectionMessage,
} from '@forge/react';

export const QuestionContent = ({ questionKey }) => {
  const { t } = useTranslation();
  return (
    <SectionMessage appearance="discovery">
      <Text weight="bold" size="medium">
        {t(`question.${questionKey}`)}
      </Text>
    </SectionMessage>
  );
};
```
```

For example, if the current question index is `0`, then the `questionKey` is `q_0` and the translation key will be `question.q_0`. This translation key will be passed to the translation function, which returns the translated string based on the user’s locale.

```
```
1
2
```



```
"question": {
    "q_0": "What's the best thing you've crossed off your bucket list? [en-US]",
    ...
},
```
```

Next, we will create the `QuestionGeneratorPanel` component.

Create the file `src/frontend/QuestionGeneratorPanel.jsx` and copy the code below. This component creates the UI of the question generator panel using the `QuestionContent` component. It contains a translatable header, introduction text, question, the current locale, and a *Next* button. It also contains a hook for the current question index that is passed to `QuestionContent`.

```
```
1
2
```



```
import React, { useState, useCallback } from 'react';
import {
  useTranslation,
  Stack,
  Inline,
  Text,
  Button,
  Lozenge,
  Heading
} from '@forge/react';
import { QuestionContent } from './QuestionContent';

const NUM_QUESTIONS = 54;

export const QuestionGeneratorPanel = () => {
  const { t, locale } = useTranslation(); // Creates the translation function and user locale from useTranslation()
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);

  return (
    <Stack space="space.200">
      <Heading as="h1">{t("ui.header")}</Heading> // Displays the heading of the app
      <Text>{t("ui.text.intro")}</Text>
      <QuestionContent questionKey={`q_${currentQuestionIndex}`} /> // The QuestionContent displays the current question
      <Inline alignBlock="center" space="space.100">
        <Heading as="h3">{t("ui.text.currentLocale")}</Heading>
        <Lozenge>{locale}</Lozenge>
      </Inline>
      <Inline alignInline="end">
        <Button appearance="primary">
          {t("ui.button.nextQuestion")}
        </Button>
      </Inline>
    </Stack>
  );
};
```
```

Next, add the following function before the return statement. This increments the question index when the *Next* button is clicked by a user. Also add the function onto the `onClick` prop of the button.

```
```
1
2
```



```
  const nextQuestion = useCallback(() => {
    setCurrentQuestionIndex((prevIndex) => (prevIndex + 1) % NUM_QUESTIONS);
  }, [setCurrentQuestionIndex]);

  return (
  ...
    <Button appearance="primary" onClick={nextQuestion}>
      {t("ui.button.nextQuestion")}
    </Button>
  ...
  );
```
```

Finally, add the `QuestionGeneratorPanel` to your `App` component in `src/frontend/index.jsx`. The `useTranslate()` hook will return the `ready` state, the translation function - which is bound to a specified `locale` code through the `I18nProvider` - and the user’s `locale`.

`ready` will resolve to true once the i18n context is fully initialized. While `ready` is `false`, the UI will display a loading state. When `ready` is `true`, it will return the `QuestionGeneratorPanel` component.

```
```
1
2
```



```
const App = () => {
  const { ready } = useTranslation();

  if (!ready) {
    return <Spinner size="large" />;
  }

  return <QuestionGeneratorPanel />;
};
```
```

Ensure you deploy your app with `forge deploy`.

Congratulations! You now have a question generator app in Confluence that will adapt based on the user's
language.

## Next steps

To learn more, see:
