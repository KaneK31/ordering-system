from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from Platform.models import Product, Order, OrderItem
from decimal import Decimal, InvalidOperation
from django.contrib import messages
from Platform.views import get_cart_details


# Create your views here.
def checkout_summary(request):
    cart = request.session.get('cart', {})
    items, total = get_cart_details(cart)

    invoice_id = request.session.get('invoice_id')

    if not invoice_id:
        messages.error(request, "No invoice ID found. Please start checkout again.")
        return redirect("platform:view_cart")

    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': total,
        'currency_code': 'GBP',
        'invoice': invoice_id,
        'notify_url': f"{settings.BASE_URL}{reverse('paypal-ipn')}",
        'return_url': f"{settings.BASE_URL}{reverse('payments:payment_successful', args=[invoice_id])}",
        'cancel_return': f"{settings.BASE_URL}{reverse('platform:view_cart')}",
    }
    print("INVOICE ID:", request.session.get("invoice_id"))
    print("DEBUG PAYPAL_TEST:", settings.PAYPAL_TEST)
    form = PayPalPaymentsForm(initial=paypal_dict)

    return render(request, 'platform/checkout_summary.html', {
        'cart_items': items,
        'total_price': total,
        'paypal_form': form,
        'invoice_id': invoice_id,
    })


def payment_successful(request, invoice_id):
    order = get_object_or_404(Order, invoice_id=invoice_id)

    if not order.is_paid:
        messages.warning(request, "Payment not yet verified by PayPal.")
        return redirect("platform:view_cart")

    if request.user.is_authenticated and request.user == order.user:
        messages.success(request, "Payment successful! Order confirmed.")
    else:
        messages.info(request, "Payment successful. Please log in to see your order history.")

    request.session["cart"] = {}
    return redirect('platform:order_confirmation', order_id=order.id)
