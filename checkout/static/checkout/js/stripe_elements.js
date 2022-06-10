/*
    Core logic/payment flow for this comes from here:
    https://stripe.com/docs/payments/accept-a-payment   ???? docs have changed but this still works except webhooks?
    CSS from here: 
    https://stripe.com/docs/stripe-js
*/

// slice first and last char from each pub key to remove quotation marks
var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
var clientSecret = $('#id_client_secret').text().slice(1, -1);
var stripe = Stripe(stripePublicKey);
var elements = stripe.elements();
var style = {
    base: {
        color: '#000',
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
            color: '#aab7c4'
        }
    },
    invalid: {
        color: '#dc3545',
        iconColor: '#dc3545'
    }
};
var card = elements.create('card', {style: style});
card.mount('#card-element');



// Handle realtime validation errors on the card element and display them clearly
card.addEventListener('change', function(event) {
    var errorDiv = document.getElementById('card-errors');
    if (event.error) {
        var html = `
            <span class="icon" role="alert">
                <i class="fas fa-times"></i>
            </span>
            <span>${event.error.message}</span>
        ` // back ticks around html here
        $(errorDiv).html(html);
    } else {
        errorDiv.textContent = '';
    }
});

// Handle form submit, copied from docs with a couple of changes
var form = document.getElementById('payment-form');

form.addEventListener('submit', function(ev) {
    ev.preventDefault();
    card.update({ 'disabled': true});  // this is to prevent multiple submissions
    $('#submit-button').attr('disabled', true);  // this is also to prevent multiple submissions
    $('#payment-form').fadeToggle(100);
    $('#loading-overlay').fadeToggle(100);
    // here is where stripe sends the pax's info off
    stripe.confirmCardPayment(clientSecret, {
        payment_method: {
            card: card,
            // form data needs to be added to confirmed card payment method, form data is added like below
            // use trim to get rid of white space. separate billing and shipping
            // post code is only on ship as on billing it will come from stripe, and stripe will override
            // it if we add it to billing
            billing_details: {
                name: $.trim(form.full_name.value),
                phone: $.trim(form.phone_number.value),
                email: $.trim(form.email.value),
                address:{
                    line1: $.trim(form.street_address1.value),
                    line2: $.trim(form.street_address2.value),
                    city: $.trim(form.town_or_city.value),
                    country: $.trim(form.country.value),
                    state: $.trim(form.county.value),
                }
            }
        },
        shipping: {
            name: $.trim(form.full_name.value),
            phone: $.trim(form.phone_number.value),
            address: {
                line1: $.trim(form.street_address1.value),
                line2: $.trim(form.street_address2.value),
                city: $.trim(form.town_or_city.value),
                country: $.trim(form.country.value),
                postal_code: $.trim(form.postcode.value),
                state: $.trim(form.county.value),
            }
        },
    }).then(function(result) {
        if (result.error) {
            // shows error to pax, same as before
            var errorDiv = document.getElementById('card-errors');
            var html = `
                <span class="icon" role="alert">
                <i class="fas fa-times"></i>
                </span>
                <span>${result.error.message}</span>`;
            $(errorDiv).html(html);
            $('#payment-form').fadeToggle(100);
            $('#loading-overlay').fadeToggle(100);
            card.update({ 'disabled': false});  // re-enables card to alow user to fix it
            $('#submit-button').attr('disabled', false);
        } else {
            if (result.paymentIntent.status === 'succeeded') {
                form.submit();
                // there's a risk of pax closing the window before callback execution.
                // set up webhook or plugin to handle any busi-critical post payment action
                // or just include msg saying don't close the window?
            }
        }
    });
});
