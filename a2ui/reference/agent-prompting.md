# A2UI Agent Development and LLM Prompting

This guide covers building AI agents that generate A2UI interfaces.

## Overview

Building an A2UI agent:

```
1. Understand user intent → Decide what UI to show
2. Generate A2UI JSON → Use LLM structured output
3. Validate & stream → Check schema, send to client
4. Handle actions → Respond to user interactions
```

## Output Format

The recommended output format separates conversational text from A2UI JSON:

```
[Conversational response text]

---a2ui_JSON---

[A2UI JSON array]
```

### Example Output

```
Here are some restaurants near you. I found 3 great options!

---a2ui_JSON---

[
  {"surfaceUpdate": {"surfaceId": "results", "components": [...]}},
  {"dataModelUpdate": {"surfaceId": "results", "contents": [...]}},
  {"beginRendering": {"surfaceId": "results", "root": "root"}}
]
```

## Prompt Template

### Basic Structure

```python
AGENT_INSTRUCTION = """
You are a helpful assistant that generates rich UIs.

Your final output MUST be in two parts, separated by: `---a2ui_JSON---`

1. First part: Your conversational text response
2. Second part: A single JSON array of A2UI messages

The JSON part MUST validate against the A2UI JSON SCHEMA provided below.

--- UI TEMPLATE RULES ---
- For list displays, use Column with List component
- For forms, use TextField, DateTimeInput, etc.
- For confirmations, use Card with Icon and Text

{UI_EXAMPLES}

---BEGIN A2UI JSON SCHEMA---
{A2UI_SCHEMA}
---END A2UI JSON SCHEMA---
"""
```

### With Examples (Few-Shot)

```python
UI_EXAMPLES = """
### List Example
For displaying a list of items:
```json
[
  {"surfaceUpdate": {"surfaceId": "list", "components": [
    {"id": "root", "component": {"Column": {"children": {"explicitList": ["title", "items"]}}}},
    {"id": "title", "component": {"Text": {"text": {"literalString": "Results"}, "usageHint": "h2"}}},
    {"id": "items", "component": {"List": {"children": {"template": {"dataBinding": "/items", "componentId": "item_card"}}}}}
  ]}},
  {"dataModelUpdate": {"surfaceId": "list", "contents": [{"key": "items", "valueMap": [...]}]}},
  {"beginRendering": {"surfaceId": "list", "root": "root"}}
]
```

### Form Example
For collecting user input:
```json
[
  {"surfaceUpdate": {"surfaceId": "form", "components": [
    {"id": "root", "component": {"Card": {"child": "form_content"}}},
    {"id": "form_content", "component": {"Column": {"children": {"explicitList": ["name_field", "submit_btn"]}}}},
    {"id": "name_field", "component": {"TextField": {"label": {"literalString": "Name"}, "text": {"path": "/form/name"}}}},
    {"id": "submit_btn", "component": {"Button": {"child": "submit_text", "action": {"name": "submit", "context": [{"key": "name", "value": {"path": "/form/name"}}]}}}}
  ]}},
  {"beginRendering": {"surfaceId": "form", "root": "root"}}
]
```
"""
```

## Using Google ADK

### Basic Agent Setup

```python
from google.adk.agents.llm_agent import Agent
from google.adk.tools.tool_context import ToolContext
import json

def get_data(tool_context: ToolContext) -> str:
    """Fetch data for the UI."""
    return json.dumps([
        {"id": "1", "name": "Item 1"},
        {"id": "2", "name": "Item 2"}
    ])

root_agent = Agent(
    model='gemini-2.5-flash',
    name="ui_agent",
    description="An agent that generates A2UI interfaces",
    instruction=AGENT_INSTRUCTION,
    tools=[get_data],
)
```

### Running the Agent

```bash
pip install google-adk
adk web  # Opens web interface
```

## JSON Schema Validation

Always validate LLM output before sending to client:

```python
import json
import jsonschema

def validate_a2ui(output: str, schema: dict) -> list:
    """Extract and validate A2UI JSON from agent output."""

    # Split by delimiter
    parts = output.split('---a2ui_JSON---')
    if len(parts) != 2:
        raise ValueError("Missing ---a2ui_JSON--- delimiter")

    json_part = parts[1].strip()

    # Parse JSON
    messages = json.loads(json_part)

    # Validate each message
    for msg in messages:
        jsonschema.validate(instance=msg, schema=schema)

    return messages
```

## A2UI Schema (Simplified)

```python
A2UI_SCHEMA = {
    "type": "object",
    "properties": {
        "surfaceUpdate": {
            "type": "object",
            "properties": {
                "surfaceId": {"type": "string"},
                "components": {"type": "array"}
            },
            "required": ["surfaceId", "components"]
        },
        "dataModelUpdate": {
            "type": "object",
            "properties": {
                "surfaceId": {"type": "string"},
                "contents": {"type": "array"}
            },
            "required": ["surfaceId", "contents"]
        },
        "beginRendering": {
            "type": "object",
            "properties": {
                "surfaceId": {"type": "string"},
                "root": {"type": "string"}
            },
            "required": ["surfaceId", "root"]
        },
        "deleteSurface": {
            "type": "object",
            "properties": {
                "surfaceId": {"type": "string"}
            },
            "required": ["surfaceId"]
        }
    }
}
```

For full schema, see the [standard catalog definition](https://github.com/google/A2UI/blob/main/specification/0.8/json/standard_catalog_definition.json).

## Handling User Actions

When user clicks a button, client sends `userAction`:

```python
async def handle_user_action(action: dict):
    action_name = action.get("name")
    context = action.get("context", {})

    if action_name == "submit_booking":
        # Process booking
        result = await create_booking(context)

        # Generate confirmation UI
        return generate_confirmation_ui(result)

    elif action_name == "cancel":
        # Return to previous state
        return generate_main_ui()
```

## Best Practices

### 1. Schema Injection

Always inject the full schema into the prompt. This helps the LLM understand valid structures.

### 2. Provide Examples

Few-shot examples dramatically improve output quality. Include examples for each UI pattern.

### 3. Template Rules

Give clear rules for which UI pattern to use:

```
- If showing a list → use List template
- If collecting input → use Form template
- If confirming action → use Confirmation template
```

### 4. Validate Everything

```python
try:
    messages = validate_a2ui(output, schema)
    stream_messages(messages)
except (json.JSONDecodeError, jsonschema.ValidationError) as e:
    # Log error, retry, or return fallback UI
    logger.error(f"Invalid A2UI: {e}")
```

### 5. Handle Partial Output

LLMs may produce incomplete output. Handle gracefully:

```python
def safe_parse(output: str) -> list:
    try:
        return validate_a2ui(output, schema)
    except Exception:
        # Return error UI
        return [
            {"surfaceUpdate": {"surfaceId": "error", "components": [
                {"id": "root", "component": {"Text": {"text": {"literalString": "Something went wrong"}}}}
            ]}},
            {"beginRendering": {"surfaceId": "error", "root": "root"}}
        ]
```

### 6. Test with Real Models

Different models may format output differently. Test with your target model.

## Common Issues

| Issue | Solution |
|-------|----------|
| JSON in markdown fences | Strip ` ```json ` and ` ``` ` |
| Missing delimiter | Retry with clearer prompt |
| Invalid component types | Ensure schema includes all components |
| Nested JSON errors | Validate incrementally |

## Debugging

### Log Raw Output

```python
logger.debug(f"Raw LLM output:\n{output}")
```

### Validate Components Individually

```python
for component in components:
    try:
        validate_component(component)
    except Exception as e:
        logger.error(f"Invalid component {component['id']}: {e}")
```
