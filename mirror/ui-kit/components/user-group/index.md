# User group

To add the `UserGroup` component to your app:

```
1import { UserGroup } from '@forge/react';
2
```

## Description

A stack of multiple [users](/platform/forge/ui-kit-2/user/)
(name and profile picture), subject to their [privacy settings](https://confluence.atlassian.com/x/lwkvOg).
The `UserGroup` component can also be [used within a Text component](/platform/forge/ui-kit-2/text/#usergroup),
appearing as lozenges with the names of the users when used within this context.

## Props

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| `children` | `Array<User>` | Yes | The users (specified by Atlassian account ID) whose avatars and/or names are displayed in the `UserGroup`. See [User](/platform/forge/ui-kit-2/user) for further details on the props. |

## Examples

### Default

A simple group of seven users using the `UserGroup` component.

![Example image of a rendered group of seven Atlassian users](https://dac-static.atlassian.com/platform/forge/images/ui-kit-2/user-group.png?_v=1.5800.2310)

```
1import { UserGroup, User } from '@forge/react';
2const App = () => {
3    return (
4        <UserGroup>
5            <User accountId="5a1234bc8d12345e3f1g11hi"/>
6            <User accountId="2a98a42dbc7ab42e12ee360d"/>
7            <User accountId="5d8732lq8jg85a0e3f1g90as"/>
8            <User accountId="2h98a10dbl5ab93e62hja23z"/>
9            <User accountId="7b20f0bc2d05325e3f1g43ty"/>
10            <User accountId="2p72s42dbc7ab42e90gf252d"/>
11            <User accountId="2l01x78mf4pqw42e84fg40ad"/>
12        </UserGroup>
13    );
14};
15
```

### Inline

![Example image of a rendered inline group of three Atlassian users within a Text component](https://dac-static.atlassian.com/platform/forge/images/ui-kit-2/user-group-inline.png?_v=1.5800.2310)

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
<Text>
  Contributors: <UserGroup>
        <User accountId="5a1234bc8d12345e3f1g11hi" />
        <User accountId="3a1236bc8d12345e3f1g11ok" />
        <User accountId="3g123an8t12345a3c1h11ris" />
    </UserGroup>
</Text>
```
```
