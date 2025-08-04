from django.dispatch import receiver
from paypal.standard.ipn.signals import valid_ipn_received
from Platform.models import Order

@receiver(valid_ipn_received)
def payment_notification(sender, **kwargs):
    ipn = sender
    if ipn.payment_status == "Completed":
        try:
            order = Order.objects.get(invoice_id=ipn.invoice)

            if not order.is_paid:
                # Mark as paid
                order.total_price = order.get_total_cost()
                order.is_paid = True
                order.save()

                # Deduct stock
                for item in order.items.all():
                    item.product.product_stock -= item.quantity
                    item.product.save()

                print(f"[IPN] Order {order.id} marked as paid. Stock updated.")

        except Order.DoesNotExist:
            print(f"[IPN] No matching order found for invoice {ipn.invoice}")
