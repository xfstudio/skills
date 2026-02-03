# A2UI Form Examples

Complete examples of form patterns using A2UI components.

## Simple Login Form

```jsonl
{"surfaceUpdate": {"surfaceId": "login", "components": [
  {"id": "root", "component": {"Card": {"child": "form_content"}}},
  {"id": "form_content", "component": {"Column": {"children": {"explicitList": ["title", "email_field", "password_field", "remember_row", "submit_btn"]}, "alignment": "stretch"}}},
  {"id": "title", "component": {"Text": {"text": {"literalString": "Sign In"}, "usageHint": "h2"}}},
  {"id": "email_field", "component": {"TextField": {"label": {"literalString": "Email"}, "text": {"path": "/form/email"}, "textFieldType": "shortText"}}},
  {"id": "password_field", "component": {"TextField": {"label": {"literalString": "Password"}, "text": {"path": "/form/password"}, "textFieldType": "obscured"}}},
  {"id": "remember_row", "component": {"Row": {"children": {"explicitList": ["remember_check"]}, "distribution": "start"}}},
  {"id": "remember_check", "component": {"CheckBox": {"label": {"literalString": "Remember me"}, "value": {"path": "/form/remember", "literalBoolean": false}}}},
  {"id": "submit_btn", "component": {"Button": {"child": "submit_text", "primary": true, "action": {"name": "login", "context": [{"key": "email", "value": {"path": "/form/email"}}, {"key": "password", "value": {"path": "/form/password"}}, {"key": "remember", "value": {"path": "/form/remember"}}]}}}},
  {"id": "submit_text", "component": {"Text": {"text": {"literalString": "Sign In"}}}}
]}}
{"dataModelUpdate": {"surfaceId": "login", "contents": [{"key": "form", "valueMap": [{"key": "email", "valueString": ""}, {"key": "password", "valueString": ""}, {"key": "remember", "valueBoolean": false}]}]}}
{"beginRendering": {"surfaceId": "login", "root": "root"}}
```

## Registration Form

```jsonl
{"surfaceUpdate": {"surfaceId": "register", "components": [
  {"id": "root", "component": {"Column": {"children": {"explicitList": ["header", "form_card"]}, "alignment": "stretch"}}},
  {"id": "header", "component": {"Text": {"text": {"literalString": "Create Account"}, "usageHint": "h1"}}},
  {"id": "form_card", "component": {"Card": {"child": "form_fields"}}},
  {"id": "form_fields", "component": {"Column": {"children": {"explicitList": ["name_row", "email_field", "password_field", "confirm_field", "terms_check", "submit_btn"]}, "alignment": "stretch"}}},
  {"id": "name_row", "component": {"Row": {"children": {"explicitList": ["first_name", "last_name"]}, "distribution": "spaceBetween"}}},
  {"id": "first_name", "weight": 1, "component": {"TextField": {"label": {"literalString": "First Name"}, "text": {"path": "/form/firstName"}}}},
  {"id": "last_name", "weight": 1, "component": {"TextField": {"label": {"literalString": "Last Name"}, "text": {"path": "/form/lastName"}}}},
  {"id": "email_field", "component": {"TextField": {"label": {"literalString": "Email Address"}, "text": {"path": "/form/email"}, "validationRegexp": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"}}},
  {"id": "password_field", "component": {"TextField": {"label": {"literalString": "Password"}, "text": {"path": "/form/password"}, "textFieldType": "obscured"}}},
  {"id": "confirm_field", "component": {"TextField": {"label": {"literalString": "Confirm Password"}, "text": {"path": "/form/confirmPassword"}, "textFieldType": "obscured"}}},
  {"id": "terms_check", "component": {"CheckBox": {"label": {"literalString": "I agree to the Terms of Service"}, "value": {"path": "/form/agreedToTerms", "literalBoolean": false}}}},
  {"id": "submit_btn", "component": {"Button": {"child": "submit_text", "primary": true, "action": {"name": "register", "context": [{"key": "firstName", "value": {"path": "/form/firstName"}}, {"key": "lastName", "value": {"path": "/form/lastName"}}, {"key": "email", "value": {"path": "/form/email"}}, {"key": "password", "value": {"path": "/form/password"}}]}}}}
  {"id": "submit_text", "component": {"Text": {"text": {"literalString": "Create Account"}}}}
]}}
{"dataModelUpdate": {"surfaceId": "register", "contents": [{"key": "form", "valueMap": [{"key": "firstName", "valueString": ""}, {"key": "lastName", "valueString": ""}, {"key": "email", "valueString": ""}, {"key": "password", "valueString": ""}, {"key": "confirmPassword", "valueString": ""}, {"key": "agreedToTerms", "valueBoolean": false}]}]}}
{"beginRendering": {"surfaceId": "register", "root": "root"}}
```

## Booking Form with Date/Time

```jsonl
{"surfaceUpdate": {"surfaceId": "booking", "components": [
  {"id": "root", "component": {"Card": {"child": "booking_form"}}},
  {"id": "booking_form", "component": {"Column": {"children": {"explicitList": ["title", "divider1", "guest_section", "datetime_section", "preferences_section", "divider2", "submit_row"]}, "alignment": "stretch"}}},
  {"id": "title", "component": {"Text": {"text": {"literalString": "Book a Table"}, "usageHint": "h2"}}},
  {"id": "divider1", "component": {"Divider": {"axis": "horizontal"}}},
  {"id": "guest_section", "component": {"Column": {"children": {"explicitList": ["guest_label", "guest_slider"]}, "alignment": "stretch"}}},
  {"id": "guest_label", "component": {"Text": {"text": {"literalString": "Number of Guests"}, "usageHint": "h4"}}},
  {"id": "guest_slider", "component": {"Slider": {"value": {"path": "/booking/guests", "literalNumber": 2}, "minValue": 1, "maxValue": 10}}},
  {"id": "datetime_section", "component": {"Row": {"children": {"explicitList": ["date_picker", "time_picker"]}, "distribution": "spaceBetween"}}},
  {"id": "date_picker", "weight": 1, "component": {"DateTimeInput": {"value": {"path": "/booking/date"}, "enableDate": true, "enableTime": false}}},
  {"id": "time_picker", "weight": 1, "component": {"DateTimeInput": {"value": {"path": "/booking/time"}, "enableDate": false, "enableTime": true}}},
  {"id": "preferences_section", "component": {"Column": {"children": {"explicitList": ["pref_label", "seating_choice"]}, "alignment": "stretch"}}},
  {"id": "pref_label", "component": {"Text": {"text": {"literalString": "Seating Preference"}, "usageHint": "h4"}}},
  {"id": "seating_choice", "component": {"MultipleChoice": {"selections": {"path": "/booking/seating", "literalArray": []}, "options": [{"label": {"literalString": "Indoor"}, "value": "indoor"}, {"label": {"literalString": "Outdoor"}, "value": "outdoor"}, {"label": {"literalString": "Bar"}, "value": "bar"}], "maxAllowedSelections": 1}}},
  {"id": "divider2", "component": {"Divider": {"axis": "horizontal"}}},
  {"id": "submit_row", "component": {"Row": {"children": {"explicitList": ["cancel_btn", "confirm_btn"]}, "distribution": "end"}}},
  {"id": "cancel_btn", "component": {"Button": {"child": "cancel_text", "action": {"name": "cancel_booking", "context": []}}}},
  {"id": "cancel_text", "component": {"Text": {"text": {"literalString": "Cancel"}}}},
  {"id": "confirm_btn", "component": {"Button": {"child": "confirm_text", "primary": true, "action": {"name": "confirm_booking", "context": [{"key": "guests", "value": {"path": "/booking/guests"}}, {"key": "date", "value": {"path": "/booking/date"}}, {"key": "time", "value": {"path": "/booking/time"}}, {"key": "seating", "value": {"path": "/booking/seating"}}]}}}},
  {"id": "confirm_text", "component": {"Text": {"text": {"literalString": "Confirm Booking"}}}}
]}}
{"dataModelUpdate": {"surfaceId": "booking", "contents": [{"key": "booking", "valueMap": [{"key": "guests", "valueNumber": 2}, {"key": "date", "valueString": ""}, {"key": "time", "valueString": ""}, {"key": "seating", "valueMap": []}]}]}}
{"beginRendering": {"surfaceId": "booking", "root": "root"}}
```

## Search Form with Filters

```jsonl
{"surfaceUpdate": {"surfaceId": "search", "components": [
  {"id": "root", "component": {"Column": {"children": {"explicitList": ["search_bar", "filters_card"]}, "alignment": "stretch"}}},
  {"id": "search_bar", "component": {"Row": {"children": {"explicitList": ["search_input", "search_btn"]}, "alignment": "center"}}},
  {"id": "search_input", "weight": 1, "component": {"TextField": {"label": {"literalString": "Search"}, "text": {"path": "/search/query"}}}},
  {"id": "search_btn", "component": {"Button": {"child": "search_icon", "action": {"name": "search", "context": [{"key": "query", "value": {"path": "/search/query"}}, {"key": "cuisine", "value": {"path": "/search/cuisine"}}, {"key": "priceRange", "value": {"path": "/search/priceRange"}}]}}}},
  {"id": "search_icon", "component": {"Icon": {"name": {"literalString": "search"}}}},
  {"id": "filters_card", "component": {"Card": {"child": "filters_content"}}},
  {"id": "filters_content", "component": {"Column": {"children": {"explicitList": ["filter_title", "cuisine_section", "price_section"]}, "alignment": "stretch"}}},
  {"id": "filter_title", "component": {"Text": {"text": {"literalString": "Filters"}, "usageHint": "h3"}}},
  {"id": "cuisine_section", "component": {"Column": {"children": {"explicitList": ["cuisine_label", "cuisine_choice"]}, "alignment": "stretch"}}},
  {"id": "cuisine_label", "component": {"Text": {"text": {"literalString": "Cuisine Type"}}}},
  {"id": "cuisine_choice", "component": {"MultipleChoice": {"selections": {"path": "/search/cuisine", "literalArray": []}, "options": [{"label": {"literalString": "Italian"}, "value": "italian"}, {"label": {"literalString": "Chinese"}, "value": "chinese"}, {"label": {"literalString": "Japanese"}, "value": "japanese"}, {"label": {"literalString": "Mexican"}, "value": "mexican"}]}}},
  {"id": "price_section", "component": {"Column": {"children": {"explicitList": ["price_label", "price_slider"]}, "alignment": "stretch"}}},
  {"id": "price_label", "component": {"Text": {"text": {"literalString": "Max Price ($)"}}}},
  {"id": "price_slider", "component": {"Slider": {"value": {"path": "/search/priceRange", "literalNumber": 50}, "minValue": 10, "maxValue": 200}}}
]}}
{"dataModelUpdate": {"surfaceId": "search", "contents": [{"key": "search", "valueMap": [{"key": "query", "valueString": ""}, {"key": "cuisine", "valueMap": []}, {"key": "priceRange", "valueNumber": 50}]}]}}
{"beginRendering": {"surfaceId": "search", "root": "root"}}
```

## Form Validation Patterns

### Required Field Indication

Use `usageHint` and text formatting:

```json
{"id": "email_label", "component": {"Text": {"text": {"literalString": "Email *"}, "usageHint": "body"}}}
```

### Validation Regex

Apply client-side validation:

```json
{"id": "phone", "component": {"TextField": {
  "label": {"literalString": "Phone Number"},
  "text": {"path": "/form/phone"},
  "validationRegexp": "^\\+?[1-9]\\d{1,14}$"
}}}
```

### Different Input Types

```json
// Email
{"textFieldType": "shortText", "validationRegexp": "^[^@]+@[^@]+\\.[^@]+$"}

// Password
{"textFieldType": "obscured"}

// Number
{"textFieldType": "number"}

// Long text (textarea)
{"textFieldType": "longText"}
```
