# invoke

The `invoke` bridge method enables UI Kit and Custom UI apps to run backend FaaS functions hosted by Atlassian.

To use the `invoke` bridge method, you need to define your functions using the
[Forge UI resolver](/platform/forge/runtime-reference/forge-resolver/).

Invocations from users, webtriggers, or scheduled triggers are subject to Forge's [invocation limits](/platform/forge/platform-quotas-and-limits/#invocation-limits).

## Function signature

```
1
2
3
4
function invoke(
  functionKey: string,
  payload?: { [key in number | string]: any }
): Promise<{ [key: string]: any } | void>;
```

## Arguments

* **functionKey**: A string identifier for the resolver function to invoke with this method.
  This string should exactly match the `functionKey` in one of your resolver function definitions.
* **payload**: Data that is passed into the resolver function.

## Returns

* A `Promise` that resolves with the data returned from the invoked function.

## Example

```
```
1
2
```



```
import { invoke } from '@forge/bridge';

invoke('getText', { example: 'my-invoke-variable' }).then((data) => console.log(data));
```
```

## Type-safe invocations

When using TypeScript, you can reuse the types between the backend and frontend
code to make invocations type-safe. See
[resolver documentation](/platform/forge/runtime-reference/forge-resolver/#type-safe-invocations)
for more details.

Type safety prevents accidental mistakes when developing the application. It is
not a security mechanism: if another part of the application or a third-party
library uses type overrides like `any`, the error will not be caught at runtime.
Sensitive data should be validated separately.

```
```
1
2
```



```
// In a definitions file shared between UI and backend:
export type Defs = {
  getText: (example: string) => { text: string };
};

// In the UI:
import { makeInvoke } from '@forge/bridge';

const invoke = makeInvoke<Defs>();

// This call will ensure correct types
const result = await invoke('getText', { example: 'my-invoke-variable' });
console.log(result.text);
```
```

The following incorrect calls will be rejected by the compiler:

```
```
1
2
```



```
// ERROR: 'message' is not defined on the result
console.log(result.message);

// ERROR: 'sample' is not the right parameter
await invoke('getText', { sample: 'my-invoke-variable' });
```
```

### Function signature

```
```
1
2
```



```
function makeInvoke<D extends Definitions>(): Invoke<D>;
```
```

The `Definitions`, `Invoke`, and associated types ensure the parameters and
return types conform to the shared definitions.
