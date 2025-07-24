from django.urls import path
from . import views

app_name = "payments"

urlpatterns = [
    path('checkout/summary/', views.checkout_summary, name='checkout_summary'),
    path('payment-success/<str:invoice_id>/', views.payment_successful, name='payment_successful'),
]
