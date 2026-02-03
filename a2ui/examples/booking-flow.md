# A2UI Booking Flow Example

Complete end-to-end business flow demonstrating restaurant booking.

## Flow Overview

```
1. Search → 2. Results → 3. Details → 4. Booking Form → 5. Confirmation
```

## Step 1: Search Interface

Initial search form for restaurant discovery:

```jsonl
{"surfaceUpdate": {"surfaceId": "booking", "components": [
  {"id": "root", "component": {"Column": {"children": {"explicitList": ["header", "search_form", "search_btn"]}}}},
  {"id": "header", "component": {"Text": {"text": {"literalString": "Find a Restaurant"}, "usageHint": "h1"}}},
  {"id": "search_form", "component": {"Column": {"children": {"explicitList": ["location_field", "date_picker", "guests_field"]}}}},
  {"id": "location_field", "component": {"TextField": {"label": {"literalString": "Location"}, "text": {"path": "/search/location"}}}},
  {"id": "date_picker", "component": {"DateTimeInput": {"value": {"path": "/search/date"}, "enableDate": true, "enableTime": true}}},
  {"id": "guests_field", "component": {"Slider": {"value": {"path": "/search/guests", "literalNumber": 2}, "minValue": 1, "maxValue": 10}}},
  {"id": "search_btn", "component": {"Button": {"child": "search_text", "primary": true, "action": {"name": "search_restaurants", "context": [{"key": "location", "value": {"path": "/search/location"}}, {"key": "date", "value": {"path": "/search/date"}}, {"key": "guests", "value": {"path": "/search/guests"}}]}}}},
  {"id": "search_text", "component": {"Text": {"text": {"literalString": "Search"}}}}
]}}
{"dataModelUpdate": {"surfaceId": "booking", "contents": [{"key": "search", "valueMap": [{"key": "location", "valueString": ""}, {"key": "date", "valueString": ""}, {"key": "guests", "valueNumber": 2}]}]}}
{"beginRendering": {"surfaceId": "booking", "root": "root", "styles": {"primaryColor": "#E91E63"}}}
```

## Step 2: Search Results

Display restaurant list after search:

```jsonl
{"surfaceUpdate": {"surfaceId": "booking", "components": [
  {"id": "root", "component": {"Column": {"children": {"explicitList": ["back_btn", "results_header", "results_list"]}}}},
  {"id": "back_btn", "component": {"Button": {"child": "back_text", "action": {"name": "go_back"}}}},
  {"id": "back_text", "component": {"Row": {"children": {"explicitList": ["back_icon", "back_label"]}}}},
  {"id": "back_icon", "component": {"Icon": {"name": {"literalString": "arrowBack"}}}},
  {"id": "back_label", "component": {"Text": {"text": {"literalString": "Back"}}}},
  {"id": "results_header", "component": {"Text": {"text": {"path": "/results/header"}, "usageHint": "h2"}}},
  {"id": "results_list", "component": {"List": {"children": {"template": {"dataBinding": "/results/restaurants", "componentId": "restaurant_card"}}}}},
  {"id": "restaurant_card", "component": {"Card": {"child": "restaurant_content"}}},
  {"id": "restaurant_content", "component": {"Column": {"children": {"explicitList": ["restaurant_image", "restaurant_info", "select_btn"]}}}},
  {"id": "restaurant_image", "component": {"Image": {"url": {"path": "imageUrl"}, "usageHint": "mediumFeature", "fit": "cover"}}},
  {"id": "restaurant_info", "component": {"Column": {"children": {"explicitList": ["restaurant_name", "restaurant_cuisine", "restaurant_rating"]}}}},
  {"id": "restaurant_name", "component": {"Text": {"text": {"path": "name"}, "usageHint": "h3"}}},
  {"id": "restaurant_cuisine", "component": {"Text": {"text": {"path": "cuisine"}, "usageHint": "caption"}}},
  {"id": "restaurant_rating", "component": {"Row": {"children": {"explicitList": ["star_icon", "rating_text"]}}}},
  {"id": "star_icon", "component": {"Icon": {"name": {"literalString": "star"}}}},
  {"id": "rating_text", "component": {"Text": {"text": {"path": "rating"}}}},
  {"id": "select_btn", "component": {"Button": {"child": "select_text", "primary": true, "action": {"name": "select_restaurant", "context": [{"key": "restaurantId", "value": {"path": "id"}}, {"key": "name", "value": {"path": "name"}}]}}}}
  {"id": "select_text", "component": {"Text": {"text": {"literalString": "Book Now"}}}}
]}}
{"dataModelUpdate": {"surfaceId": "booking", "contents": [
  {"key": "results", "valueMap": [
    {"key": "header", "valueString": "3 restaurants found"},
    {"key": "restaurants", "valueMap": [
      {"key": "0", "valueMap": [{"key": "id", "valueString": "r1"}, {"key": "name", "valueString": "La Bella Italia"}, {"key": "cuisine", "valueString": "Italian"}, {"key": "rating", "valueString": "4.8"}, {"key": "imageUrl", "valueString": "https://example.com/bella.jpg"}]},
      {"key": "1", "valueMap": [{"key": "id", "valueString": "r2"}, {"key": "name", "valueString": "Dragon Palace"}, {"key": "cuisine", "valueString": "Chinese"}, {"key": "rating", "valueString": "4.5"}, {"key": "imageUrl", "valueString": "https://example.com/dragon.jpg"}]},
      {"key": "2", "valueMap": [{"key": "id", "valueString": "r3"}, {"key": "name", "valueString": "El Mariachi"}, {"key": "cuisine", "valueString": "Mexican"}, {"key": "rating", "valueString": "4.6"}, {"key": "imageUrl", "valueString": "https://example.com/mariachi.jpg"}]}
    ]}
  ]}
]}}
{"beginRendering": {"surfaceId": "booking", "root": "root"}}
```

## Step 3: Booking Form

Collect booking details:

```jsonl
{"surfaceUpdate": {"surfaceId": "booking", "components": [
  {"id": "root", "component": {"Column": {"children": {"explicitList": ["header", "restaurant_summary", "booking_form", "actions"]}}}},
  {"id": "header", "component": {"Text": {"text": {"literalString": "Complete Your Booking"}, "usageHint": "h1"}}},
  {"id": "restaurant_summary", "component": {"Card": {"child": "summary_content"}}},
  {"id": "summary_content", "component": {"Row": {"children": {"explicitList": ["summary_icon", "summary_text"]}}}},
  {"id": "summary_icon", "component": {"Icon": {"name": {"literalString": "locationOn"}}}},
  {"id": "summary_text", "component": {"Text": {"text": {"path": "/booking/restaurantName"}}}},
  {"id": "booking_form", "component": {"Column": {"children": {"explicitList": ["name_field", "email_field", "phone_field", "special_requests"]}}}},
  {"id": "name_field", "component": {"TextField": {"label": {"literalString": "Your Name"}, "text": {"path": "/booking/name"}}}},
  {"id": "email_field", "component": {"TextField": {"label": {"literalString": "Email"}, "text": {"path": "/booking/email"}, "validationRegexp": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$"}}},
  {"id": "phone_field", "component": {"TextField": {"label": {"literalString": "Phone"}, "text": {"path": "/booking/phone"}}}},
  {"id": "special_requests", "component": {"TextField": {"label": {"literalString": "Special Requests (optional)"}, "text": {"path": "/booking/requests"}, "textFieldType": "longText"}}},
  {"id": "actions", "component": {"Row": {"children": {"explicitList": ["cancel_btn", "confirm_btn"]}, "distribution": "spaceEvenly"}}},
  {"id": "cancel_btn", "component": {"Button": {"child": "cancel_text", "action": {"name": "cancel_booking"}}}},
  {"id": "cancel_text", "component": {"Text": {"text": {"literalString": "Cancel"}}}},
  {"id": "confirm_btn", "component": {"Button": {"child": "confirm_text", "primary": true, "action": {"name": "confirm_booking", "context": [{"key": "restaurantId", "value": {"path": "/booking/restaurantId"}}, {"key": "name", "value": {"path": "/booking/name"}}, {"key": "email", "value": {"path": "/booking/email"}}, {"key": "phone", "value": {"path": "/booking/phone"}}, {"key": "requests", "value": {"path": "/booking/requests"}}]}}}},
  {"id": "confirm_text", "component": {"Text": {"text": {"literalString": "Confirm Booking"}}}}
]}}
{"dataModelUpdate": {"surfaceId": "booking", "contents": [{"key": "booking", "valueMap": [{"key": "restaurantId", "valueString": "r1"}, {"key": "restaurantName", "valueString": "La Bella Italia"}, {"key": "name", "valueString": ""}, {"key": "email", "valueString": ""}, {"key": "phone", "valueString": ""}, {"key": "requests", "valueString": ""}]}]}}
{"beginRendering": {"surfaceId": "booking", "root": "root"}}
```

## Step 4: Confirmation

Success confirmation after booking:

```jsonl
{"surfaceUpdate": {"surfaceId": "booking", "components": [
  {"id": "root", "component": {"Column": {"children": {"explicitList": ["success_icon", "success_title", "confirmation_card", "done_btn"]}, "alignment": "center"}}},
  {"id": "success_icon", "component": {"Icon": {"name": {"literalString": "check"}}}},
  {"id": "success_title", "component": {"Text": {"text": {"literalString": "Booking Confirmed!"}, "usageHint": "h1"}}},
  {"id": "confirmation_card", "component": {"Card": {"child": "confirmation_content"}}},
  {"id": "confirmation_content", "component": {"Column": {"children": {"explicitList": ["conf_restaurant", "conf_date", "conf_guests", "conf_number"]}}}},
  {"id": "conf_restaurant", "component": {"Text": {"text": {"path": "/confirmation/restaurant"}}}},
  {"id": "conf_date", "component": {"Text": {"text": {"path": "/confirmation/dateTime"}}}},
  {"id": "conf_guests", "component": {"Text": {"text": {"path": "/confirmation/guests"}}}},
  {"id": "conf_number", "component": {"Text": {"text": {"path": "/confirmation/confirmationNumber"}, "usageHint": "h3"}}},
  {"id": "done_btn", "component": {"Button": {"child": "done_text", "primary": true, "action": {"name": "done"}}}},
  {"id": "done_text", "component": {"Text": {"text": {"literalString": "Done"}}}}
]}}
{"dataModelUpdate": {"surfaceId": "booking", "contents": [{"key": "confirmation", "valueMap": [{"key": "restaurant", "valueString": "La Bella Italia"}, {"key": "dateTime", "valueString": "January 15, 2025 at 7:00 PM"}, {"key": "guests", "valueString": "2 guests"}, {"key": "confirmationNumber", "valueString": "Confirmation #BK-2025-0001"}]}]}}
{"beginRendering": {"surfaceId": "booking", "root": "root"}}
```

## Action Handling

Server-side action processing:

```python
async def handle_booking_action(action: dict) -> AsyncIterable[dict]:
    name = action["name"]
    context = action.get("context", {})

    if name == "search_restaurants":
        restaurants = await search_restaurants(
            location=context["location"],
            date=context["date"],
            guests=context["guests"]
        )
        # Return results UI...

    elif name == "select_restaurant":
        restaurant_id = context["restaurantId"]
        # Return booking form UI...

    elif name == "confirm_booking":
        booking = await create_booking(
            restaurant_id=context["restaurantId"],
            name=context["name"],
            email=context["email"],
            phone=context["phone"],
            requests=context.get("requests", "")
        )
        # Return confirmation UI...

    elif name == "cancel_booking":
        # Return to search UI...

    elif name == "done":
        yield {"deleteSurface": {"surfaceId": "booking"}}
```

## Best Practices Demonstrated

1. **Progressive flow**: Each step builds on the previous
2. **Data persistence**: User data flows through the entire process
3. **Clear actions**: Descriptive action names (`search_restaurants`, `confirm_booking`)
4. **Visual feedback**: Success icons and confirmation details
5. **Error handling**: Email validation, required fields
6. **Cleanup**: `deleteSurface` when flow completes
