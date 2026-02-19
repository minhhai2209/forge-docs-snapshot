# requestBitbucket

The `requestBitbucket` bridge method enables Forge apps to call the
[Bitbucket Cloud REST API](/cloud/bitbucket/rest/) as the current user.

## Function signature

```
1
2
3
4
function requestBitbucket(
  uri: string,
  options?: RequestInit,
): Promise<Response>
```

## Arguments

## Returns

## Example

```
1
2
3
4
5
import { view, requestBitbucket } from '@forge/bridge';

const context = await view.getContext();
const response = await requestBitbucket(`/2.0/repositories/${context.workspaceId}/${context.extension.repository.uuid}`);
console.log(await response.json());
```
