from django.urls import path
from . import views

app_name = "platform"

urlpatterns = [
    path("", views.index, name="index"),
    path('login_user/', views.login_user, name='login_user'),
    path("signup/", views.signup, name="signup"),
    path('logout/', views.logout_view, name='logout'),
    path('products/', views.product_list, name='product_list'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('view_cart/', views.view_cart, name='view_cart'),
    path('cart/remove/<int:product_id>/', views.remove_item, name='remove_item'),
    path('checkout/', views.checkout, name='checkout'),
    path('order_confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('order_history/', views.order_history, name='order_history'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path("admin_dashboard/order/<int:order_id>/", views.order_detail_admin, name="order_detail_admin"),
    path("my_account/", views.my_account, name="my_account"),
    path('home/', views.home, name='home'),

]
