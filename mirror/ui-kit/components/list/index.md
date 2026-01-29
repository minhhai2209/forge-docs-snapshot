# List

To add the `List` and `ListItem` components to your app:

```
1
import { List, ListItem } from "@forge/react";
```

## Description

An unordered (bulleted) or ordered (numbered) list.

## Props

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| `type` | `"ordered" | "unordered"` | No | The `ordered` type should be used when representing an ordered list of items. The `unordered` type should be used when representing an unordered list of items. The type is set to `unordered` by default |
| `children` | `Array<ListItem>` | Yes | The items to render inside a `List` group. |

## Examples

### Unordered list

An unordered list is rendered with bullets.

![Example image of an unordered list](https://dac-static.atlassian.com/platform/forge/ui-kit/images/list/list-unordered.png?_v=1.5800.1805)

```
```
1
2
```



```
import { List, ListItem } from "@forge/react";

const App = () => {
  return (
    <List type="unordered">
      <ListItem>Confluence</ListItem>
      <ListItem>Jira</ListItem>
      <ListItem>Bitbucket</ListItem>
    </List>
  );
};
```
```

### Nested unordered list

A nested unordered list. Bullet styles rotate in the following order when nested: Disc, Circle, Square.

![Example image of an nested unordered list](https://dac-static.atlassian.com/platform/forge/ui-kit/images/list/list-unordered-nested.png?_v=1.5800.1805)

```
```
1
2
```



```
import { List, ListItem, Text } from "@forge/react";

const App = () => {
  return (
    <List type="unordered">
      <ListItem>
        One
        <List type="unordered">
          <ListItem>
            <Text>Two</Text>
            <List type="unordered">
              <ListItem>
                <Text>Three</Text>
                <List type="unordered">
                  <ListItem>
                    <Text>Four</Text>
                    <List type="unordered">
                      <ListItem>
                        <Text>Five</Text>
                        <List type="unordered">
                          <ListItem>
                            <Text>Six</Text>
                          </ListItem>
                        </List>
                      </ListItem>
                    </List>
                  </ListItem>
                </List>
              </ListItem>
            </List>
          </ListItem>
        </List>
      </ListItem>
    </List>
  );
};
```
```

### Ordered List

An ordered (numbered) list

![Example image of an ordered list](https://dac-static.atlassian.com/platform/forge/ui-kit/images/list/list-ordered.png?_v=1.5800.1805)

```
```
1
2
```



```
import { List, ListItem } from "@forge/react";

const App = () => {
  return (
    <List type="ordered">
      <ListItem>Confluence</ListItem>
      <ListItem>Jira</ListItem>
      <ListItem>Bitbucket</ListItem>
    </List>
  );
};
```
```

### Nested ordered list

A nested ordered list. Bullet styles rotate in the following order when nested: Decimal, Lower-Alpha, Lower-Roman.

![Example image of an nested ordered list](https://dac-static.atlassian.com/platform/forge/ui-kit/images/list/list-ordered-nested.png?_v=1.5800.1805)

```
```
1
2
```



```
import { List, ListItem, Text } from "@forge/react";

const App = () => {
  return (
    <List type="ordered">
      <ListItem>
        One
        <List type="ordered">
          <ListItem>
            <Text>Two</Text>
            <List type="ordered">
              <ListItem>
                <Text>Three</Text>
                <List type="ordered">
                  <ListItem>
                    <Text>Four</Text>
                    <List type="ordered">
                      <ListItem>
                        <Text>Five</Text>
                        <List type="ordered">
                          <ListItem>
                            <Text>Six</Text>
                          </ListItem>
                        </List>
                      </ListItem>
                    </List>
                  </ListItem>
                </List>
              </ListItem>
            </List>
          </ListItem>
        </List>
      </ListItem>
    </List>
  );
};
```
```

### Nested mixed list

A nested list with a mix of unordered and ordered lists, which maintains the aforementioned bullet style pattern at each nest level regardless of list type.

![Example image of an nested mixed list](https://dac-static.atlassian.com/platform/forge/ui-kit/images/list/list-mixed-nested.png?_v=1.5800.1805)

```
```
1
2
```



```
import { List, ListItem, Text } from "@forge/react";

const App = () => {
  return (
    <List type="ordered">
      <ListItem>
        <Text>Confluence</Text>
        <List type="unordered">
          <ListItem>One</ListItem>
          <ListItem>
            <Text>Two</Text>
            <List type="unordered">
              <ListItem>Three</ListItem>
            </List>
          </ListItem>
        </List>
      </ListItem>

      <ListItem>
        <Text>Jira</Text>
        <List type="unordered">
          <ListItem>One</ListItem>
          <ListItem>
            <Text>Two</Text>
            <List type="unordered">
              <ListItem>Three</ListItem>
            </List>
          </ListItem>
        </List>
      </ListItem>
    </List>
  );
};
```
```
