# A2UI Streaming Example

Demonstrates progressive rendering strategies for optimal user experience.

## Why Stream?

| Benefit | Description |
|---------|-------------|
| **Low latency** | First content visible immediately |
| **Progressive UX** | UI builds up naturally |
| **LLM-friendly** | Easy to generate piece by piece |
| **Error resilience** | Partial failures don't break everything |

## Strategy 1: Skeleton First

Show layout structure immediately, then fill in content:

```jsonl
{"surfaceUpdate": {"surfaceId": "search", "components": [
  {"id": "root", "component": {"Column": {"children": {"explicitList": ["header", "loading", "results"]}}}},
  {"id": "header", "component": {"Text": {"text": {"literalString": "Search Results"}, "usageHint": "h1"}}},
  {"id": "loading", "component": {"Text": {"text": {"literalString": "Loading..."}, "usageHint": "caption"}}},
  {"id": "results", "component": {"List": {"children": {"template": {"dataBinding": "/items", "componentId": "result_card"}}}}}
]}}
{"dataModelUpdate": {"surfaceId": "search", "contents": [{"key": "items", "valueMap": []}]}}
{"beginRendering": {"surfaceId": "search", "root": "root"}}
```

User sees "Loading..." immediately. Then stream results:

```jsonl
{"dataModelUpdate": {"surfaceId": "search", "contents": [{"key": "items", "valueMap": [
  {"key": "0", "valueMap": [{"key": "title", "valueString": "First Result"}, {"key": "description", "valueString": "Description here..."}]}
]}]}}
```

```jsonl
{"dataModelUpdate": {"surfaceId": "search", "contents": [{"key": "items", "valueMap": [
  {"key": "0", "valueMap": [{"key": "title", "valueString": "First Result"}, {"key": "description", "valueString": "Description here..."}]},
  {"key": "1", "valueMap": [{"key": "title", "valueString": "Second Result"}, {"key": "description", "valueString": "Another description..."}]}
]}]}}
```

Finally, remove loading indicator:

```jsonl
{"surfaceUpdate": {"surfaceId": "search", "components": [
  {"id": "loading", "component": {"Text": {"text": {"literalString": ""}}}}
]}}
```

## Strategy 2: Incremental Components

Stream components as they're generated:

```jsonl
{"surfaceUpdate": {"surfaceId": "chat", "components": [
  {"id": "root", "component": {"Column": {"children": {"explicitList": ["msg1"]}}}}
]}}
{"surfaceUpdate": {"surfaceId": "chat", "components": [
  {"id": "msg1", "component": {"Text": {"text": {"literalString": "Hello! I'm looking up that information..."}}}}
]}}
{"beginRendering": {"surfaceId": "chat", "root": "root"}}
```

User sees first message. Agent continues generating:

```jsonl
{"surfaceUpdate": {"surfaceId": "chat", "components": [
  {"id": "root", "component": {"Column": {"children": {"explicitList": ["msg1", "msg2"]}}}}
]}}
{"surfaceUpdate": {"surfaceId": "chat", "components": [
  {"id": "msg2", "component": {"Card": {"child": "result_content"}}}
]}}
{"surfaceUpdate": {"surfaceId": "chat", "components": [
  {"id": "result_content", "component": {"Column": {"children": {"explicitList": ["result_title", "result_body"]}}}}
]}}
{"surfaceUpdate": {"surfaceId": "chat", "components": [
  {"id": "result_title", "component": {"Text": {"text": {"literalString": "Here's what I found:"}, "usageHint": "h3"}}}
]}}
{"surfaceUpdate": {"surfaceId": "chat", "components": [
  {"id": "result_body", "component": {"Text": {"text": {"literalString": "The restaurant is open from 11am to 10pm daily."}}}}
]}}
```

## Strategy 3: Data-Only Streaming

Keep components static, stream only data updates:

```jsonl
{"surfaceUpdate": {"surfaceId": "dashboard", "components": [
  {"id": "root", "component": {"Column": {"children": {"explicitList": ["stats_row", "chart_area"]}}}},
  {"id": "stats_row", "component": {"Row": {"children": {"explicitList": ["stat1", "stat2", "stat3"]}, "distribution": "spaceEvenly"}}},
  {"id": "stat1", "component": {"Card": {"child": "stat1_content"}}},
  {"id": "stat1_content", "component": {"Column": {"children": {"explicitList": ["stat1_value", "stat1_label"]}}}},
  {"id": "stat1_value", "component": {"Text": {"text": {"path": "/stats/users"}, "usageHint": "h2"}}},
  {"id": "stat1_label", "component": {"Text": {"text": {"literalString": "Users"}, "usageHint": "caption"}}},
  {"id": "stat2", "component": {"Card": {"child": "stat2_content"}}},
  {"id": "stat2_content", "component": {"Column": {"children": {"explicitList": ["stat2_value", "stat2_label"]}}}},
  {"id": "stat2_value", "component": {"Text": {"text": {"path": "/stats/revenue"}, "usageHint": "h2"}}},
  {"id": "stat2_label", "component": {"Text": {"text": {"literalString": "Revenue"}, "usageHint": "caption"}}},
  {"id": "stat3", "component": {"Card": {"child": "stat3_content"}}},
  {"id": "stat3_content", "component": {"Column": {"children": {"explicitList": ["stat3_value", "stat3_label"]}}}},
  {"id": "stat3_value", "component": {"Text": {"text": {"path": "/stats/orders"}, "usageHint": "h2"}}},
  {"id": "stat3_label", "component": {"Text": {"text": {"literalString": "Orders"}, "usageHint": "caption"}}},
  {"id": "chart_area", "component": {"Text": {"text": {"path": "/chart/status"}}}}
]}}
{"dataModelUpdate": {"surfaceId": "dashboard", "contents": [
  {"key": "stats", "valueMap": [{"key": "users", "valueString": "..."}, {"key": "revenue", "valueString": "..."}, {"key": "orders", "valueString": "..."}]},
  {"key": "chart", "valueMap": [{"key": "status", "valueString": "Loading chart..."}]}
]}}
{"beginRendering": {"surfaceId": "dashboard", "root": "root"}}
```

Then stream data updates:

```jsonl
{"dataModelUpdate": {"surfaceId": "dashboard", "path": "/stats/users", "contents": [{"key": "users", "valueString": "1,234"}]}}
{"dataModelUpdate": {"surfaceId": "dashboard", "path": "/stats/revenue", "contents": [{"key": "revenue", "valueString": "$45,678"}]}}
{"dataModelUpdate": {"surfaceId": "dashboard", "path": "/stats/orders", "contents": [{"key": "orders", "valueString": "567"}]}}
{"dataModelUpdate": {"surfaceId": "dashboard", "path": "/chart/status", "contents": [{"key": "status", "valueString": "Chart loaded!"}]}}
```

## Client-Side Implementation

### JavaScript SSE Handler

```javascript
const eventSource = new EventSource('/a2ui-stream');
const componentBuffer = new Map();  // surfaceId -> components
const dataModel = new Map();        // surfaceId -> data

eventSource.onmessage = (event) => {
  const message = JSON.parse(event.data);

  if (message.surfaceUpdate) {
    const { surfaceId, components } = message.surfaceUpdate;
    // Merge into buffer
    const existing = componentBuffer.get(surfaceId) || [];
    components.forEach(c => {
      const idx = existing.findIndex(e => e.id === c.id);
      if (idx >= 0) existing[idx] = c;
      else existing.push(c);
    });
    componentBuffer.set(surfaceId, existing);
  }

  else if (message.dataModelUpdate) {
    const { surfaceId, contents, path } = message.dataModelUpdate;
    // Update data model
    updateDataModel(surfaceId, path || '/', contents);
  }

  else if (message.beginRendering) {
    const { surfaceId, root, styles } = message.beginRendering;
    // Render from buffer
    renderSurface(surfaceId, root, componentBuffer.get(surfaceId), styles);
  }

  else if (message.deleteSurface) {
    const { surfaceId } = message.deleteSurface;
    removeSurface(surfaceId);
    componentBuffer.delete(surfaceId);
    dataModel.delete(surfaceId);
  }
};
```

### Render Batching

Batch multiple updates into single render:

```javascript
let pendingRender = null;

function scheduleRender(surfaceId) {
  if (pendingRender) return;

  pendingRender = requestAnimationFrame(() => {
    renderSurface(surfaceId);
    pendingRender = null;
  });
}
```

## Performance Tips

| Tip | Description |
|-----|-------------|
| **Batch components** | Send related components in one `surfaceUpdate` |
| **Use path updates** | Update specific data paths, not entire model |
| **Render early** | Send `beginRendering` before all data arrives |
| **Buffer on client** | Don't re-render on every message |

## Error Handling

Handle partial stream failures gracefully:

```javascript
eventSource.onerror = (error) => {
  console.error('Stream error:', error);

  // Show error UI
  renderErrorState();

  // Attempt reconnection
  setTimeout(() => {
    reconnectStream();
  }, 3000);
};
```

## Agent-Side Streaming

```python
async def stream_search_results(query: str):
    # Send skeleton immediately
    yield {"surfaceUpdate": {"surfaceId": "results", "components": [
        {"id": "root", "component": {"Column": {"children": {"explicitList": ["header", "list"]}}}},
        {"id": "header", "component": {"Text": {"text": {"literalString": f"Results for: {query}"}, "usageHint": "h1"}}},
        {"id": "list", "component": {"List": {"children": {"template": {"dataBinding": "/items", "componentId": "item"}}}}}
    ]}}
    yield {"dataModelUpdate": {"surfaceId": "results", "contents": [{"key": "items", "valueMap": []}]}}
    yield {"beginRendering": {"surfaceId": "results", "root": "root"}}

    # Stream results as they come
    async for result in search_database(query):
        items = await get_current_items()
        items.append(result)
        yield {"dataModelUpdate": {"surfaceId": "results", "contents": [
            {"key": "items", "valueMap": format_items(items)}
        ]}}
```
