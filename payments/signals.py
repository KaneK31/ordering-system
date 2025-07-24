from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from django.dispatch import receiver
from Platform.models import Order
from decimal import Decimal


@receiver(valid_ipn_received)
def paypal_ipn_handler(sender, **kwargs):
    ipn = sender
    if ipn.payment_status == ST_PP_COMPLETED:
        try:
            order = Order.objects.get(invoice_id=ipn.invoice)
            if ipn.mc_gross == float(order.get_total_cost()) and ipn.mc_currency == "GBP":
                order.is_paid = True
                order.save()
        except Order.DoesNotExist:
            pass
