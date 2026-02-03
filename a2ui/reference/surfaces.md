# A2UI Surface Management

This guide covers managing multiple UI surfaces in A2UI.

## What is a Surface?

A **Surface** is a contiguous UI region that can be rendered independently. Each surface has:
- Unique `surfaceId`
- Own component tree (starting from a root)
- Own data model
- Independent lifecycle

## Architecture

```
┌─────────────────────────────────────────────────┐
│                 Application                      │
│  ┌──────────────────┐  ┌─────────────────────┐  │
│  │   Surface: main  │  │  Surface: sidebar   │  │
│  │  ┌────────────┐  │  │  ┌───────────────┐  │  │
│  │  │   Column   │  │  │  │    Column     │  │  │
│  │  │  ├─ Text   │  │  │  │  ├─ Text      │  │  │
│  │  │  ├─ List   │  │  │  │  └─ List      │  │  │
│  │  │  └─ Button │  │  │  │               │  │  │
│  │  └────────────┘  │  │  └───────────────┘  │  │
│  │  Data Model: {}  │  │  Data Model: {}     │  │
│  └──────────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────┘
```

## Surface Lifecycle

### 1. Create Surface

Send `surfaceUpdate` with a new `surfaceId`:

```json
{"surfaceUpdate": {
  "surfaceId": "new-surface",
  "components": [
    {"id": "root", "component": {"Text": {"text": {"literalString": "Hello"}}}}
  ]
}}
```

### 2. Populate Data

Send `dataModelUpdate` for the surface:

```json
{"dataModelUpdate": {
  "surfaceId": "new-surface",
  "contents": [{"key": "title", "valueString": "My Surface"}]
}}
```

### 3. Render Surface

Send `beginRendering` to trigger display:

```json
{"beginRendering": {
  "surfaceId": "new-surface",
  "root": "root"
}}
```

### 4. Update Surface

Send additional `surfaceUpdate` or `dataModelUpdate`:

```json
{"dataModelUpdate": {
  "surfaceId": "new-surface",
  "path": "/title",
  "contents": [{"key": "title", "valueString": "Updated Title"}]
}}
```

### 5. Delete Surface

Remove surface with `deleteSurface`:

```json
{"deleteSurface": {"surfaceId": "new-surface"}}
```

## Multiple Surfaces Example

### Chat Application

Each AI response renders in its own surface:

```jsonl
{"surfaceUpdate": {"surfaceId": "response-1", "components": [...]}}
{"dataModelUpdate": {"surfaceId": "response-1", "contents": [...]}}
{"beginRendering": {"surfaceId": "response-1", "root": "root"}}

{"surfaceUpdate": {"surfaceId": "response-2", "components": [...]}}
{"dataModelUpdate": {"surfaceId": "response-2", "contents": [...]}}
{"beginRendering": {"surfaceId": "response-2", "root": "root"}}
```

### Dashboard with Sidebar

Main content and sidebar as separate surfaces:

```jsonl
{"surfaceUpdate": {"surfaceId": "main", "components": [
  {"id": "root", "component": {"Column": {"children": {"explicitList": ["header", "content"]}}}},
  {"id": "header", "component": {"Text": {"text": {"literalString": "Dashboard"}, "usageHint": "h1"}}},
  {"id": "content", "component": {"Text": {"text": {"path": "/data/summary"}}}}
]}}

{"surfaceUpdate": {"surfaceId": "sidebar", "components": [
  {"id": "root", "component": {"Column": {"children": {"explicitList": ["nav_title", "nav_list"]}}}},
  {"id": "nav_title", "component": {"Text": {"text": {"literalString": "Navigation"}, "usageHint": "h3"}}},
  {"id": "nav_list", "component": {"List": {"children": {"template": {"dataBinding": "/items", "componentId": "nav_item"}}}}}
]}}

{"dataModelUpdate": {"surfaceId": "main", "contents": [{"key": "data", "valueMap": [{"key": "summary", "valueString": "Overview..."}]}]}}
{"dataModelUpdate": {"surfaceId": "sidebar", "contents": [{"key": "items", "valueMap": [...]}]}}

{"beginRendering": {"surfaceId": "main", "root": "root"}}
{"beginRendering": {"surfaceId": "sidebar", "root": "root"}}
```

## surfaceId Naming Conventions

| Pattern | Use Case | Example |
|---------|----------|---------|
| `main` | Primary content area | `main` |
| `sidebar` | Auxiliary panel | `sidebar`, `sidebar-left` |
| `modal-{id}` | Modal dialogs | `modal-confirm`, `modal-edit` |
| `response-{n}` | Chat responses | `response-1`, `response-2` |
| `{feature}-{id}` | Feature-specific | `booking-form`, `search-results` |

## Data Model Isolation

Each surface has its own data model. The same path can exist in different surfaces:

```jsonl
{"dataModelUpdate": {"surfaceId": "main", "contents": [{"key": "user", "valueMap": [{"key": "name", "valueString": "Alice"}]}]}}
{"dataModelUpdate": {"surfaceId": "profile", "contents": [{"key": "user", "valueMap": [{"key": "name", "valueString": "Bob"}]}]}}
```

`/user/name` in `main` = "Alice"
`/user/name` in `profile` = "Bob"

## Updating vs Replacing

### Incremental Update

Add or update specific components:

```json
{"surfaceUpdate": {
  "surfaceId": "main",
  "components": [
    {"id": "new-item", "component": {"Text": {"text": {"literalString": "New item"}}}}
  ]
}}
```

### Full Replacement

To replace all components, send complete component list and re-render:

```jsonl
{"surfaceUpdate": {"surfaceId": "main", "components": [/* all new components */]}}
{"beginRendering": {"surfaceId": "main", "root": "new-root"}}
```

## Cleanup Pattern

When finishing a flow, clean up surfaces:

```jsonl
{"deleteSurface": {"surfaceId": "booking-form"}}
{"surfaceUpdate": {"surfaceId": "confirmation", "components": [...]}}
{"beginRendering": {"surfaceId": "confirmation", "root": "root"}}
```

## Best Practices

1. **Use descriptive IDs**: `booking-form` not `surface1`

2. **Clean up unused surfaces**: Delete surfaces when flows complete

3. **Keep data models focused**: Each surface's data model should only contain what it needs

4. **Consider render order**: User sees surfaces in order of `beginRendering`

5. **Handle missing surfaces**: Client should gracefully handle updates to non-existent surfaces
