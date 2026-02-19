# Compass events

Forge apps can subscribe to Compass events for:

Your Forge app must have permission from the
site admin to access the data it provides within the event payload.
The OAuth scope required for each event is documented below.

## Component Links

Forge apps can subscribe to these events on a component:

* Link created: `avi:compass:created:component_link`
* Link updated: `avi:compass:updated:component_link`
* Link deleted: `avi:compass:deleted:component_link`

All component events require the OAuth scope `read:component:compass`.

All component events share the same payload format.

### Payload

| Name | Type | Description |
| --- | --- | --- |
| eventType | `string` | The event name such as `avi:compass:created:component_link`. |
| component | `Component` | The component that had a link change |

### Type reference

```
1
2
3
interface Component {
  id: string;
}
```

### Example

This is an example payload.

```
```
1
2
```



```
{
  "eventType": "avi:compass:created:component_link",
  "component": {
    "id": "ari:cloud:compass:00000000-0000-0000-0000-000000000000:component/00000000-0000-0000-0000-000000000000/00000000-0000-0000-0000-000000000000"
  }
}
```
```
