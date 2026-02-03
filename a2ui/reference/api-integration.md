# A2UI API Integration Guide

This guide covers how to handle user interactions and integrate with backend services.

## Event Flow Overview

```
┌─────────────┐     surfaceUpdate      ┌─────────────┐
│   Agent     │ ────────────────────▶  │   Client    │
│  (Server)   │     dataModelUpdate    │  (Renderer) │
│             │     beginRendering     │             │
└─────────────┘                        └─────────────┘
       ▲                                      │
       │              userAction              │
       └──────────────────────────────────────┘
```

1. Agent sends UI definition via JSONL stream
2. Client renders the UI
3. User interacts with components
4. Client sends `userAction` to server
5. Server processes and sends updated UI

## Defining Actions on Components

### Button Action

```json
{
  "id": "submit_btn",
  "component": {
    "Button": {
      "child": "submit_text",
      "primary": true,
      "action": {
        "name": "submit_form",
        "context": [
          {"key": "email", "value": {"path": "/form/email"}},
          {"key": "password", "value": {"path": "/form/password"}},
          {"key": "remember", "value": {"path": "/form/rememberMe"}}
        ]
      }
    }
  }
}
```

### Action Object Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `name` | string | Yes | Unique action identifier |
| `context` | array | No | Data to collect and send |

### Context Value Resolution

Each context item has:
- `key`: The property name in the payload
- `value`: A BoundValue that resolves to the actual value

```json
// Definition
{"key": "userId", "value": {"path": "/user/id"}}
{"key": "action", "value": {"literalString": "delete"}}

// Resolved (if /user/id is "user-123")
{"userId": "user-123", "action": "delete"}
```

## userAction Message Format

When a user triggers an action, the client sends:

```json
{
  "userAction": {
    "name": "submit_form",
    "surfaceId": "login_surface",
    "sourceComponentId": "submit_btn",
    "timestamp": "2025-01-01T10:30:00Z",
    "context": {
      "email": "user@example.com",
      "password": "secretpassword",
      "remember": true
    }
  }
}
```

### userAction Properties

| Property | Type | Description |
|----------|------|-------------|
| `name` | string | Action name from component definition |
| `surfaceId` | string | Surface where action originated |
| `sourceComponentId` | string | Component that triggered the action |
| `timestamp` | string | ISO 8601 timestamp |
| `context` | object | Resolved key-value pairs from action.context |

## Error Reporting

Clients can report errors via the `error` message:

```json
{
  "error": {
    "type": "RENDER_ERROR",
    "message": "Component 'user_card' references missing child 'avatar'",
    "surfaceId": "main",
    "componentId": "user_card",
    "timestamp": "2025-01-01T10:30:05Z"
  }
}
```

### Error Types

| Type | Description |
|------|-------------|
| `RENDER_ERROR` | Component rendering failed |
| `VALIDATION_ERROR` | Invalid component structure or data |
| `REFERENCE_ERROR` | Missing component or data reference |
| `CATALOG_ERROR` | Unknown component type or catalog mismatch |
| `DATA_BINDING_ERROR` | Failed to resolve data path |

### Agent Error Handling

```python
async def handle_client_error(error: dict):
    error_type = error.get("type")
    component_id = error.get("componentId")

    if error_type == "RENDER_ERROR":
        # Send fallback UI
        yield {"surfaceUpdate": {"surfaceId": error["surfaceId"], "components": [
            {"id": "error_msg", "component": {"Text": {
                "text": {"literalString": "Something went wrong. Please try again."}
            }}}
        ]}}
        yield {"beginRendering": {"surfaceId": error["surfaceId"], "root": "error_msg"}}
```

## Transport Options

A2UI supports multiple transport mechanisms:

| Transport | Direction | Use Case |
|-----------|-----------|----------|
| **SSE (Server-Sent Events)** | Server → Client | Web streaming, simple setup |
| **WebSockets** | Bidirectional | Real-time apps, low latency |
| **A2A Protocol** | Bidirectional | Multi-agent systems |
| **AG UI** | Bidirectional | React integration |

### SSE Example

```javascript
const eventSource = new EventSource('/a2ui-stream');
eventSource.onmessage = (event) => {
  const message = JSON.parse(event.data);
  processA2UIMessage(message);
};
```

### WebSocket Example

```javascript
const ws = new WebSocket('wss://agent.example.com/a2ui');
ws.onmessage = (event) => {
  const message = JSON.parse(event.data);
  processA2UIMessage(message);
};

// Send user action
ws.send(JSON.stringify({
  userAction: {
    name: "submit_form",
    surfaceId: "main",
    sourceComponentId: "submit_btn",
    timestamp: new Date().toISOString(),
    context: { email: "user@example.com" }
  }
}));
```

## A2A Protocol Integration

A2UI is commonly used with the A2A (Agent-to-Agent) protocol for agent communication.

### Agent Card Extension

Advertise A2UI support in your agent card:

```json
{
  "name": "My Agent",
  "capabilities": {
    "extensions": [
      {
        "uri": "https://a2ui.org/a2a-extension/a2ui/v0.8",
        "params": {
          "supportedCatalogIds": [
            "https://github.com/google/A2UI/blob/main/specification/0.8/json/standard_catalog_definition.json"
          ],
          "acceptsInlineCatalogs": false
        }
      }
    ]
  }
}
```

### Client Capabilities in Messages

Include A2UI capabilities in every A2A message:

```json
{
  "metadata": {
    "a2uiClientCapabilities": {
      "supportedCatalogIds": [
        "https://github.com/google/A2UI/blob/main/specification/0.8/json/standard_catalog_definition.json"
      ]
    }
  },
  "message": {
    "prompt": {
      "text": "Find me restaurants nearby"
    }
  }
}
```

## Handling User Actions in Your Agent

### Python Example (using ADK)

```python
async def handle_user_action(action: dict) -> AsyncIterable[dict]:
    action_name = action.get("name")
    context = action.get("context", {})

    if action_name == "submit_booking":
        # Process the booking
        restaurant = context.get("restaurant")
        date = context.get("date")
        guests = context.get("guests")

        # Call your backend API
        result = await create_booking(restaurant, date, guests)

        # Generate confirmation UI
        yield {"surfaceUpdate": {"surfaceId": "booking", "components": [
            {"id": "root", "component": {"Column": {"children": {"explicitList": ["success_icon", "message"]}}}},
            {"id": "success_icon", "component": {"Icon": {"name": {"literalString": "check"}}}},
            {"id": "message", "component": {"Text": {"text": {"literalString": f"Booking confirmed for {date}!"}}}}
        ]}}
        yield {"beginRendering": {"surfaceId": "booking", "root": "root"}}
```

## Common Integration Patterns

### Form Submission

1. Define form with TextField/DateTimeInput components
2. Button action collects form values via `path`
3. Server validates and processes
4. Server responds with success/error UI

```json
// Form button
{
  "action": {
    "name": "create_account",
    "context": [
      {"key": "name", "value": {"path": "/form/name"}},
      {"key": "email", "value": {"path": "/form/email"}},
      {"key": "password", "value": {"path": "/form/password"}}
    ]
  }
}
```

### List Item Selection

Pass item identifiers in context:

```json
{
  "action": {
    "name": "select_item",
    "context": [
      {"key": "itemId", "value": {"path": "id"}},
      {"key": "itemName", "value": {"path": "name"}}
    ]
  }
}
```

### Confirmation Dialogs

Use Modal with confirmation actions:

```json
// Delete button opens modal
{"id": "delete_modal", "component": {"Modal": {
  "entryPointChild": "delete_btn",
  "contentChild": "confirm_dialog"
}}}

// Confirm button in modal
{"id": "confirm_delete", "component": {"Button": {
  "child": "confirm_text",
  "action": {
    "name": "confirm_delete",
    "context": [
      {"key": "itemId", "value": {"path": "/selectedItem/id"}}
    ]
  }
}}}
```

### Pagination

Track page state in data model:

```json
// Data model
{"key": "pagination", "valueMap": [
  {"key": "page", "valueNumber": 1},
  {"key": "totalPages", "valueNumber": 10}
]}

// Next button
{
  "action": {
    "name": "load_page",
    "context": [
      {"key": "page", "value": {"path": "/pagination/page"}},
      {"key": "direction", "value": {"literalString": "next"}}
    ]
  }
}
```

## Best Practices

1. **Use descriptive action names**: `submit_booking` is better than `action1`

2. **Include necessary context**: Collect all data needed to process the action

3. **Handle errors gracefully**: Return error UI when processing fails

4. **Provide feedback**: Show loading states and confirmations

5. **Validate server-side**: Never trust client data without validation

6. **Use consistent surface IDs**: Make it easy to update specific UI areas

7. **Keep actions idempotent**: Same action with same context should have same result
