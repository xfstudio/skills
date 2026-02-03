# A2UI Standard Catalog Components Reference

Complete reference for all 16 components in the A2UI 0.8 Standard Catalog.

## Component Weight (Flex Layout)

Components inside Row/Column can use `weight` for flex-based sizing:

```json
{"surfaceUpdate": {"surfaceId": "main", "components": [
  {"id": "layout", "component": {"Row": {"children": {"explicitList": ["sidebar", "content"]}}}},
  {"id": "sidebar", "weight": 1, "component": {"Column": {"children": {"explicitList": ["nav"]}}}},
  {"id": "content", "weight": 3, "component": {"Column": {"children": {"explicitList": ["main_area"]}}}}
]}}
```

In this example, `sidebar` takes 1/4 (25%) and `content` takes 3/4 (75%) of the available width.

| Property | Type | Description |
|----------|------|-------------|
| `weight` | number | Flex weight for proportional sizing within Row/Column |

## Layout Components

### Row

Horizontal container for arranging children in a row.

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `children` | Children | Yes | Child components (explicitList or template) |
| `distribution` | string | No | Main axis arrangement: `start`, `center`, `end`, `spaceBetween`, `spaceAround`, `spaceEvenly` |
| `alignment` | string | No | Cross axis alignment: `start`, `center`, `end`, `stretch` |

```json
{"id": "header_row", "component": {"Row": {
  "children": {"explicitList": ["logo", "nav", "user_menu"]},
  "distribution": "spaceBetween",
  "alignment": "center"
}}}
```

### Column

Vertical container for arranging children in a column.

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `children` | Children | Yes | Child components |
| `distribution` | string | No | Main axis arrangement |
| `alignment` | string | No | Cross axis alignment |

```json
{"id": "form_column", "component": {"Column": {
  "children": {"explicitList": ["title", "input1", "input2", "submit"]},
  "alignment": "stretch"
}}}
```

### List

Scrollable container for multiple items.

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `children` | Children | Yes | Child components |
| `direction` | string | No | `vertical` (default) or `horizontal` |
| `alignment` | string | No | Cross axis alignment |

```json
{"id": "item_list", "component": {"List": {
  "children": {"template": {"dataBinding": "/items", "componentId": "item_template"}},
  "direction": "vertical"
}}}
```

### Card

Material design card wrapper.

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `child` | string | Yes | ID of the child component |

```json
{"id": "user_card", "component": {"Card": {"child": "card_content"}}}
```

### Tabs

Tab navigation component.

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `tabItems` | array | Yes | Array of `{title: BoundValue, child: string}` |

```json
{"id": "settings_tabs", "component": {"Tabs": {
  "tabItems": [
    {"title": {"literalString": "Profile"}, "child": "profile_panel"},
    {"title": {"literalString": "Security"}, "child": "security_panel"}
  ]
}}}
```

### Modal

Dialog/popup component.

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `entryPointChild` | string | Yes | ID of trigger component (e.g., button) |
| `contentChild` | string | Yes | ID of modal content component |

```json
{"id": "confirm_modal", "component": {"Modal": {
  "entryPointChild": "delete_btn",
  "contentChild": "confirm_dialog"
}}}
```

### Divider

Visual separator line.

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `axis` | string | No | `horizontal` (default) or `vertical` |

```json
{"id": "section_divider", "component": {"Divider": {"axis": "horizontal"}}}
```

## Display Components

### Text

Text display component with simple Markdown support.

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `text` | BoundValue | Yes | Text content (supports simple Markdown) |
| `usageHint` | string | No | Style hint: `h1`, `h2`, `h3`, `h4`, `h5`, `caption`, `body` |

**Markdown Support:**
The Text component supports simple Markdown formatting:
- `**bold**` → **bold**
- `*italic*` → *italic*
- `[link text](url)` → clickable link
- `` `code` `` → inline code

```json
{"id": "page_title", "component": {"Text": {
  "text": {"literalString": "Welcome"},
  "usageHint": "h1"
}}}

// With Markdown
{"id": "description", "component": {"Text": {
  "text": {"literalString": "Visit our **website** for [more info](https://example.com)"}
}}}
```

### Image

Image display component.

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `url` | BoundValue | Yes | Image URL |
| `fit` | string | No | `contain`, `cover`, `fill`, `none`, `scale-down` |
| `usageHint` | string | No | `icon`, `avatar`, `smallFeature`, `mediumFeature`, `largeFeature`, `header` |

```json
{"id": "profile_avatar", "component": {"Image": {
  "url": {"path": "/user/avatarUrl"},
  "usageHint": "avatar",
  "fit": "cover"
}}}
```

### Icon

Icon from the standard icon set.

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `name` | BoundValue | Yes | Icon name from standard set |

**Available Icons:**
`accountCircle`, `add`, `arrowBack`, `arrowForward`, `attachFile`, `calendarToday`, `call`, `camera`, `check`, `close`, `delete`, `download`, `edit`, `event`, `error`, `favorite`, `favoriteOff`, `folder`, `help`, `home`, `info`, `locationOn`, `lock`, `lockOpen`, `mail`, `menu`, `moreVert`, `moreHoriz`, `notificationsOff`, `notifications`, `payment`, `person`, `phone`, `photo`, `print`, `refresh`, `search`, `send`, `settings`, `share`, `shoppingCart`, `star`, `starHalf`, `starOff`, `upload`, `visibility`, `visibilityOff`, `warning`

```json
{"id": "settings_icon", "component": {"Icon": {"name": {"literalString": "settings"}}}}
```

### Video

Video player component.

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `url` | BoundValue | Yes | Video URL |

```json
{"id": "intro_video", "component": {"Video": {"url": {"literalString": "https://example.com/intro.mp4"}}}}
```

### AudioPlayer

Audio player component.

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `url` | BoundValue | Yes | Audio URL |
| `description` | BoundValue | No | Audio description/title |

```json
{"id": "podcast_player", "component": {"AudioPlayer": {
  "url": {"path": "/episode/audioUrl"},
  "description": {"path": "/episode/title"}
}}}
```

## Input Components

### Button

Clickable button component.

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `child` | string | Yes | ID of child component (typically Text) |
| `action` | Action | Yes | Action to trigger on click |
| `primary` | boolean | No | Primary button styling |

```json
{"id": "submit_btn", "component": {"Button": {
  "child": "submit_text",
  "primary": true,
  "action": {
    "name": "submit_form",
    "context": [
      {"key": "email", "value": {"path": "/form/email"}}
    ]
  }
}}}
```

### TextField

Text input field.

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `label` | BoundValue | Yes | Field label |
| `text` | BoundValue | No | Current value |
| `textFieldType` | string | No | `shortText`, `longText`, `number`, `date`, `obscured` |
| `validationRegexp` | string | No | Validation regex pattern |

```json
{"id": "email_field", "component": {"TextField": {
  "label": {"literalString": "Email Address"},
  "text": {"path": "/form/email"},
  "textFieldType": "shortText",
  "validationRegexp": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"
}}}
```

### CheckBox

Toggle checkbox component.

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `label` | BoundValue | Yes | Checkbox label |
| `value` | BoundValue | Yes | Checked state (boolean) |

```json
{"id": "terms_checkbox", "component": {"CheckBox": {
  "label": {"literalString": "I agree to the terms"},
  "value": {"path": "/form/agreedToTerms", "literalBoolean": false}
}}}
```

### DateTimeInput

Date and/or time picker.

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `value` | BoundValue | Yes | Selected date/time (ISO 8601) |
| `enableDate` | boolean | No | Enable date selection |
| `enableTime` | boolean | No | Enable time selection |

```json
{"id": "appointment_picker", "component": {"DateTimeInput": {
  "value": {"path": "/booking/dateTime"},
  "enableDate": true,
  "enableTime": true
}}}
```

### MultipleChoice

Selection component for multiple options.

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `selections` | BoundValue | Yes | Currently selected values (array) |
| `options` | array | Yes | Available options `{label: BoundValue, value: string}` |
| `maxAllowedSelections` | integer | No | Maximum selections allowed |

```json
{"id": "cuisine_picker", "component": {"MultipleChoice": {
  "selections": {"path": "/filters/cuisines", "literalArray": []},
  "options": [
    {"label": {"literalString": "Italian"}, "value": "italian"},
    {"label": {"literalString": "Chinese"}, "value": "chinese"},
    {"label": {"literalString": "Mexican"}, "value": "mexican"}
  ],
  "maxAllowedSelections": 3
}}}
```

### Slider

Range slider component.

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `value` | BoundValue | Yes | Current value |
| `minValue` | number | No | Minimum value |
| `maxValue` | number | No | Maximum value |

```json
{"id": "price_slider", "component": {"Slider": {
  "value": {"path": "/filters/maxPrice", "literalNumber": 50},
  "minValue": 0,
  "maxValue": 200
}}}
```

## Children Object

The `children` property used by Row, Column, and List has two forms:

### explicitList
Fixed list of child component IDs:
```json
{"children": {"explicitList": ["child1", "child2", "child3"]}}
```

### template
Dynamic list from data model:
```json
{"children": {"template": {"dataBinding": "/items", "componentId": "item_template"}}}
```

## Action Object

The `action` property for Button:

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `name` | string | Yes | Action identifier |
| `context` | array | No | Data to include: `{key: string, value: BoundValue}` |

```json
{
  "action": {
    "name": "add_to_cart",
    "context": [
      {"key": "productId", "value": {"literalString": "prod-123"}},
      {"key": "quantity", "value": {"path": "/form/quantity"}}
    ]
  }
}
```
