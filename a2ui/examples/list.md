# A2UI List Examples

Examples of rendering dynamic lists using templates and data binding.

## Simple Card List

Render a list of items as cards using `template`:

```jsonl
{"surfaceUpdate": {"surfaceId": "items", "components": [
  {"id": "root", "component": {"Column": {"children": {"explicitList": ["title", "item_list"]}, "alignment": "stretch"}}},
  {"id": "title", "component": {"Text": {"text": {"literalString": "My Items"}, "usageHint": "h1"}}},
  {"id": "item_list", "component": {"List": {"children": {"template": {"dataBinding": "/items", "componentId": "item_card"}}, "direction": "vertical"}}},
  {"id": "item_card", "component": {"Card": {"child": "item_content"}}},
  {"id": "item_content", "component": {"Row": {"children": {"explicitList": ["item_icon", "item_details"]}, "alignment": "center"}}},
  {"id": "item_icon", "component": {"Icon": {"name": {"literalString": "folder"}}}},
  {"id": "item_details", "weight": 1, "component": {"Column": {"children": {"explicitList": ["item_name", "item_desc"]}, "alignment": "start"}}},
  {"id": "item_name", "component": {"Text": {"text": {"path": "name"}, "usageHint": "h4"}}},
  {"id": "item_desc", "component": {"Text": {"text": {"path": "description"}, "usageHint": "caption"}}}
]}}
{"dataModelUpdate": {"surfaceId": "items", "contents": [{"key": "items", "valueMap": [{"key": "0", "valueMap": [{"key": "name", "valueString": "Project Alpha"}, {"key": "description", "valueString": "Main project folder"}]}, {"key": "1", "valueMap": [{"key": "name", "valueString": "Documents"}, {"key": "description", "valueString": "Important documents"}]}, {"key": "2", "valueMap": [{"key": "name", "valueString": "Images"}, {"key": "description", "valueString": "Photo gallery"}]}]}]}}
{"beginRendering": {"surfaceId": "items", "root": "root"}}
```

## Restaurant List with Actions

```jsonl
{"surfaceUpdate": {"surfaceId": "restaurants", "components": [
  {"id": "root", "component": {"Column": {"children": {"explicitList": ["header", "restaurant_list"]}, "alignment": "stretch"}}},
  {"id": "header", "component": {"Row": {"children": {"explicitList": ["title", "filter_btn"]}, "distribution": "spaceBetween", "alignment": "center"}}},
  {"id": "title", "component": {"Text": {"text": {"literalString": "Nearby Restaurants"}, "usageHint": "h2"}}},
  {"id": "filter_btn", "component": {"Button": {"child": "filter_icon", "action": {"name": "open_filters", "context": []}}}},
  {"id": "filter_icon", "component": {"Icon": {"name": {"literalString": "menu"}}}},
  {"id": "restaurant_list", "component": {"List": {"children": {"template": {"dataBinding": "/restaurants", "componentId": "restaurant_card"}}, "direction": "vertical"}}},
  {"id": "restaurant_card", "component": {"Card": {"child": "restaurant_content"}}},
  {"id": "restaurant_content", "component": {"Column": {"children": {"explicitList": ["restaurant_image", "restaurant_info", "restaurant_actions"]}, "alignment": "stretch"}}},
  {"id": "restaurant_image", "component": {"Image": {"url": {"path": "imageUrl"}, "usageHint": "mediumFeature", "fit": "cover"}}},
  {"id": "restaurant_info", "component": {"Column": {"children": {"explicitList": ["restaurant_name", "restaurant_rating", "restaurant_address"]}, "alignment": "start"}}},
  {"id": "restaurant_name", "component": {"Text": {"text": {"path": "name"}, "usageHint": "h3"}}},
  {"id": "restaurant_rating", "component": {"Row": {"children": {"explicitList": ["star_icon", "rating_text"]}, "alignment": "center"}}},
  {"id": "star_icon", "component": {"Icon": {"name": {"literalString": "star"}}}},
  {"id": "rating_text", "component": {"Text": {"text": {"path": "rating"}}}},
  {"id": "restaurant_address", "component": {"Row": {"children": {"explicitList": ["location_icon", "address_text"]}, "alignment": "center"}}},
  {"id": "location_icon", "component": {"Icon": {"name": {"literalString": "locationOn"}}}},
  {"id": "address_text", "component": {"Text": {"text": {"path": "address"}, "usageHint": "caption"}}},
  {"id": "restaurant_actions", "component": {"Row": {"children": {"explicitList": ["view_btn", "book_btn"]}, "distribution": "end"}}},
  {"id": "view_btn", "component": {"Button": {"child": "view_text", "action": {"name": "view_restaurant", "context": [{"key": "id", "value": {"path": "id"}}]}}}},
  {"id": "view_text", "component": {"Text": {"text": {"literalString": "View Menu"}}}},
  {"id": "book_btn", "component": {"Button": {"child": "book_text", "primary": true, "action": {"name": "book_restaurant", "context": [{"key": "id", "value": {"path": "id"}}, {"key": "name", "value": {"path": "name"}}]}}}},
  {"id": "book_text", "component": {"Text": {"text": {"literalString": "Book Now"}}}}
]}}
{"dataModelUpdate": {"surfaceId": "restaurants", "contents": [{"key": "restaurants", "valueMap": [{"key": "0", "valueMap": [{"key": "id", "valueString": "rest-001"}, {"key": "name", "valueString": "La Piazza"}, {"key": "rating", "valueString": "4.5"}, {"key": "address", "valueString": "123 Main St"}, {"key": "imageUrl", "valueString": "https://example.com/lapiazza.jpg"}]}, {"key": "1", "valueMap": [{"key": "id", "valueString": "rest-002"}, {"key": "name", "valueString": "Golden Dragon"}, {"key": "rating", "valueString": "4.2"}, {"key": "address", "valueString": "456 Oak Ave"}, {"key": "imageUrl", "valueString": "https://example.com/dragon.jpg"}]}]}]}}
{"beginRendering": {"surfaceId": "restaurants", "root": "root"}}
```

## Horizontal Scroll List

```jsonl
{"surfaceUpdate": {"surfaceId": "categories", "components": [
  {"id": "root", "component": {"Column": {"children": {"explicitList": ["section_title", "category_scroll"]}, "alignment": "stretch"}}},
  {"id": "section_title", "component": {"Text": {"text": {"literalString": "Categories"}, "usageHint": "h3"}}},
  {"id": "category_scroll", "component": {"List": {"children": {"template": {"dataBinding": "/categories", "componentId": "category_item"}}, "direction": "horizontal"}}},
  {"id": "category_item", "component": {"Card": {"child": "category_content"}}},
  {"id": "category_content", "component": {"Column": {"children": {"explicitList": ["category_icon", "category_name"]}, "alignment": "center"}}},
  {"id": "category_icon", "component": {"Image": {"url": {"path": "iconUrl"}, "usageHint": "icon"}}},
  {"id": "category_name", "component": {"Text": {"text": {"path": "name"}, "usageHint": "caption"}}}
]}}
{"dataModelUpdate": {"surfaceId": "categories", "contents": [{"key": "categories", "valueMap": [{"key": "0", "valueMap": [{"key": "name", "valueString": "Food"}, {"key": "iconUrl", "valueString": "https://example.com/food.png"}]}, {"key": "1", "valueMap": [{"key": "name", "valueString": "Drinks"}, {"key": "iconUrl", "valueString": "https://example.com/drinks.png"}]}, {"key": "2", "valueMap": [{"key": "name", "valueString": "Desserts"}, {"key": "iconUrl", "valueString": "https://example.com/desserts.png"}]}]}]}}
{"beginRendering": {"surfaceId": "categories", "root": "root"}}
```

## Two-Column Grid Layout

Using Row with weighted columns:

```jsonl
{"surfaceUpdate": {"surfaceId": "grid", "components": [
  {"id": "root", "component": {"Column": {"children": {"explicitList": ["title", "grid_container"]}, "alignment": "stretch"}}},
  {"id": "title", "component": {"Text": {"text": {"literalString": "Product Grid"}, "usageHint": "h2"}}},
  {"id": "grid_container", "component": {"List": {"children": {"template": {"dataBinding": "/productRows", "componentId": "product_row"}}, "direction": "vertical"}}},
  {"id": "product_row", "component": {"Row": {"children": {"template": {"dataBinding": "items", "componentId": "product_card"}}, "distribution": "spaceEvenly"}}},
  {"id": "product_card", "component": {"Card": {"child": "product_content"}}},
  {"id": "product_content", "component": {"Column": {"children": {"explicitList": ["product_image", "product_name", "product_price"]}, "alignment": "center"}}},
  {"id": "product_image", "component": {"Image": {"url": {"path": "imageUrl"}, "usageHint": "smallFeature"}}},
  {"id": "product_name", "component": {"Text": {"text": {"path": "name"}, "usageHint": "body"}}},
  {"id": "product_price", "component": {"Text": {"text": {"path": "price"}, "usageHint": "h4"}}}
]}}
{"dataModelUpdate": {"surfaceId": "grid", "contents": [{"key": "productRows", "valueMap": [{"key": "0", "valueMap": [{"key": "items", "valueMap": [{"key": "0", "valueMap": [{"key": "name", "valueString": "Widget A"}, {"key": "price", "valueString": "$29.99"}, {"key": "imageUrl", "valueString": "https://example.com/a.jpg"}]}, {"key": "1", "valueMap": [{"key": "name", "valueString": "Widget B"}, {"key": "price", "valueString": "$39.99"}, {"key": "imageUrl", "valueString": "https://example.com/b.jpg"}]}]}]}, {"key": "1", "valueMap": [{"key": "items", "valueMap": [{"key": "0", "valueMap": [{"key": "name", "valueString": "Widget C"}, {"key": "price", "valueString": "$19.99"}, {"key": "imageUrl", "valueString": "https://example.com/c.jpg"}]}, {"key": "1", "valueMap": [{"key": "name", "valueString": "Widget D"}, {"key": "price", "valueString": "$49.99"}, {"key": "imageUrl", "valueString": "https://example.com/d.jpg"}]}]}]}]}]}}
{"beginRendering": {"surfaceId": "grid", "root": "root"}}
```

## Empty State Handling

Handle empty lists with conditional content:

```jsonl
{"surfaceUpdate": {"surfaceId": "results", "components": [
  {"id": "root", "component": {"Column": {"children": {"explicitList": ["title", "empty_state"]}, "alignment": "center"}}},
  {"id": "title", "component": {"Text": {"text": {"literalString": "Search Results"}, "usageHint": "h2"}}},
  {"id": "empty_state", "component": {"Column": {"children": {"explicitList": ["empty_icon", "empty_message", "retry_btn"]}, "alignment": "center"}}},
  {"id": "empty_icon", "component": {"Icon": {"name": {"literalString": "search"}}}},
  {"id": "empty_message", "component": {"Text": {"text": {"literalString": "No results found. Try a different search."}, "usageHint": "body"}}},
  {"id": "retry_btn", "component": {"Button": {"child": "retry_text", "action": {"name": "clear_search", "context": []}}}},
  {"id": "retry_text", "component": {"Text": {"text": {"literalString": "Clear Search"}}}}
]}}
{"dataModelUpdate": {"surfaceId": "results", "contents": [{"key": "results", "valueMap": []}, {"key": "hasResults", "valueBoolean": false}]}}
{"beginRendering": {"surfaceId": "results", "root": "root"}}
```

## Key Concepts

### Template Binding
- `dataBinding`: Path to array in data model
- `componentId`: Template component to repeat

### Relative Paths in Templates
Inside template context, paths are relative to current item:
```json
{"path": "name"}  // resolves to current item's name
{"path": "/global/setting"}  // absolute path, from root
```

### Data Model Structure for Lists
Lists use numeric string keys:
```json
{"key": "items", "valueMap": [
  {"key": "0", "valueMap": [...]},
  {"key": "1", "valueMap": [...]},
  {"key": "2", "valueMap": [...]}
]}
```
