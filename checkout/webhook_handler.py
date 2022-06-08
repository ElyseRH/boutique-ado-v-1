from django.http import HttpResponse


class StripeWH_Handler:
    """
    Handle Stripe webhooks
    """
    def __init__(self, request):
        self.request = request
        # this makes sure that any request of this class are instances of the self
    
    def handle_event(self, event):
        """
        Handle a generic/unknown/unexpected webhook event
        """
        return HttpResponse(
            content=f'Webbook received: {event["type"]}',
            status=200)
