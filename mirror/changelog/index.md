# Forge changelog

### EMPTY operators for issue properties and Epic Label

| JQL expression | Previous behavior (Match API/webhooks) | New behavior |
| --- | --- | --- |
| `field = EMPTY` | Did not match issues where the field was unset | Matches issues where the field is unset |
| `field IS EMPTY` | Matched correctly | No change |
| `field IN (EMPTY)` | Did not match issues where the field was unset | Matches issues where the field is unset |
| `field != EMPTY` | Matched all issues, including those where the field was unset | Only matches issues where the field is set |
| `field IS NOT EMPTY` | Matched correctly | No change |
| `field NOT IN (EMPTY)` | Matched all issues, including those where the field was unset | Only matches issues where the field is set |

This applies to both issue properties (for example, `issue.property[key].path`) and the "**Epic Label**" field.

### != comparisons for issue properties

| JQL expression | Previous behavior | New behavior |
| --- | --- | --- |
| `issue.property[key].path != "a"` | Returned issues where the property was never set | Only matches issues where the property exists and its value is not `"a"` |

### Impact

You may see differences in:

### Developer guidance

Review any JQL used in webhook filters or Match API requests that contains:

**Best practices:**

| Goal | Recommended JQL |
| --- | --- |
| Check if a field is set | `field IS NOT EMPTY` |
| Check if a field is not set | `field IS EMPTY` |

**Specific scenarios:**

To find issues where a property is either not set OR has a different value:

`issue.property[key].path != "a" OR issue.property[key].path IS EMPTY`

To find issues where a property is set AND has a different value:

`issue.property[key].path != "a" AND issue.property[key].path IS NOT EMPTY`

Test critical webhook flows and integrations that use the Match API to confirm they behave as expected.
