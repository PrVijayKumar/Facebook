from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView, ListView

from .models import Price, Product
from user.models import CustomUser, Stars
import stripe
from django.conf import settings
from django.shortcuts import redirect
from .models import Price, Product, PurchaseHistory
from django.views.generic import TemplateView
import json
from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.
# products/views.py


class ProductListView(ListView):
    model = Product
    context_object_name = "products"
    template_name = "a_stripe/product_list.html"

class ProductDetailView(DetailView):
    model = Product
    context_object_name = "product"
    template_name = "a_stripe/product_detail.html"

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data()
        context["prices"] = Price.objects.filter(product=self.get_object())
        return context
    


class CreateStripeCheckoutSessionView(View):
    """
    Create a checkout session and redirect the user to Stripe's checkout page
    """

    def post(self, request, *args, **kwargs):
        price = Price.objects.get(id=self.kwargs["pk"])

        # breakpoint()
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "unit_amount": int(price.price) * 100,
                        "product_data": {
                            "name": price.product.name,
                            "description": price.product.desc,
                            "images": [
                                f"{settings.BACKEND_DOMAIN}{price.product.thumbnail.url}"
                            ],
                        },
                    },
                    "quantity": price.product.quantity,
                }
            ],
            metadata={
                "product_id": price.product.id,
                "user_id": request.user.id,
                "quantity": price.product.quantity,
                "amount_paid": int(price.price) * price.product.quantity,
            },
            mode="payment",
            success_url=settings.PAYMENT_SUCCESS_URL,
            cancel_url=settings.PAYMENT_CANCEL_URL,
        )
        return redirect(checkout_session.url)
    


class SuccessView(TemplateView):
    template_name = "a_stripe/success.html"

    def get(self, request, *args, **kwargs):
        print("get", request.body)
        # breakpoint()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # breakpoint()
        print("post", request.body)
        return super().post(request, *args, **kwargs)
    


class CancelView(TemplateView):
    template_name = "a_stripe/cancel.html"


# payments/views.py

@csrf_exempt
def stripe_webhook(request):
# payment views
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    # except ValueError as e:
    except ValueError:
        # Invalid payload
        # print(e)
        return HttpResponse(status=400)
    
    # except stripe.error.SignatureVerificationError as e:
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        # print(e)
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        # breakpoint()
        print("Payment was successful.")
        session = event['data']['object']
        # breakpoint()
        product_id = session['metadata']['product_id']
        user_id = session['metadata']['user_id']
        quantity = int(session['metadata']['quantity'])
        amount_paid = session['metadata']['amount_paid']
        get_product = Product.objects.get(id=product_id)
        get_user = CustomUser.objects.get(id=user_id)
        print("amount paid", amount_paid)
        PurchaseHistory.objects.create(product=get_product, purchase_success=True, user=get_user, amount_paid=amount_paid)
        stars = Stars.objects.get(user_id=user_id)
        stars.amount += quantity
        stars.save()
        # TODO:
        # breakpoint()
        # import json
        # obj = request.body.decode('utf-8')
        # obj = json.loads(obj)
        # print(obj['data']['object']['metadata']['product_id'])


    return HttpResponse(status=200)


# # Using Django
# @csrf_exempt
# def my_webhook_view(request):
#     payload = request.body
#     event = None

#     try:
#         event = stripe.Event.construct_from(
#             json.loads(payload), stripe.api_key
#         )
#     except ValueError as e:
#     # Invalid payload
#         return HttpResponse(status=400)

#     # Handle the event
#     if event.type == 'payment_intent.succeeded':
#         payment_intent = event.data.object # contains a stripe.PaymentIntent
#         # Then define and call a method to handle the successful payment intent.
#         # handle_payment_intent_succeeded(payment_intent)
#     elif event.type == 'payment_method.attached':
#         payment_method = event.data.object # contains a stripe.PaymentMethod
#         # Then define and call a method to handle the successful attachment of a PaymentMethod.
#         # handle_payment_method_attached(payment_method)
#         # ... handle other event types
#     else:
#         print('Unhandled event type {}'.format(event.type))

#     return HttpResponse(status=200)