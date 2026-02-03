# A2UI Multi-Surface Example

Demonstrates managing multiple independent UI regions.

## Architecture

```
┌────────────────────────────────────────────────────┐
│                    Application                      │
│  ┌─────────────────┐  ┌──────────────────────────┐ │
│  │ Surface: sidebar│  │    Surface: main         │ │
│  │                 │  │  ┌────────────────────┐  │ │
│  │  Navigation     │  │  │ Surface: modal     │  │ │
│  │  Quick Actions  │  │  │ (when active)      │  │ │
│  │                 │  │  └────────────────────┘  │ │
│  └─────────────────┘  └──────────────────────────┘ │
└────────────────────────────────────────────────────┘
```

## Step 1: Initialize Sidebar

Create the navigation sidebar:

```jsonl
{"surfaceUpdate": {"surfaceId": "sidebar", "components": [
  {"id": "root", "component": {"Column": {"children": {"explicitList": ["logo", "divider", "nav_list", "spacer", "user_section"]}}}},
  {"id": "logo", "component": {"Text": {"text": {"literalString": "MyApp"}, "usageHint": "h2"}}},
  {"id": "divider", "component": {"Divider": {"axis": "horizontal"}}},
  {"id": "nav_list", "component": {"List": {"children": {"template": {"dataBinding": "/nav/items", "componentId": "nav_item"}}}}},
  {"id": "nav_item", "component": {"Button": {"child": "nav_item_content", "action": {"name": "navigate", "context": [{"key": "page", "value": {"path": "id"}}]}}}},
  {"id": "nav_item_content", "component": {"Row": {"children": {"explicitList": ["nav_icon", "nav_label"]}}}},
  {"id": "nav_icon", "component": {"Icon": {"name": {"path": "icon"}}}},
  {"id": "nav_label", "component": {"Text": {"text": {"path": "label"}}}},
  {"id": "spacer", "weight": 1, "component": {"Column": {"children": {"explicitList": []}}}},
  {"id": "user_section", "component": {"Row": {"children": {"explicitList": ["user_avatar", "user_name"]}}}},
  {"id": "user_avatar", "component": {"Icon": {"name": {"literalString": "accountCircle"}}}},
  {"id": "user_name", "component": {"Text": {"text": {"path": "/user/name"}}}}
]}}
{"dataModelUpdate": {"surfaceId": "sidebar", "contents": [
  {"key": "nav", "valueMap": [
    {"key": "items", "valueMap": [
      {"key": "0", "valueMap": [{"key": "id", "valueString": "dashboard"}, {"key": "icon", "valueString": "home"}, {"key": "label", "valueString": "Dashboard"}]},
      {"key": "1", "valueMap": [{"key": "id", "valueString": "orders"}, {"key": "icon", "valueString": "shoppingCart"}, {"key": "label", "valueString": "Orders"}]},
      {"key": "2", "valueMap": [{"key": "id", "valueString": "settings"}, {"key": "icon", "valueString": "settings"}, {"key": "label", "valueString": "Settings"}]}
    ]}
  ]},
  {"key": "user", "valueMap": [{"key": "name", "valueString": "John Doe"}]}
]}}
{"beginRendering": {"surfaceId": "sidebar", "root": "root"}}
```

## Step 2: Initialize Main Content

Create the main content area:

```jsonl
{"surfaceUpdate": {"surfaceId": "main", "components": [
  {"id": "root", "component": {"Column": {"children": {"explicitList": ["header", "content_area"]}}}},
  {"id": "header", "component": {"Row": {"children": {"explicitList": ["page_title", "header_actions"]}, "distribution": "spaceBetween", "alignment": "center"}}},
  {"id": "page_title", "component": {"Text": {"text": {"path": "/page/title"}, "usageHint": "h1"}}},
  {"id": "header_actions", "component": {"Row": {"children": {"explicitList": ["refresh_btn", "add_btn"]}}}},
  {"id": "refresh_btn", "component": {"Button": {"child": "refresh_icon", "action": {"name": "refresh"}}}},
  {"id": "refresh_icon", "component": {"Icon": {"name": {"literalString": "refresh"}}}},
  {"id": "add_btn", "component": {"Button": {"child": "add_content", "primary": true, "action": {"name": "open_add_modal"}}}},
  {"id": "add_content", "component": {"Row": {"children": {"explicitList": ["add_icon", "add_text"]}}}},
  {"id": "add_icon", "component": {"Icon": {"name": {"literalString": "add"}}}},
  {"id": "add_text", "component": {"Text": {"text": {"literalString": "New Item"}}}},
  {"id": "content_area", "component": {"Column": {"children": {"explicitList": ["stats_row", "items_list"]}}}},
  {"id": "stats_row", "component": {"Row": {"children": {"explicitList": ["stat1", "stat2", "stat3"]}, "distribution": "spaceEvenly"}}},
  {"id": "stat1", "component": {"Card": {"child": "stat1_content"}}},
  {"id": "stat1_content", "component": {"Column": {"children": {"explicitList": ["stat1_value", "stat1_label"]}, "alignment": "center"}}},
  {"id": "stat1_value", "component": {"Text": {"text": {"path": "/stats/orders"}, "usageHint": "h2"}}},
  {"id": "stat1_label", "component": {"Text": {"text": {"literalString": "Orders"}, "usageHint": "caption"}}},
  {"id": "stat2", "component": {"Card": {"child": "stat2_content"}}},
  {"id": "stat2_content", "component": {"Column": {"children": {"explicitList": ["stat2_value", "stat2_label"]}, "alignment": "center"}}},
  {"id": "stat2_value", "component": {"Text": {"text": {"path": "/stats/revenue"}, "usageHint": "h2"}}},
  {"id": "stat2_label", "component": {"Text": {"text": {"literalString": "Revenue"}, "usageHint": "caption"}}},
  {"id": "stat3", "component": {"Card": {"child": "stat3_content"}}},
  {"id": "stat3_content", "component": {"Column": {"children": {"explicitList": ["stat3_value", "stat3_label"]}, "alignment": "center"}}},
  {"id": "stat3_value", "component": {"Text": {"text": {"path": "/stats/customers"}, "usageHint": "h2"}}},
  {"id": "stat3_label", "component": {"Text": {"text": {"literalString": "Customers"}, "usageHint": "caption"}}},
  {"id": "items_list", "component": {"List": {"children": {"template": {"dataBinding": "/items", "componentId": "item_row"}}}}}
]}}
{"dataModelUpdate": {"surfaceId": "main", "contents": [
  {"key": "page", "valueMap": [{"key": "title", "valueString": "Dashboard"}]},
  {"key": "stats", "valueMap": [{"key": "orders", "valueString": "156"}, {"key": "revenue", "valueString": "$12,450"}, {"key": "customers", "valueString": "89"}]},
  {"key": "items", "valueMap": []}
]}}
{"beginRendering": {"surfaceId": "main", "root": "root", "styles": {"primaryColor": "#1976D2"}}}
```

## Step 3: Open Modal (New Surface)

Create a modal dialog as a separate surface:

```jsonl
{"surfaceUpdate": {"surfaceId": "modal-add", "components": [
  {"id": "root", "component": {"Card": {"child": "modal_content"}}},
  {"id": "modal_content", "component": {"Column": {"children": {"explicitList": ["modal_header", "modal_form", "modal_actions"]}}}},
  {"id": "modal_header", "component": {"Row": {"children": {"explicitList": ["modal_title", "close_btn"]}, "distribution": "spaceBetween", "alignment": "center"}}},
  {"id": "modal_title", "component": {"Text": {"text": {"literalString": "Add New Item"}, "usageHint": "h2"}}},
  {"id": "close_btn", "component": {"Button": {"child": "close_icon", "action": {"name": "close_modal"}}}},
  {"id": "close_icon", "component": {"Icon": {"name": {"literalString": "close"}}}},
  {"id": "modal_form", "component": {"Column": {"children": {"explicitList": ["name_field", "description_field", "price_field"]}}}},
  {"id": "name_field", "component": {"TextField": {"label": {"literalString": "Item Name"}, "text": {"path": "/form/name"}}}},
  {"id": "description_field", "component": {"TextField": {"label": {"literalString": "Description"}, "text": {"path": "/form/description"}, "textFieldType": "longText"}}},
  {"id": "price_field", "component": {"TextField": {"label": {"literalString": "Price"}, "text": {"path": "/form/price"}, "textFieldType": "number"}}},
  {"id": "modal_actions", "component": {"Row": {"children": {"explicitList": ["cancel_btn", "save_btn"]}, "distribution": "end"}}},
  {"id": "cancel_btn", "component": {"Button": {"child": "cancel_text", "action": {"name": "close_modal"}}}},
  {"id": "cancel_text", "component": {"Text": {"text": {"literalString": "Cancel"}}}},
  {"id": "save_btn", "component": {"Button": {"child": "save_text", "primary": true, "action": {"name": "save_item", "context": [{"key": "name", "value": {"path": "/form/name"}}, {"key": "description", "value": {"path": "/form/description"}}, {"key": "price", "value": {"path": "/form/price"}}]}}}},
  {"id": "save_text", "component": {"Text": {"text": {"literalString": "Save"}}}}
]}}
{"dataModelUpdate": {"surfaceId": "modal-add", "contents": [{"key": "form", "valueMap": [{"key": "name", "valueString": ""}, {"key": "description", "valueString": ""}, {"key": "price", "valueString": ""}]}]}}
{"beginRendering": {"surfaceId": "modal-add", "root": "root"}}
```

## Step 4: Close Modal and Update Main

After saving, close modal and refresh main content:

```jsonl
{"deleteSurface": {"surfaceId": "modal-add"}}
{"dataModelUpdate": {"surfaceId": "main", "path": "/items", "contents": [
  {"key": "0", "valueMap": [{"key": "name", "valueString": "New Product"}, {"key": "price", "valueString": "$99.00"}]}
]}}
```

## Data Model Isolation

Each surface has independent data:

| Surface | Data Model |
|---------|------------|
| `sidebar` | `/nav/items`, `/user/name` |
| `main` | `/page/title`, `/stats/*`, `/items` |
| `modal-add` | `/form/*` |

## Action Handling

```python
async def handle_action(action: dict):
    name = action["name"]
    surface_id = action["surfaceId"]

    if name == "navigate":
        page = action["context"]["page"]
        # Update main surface with new page content
        yield from render_page(page)

    elif name == "open_add_modal":
        # Create new modal surface
        yield from render_add_modal()

    elif name == "close_modal":
        # Remove modal surface
        yield {"deleteSurface": {"surfaceId": "modal-add"}}

    elif name == "save_item":
        # Save to backend
        item = await save_item(action["context"])
        # Close modal and update main
        yield {"deleteSurface": {"surfaceId": "modal-add"}}
        yield from update_items_list()
```

## Best Practices

1. **Meaningful surface IDs**: `sidebar`, `main`, `modal-add` are descriptive
2. **Independent data models**: Each surface manages its own state
3. **Clean lifecycle**: Create surfaces when needed, delete when done
4. **Consistent actions**: Same action patterns across surfaces
5. **Flex layout**: Use `weight` for dynamic sizing (`spacer` with weight: 1)
