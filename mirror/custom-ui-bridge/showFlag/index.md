# showFlag

The `showFlag` bridge method enables UI Kit and Custom UI apps to open flags in the Atlassian app's flag group.

## Function signature

```
1function showFlag(flagOptions: FlagOptions): { close: () => Promise<boolean | void> };
2
3interface FlagOptions {
4  id: string;
5  title?: string;
6  description?: string;
7  type?: 'info' | 'success' | 'warning' | 'error';
8  appearance?: 'info' | 'success' | 'warning' | 'error';
9  actions?: FlagAction[];
10  isAutoDismiss?: boolean;
11}
12
13interface FlagAction {
14  text: string;
15  onClick: () => void;
16}
17
```

## Arguments

* **flagOptions**
  * **id**: A unique string identifier for the flag. This property is required.
  * **title**: The bold text shown at the top of the flag.
  * **description**: The secondary content shown below the flag's title.
  * **type**: The type of the flag. This will determine the flag's icon.
  * **appearance**: Makes the flag appearance bold if provided.
  * **actions**: The list of clickable actions to be shown at the bottom of the flag.
  * **isAutoDismiss**: Whether the flag is auto-dismissable or not. If set to `true`, the flag will automatically close after 8 seconds.

## Returns

* A flag object that contains a `close` function.

## Example

```
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
12
13
14
15
16
17
18
19
20
```



```
import { showFlag } from '@forge/bridge';

const flag = showFlag({
  id: 'success-flag',
  title: 'Hello World!',
  type: 'info',
  description: 'Here is a flag body description.',
  actions: [
    {
      text: 'Flag action',
      onClick: () => {
        console.log('flag action clicked');
      },
    }
  ],
  isAutoDismiss: true,
});

flag.close();
```
```
