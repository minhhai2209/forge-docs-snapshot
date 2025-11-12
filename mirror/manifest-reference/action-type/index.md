# Action type

### Modal

`modal` displays the app contents directly in a modal, so you don't need to use the
[UI Kit modal](/platform/forge/ui-kit/components/modal/) component. Modal closing is also managed
by default so there is no need to explicitly call [view.close()](/platform/forge/apis-reference/ui-api-bridge/view/#close)
to terminate the application.

```
```
1
2
```



```
import React from 'react';
import ForgeReconciler, { Text } from '@forge/react';
import { view } from '@forge/bridge';

const App = () => {
  return <Text>App Content</Text>;
};

ForgeReconciler.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```
```

### Dynamic

As `dynamic` does not have a pre-configured UI element, app content will not be rendered visibly
by default. Any app content that you would like to appear in the UI needs to be configured with
the relevant UI element, such as a [UI Kit modal](/platform/forge/ui-kit/components/modal/) or a
[flag](/platform/forge/apis-reference/ui-api-bridge/showFlag/#showflag).

When using `dynamic`, [view.close()](/platform/forge/apis-reference/ui-api-bridge/view/#close) should be called to properly terminate the Forge app. For example, if the app uses a UI Kit modal, the modal’s onClose handler should call [view.close()](/platform/forge/apis-reference/ui-api-bridge/view/#close) to close the app properly.

```
```
1
2
```



```
import React from 'react';
import ForgeReconciler, { Modal, ModalTransition, Button, Text } from '@forge/react';
import { view, showFlag } from '@forge/bridge';

const App = () => {
  const displayFlag = () => {
    showFlag({
      id: 'hello-world',
      title: 'Hello World',
      type: 'info',
      description: 'hi',
    });
  };

  return (
    <ModalTransition>
      <Modal onClose={() => view.close()}>
        <Text>App Content</Text>
        <Button onClick={displayFlag}>Display Flag</Button>
      </Modal>
    </ModalTransition>
  );
};

ForgeReconciler.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```
```
