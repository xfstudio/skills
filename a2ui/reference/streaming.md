# A2UI Streaming and Performance

This guide covers progressive rendering and performance optimization.

## Streaming Architecture

```
Agent (LLM) → JSONL Stream → Transport (SSE/WS) → Client Buffer → Renderer → UI
```

A2UI uses JSON Lines (JSONL) format where each line is a complete JSON message:

```jsonl
{"surfaceUpdate": {"surfaceId": "main", "components": [...]}}
{"dataModelUpdate": {"surfaceId": "main", "contents": [...]}}
{"beginRendering": {"surfaceId": "main", "root": "root"}}
```

## Why Streaming?

| Benefit | Description |
|---------|-------------|
| **Progressive rendering** | UI appears incrementally as data arrives |
| **LLM-friendly** | Easy for models to generate piece-by-piece |
| **Error resilience** | One malformed line doesn't break entire stream |
| **Low latency** | First content visible before full generation |

## Client-Side Flow

```
1. Receive JSONL line
2. Parse as JSON
3. Route by message type:
   - surfaceUpdate → store components in buffer
   - dataModelUpdate → update data model
   - beginRendering → trigger render from buffer
   - deleteSurface → remove surface
4. Continue receiving until stream ends
```

### Buffering Before Render

The client buffers components and data until `beginRendering`:

```jsonl
{"surfaceUpdate": {"surfaceId": "main", "components": [...]}}  # Buffered
{"surfaceUpdate": {"surfaceId": "main", "components": [...]}}  # Buffered
{"dataModelUpdate": {"surfaceId": "main", "contents": [...]}}  # Buffered
{"beginRendering": {"surfaceId": "main", "root": "root"}}      # NOW RENDER
```

This prevents "flash of incomplete content".

## Progressive Rendering Strategies

### Strategy 1: Skeleton First

Send layout structure, then content:

```jsonl
{"surfaceUpdate": {"surfaceId": "main", "components": [
  {"id": "root", "component": {"Column": {"children": {"explicitList": ["header", "list"]}}}},
  {"id": "header", "component": {"Text": {"text": {"literalString": "Loading..."}, "usageHint": "h1"}}},
  {"id": "list", "component": {"List": {"children": {"template": {"dataBinding": "/items", "componentId": "item"}}}}}
]}}
{"dataModelUpdate": {"surfaceId": "main", "contents": [{"key": "items", "valueMap": []}]}}
{"beginRendering": {"surfaceId": "main", "root": "root"}}

{"dataModelUpdate": {"surfaceId": "main", "contents": [{"key": "items", "valueMap": [
  {"key": "0", "valueMap": [{"key": "name", "valueString": "Item 1"}]},
  {"key": "1", "valueMap": [{"key": "name", "valueString": "Item 2"}]}
]}]}}
```

### Strategy 2: Incremental Components

Send components as they're generated:

```jsonl
{"surfaceUpdate": {"surfaceId": "main", "components": [{"id": "root", "component": {"Column": {"children": {"explicitList": ["title"]}}}}]}}
{"surfaceUpdate": {"surfaceId": "main", "components": [{"id": "title", "component": {"Text": {"text": {"literalString": "Results"}}}}]}}
{"beginRendering": {"surfaceId": "main", "root": "root"}}

{"surfaceUpdate": {"surfaceId": "main", "components": [{"id": "item1", "component": {"Card": {"child": "item1_content"}}}]}}
{"surfaceUpdate": {"surfaceId": "main", "components": [{"id": "item1_content", "component": {"Text": {"text": {"literalString": "First result"}}}}]}}
```

### Strategy 3: Data Streaming

Keep components static, stream data:

```jsonl
{"surfaceUpdate": {"surfaceId": "main", "components": [...]}}
{"beginRendering": {"surfaceId": "main", "root": "root"}}

{"dataModelUpdate": {"surfaceId": "main", "path": "/items/0", "contents": [{"key": "name", "valueString": "Item 1"}]}}
{"dataModelUpdate": {"surfaceId": "main", "path": "/items/1", "contents": [{"key": "name", "valueString": "Item 2"}]}}
{"dataModelUpdate": {"surfaceId": "main", "path": "/items/2", "contents": [{"key": "name", "valueString": "Item 3"}]}}
```

## Performance Optimization

### 1. Granular Data Updates

Update specific paths instead of full model:

```json
// Good - update only what changed
{"dataModelUpdate": {"surfaceId": "main", "path": "/user/name", "contents": [{"key": "name", "valueString": "Alice"}]}}

// Avoid - replacing entire model
{"dataModelUpdate": {"surfaceId": "main", "contents": [/* entire data model */]}}
```

### 2. Batch Component Updates

Send multiple components in one message:

```json
// Good - one message with all components
{"surfaceUpdate": {"surfaceId": "main", "components": [
  {"id": "comp1", "component": {...}},
  {"id": "comp2", "component": {...}},
  {"id": "comp3", "component": {...}}
]}}

// Avoid - multiple messages for related components
{"surfaceUpdate": {"surfaceId": "main", "components": [{"id": "comp1", ...}]}}
{"surfaceUpdate": {"surfaceId": "main", "components": [{"id": "comp2", ...}]}}
```

### 3. Client-Side Batching

Clients should batch renders (typically 16ms):

```
Messages at t=0ms, t=5ms, t=10ms → Single render at t=16ms
```

### 4. Diff-Based Updates

Clients should diff old/new component trees and update only changes.

### 5. Lazy Loading

For long lists, use pagination or infinite scroll:

```json
{"dataModelUpdate": {"surfaceId": "main", "contents": [
  {"key": "page", "valueNumber": 1},
  {"key": "hasMore", "valueBoolean": true},
  {"key": "items", "valueMap": [/* first 20 items */]}
]}}
```

## Transport Options

| Transport | Pros | Cons | Use Case |
|-----------|------|------|----------|
| **SSE** | Simple, HTTP-based | Unidirectional | Web streaming |
| **WebSockets** | Bidirectional, low latency | More complex | Real-time apps |
| **A2A Protocol** | Standard, secure | Requires A2A setup | Multi-agent |
| **AG UI** | React integration | AG UI specific | React apps |

### SSE Example

```javascript
const eventSource = new EventSource('/a2ui-stream');
eventSource.onmessage = (event) => {
  const message = JSON.parse(event.data);
  processA2UIMessage(message);
};
```

## Error Handling

### Malformed Messages

Skip and continue:

```javascript
try {
  const message = JSON.parse(line);
  processMessage(message);
} catch (e) {
  console.warn('Skipping malformed message:', line);
  // Continue with next line
}
```

### Network Interruptions

1. Display error state
2. Attempt reconnection
3. Agent resends or resumes

## Best Practices

1. **Send beginRendering promptly**: Don't wait for all data before first render

2. **Use meaningful surfaceIds**: Helps debugging stream issues

3. **Keep messages small**: Large messages slow parsing

4. **Test with slow connections**: Ensure UI looks good during streaming

5. **Handle partial state**: UI should be usable even with incomplete data

6. **Log stream events**: Helps debug generation issues

## Debugging

### View Raw Stream

```bash
curl -N https://your-agent/stream | jq -c '.'
```

### Validate Messages

```python
import jsonschema

for line in stream:
    message = json.loads(line)
    jsonschema.validate(message, a2ui_schema)
```
