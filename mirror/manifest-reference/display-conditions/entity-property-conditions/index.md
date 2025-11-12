# Entity property conditions

In addition to [common](/platform/forge/manifest-reference/display-conditions/#common-properties)
and [Jira-](/platform/forge/manifest-reference/display-conditions/jira/) or [Confluence-](/platform/forge/manifest-reference/display-conditions/confluence/)specific conditions,
both Atlassian apps support conditions that are based on the properties of an entity being viewed
(for example, an issue, page or blog post) or its container (for example, a project or space).

The following property conditions are supported:

* `entityPropertyExists`
* `entityPropertyEqualTo`
* `entityPropertyContainsAny`
* `entityPropertyContainsAll`
* `entityPropertyContainsAnyUserGroup` (Confluence only)

These property conditions allow comparisons to be made against data (properties) stored by the Forge app
in the host Atlassian app. Usually, properties are set by a REST call against an entity type. See the
REST API documentation for details on how to manage
properties for different types of entities for [Jira](/cloud/jira/platform/rest) or [Confluence](/cloud/confluence/rest).

Property conditions are defined in the `displayConditions` section of a module in the `manifest.yml`
file, as shown below:

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
modules:
  confluence:contentBylineItem:
    - key: example-app-key
      function: main
      title: Example App
      displayConditions:
        entityPropertyEqualTo:
          entity: content
          propertyKey: myPropertyKey
          value: myValue
          objectName: myNestedField.subField
```

You can use the operators `and`, `or`, and `not` to build more complex display rules that involve
multiple common properties and conditions. See
[Usage of complex display rules](#usage-of-complex-display-rules)
for more details.

## Parameters

The following parameters define all four property conditions.

| Name | Type | Required | Description |
| --- | --- | --- | --- |
| `entity` | `string` | Yes | The type of an entity to read the property from. If an entity of the expected type is not present in the rendering context of the user interface element, the condition evaluates to `false`.  Depending on the Atlassian app and module, supported values are:   * `app` (Jira, Confluence) * `issue` (Jira) * `issueType` (Jira) * `project` (Jira) * `user` (Jira, Confluence) * `content` (Confluence) * `space` (Confluence) |
| `propertyKey` | `string` | Yes | The key of the property that's being checked. If the property is not present, the condition evaluates to `false`. |
| `value` | `string`, `Array<string>` | Required in all property conditions except `entityPropertyExists` | The value to match the actual property value with. This can be a `string` or an array of strings, depending on the property condition type. |
| `objectName` | `string` |  | If the property value is a JSON object, this parameter allows you to specify a path inside the object to match a value from.  If specified, the evaluation is done against a value of a field inside the JSON property value, not the property value itself.  If there is no field inside JSON that corresponds to the value specified in `objectName`, the condition evaluates to `false`. |

As an example, if the value of `objectName` is defined as `myField.mySubField`, then the condition
is evaluated against the string `myValue` for the JSON property shown below:

```
```
1
2
```



```
{
  "theirField": "theirValue",
  "myField": {
    "mySubField": "myValue",
    "otherSubField": "otherValue"
  }
}
```
```

## Evaluation of property conditions

The evaluation of property conditions depends on the property condition type itself and how the
parameters for the property conditions are defined.

### entityPropertyExists

`entityPropertyExists` evaluates to `true` if an entity property with a key defined by the
`propertyKey` parameter exists for an entity. If `objectName` is specified, the condition evaluates
to `true` if property value is a JSON object and has a nested field that corresponds to a specified path,
as described in the [Parameters](#parameters) section.

#### Example 1

The property condition shown below evaluates to `true` if the page or blog post the user is viewing has a
property with the key `myPropertyKey`:

```
```
1
2
```



```
entityPropertyExists:
  entity: content
  propertyKey: myPropertyKey
```
```

#### Example 2

```
```
1
2
```



```
entityPropertyExists:
  entity: content
  propertyKey: myPropertyKey
  objectName: completed
```
```

The property condition evaluates to `true` for the property value shown below:

```
```
1
2
```



```
{
  "completed": "2021-08-01",
  "otherField": true
}
```
```

### entityPropertyEqualTo

`entityPropertyEqualTo` evaluates to `true` if a value of an entity property with a key defined
by the `propertyKey` parameter is equal to the value specified in the `value` parameter of a condition.
If `objectName` is specified, the comparison is done against a field inside a JSON property value,
as described in the [Parameters](#parameters) section.

The referred property value or field value is converted to a string before the comparison. See
[Comparison of non-string values](#comparison-of-non-string-values) for more details.

#### Example

```
```
1
2
```



```
entityPropertyEqualTo:
  entity: space
  propertyKey: myAppSpaceSettings
  objectName: isEnabled
  value: true
```
```

The property condition evaluates to `true` for the property value shown below:

```
```
1
2
```



```
{
  "isEnabled": true,
  "otherFields": "..."
}
```
```

### entityPropertyContainsAny

`entityPropertyContainsAny` evaluates to `true` if a value of an entity property with a key defined
by the `propertyKey` parameter is an array and contains at least one of the values specified
in the `value` condition parameter. If `objectName` is specified, the comparison is done against
a field inside a JSON property value, as described in the [Parameters](#parameters) section.

By default, both the property value and the condition `value` parameter are expected to be arrays.
If you define these values as regular strings, the values are treated as arrays containing one element.

The Forge manifest schema enforces all elements in the `value` parameter array to be strings.
As for the entity property value, all elements in the array are converted to strings before the comparison.
See [Comparison of non-string values](#comparison-of-non-string-values) for more details.

#### Example 1

The property condition shown below evaluates to `true` for the property value
[`"otherValue1"`, `"myValue2"`, `"otherValue2"`] because `"myValue2"` is in both arrays:

```
```
1
2
```



```
entityPropertyContainsAny:
  entity: space
  propertyKey: myPropertyKey
  value:
    - myValue1
    - myValue2
```
```

#### Example 2

The property condition shown below evaluates to `true` for the property value
[`"otherValue1"`, `"myValue2"`, `"otherValue2"`] because `"myValue2"` is a value of the condition
and is contained in the property value array:

```
```
1
2
```



```
entityPropertyContainsAny:
  entity: space
  propertyKey: myPropertyKey
  value: myValue2
```
```

### entityPropertyContainsAll

`entityPropertyContainsAll` evaluates to `true` if a value of an entity property with a key defined
by the `propertyKey` parameter is an array and it contains all of the values specified
in the `value` condition parameter. If `objectName` is specified, the comparison is done against
a field inside a JSON property value, as described in the [Parameters](#parameters) section.

Allowed values and limitations for property values and the condition `value` parameter are the same
as for the [entityPropertyContainsAny](#entitypropertycontainsany) condition type.

#### Example

The property condition shown below evaluates to `true` for the property value
[`"otherValue1"`, `"myValue2"`, `"otherValue2"`, `"myValue1"`] because both `"myValue1"` and
`"myValue2"` are in the property value array:

```
```
1
2
```



```
entityPropertyContainsAll:
  entity: space
  propertyKey: myPropertyKey
  value:
    - myValue1
    - myValue2
```
```

### entityPropertyContainsAnyUserGroup (Confluence only)

`entityPropertyContainsAnyUserGroup` evaluates to `true` when the entity property specified by propertyKey contains an array of group names or IDs, and the currently logged-in user is a member of at least one of those groups. If `objectName` is specified, the comparison is done against
a field inside a JSON property value, as described in the [Parameters](#parameters) section.

Do not specify a value parameter for this condition. The system automatically uses the group memberships of the currently logged-in user to perform the comparison against the array found in the entity property

## Comparison of non-string values

Since the Forge manifest schema only allows a string or an array of strings as a property condition value,
entity property values are converted to strings before the comparison.

* If the referenced value is a primitive other than a `string`, the value is converted to a string.
* If the referenced value is an object, the value is converted to a string by applying
  the `JSON.stringify` function.
* If the referenced value is an array, the value remains as an array, but its elements are converted
  to strings.

This includes elements that are objects or arrays themselves. They are converted to a string
by applying the `JSON.stringify` function.

### Example 1

```
```
1
2
```



```
{
  "myField": {
    "mySubField": 42
  }
}
```
```

If a condition has `objectName` equals to `myField`, the matching property value is `"{\"mySubField\":42}"`.

If `objectName` equals to `myField.mySubField`, the matching property value is `"42"` (string).

### Example 2

```
```
1
2
```



```
{
  "myField": ["value1", "value2", { "mySubField": 42 }]
}
```
```

If a condition has `objectName` equals to `myField`, the matching property value is
`["value1", "value2", "{\"mySubField\":42}"]`.

### Example 3

```
```
1
2
```



```
["value1", "value2", ["subValue1", "subValue2"]]
```
```

The matching property value is `["value1", "value2", "[\"subValue1\",\"subValue2\"]"]`.

## Usage of complex display rules

You can use the [operators](/platform/forge/manifest-reference/display-conditions/#operators)
`and`, `or`, and `not` to build complex rules that involve multiple different types of conditions.

In Jira, this works the same as for all other conditions.
In Confluence, the rules described below apply.

#### One property condition per level (Confluence only)

Only one property condition is allowed on the same level of a display conditions tree. For example, the following
structure is *not* allowed:

```
```
1
2
```



```
displayConditions:
  or:
    entityPropertyExists:
      ...
    entityPropertyEqualTo:
      ...
```
```

You can use an array if you need to use multiple property conditions on the same level, as shown below:

```
```
1
2
```



```
displayConditions:
  or:
    - entityPropertyExists:
        ...
    - entityPropertyEqualTo:
        ...
```
```

Only property conditions are allowed as array elements. You cannot use operators and
common properties in arrays.

Alternatively, the same condition can be defined like this:

```
```
1
2
```



```
displayConditions:
  or:
    entityPropertyExists:
      ...
    or:
      entityPropertyEqualTo:
        ...
```
```

#### Property conditions and common properties on the same level

Property conditions may be used together with common properties on the same level of a display
conditions tree:

```
```
1
2
```



```
displayConditions:
  or:
    isAdmin: true
    entityPropertyExists:
      ...
```
```

In Confluence, while multiple common properties are allowed on the same level of a conditions tree, only one
property condition is allowed on that level.
