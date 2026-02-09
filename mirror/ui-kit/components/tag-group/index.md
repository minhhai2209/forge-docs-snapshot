# Tag group

To add the `TagGroup` component to your app:

```
1
import { TagGroup } from '@forge/react';
```

## Description

A tag group controls the layout and alignment for a collection of tags.

## Props

| `Name` | `Type` | Required | Description |
| --- | --- | --- | --- |
| `alignment` | `"start" | "end"` | No | Whether the tags should be left-aligned or right-aligned. |
| `children` | `ForgeComponent` | Yes | Tags to render within the tag group. |

## Examples

### Default

By default, a tag group lays out a collection of tags from left to right, handling overflow by wrapping to the next line.

In most cases, all of the tags inside of a tag group should be of the same type to provide a consistent user experience.

![Example image of a tag group](https://dac-static.atlassian.com/platform/forge/ui-kit/images/tag-group/tag-group-default.png?_v=1.5800.1834)

```
```
1
2
```



```
const TagGroupDefaultExample = () => {
  return (
    <TagGroup>
      <Tag text="Bitbucket" />
      <Tag text="Compass" />
      <Tag text="Confluence" />
      <Tag text="Jira" />
      <Tag text="Jira Service Management" />
      <Tag text="Jira Software" />
      <Tag text="Jira Work Management" />
      <Tag text="Opsgenie" />
      <Tag text="Statuspage" />
      <Tag text="Trello" />
    </TagGroup>
  );
};
```
```

### Alignment

The alignment direction can be set to either the `start` or `end` of the tag group container using the `alignment` prop.

#### Start

Set the `alignment` prop to `start` to align the tags to the start of the tag group container.

![Example image of a start aligned tag group](https://dac-static.atlassian.com/platform/forge/ui-kit/images/tag-group/tag-group-alignment-start.png?_v=1.5800.1834)

```
```
1
2
```



```
const TagGroupStartAlignmentExample = () => {
  return (
    <TagGroup alignment="start">
      <Tag text="Bitbucket" />
      <Tag text="Compass" />
      <Tag text="Confluence" />
      <Tag text="Jira" />
      <Tag text="Jira Service Management" />
      <Tag text="Jira Software" />
      <Tag text="Jira Work Management" />
      <Tag text="Opsgenie" />
      <Tag text="Statuspage" />
      <Tag text="Trello" />
    </TagGroup>
  );
};
```
```

#### End

Set the`alignment` prop to `end` to align the tags to the end of the group.

![Example image of an end aligned tag group](https://dac-static.atlassian.com/platform/forge/ui-kit/images/tag-group/tag-group-alignment-end.png?_v=1.5800.1834)

```
```
1
2
```



```
const TagGroupEndAlignmentExample = () => {
  return (
    <TagGroup alignment="end">
      <Tag text="Bitbucket" />
      <Tag text="Compass" />
      <Tag text="Confluence" />
      <Tag text="Jira" />
      <Tag text="Jira Service Management" />
      <Tag text="Jira Software" />
      <Tag text="Jira Work Management" />
      <Tag text="Opsgenie" />
      <Tag text="Statuspage" />
      <Tag text="Trello" />
    </TagGroup>
  );
};
```
```
