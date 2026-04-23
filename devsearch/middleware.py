import json
from django.contrib.messages import get_messages

class HtmxMessageMiddleware:
    """
    Middleware that moves Django messages into the HX-Trigger header for HTMX requests.
    This allows frontend JavaScript (like SweetAlert2) to intercept them seamlessly
    without needing a full page reload or Out-of-Band (OOB) swaps.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Only process if it's an HTMX request
        if "Hx-Request" not in request.headers:
            return response

        # Don't process on redirects, because the browser transparently follows them
        # and HTMX won't see the HX-Trigger headers on the 302 response.
        # Leave the messages in the session for the subsequent request.
        if 300 <= response.status_code < 400:
            return response

        messages = get_messages(request)
        if not messages:
            return response

        # Extract messages
        message_list = [{"message": msg.message, "tags": msg.tags} for msg in messages]

        # Merge with existing HX-Trigger if any
        hx_trigger = response.headers.get("HX-Trigger")
        if hx_trigger:
            try:
                trigger_data = json.loads(hx_trigger)
                trigger_data["messages"] = message_list
                response.headers["HX-Trigger"] = json.dumps(trigger_data)
            except json.JSONDecodeError:
                # If it's a simple string trigger, convert to object
                response.headers["HX-Trigger"] = json.dumps({
                    hx_trigger: "",
                    "messages": message_list
                })
        else:
            response.headers["HX-Trigger"] = json.dumps({"messages": message_list})

        return response
