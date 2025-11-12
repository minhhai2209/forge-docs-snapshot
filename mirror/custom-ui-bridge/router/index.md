# router

The `router` object enables you to navigate the host Atlassian app to another page.

## navigate

The `navigate` method allows you to navigate the host window to a given URL.
If you’re linking to an external site, the user is prompted before opening the link in a new tab.
If the user declines to proceed, the returned `Promise` is rejected.

If you’re using relative URLs (starts with `/`), the user won’t be prompted.

### Function signature

```
1
function navigate(url: string): Promise<void>;
```

### Example

```
1
2
3
4
5
import { router } from '@forge/bridge';

router.navigate('/browse/ISSUE-1234');

router.navigate('https://example.com');
```

## open

The `open` method allows you to open a new window to a given URL.
If you’re linking to an external site, the user is prompted before opening the link in a new window.
If the user declines to proceed, the returned `Promise` is rejected.

If you’re using relative URLs (starts with `/`), the user won’t be prompted.

### Function signature

```
```
1
2
```



```
function open(url: string): Promise<void>;
```
```

### Example

```
```
1
2
```



```
import { router } from '@forge/bridge';

router.open('/browse/ISSUE-1234');

router.open('https://example.com');
```
```

## reload

The `reload` method allows you to reload the host window.

### Function signature

```
```
1
2
```



```
function reload(): Promise<void>;
```
```

### Example

```
```
1
2
```



```
import { router } from '@forge/bridge';

router.reload();
```
```
