# A2UI JSON Schema Reference

Quick reference for A2UI 0.8 message schemas.

## Message Types

A2UI uses JSONL (JSON Lines) format. Each line is one of these message types:

| Message Type | Purpose |
|--------------|---------|
| `surfaceUpdate` | Define/update UI components |
| `dataModelUpdate` | Set/update data model values |
| `beginRendering` | Signal client to render |
| `deleteSurface` | Remove a surface |

## surfaceUpdate Schema

```json
{
  "surfaceUpdate": {
    "surfaceId": "string (required)",
    "components": [
      {
        "id": "string (required)",
        "weight": "number (optional, for flex layout)",
        "component": {
          "<ComponentType>": { /* component properties */ }
        }
      }
    ]
  }
}
```

### Component Wrapper

The `component` field must contain exactly ONE key (the component type):

```json
// Correct
{"component": {"Text": {"text": {"literalString": "Hello"}}}}

// Wrong - multiple types
{"component": {"Text": {...}, "Button": {...}}}
```

## dataModelUpdate Schema

```json
{
  "dataModelUpdate": {
    "surfaceId": "string (required)",
    "path": "string (optional, defaults to root)",
    "contents": [
      {
        "key": "string (required)",
        "valueString": "string",
        "valueNumber": "number",
        "valueBoolean": "boolean",
        "valueMap": [ /* nested contents */ ]
      }
    ]
  }
}
```

### Value Types (mutually exclusive)

Only ONE value type per entry:

```json
{"key": "name", "valueString": "John"}
{"key": "age", "valueNumber": 30}
{"key": "active", "valueBoolean": true}
{"key": "profile", "valueMap": [...]}
```

## beginRendering Schema

```json
{
  "beginRendering": {
    "surfaceId": "string (required)",
    "root": "string (required, component ID)",
    "catalogId": "string (optional)",
    "styles": {
      "font": "string (optional)",
      "primaryColor": "string (optional, hex format #RRGGBB)"
    }
  }
}
```

### Styles Object

| Property | Type | Description |
|----------|------|-------------|
| `font` | string | Primary font family (e.g., "Roboto", "Open Sans") |
| `primaryColor` | string | Theme color in hex format `#RRGGBB` (e.g., "#1976D2") |

```json
// Example with styles
{"beginRendering": {
  "surfaceId": "main",
  "root": "root",
  "styles": {
    "font": "Inter",
    "primaryColor": "#6200EE"
  }
}}
```

## deleteSurface Schema

```json
{
  "deleteSurface": {
    "surfaceId": "string (required)"
  }
}
```

## BoundValue Schema

Used for data-bindable properties:

```json
{
  "literalString": "string",
  "literalNumber": "number",
  "literalBoolean": "boolean",
  "literalArray": ["string"],
  "path": "string (JSON Pointer format)"
}
```

### Valid Combinations

```json
// Literal only
{"literalString": "Hello"}
{"literalNumber": 42}
{"literalBoolean": true}
{"literalArray": ["a", "b"]}

// Path only
{"path": "/user/name"}

// Both (initialization shorthand)
{"path": "/form/email", "literalString": "default@example.com"}
```

## Children Schema

Used by Row, Column, List:

```json
{
  "children": {
    "explicitList": ["componentId1", "componentId2"],
    // OR
    "template": {
      "dataBinding": "/items",
      "componentId": "item_template"
    }
  }
}
```

Only ONE of `explicitList` or `template` allowed.

## Action Schema

Used by Button component:

```json
{
  "action": {
    "name": "string (required)",
    "context": [
      {
        "key": "string (required)",
        "value": { /* BoundValue */ }
      }
    ]
  }
}
```

## Client-to-Server Messages

### userAction

```json
{
  "userAction": {
    "name": "string (required)",
    "surfaceId": "string (required)",
    "sourceComponentId": "string (required)",
    "timestamp": "string (required, ISO 8601)",
    "context": { /* resolved key-value pairs */ }
  }
}
```

### error

```json
{
  "error": {
    "type": "string (required)",
    "message": "string (required)",
    "surfaceId": "string (optional)",
    "componentId": "string (optional)",
    "timestamp": "string (required, ISO 8601)"
  }
}
```

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `type` | string | Yes | Error type: `RENDER_ERROR`, `VALIDATION_ERROR`, `REFERENCE_ERROR`, `CATALOG_ERROR`, `DATA_BINDING_ERROR` |
| `message` | string | Yes | Human-readable error description |
| `surfaceId` | string | No | Surface where error occurred |
| `componentId` | string | No | Component that caused the error |
| `timestamp` | string | Yes | ISO 8601 timestamp |

## Complete Message Example

```jsonl
{"surfaceUpdate":{"surfaceId":"main","components":[{"id":"root","component":{"Column":{"children":{"explicitList":["title","form"]}}}},{"id":"title","component":{"Text":{"text":{"literalString":"Login"},"usageHint":"h1"}}},{"id":"form","component":{"Column":{"children":{"explicitList":["email","password","submit"]}}}},{"id":"email","component":{"TextField":{"label":{"literalString":"Email"},"text":{"path":"/form/email"}}}},{"id":"password","component":{"TextField":{"label":{"literalString":"Password"},"text":{"path":"/form/password"},"textFieldType":"obscured"}}},{"id":"submit","component":{"Button":{"child":"submit_text","action":{"name":"login","context":[{"key":"email","value":{"path":"/form/email"}},{"key":"password","value":{"path":"/form/password"}}]}}}},{"id":"submit_text","component":{"Text":{"text":{"literalString":"Sign In"}}}}]}}
{"dataModelUpdate":{"surfaceId":"main","contents":[{"key":"form","valueMap":[{"key":"email","valueString":""},{"key":"password","valueString":""}]}]}}
{"beginRendering":{"surfaceId":"main","root":"root"}}
```

## Standard Catalog ID

```
https://github.com/google/A2UI/blob/main/specification/0.8/json/standard_catalog_definition.json
```

## Validation Tips

1. **surfaceId consistency**: Same surfaceId across related messages
2. **Component IDs unique**: No duplicate IDs within a surface
3. **Valid references**: All child/componentId references must exist
4. **One value type**: Only one valueString/valueNumber/valueBoolean/valueMap per entry
5. **Required properties**: Check required fields for each component type
6. **BoundValue format**: Use correct literal type or path format
