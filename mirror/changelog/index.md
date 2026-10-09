# Forge changelog

**What's changing**  
Forge display conditions for Jira and Jira Service Management (JSM) modules now support arrays under the `and`, `or`, and `not` logical operators.

Previously, manifest keys had to be unique at each level, which made it difficult to repeat the same condition type or group multiple logical expressions. With this update, you can use an array of condition objects to define complex visibility logic more easily.

For example, you can now structure your manifest to group conditions or repeat the same condition type:

`1displayConditions:
2 or:
3 - and:
4 - entityPropertyExists: { entity: user, propertyKey: a }
5 - entityPropertyExists: { entity: user, propertyKey: b }
6 - and:
7 - entityPropertyExists: { entity: user, propertyKey: c }
8 - entityPropertyExists: { entity: user, propertyKey: d }`

**What you need to do**  
No action is required for existing apps, as the previous syntax remains supported. If you want to simplify complex logic or repeat conditions in your Jira or JSM modules, you can update your manifest to use the new array-based syntax.

For more details and examples, see the [Forge display conditions documentation](https://developer.atlassian.com/platform/forge/manifest-reference/display-conditions/#use-the-same-condition-more-than-once--jira-and-jira-service-management- "https://developer.atlassian.com/platform/forge/manifest-reference/display-conditions/#use-the-same-condition-more-than-once--jira-and-jira-service-management-").
