# Manage the 1,000 value limit in custom JQL functions

When using custom JQL functions that return large result sets, customers encounter this error:

> The JQL function 'x' returns more issues (over 1000) than the maximum allowed.

**Specific Error Details:**

* **Error Type**: `VALIDATION_ERROR`
* **User Message**: "Function '{function\_name}' provided by '{app\_name}' has returned more than the maximum of 1000 values for this JQL fragment."

### Why This Happens

Custom JQL functions often serve broad purposes that naturally return large datasets. Common examples:

* Finding all items associated with a parent entity
* Retrieving all linked issues of a certain type
* Finding all issues with specific custom field values
* Querying hierarchical relationships across projects

For large enterprise customers, these queries can easily return thousands of results, which may have been acceptable in Data Center environments but hits the Cloud platform limit. The 1000 value limit exists primarily due to PostgreSQL database constraints and performance concerns in a multi-tenant cloud environment. Large IN clauses with thousands of values cause exponential increases in query planning time, consume excessive memory across multiple layers (app cache, database, network), and can degrade performance for all customers sharing the infrastructure. Keeping all these factors in mind, a limit of 1000 has been decided.

---

## Available Workarounds

App developers and customers have several options to work within the 1000 value limit while achieving similar outcomes to Data Center environments.

### Write more specific queries

**Strategy**: Add function parameters or additional JQL predicates to narrow down results.

#### Implementation for App Developers

**Current function design:**

```
```
1
2
```



```
// Function: relatedIssues(parentKey)
// Returns: ALL related issues for a parent (might be 5000+)
function relatedIssues(parentKey) {
  const issues = getAllRelatedIssues(parentKey);
  return {
    jql: `key IN (${issues.join(', ')})`  // ❌ Fails if > 1000
  };
}
```
```

**Improved design with filters:**

```
```
1
2
```



```
// Function: relatedIssues(parentKey, status, dateRange)
// Returns: Filtered related issues (< 1000)
function relatedIssues(parentKey, status, dateRange) {
  const issues = getFilteredRelatedIssues(parentKey, status, dateRange);
  return {
    jql: `key IN (${issues.join(', ')})`  // ✅ Under 1000
  };
}
```
```

#### Usage Example

**Instead of:**

```
```
1
2
```



```
issue in relatedIssues("PARENT-123")
```
```

**Use:**

```
```
1
2
```



```
issue in relatedIssues("PARENT-123", "Open", "-30d") AND priority = High
```
```

---

**Strategy**: Build pagination directly into custom JQL functions.

#### Implementation for App Developers

Add pagination parameters to function signatures:

```
```
1
2
```



```
// Function: relatedIssues(parentKey, page, pageSize)
function relatedIssues(parentKey, page = 1, pageSize = 500) {
  const allIssues = getAllRelatedIssues(parentKey);
  const totalResults = allIssues.length;
  const totalPages = Math.ceil(totalResults / pageSize);
  
  // Calculate pagination
  const startIndex = (page - 1) * pageSize;
  const endIndex = startIndex + pageSize;
  const pageResults = allIssues.slice(startIndex, endIndex);
  
  if (pageResults.length === 0) {
    return {
      error: `No results on page ${page}. Total pages: ${totalPages}`,
      storeErrorAsPrecomputation: true
    };
  }
  
  return {
    jql: `key IN (${pageResults.join(', ')})`  // ✅ Max 500 per page
  };
}
```
```

#### Usage Example

Query page by page:

```
```
1
2
```



```
-- Page 1 (results 1-500)
issue in relatedIssues("PARENT-123", 1, 500)

-- Page 2 (results 501-1000)
issue in relatedIssues("PARENT-123", 2, 500)

-- Page 3 (results 1001-1500)
issue in relatedIssues("PARENT-123", 3, 500)
```
```

Or combine pages:

```
```
1
2
```



```
issue in relatedIssues("PARENT-123", 1, 500) 
  OR issue in relatedIssues("PARENT-123", 2, 500)
```
```

---

### Return JQL queries instead of value lists

**Strategy**: Return a JQL query that expresses the search criteria, rather than an explicit list of issue keys.

**This is the most powerful and recommended approach** as it bypasses the value limit entirely.

#### Understanding the Difference

When a custom JQL function returns a response, it provides a JQL fragment that Jira then parses and executes.

**❌ AVOID: Returning explicit value lists**

```
```
1
2
```



```
{
  "jql": "key IN (ISSUE-1, ISSUE-2, ISSUE-3, ..., ISSUE-1500)"
}
```
```

* This creates 1500 literal values in the JQL
* Hits the 1000 value limit
* Validation fails before query execution

**✅ PREFER: Returning JQL query conditions**

```
```
1
2
```



```
{
  "jql": "project = XTP AND labels = test-execution AND 'Test Plan' = PLAN-123"
}
```
```

* This is a query condition, not a value list
* No limit on how many results the query returns
* Jira executes the query naturally
* Can return millions of results without hitting the limit

#### How JQL Fragment Validation Works

The Jira platform validates JQL fragments by counting the number of literal values on the right-hand side of operators.

**What counts as a "value":**

* Each literal in `key IN (A, B, C)` → 3 values
* Each literal in `status IN (Open, Closed)` → 2 values
* Query conditions like `project = ABC` → 1 value
* Multiple conditions combined with `AND` → 1 value per condition

**Validation Logic:**

The platform counts all literal values in the JQL fragment. If the total exceeds 1000, the validation fails with a `TOO_LONG_VALUES_LIST` error.

#### Implementation for App Developers

The key is to structure your data so you can query it using Jira's native fields and custom fields.

**Approach A: Use Custom Fields**

If your app stores metadata in custom fields:

```
```
1
2
```



```
// Instead of returning a list of keys
function relatedIssues(parentKey) {
  // ❌ OLD WAY - Returns explicit list
  // const issues = getAllRelatedIssues(parentKey);
  // return { jql: `key IN (${issues.join(', ')})` };
  
  // ✅ NEW WAY - Query by custom field
  return {
    jql: `"Parent Reference" = "${parentKey}" AND type = "Sub-task"`
  };
}
```
```

**Approach B: Use Labels**

```
```
1
2
```



```
function relatedIssues(parentKey) {
  // When issues are created, tag them with labels
  return {
    jql: `labels = "parent-${parentKey}" AND type = "Related Issue"`
  };
}
```
```

**Approach C: Use Issue Links**

```
```
1
2
```



```
function relatedIssues(parentKey) {
  // Query issues linked to the parent
  return {
    jql: `issue in linkedIssues("${parentKey}", "relates to")`
  };
}
```
```

**Approach D: Combine Multiple Conditions**

```
```
1
2
```



```
function complexQuery(projectKey, category, status) {
  return {
    jql: `
      project = ${projectKey}
      AND "Category" = "${category}"
      AND status = ${status}
      AND created >= -90d
    `.trim()
  };
}
```
```

#### Usage Example

Transparent to the user:

```
```
1
2
```



```
issue in relatedIssues("PARENT-123")
```
```

Under the hood, this expands to:

```
```
1
2
```



```
issue in (
  "Parent Reference" = "PARENT-123" AND type = "Sub-task"
)
```
```

The platform executes this as a natural query, returning any number of results without hitting the value limit.

---

### Hybrid approach

**Strategy**: Combine the above approaches for optimal results.

#### Example Implementation

```
```
1
2
```



```
function relatedIssues(parentKey, page = null, status = null) {
  // Build base query using JQL conditions
  let jqlParts = [
    `"Parent Reference" = "${parentKey}"`,
    `type = "Sub-task"`
  ];
  
  // Add filters if provided to narrow results
  if (status) {
    jqlParts.push(`status = "${status}"`);
  }
  
  const baseJql = jqlParts.join(' AND ');
  
  // If no pagination needed, return query directly
  if (page === null) {
    return { jql: baseJql };
  }
  
  // If pagination requested, fall back to explicit enumeration
  const results = executeQuery(baseJql);
  const pageSize = 500;
  const startIndex = (page - 1) * pageSize;
  const pageResults = results.slice(startIndex, startIndex + pageSize);
  
  return {
    jql: `key IN (${pageResults.map(r => r.key).join(', ')})`
  };
}
```
```

#### Usage Example

**Simple case (returns all via query):**

```
```
1
2
```



```
issue in relatedIssues("PARENT-123")
```
```

**Filtered case:**

```
```
1
2
```



```
issue in relatedIssues("PARENT-123", null, "Open")
```
```

**Paginated case:**

```
```
1
2
```



```
issue in relatedIssues("PARENT-123", 1)
```
```

---

## Comparison

| Criteria | Write more specific queries | Implement pagination | Return JQL queries | Hybrid approach |
| --- | --- | --- | --- | --- |
| **Bypasses 1000 limit** | No | No | Yes ✓ | Conditional |
| **Implementation complexity** | Low | Medium | Medium-High | High |
| **Performance** | Good | Predictable | Best | Good |
| **User experience** | Requires extra parameters | Requires pagination calls | Transparent | Flexible |
| **Scalability** | Limited | Limited | Unlimited | Flexible |
| **Maintenance** | Low | Medium | Low | Medium-High |
| **Best for** | Small filtered datasets | Known large datasets | All use cases | Complex requirements |
| **Requires data model changes** | No | No | Yes | Yes |
| **Platform optimization** | Standard | Standard | Full leverage | Mixed |

### Key takeaways

* **Return JQL queries** is the most powerful and recommended approach—it bypasses the limit entirely and leverages platform optimization
* **Write more specific queries** works well when results naturally fit under 1000 with minimal filtering
* **Implement pagination** is useful when you need explicit control or temporary workarounds
* **Hybrid approach** combines multiple strategies for maximum flexibility but adds complexity

---

## Recommendations

### Return JQL queries instead of value lists

This is the most scalable and user-friendly solution:

1. **Audit existing functions**: Identify which functions frequently return > 1000 values
2. **Design data model**: Ensure app metadata is stored in queryable Jira fields (custom fields, labels, links)
3. **Refactor functions**: Rewrite functions to return JQL queries instead of key lists
4. **Migrate data**: Backfill custom fields for existing issues if needed
5. **Update documentation**: Show customers the improved function behavior

For functions that genuinely need explicit enumeration:

1. Add optional `page` and `pageSize` parameters to function signatures
2. Document pagination usage in customer-facing docs
3. Provide helper functions or error messages to communicate total counts

### Add filtering parameters

For all high-volume functions:

1. Add optional filter parameters (status, date range, assignee, etc.)
2. Encourage customers to use filters in documentation
3. Make filters easy to discover (good parameter names, examples)

---
