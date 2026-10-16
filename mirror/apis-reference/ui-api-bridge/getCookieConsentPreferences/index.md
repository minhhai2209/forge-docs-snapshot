# getCookieConsentPreferences

The `getCookieConsentPreferences` bridge method enables Forge apps to read the user's current
cookie consent preferences. Use it to decide whether your app may store data in the browser, such as
cookies, `localStorage`, or analytics identifiers.

## Overview

Users choose which categories of cookies and similar technologies they accept. Your app runs inside the
host page, so it should respect those choices before it stores or reads anything that isn't essential
for the app to work.

`getCookieConsentPreferences` returns the user's choices for each cookie category. When the user changes
their choices, the host emits a `FORGE_COOKIE_CONSENT_CHANGED` event that your app can subscribe to.

## Function signature

```
1function getCookieConsentPreferences(): Promise<CookieConsentPreferences | null>;
2
3type CookieConsentPreferences = {
4  functional: boolean;
5  analytics: boolean;
6  marketing: boolean;
7};
8
```

## Usage

The following example reads the user's preferences and stores a value in `localStorage` only when the
user has allowed functional storage.

```
1import { getCookieConsentPreferences } from "@forge/bridge";
2
3const STORAGE_KEY = "my-app-last-view";
4
5async function saveLastView(view: string): Promise<void> {
6  const preferences = await getCookieConsentPreferences();
7
8  if (!preferences?.functional) {
9    return;
10  }
11
12  localStorage.setItem(STORAGE_KEY, view);
13}
14
```

## Subscribe to changes

Use the [`events`](/platform/forge/apis-reference/ui-api-bridge/events/) API to subscribe to
`FORGE_COOKIE_CONSENT_CHANGED`. The event payload has the same shape as the value returned by
`getCookieConsentPreferences`.

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
21
22
23
24
25
26
27
28
29
```



```
import {
  events,
  getCookieConsentPreferences,
  type CookieConsentPreferences,
} from "@forge/bridge";

const STORAGE_KEY = "my-app-last-view";

function applyPreferences(preferences: CookieConsentPreferences | null): void {
  if (!preferences?.functional) {
    localStorage.removeItem(STORAGE_KEY);
  }
}

function init(): void {
  getCookieConsentPreferences().then(applyPreferences);

  const subscription = events.on(
    "FORGE_COOKIE_CONSENT_CHANGED",
    async (preferences: CookieConsentPreferences | null) => {
      applyPreferences(preferences);
    }
  );

  window.addEventListener("pagehide", () => {
    subscription.then(({ unsubscribe }) => unsubscribe());
  });
}
```
```

`events.on` resolves to a `Subscription`, so await it or chain from the promise to reach
`unsubscribe()`. Unsubscribe when your app's view is torn down, so the listener doesn't outlive the
code that handles the event. This example uses `pagehide` rather than the deprecated `unload` event.
If your app is a React component, call `unsubscribe()` from a
[`useEffect`](https://react.dev/reference/react/useEffect#connecting-to-an-external-system) cleanup
function instead.

## Return value

`getCookieConsentPreferences` returns a `Promise` that resolves to `null` or a
`CookieConsentPreferences` object.

| Value | Description |
| --- | --- |
| `null` | The user's preferences haven't loaded yet. Treat this as unknown and don't store anything non-essential. |
| `CookieConsentPreferences` | The user's current choice for each cookie category. |

The `CookieConsentPreferences` object has the following fields:

| Field | Type | Description |
| --- | --- | --- |
| `functional` | `boolean` | Whether the user allows storage that remembers their choices or settings, such as a preferred view. |
| `analytics` | `boolean` | Whether the user allows storage used to measure how people use your app. |
| `marketing` | `boolean` | Whether the user allows storage used for advertising or marketing purposes. |

A value of `false` means the user has denied that category. Storage that is strictly necessary for your app to work doesn't require consent, so it isn't included.

## Best practices

* **Default to denied.** If the method resolves to `null`, or a category is `false`, don't store
  data for that category.
* **Don't store non-essential data until consent is known.** Wait for the method to resolve with
  preferences before you write cookies, `localStorage` values, or analytics identifiers.
* **Subscribe to changes.** Listen for `FORGE_COOKIE_CONSENT_CHANGED` so your app reacts when the user
  updates their preferences during a session, and call `unsubscribe()` when the view is torn down.
* **Clear stored data when consent is withdrawn.** When a category changes from allowed to denied, remove
  the data your app stored for that category.
