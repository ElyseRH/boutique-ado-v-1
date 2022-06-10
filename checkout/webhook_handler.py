from django.http import HttpResponse

from .models import Order, OrderLineItem
from products.models import Product

import json
import time


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

    def handle_payment_intent_succeeded(self, event):
        """
        Handle a successful payment intent
        """
        intent = event.data.object  # this accesses the data from the payment intent
        # collect extra info (these are all the variables from checkout/views.py and the json dump):
        pid = intent.id
        bag = intent.metadata.bag
        save_info = intent.metadata.save_info

        billing_details = intent.charges.data[0].billing_details
        shipping_details = intent.shipping
        grand_total = round(intent.charges.data[0].amount / 100, 2)

        # replace empty lines with None because stripe will break otherwise (clean data)
        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None
        
        order_exists = False
        # this delay exists to allow time for order to be placed, in case website is slow
        attempt = 1
        while attempt <= 5:
            try:
                order = Order.objects.get(
                    # use iexact to get exact but NOT case sensitive
                    full_name__iexact=shipping_details.name,
                    email__iexact=billing_details.email,
                    phone_number__iexact=shipping_details.phone,
                    country__iexact=shipping_details.address.country,
                    postcode__iexact=shipping_details.address.postal_code,
                    town_or_city__iexact=shipping_details.address.city,
                    street_address1__iexact=shipping_details.address.line1,
                    street_address2__iexact=shipping_details.address.line2,
                    county__iexact=shipping_details.address.state,
                    grand_total=grand_total,
                    original_bag=bag,
                    stripe_pid=pid,
                )
                order_exists = True
                break  # will break if order is found
            except Order.DoesNotExist:
                attempt += 1  # add increments
                time.sleep(1)  # python sleeps for 1 second on each increment
        
        if order_exists:  # this is what we checked above
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | SUCCESS: Verified order already in database',
                status=200)
        else:
            order = None
            try:  # get details again
                order = Order.objects.create(
                    full_name=shipping_details.name,
                    email=billing_details.email,
                    phone_number=shipping_details.phone,
                    country=shipping_details.address.country,
                    postcode=shipping_details.address.postal_code,
                    town_or_city=shipping_details.address.city,
                    street_address1=shipping_details.address.line1,
                    street_address2=shipping_details.address.line2,
                    county=shipping_details.address.state,
                    original_bag=bag,
                    stripe_pid=pid,
                )
                for item_id, item_data in json.loads(bag).items():  # iterate through json load from payment intent instead of through session bag
                    product = Product.objects.get(id=item_id)
                    if isinstance(item_data, int):
                        order_line_item = OrderLineItem(
                            order=order,
                            product=product,
                            quantity=item_data,
                        )
                        order_line_item.save()
                    else:
                        for size, quantity in item_data['items_by_size'].items():
                            order_line_item = OrderLineItem(
                                order=order,
                                product=product,
                                quantity=quantity,
                                product_size=size,
                            )
                            order_line_item.save()
            except Exception as e:  # whole thing is wrapped in try block, if anything goes wrong, delete order and return 500 error
                if order:
                    order.delete()
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | ERROR: {e}',
                    status=500)
        return HttpResponse(
            content=f'Webhook received: {event["type"]} | SUCCESS: Created order in webhook',
            status=200)
    

    def handle_payment_intent_failed(self, event):
        """
        Handle a failed payment intent
        """
        return HttpResponse(
            content=f'Webbook received: {event["type"]}',
            status=200)
    