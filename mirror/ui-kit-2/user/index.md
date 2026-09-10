# User

To add the `User` component to your app:

```
1import { User } from '@forge/react';
2
```

## Description

A component that represents a user, displaying details such as name and profile picture, subject to
the user's [privacy settings](https://confluence.atlassian.com/x/lwkvOg).

## Props

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| `accountId` | `string` | Yes | The Atlassian account ID of the user. |
| `hideDisplayName` | `boolean` | No | Hides the display name to only display the user profile picture. |

## Examples

### Default

```
1export const UserExample = () => {
2  return (
3    <User accountId="5a1234bc8d12345e3f1g11hi" />
4  );
5}
6
```

![Example image of rendered pictures and names of Atlassian users](https://dac-static.atlassian.com/platform/forge/ui-kit/images/user/user-default.png?_v=1.5800.2327)

### Inline

![Example image of a rendered picture and name of an Atlassian user within a Text component](https://dac-static.atlassian.com/platform/forge/ui-kit/images/user/user-inline.png?_v=1.5800.2327)

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
```



```
export const UserInlineExample = () => {
  return (
    <Text>
      Contributors: <User accountId="5a1234bc8d12345e3f1g11hi" />
    </Text>
  );
}
```
```
