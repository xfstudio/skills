# A2UI Catalog Negotiation

This guide explains how agents and clients negotiate which component catalog to use.

## What is a Catalog?

A **Catalog** defines the contract between server and client:
- Available component types (Row, Text, Button, etc.)
- Component properties and validation rules
- Available styles

The **Standard Catalog** for A2UI 0.8:
```
https://github.com/google/A2UI/blob/main/specification/0.8/json/standard_catalog_definition.json
```

## Negotiation Flow

```
1. Agent advertises capabilities in Agent Card
2. Client declares supported catalogs in every message
3. Agent chooses catalog and specifies in beginRendering
```

## Step 1: Agent Card Extension

Advertise A2UI support in your agent's A2A Agent Card:

```json
{
  "name": "Restaurant Finder",
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

### Extension Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `supportedCatalogIds` | string[] | Pre-defined catalogs the agent supports |
| `acceptsInlineCatalogs` | boolean | If true, accepts client-provided catalog definitions |

## Step 2: Client Capabilities

In **every** A2A message, the client includes its supported catalogs:

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

### Client Capabilities Object

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `supportedCatalogIds` | string[] | Yes | Catalogs the client can render |
| `inlineCatalogs` | object[] | No | Full catalog definitions (for development) |

### Inline Catalogs (Development Only)

For local development, clients can provide custom catalogs inline:

```json
{
  "metadata": {
    "a2uiClientCapabilities": {
      "supportedCatalogIds": [...],
      "inlineCatalogs": [
        {
          "catalogId": "https://my-company.com/dev/custom-catalog",
          "components": {
            "SignaturePad": {
              "type": "object",
              "properties": {
                "penColor": {"type": "string"}
              }
            }
          },
          "styles": {}
        }
      ]
    }
  }
}
```

Only use if the agent advertises `acceptsInlineCatalogs: true`.

## Step 3: Catalog Selection

The agent specifies the chosen catalog in `beginRendering`:

```json
{
  "beginRendering": {
    "surfaceId": "main",
    "root": "root-component",
    "catalogId": "https://github.com/google/A2UI/blob/main/specification/0.8/json/standard_catalog_definition.json"
  }
}
```

### Default Behavior

If `catalogId` is omitted, the client **MUST** use the standard catalog for the protocol version.

### Per-Surface Catalogs

Different surfaces can use different catalogs:

```jsonl
{"beginRendering": {"surfaceId": "main", "root": "root", "catalogId": "standard-catalog"}}
{"beginRendering": {"surfaceId": "chart", "root": "chart-root", "catalogId": "chart-catalog"}}
```

## Best Practices

1. **Always include standard catalog**: Even if supporting custom catalogs

2. **Version your catalogs**: Use unique IDs for breaking changes
   ```
   https://my-company.com/catalogs/v1.0
   https://my-company.com/catalogs/v1.1  # new version
   ```

3. **Validate at runtime**: Check that generated components match catalog schema

4. **Graceful degradation**: Handle missing catalogs by falling back to standard

## Resolved Schema for LLM Generation

When building an agent, use a resolved schema that includes your target catalog:

```python
import copy

def resolve_schema(base_schema, catalog):
    resolved = copy.deepcopy(base_schema)
    resolved["properties"]["surfaceUpdate"]["properties"]["components"]["items"]["properties"]["component"]["properties"] = catalog["components"]
    resolved["properties"]["beginRendering"]["properties"]["styles"]["properties"] = catalog["styles"]
    return resolved
```

This gives the LLM a complete schema with all available components.

## Common Scenarios

### Standard Catalog Only

Most agents only need the standard catalog:

```json
// Agent Card
{"supportedCatalogIds": ["https://github.com/google/A2UI/blob/main/specification/0.8/json/standard_catalog_definition.json"]}

// beginRendering - catalogId optional
{"beginRendering": {"surfaceId": "main", "root": "root"}}
```

### Multi-Agent Systems

Orchestrating agents may delegate to sub-agents with different catalog support:

```
Orchestrator (standard only)
  ├── Restaurant Agent (standard)
  └── Chart Agent (standard + chart-catalog)
```

The client should be prepared to receive surfaces using any catalog advertised by sub-agents.
