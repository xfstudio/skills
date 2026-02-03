# A2UI Modal Examples

Examples of dialog and popup patterns using the Modal component.

## Basic Confirmation Modal

```jsonl
{"surfaceUpdate": {"surfaceId": "main", "components": [
  {"id": "root", "component": {"Column": {"children": {"explicitList": ["content", "delete_modal"]}, "alignment": "stretch"}}},
  {"id": "content", "component": {"Card": {"child": "item_row"}}},
  {"id": "item_row", "component": {"Row": {"children": {"explicitList": ["item_info", "delete_trigger"]}, "distribution": "spaceBetween", "alignment": "center"}}},
  {"id": "item_info", "component": {"Text": {"text": {"path": "/item/name"}, "usageHint": "h4"}}},
  {"id": "delete_trigger", "component": {"Button": {"child": "delete_icon", "action": {"name": "open_delete_modal", "context": []}}}},
  {"id": "delete_icon", "component": {"Icon": {"name": {"literalString": "delete"}}}},
  {"id": "delete_modal", "component": {"Modal": {"entryPointChild": "delete_trigger", "contentChild": "modal_content"}}},
  {"id": "modal_content", "component": {"Card": {"child": "modal_body"}}},
  {"id": "modal_body", "component": {"Column": {"children": {"explicitList": ["modal_icon", "modal_title", "modal_message", "modal_actions"]}, "alignment": "center"}}},
  {"id": "modal_icon", "component": {"Icon": {"name": {"literalString": "warning"}}}},
  {"id": "modal_title", "component": {"Text": {"text": {"literalString": "Delete Item?"}, "usageHint": "h3"}}},
  {"id": "modal_message", "component": {"Text": {"text": {"literalString": "This action cannot be undone. Are you sure you want to delete this item?"}}}},
  {"id": "modal_actions", "component": {"Row": {"children": {"explicitList": ["cancel_btn", "confirm_btn"]}, "distribution": "spaceEvenly"}}},
  {"id": "cancel_btn", "component": {"Button": {"child": "cancel_text", "action": {"name": "close_modal", "context": []}}}},
  {"id": "cancel_text", "component": {"Text": {"text": {"literalString": "Cancel"}}}},
  {"id": "confirm_btn", "component": {"Button": {"child": "confirm_text", "primary": true, "action": {"name": "confirm_delete", "context": [{"key": "itemId", "value": {"path": "/item/id"}}]}}}},
  {"id": "confirm_text", "component": {"Text": {"text": {"literalString": "Delete"}}}}
]}}
{"dataModelUpdate": {"surfaceId": "main", "contents": [{"key": "item", "valueMap": [{"key": "id", "valueString": "item-123"}, {"key": "name", "valueString": "Project Document"}]}]}}
{"beginRendering": {"surfaceId": "main", "root": "root"}}
```

## Form Modal (Edit Dialog)

```jsonl
{"surfaceUpdate": {"surfaceId": "profile", "components": [
  {"id": "root", "component": {"Column": {"children": {"explicitList": ["profile_card", "edit_modal"]}, "alignment": "stretch"}}},
  {"id": "profile_card", "component": {"Card": {"child": "profile_content"}}},
  {"id": "profile_content", "component": {"Row": {"children": {"explicitList": ["avatar", "info_column", "edit_trigger"]}, "alignment": "center"}}},
  {"id": "avatar", "component": {"Image": {"url": {"path": "/user/avatarUrl"}, "usageHint": "avatar"}}},
  {"id": "info_column", "weight": 1, "component": {"Column": {"children": {"explicitList": ["user_name", "user_email"]}, "alignment": "start"}}},
  {"id": "user_name", "component": {"Text": {"text": {"path": "/user/name"}, "usageHint": "h4"}}},
  {"id": "user_email", "component": {"Text": {"text": {"path": "/user/email"}, "usageHint": "caption"}}},
  {"id": "edit_trigger", "component": {"Button": {"child": "edit_icon", "action": {"name": "open_edit", "context": []}}}},
  {"id": "edit_icon", "component": {"Icon": {"name": {"literalString": "edit"}}}},
  {"id": "edit_modal", "component": {"Modal": {"entryPointChild": "edit_trigger", "contentChild": "edit_dialog"}}},
  {"id": "edit_dialog", "component": {"Card": {"child": "edit_form"}}},
  {"id": "edit_form", "component": {"Column": {"children": {"explicitList": ["edit_title", "divider", "name_field", "email_field", "edit_actions"]}, "alignment": "stretch"}}},
  {"id": "edit_title", "component": {"Text": {"text": {"literalString": "Edit Profile"}, "usageHint": "h3"}}},
  {"id": "divider", "component": {"Divider": {"axis": "horizontal"}}},
  {"id": "name_field", "component": {"TextField": {"label": {"literalString": "Display Name"}, "text": {"path": "/editForm/name"}}}},
  {"id": "email_field", "component": {"TextField": {"label": {"literalString": "Email"}, "text": {"path": "/editForm/email"}}}},
  {"id": "edit_actions", "component": {"Row": {"children": {"explicitList": ["discard_btn", "save_btn"]}, "distribution": "end"}}},
  {"id": "discard_btn", "component": {"Button": {"child": "discard_text", "action": {"name": "discard_edit", "context": []}}}},
  {"id": "discard_text", "component": {"Text": {"text": {"literalString": "Discard"}}}},
  {"id": "save_btn", "component": {"Button": {"child": "save_text", "primary": true, "action": {"name": "save_profile", "context": [{"key": "name", "value": {"path": "/editForm/name"}}, {"key": "email", "value": {"path": "/editForm/email"}}]}}}},
  {"id": "save_text", "component": {"Text": {"text": {"literalString": "Save Changes"}}}}
]}}
{"dataModelUpdate": {"surfaceId": "profile", "contents": [{"key": "user", "valueMap": [{"key": "name", "valueString": "John Doe"}, {"key": "email", "valueString": "john@example.com"}, {"key": "avatarUrl", "valueString": "https://example.com/avatar.jpg"}]}, {"key": "editForm", "valueMap": [{"key": "name", "valueString": "John Doe"}, {"key": "email", "valueString": "john@example.com"}]}]}}
{"beginRendering": {"surfaceId": "profile", "root": "root"}}
```

## Information Modal

```jsonl
{"surfaceUpdate": {"surfaceId": "help", "components": [
  {"id": "root", "component": {"Row": {"children": {"explicitList": ["main_content", "help_modal"]}, "alignment": "start"}}},
  {"id": "main_content", "weight": 1, "component": {"Text": {"text": {"literalString": "Main page content here..."}}}},
  {"id": "help_trigger", "component": {"Button": {"child": "help_icon", "action": {"name": "show_help", "context": []}}}},
  {"id": "help_icon", "component": {"Icon": {"name": {"literalString": "help"}}}},
  {"id": "help_modal", "component": {"Modal": {"entryPointChild": "help_trigger", "contentChild": "help_content"}}},
  {"id": "help_content", "component": {"Card": {"child": "help_body"}}},
  {"id": "help_body", "component": {"Column": {"children": {"explicitList": ["help_header", "help_divider", "help_text", "help_close"]}, "alignment": "stretch"}}},
  {"id": "help_header", "component": {"Row": {"children": {"explicitList": ["info_icon", "help_title"]}, "alignment": "center"}}},
  {"id": "info_icon", "component": {"Icon": {"name": {"literalString": "info"}}}},
  {"id": "help_title", "component": {"Text": {"text": {"literalString": "How to Use"}, "usageHint": "h3"}}},
  {"id": "help_divider", "component": {"Divider": {"axis": "horizontal"}}},
  {"id": "help_text", "component": {"Text": {"text": {"literalString": "This feature allows you to manage your items. Click on any item to view details, or use the action buttons to edit or delete.\n\nFor more help, visit our documentation."}}}},
  {"id": "help_close", "component": {"Button": {"child": "close_text", "primary": true, "action": {"name": "close_help", "context": []}}}},
  {"id": "close_text", "component": {"Text": {"text": {"literalString": "Got it"}}}}
]}}
{"dataModelUpdate": {"surfaceId": "help", "contents": []}}
{"beginRendering": {"surfaceId": "help", "root": "root"}}
```

## Selection Modal

```jsonl
{"surfaceUpdate": {"surfaceId": "picker", "components": [
  {"id": "root", "component": {"Column": {"children": {"explicitList": ["selected_display", "picker_modal"]}, "alignment": "stretch"}}},
  {"id": "selected_display", "component": {"Row": {"children": {"explicitList": ["selected_label", "selected_value", "change_trigger"]}, "alignment": "center"}}},
  {"id": "selected_label", "component": {"Text": {"text": {"literalString": "Country: "}}}},
  {"id": "selected_value", "component": {"Text": {"text": {"path": "/selection/country"}, "usageHint": "h4"}}},
  {"id": "change_trigger", "component": {"Button": {"child": "change_text", "action": {"name": "open_picker", "context": []}}}},
  {"id": "change_text", "component": {"Text": {"text": {"literalString": "Change"}}}},
  {"id": "picker_modal", "component": {"Modal": {"entryPointChild": "change_trigger", "contentChild": "picker_content"}}},
  {"id": "picker_content", "component": {"Card": {"child": "picker_body"}}},
  {"id": "picker_body", "component": {"Column": {"children": {"explicitList": ["picker_title", "picker_list"]}, "alignment": "stretch"}}},
  {"id": "picker_title", "component": {"Text": {"text": {"literalString": "Select Country"}, "usageHint": "h3"}}},
  {"id": "picker_list", "component": {"List": {"children": {"template": {"dataBinding": "/countries", "componentId": "country_option"}}, "direction": "vertical"}}},
  {"id": "country_option", "component": {"Button": {"child": "country_name", "action": {"name": "select_country", "context": [{"key": "code", "value": {"path": "code"}}, {"key": "name", "value": {"path": "name"}}]}}}},
  {"id": "country_name", "component": {"Text": {"text": {"path": "name"}}}}
]}}
{"dataModelUpdate": {"surfaceId": "picker", "contents": [{"key": "selection", "valueMap": [{"key": "country", "valueString": "United States"}]}, {"key": "countries", "valueMap": [{"key": "0", "valueMap": [{"key": "code", "valueString": "US"}, {"key": "name", "valueString": "United States"}]}, {"key": "1", "valueMap": [{"key": "code", "valueString": "UK"}, {"key": "name", "valueString": "United Kingdom"}]}, {"key": "2", "valueMap": [{"key": "code", "valueString": "CA"}, {"key": "name", "valueString": "Canada"}]}, {"key": "3", "valueMap": [{"key": "code", "valueString": "AU"}, {"key": "name", "valueString": "Australia"}]}]}]}}
{"beginRendering": {"surfaceId": "picker", "root": "root"}}
```

## Modal Best Practices

### 1. Entry Point Pattern

The `entryPointChild` component triggers the modal:

```json
{"id": "my_modal", "component": {"Modal": {
  "entryPointChild": "trigger_btn",   // Button that opens modal
  "contentChild": "modal_content"      // Content shown in modal
}}}
```

### 2. Clear Actions

Always provide clear action buttons:
- **Cancel/Close**: Dismisses without action
- **Confirm/Submit**: Performs the action

### 3. Focus Important Content

Modal content should be concise:
- Clear title
- Brief description
- Focused actions

### 4. Data Binding for Forms

Pre-populate edit forms from data model:

```json
{"dataModelUpdate": {"surfaceId": "edit", "contents": [
  {"key": "editForm", "valueMap": [
    {"key": "name", "valueString": "Current Name"},
    {"key": "email", "valueString": "current@email.com"}
  ]}
]}}
```

### 5. Context in Actions

Include necessary context for server processing:

```json
{
  "action": {
    "name": "confirm_delete",
    "context": [
      {"key": "itemId", "value": {"path": "/item/id"}},
      {"key": "itemType", "value": {"literalString": "document"}}
    ]
  }
}
```
