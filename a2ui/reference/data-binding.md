# A2UI Data Binding Guide

This guide covers the BoundValue pattern and data model management in A2UI 0.8.

## The BoundValue Object

A `BoundValue` connects component properties to either static values or dynamic data from the data model.

### Pattern 1: Literal Value Only

Use when the value is static and won't change:

```json
// String literal
{"literalString": "Welcome to our app"}

// Number literal
{"literalNumber": 42}

// Boolean literal
{"literalBoolean": true}

// Array literal
{"literalArray": ["option1", "option2"]}
```

**Use cases:**
- Static labels and headings
- Fixed configuration values
- Default icon names

### Pattern 2: Path Only

Use when the value should always come from the data model:

```json
{"path": "/user/displayName"}
```

The `path` uses JSON Pointer format:
- Starts with `/`
- Segments separated by `/`
- Example: `/users/0/profile/name` for nested access

**Use cases:**
- Displaying user data
- Showing dynamic content from API responses
- Form field values that update

### Pattern 3: Path + Literal (Initialization Shorthand)

Use when you want to set a default value AND bind to the data model:

```json
{"path": "/form/email", "literalString": "user@example.com"}
```

This is equivalent to:
1. Setting `/form/email` to `"user@example.com"` in the data model
2. Binding the component to `/form/email`

**Use cases:**
- Form fields with default values
- Settings with initial state
- Preferences with defaults

## Data Model Structure

### dataModelUpdate Message

```json
{
  "dataModelUpdate": {
    "surfaceId": "main",
    "path": "/",
    "contents": [
      {"key": "user", "valueMap": [
        {"key": "name", "valueString": "John Doe"},
        {"key": "email", "valueString": "john@example.com"},
        {"key": "age", "valueNumber": 30},
        {"key": "verified", "valueBoolean": true}
      ]},
      {"key": "items", "valueMap": [
        {"key": "0", "valueMap": [
          {"key": "id", "valueString": "item-1"},
          {"key": "name", "valueString": "First Item"}
        ]},
        {"key": "1", "valueMap": [
          {"key": "id", "valueString": "item-2"},
          {"key": "name", "valueString": "Second Item"}
        ]}
      ]}
    ]
  }
}
```

### Value Types

| Property | JSON Type | Description |
|----------|-----------|-------------|
| `valueString` | string | Text values |
| `valueNumber` | number | Numeric values |
| `valueBoolean` | boolean | true/false |
| `valueMap` | array | Nested object (adjacency list format) |

### Adjacency List Format

Data is represented as an adjacency list (flat array of key-value pairs), not nested JSON:

```json
// This nested structure:
{
  "user": {
    "profile": {
      "name": "John"
    }
  }
}

// Becomes this adjacency list:
[
  {"key": "user", "valueMap": [
    {"key": "profile", "valueMap": [
      {"key": "name", "valueString": "John"}
    ]}
  ]}
]
```

## Dynamic List Rendering with Templates

Use `template` for rendering lists from data:

### Component Definition

```json
{"id": "item_list", "component": {"List": {
  "children": {
    "template": {
      "dataBinding": "/items",
      "componentId": "item_card"
    }
  }
}}}
```

### Template Component

```json
{"id": "item_card", "component": {"Card": {"child": "item_content"}}},
{"id": "item_content", "component": {"Column": {
  "children": {"explicitList": ["item_name", "item_desc"]}
}}},
{"id": "item_name", "component": {"Text": {
  "text": {"path": "name"},
  "usageHint": "h3"
}}},
{"id": "item_desc", "component": {"Text": {
  "text": {"path": "description"}
}}}
```

### Relative vs Absolute Paths

Inside a template context:
- **Relative path** (no leading `/`): Resolves relative to current item
  - `{"path": "name"}` → current item's `name` property
- **Absolute path** (leading `/`): Resolves from data model root
  - `{"path": "/settings/theme"}` → always from root

### Example Data Model for Lists

```json
{
  "dataModelUpdate": {
    "surfaceId": "main",
    "contents": [
      {"key": "items", "valueMap": [
        {"key": "0", "valueMap": [
          {"key": "name", "valueString": "First Item"},
          {"key": "description", "valueString": "Description of first item"}
        ]},
        {"key": "1", "valueMap": [
          {"key": "name", "valueString": "Second Item"},
          {"key": "description", "valueString": "Description of second item"}
        ]}
      ]}
    ]
  }
}
```

## Updating Data

### Partial Updates

Use `path` to update specific parts of the data model:

```json
{
  "dataModelUpdate": {
    "surfaceId": "main",
    "path": "/user/profile",
    "contents": [
      {"key": "name", "valueString": "Jane Doe"}
    ]
  }
}
```

This updates only `/user/profile/name` without affecting other data.

### Reactive Updates

When the data model changes via `dataModelUpdate`, all components bound to affected paths automatically re-render with new values.

## Best Practices

1. **Use meaningful paths**: `/user/profile/email` is better than `/a/b/c`

2. **Group related data**: Keep form fields under a common prefix like `/form/`

3. **Initialize with defaults**: Use the path+literal shorthand for forms:
   ```json
   {"path": "/form/quantity", "literalNumber": 1}
   ```

4. **Prefer paths for dynamic content**: Use `path` when data might change

5. **Use literals for static content**: Labels, icons, and fixed text should use `literalString`

6. **Keep data flat when possible**: Deeply nested structures are harder to reference

## Common Patterns

### Form with Validation State

```json
{"dataModelUpdate": {"surfaceId": "form", "contents": [
  {"key": "form", "valueMap": [
    {"key": "email", "valueString": ""},
    {"key": "emailValid", "valueBoolean": false},
    {"key": "password", "valueString": ""},
    {"key": "passwordValid", "valueBoolean": false}
  ]}
]}}
```

### Search Results

```json
{"dataModelUpdate": {"surfaceId": "search", "contents": [
  {"key": "query", "valueString": "restaurants"},
  {"key": "resultCount", "valueNumber": 5},
  {"key": "results", "valueMap": [
    {"key": "0", "valueMap": [
      {"key": "name", "valueString": "Restaurant A"},
      {"key": "rating", "valueNumber": 4.5}
    ]}
  ]}
]}}
```

### User Profile

```json
{"dataModelUpdate": {"surfaceId": "profile", "contents": [
  {"key": "user", "valueMap": [
    {"key": "id", "valueString": "user-123"},
    {"key": "name", "valueString": "John Doe"},
    {"key": "avatar", "valueString": "https://example.com/avatar.jpg"},
    {"key": "preferences", "valueMap": [
      {"key": "theme", "valueString": "dark"},
      {"key": "notifications", "valueBoolean": true}
    ]}
  ]}
]}}
```
