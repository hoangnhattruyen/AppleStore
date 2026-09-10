from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.index, name='index'),
    path('products/', views.product_list, name='product_list'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    
    # Cart API
    path('cart/add/', views.cart_add, name='cart_add'),
    path('cart/update/', views.cart_update, name='cart_update'),
    path('cart/remove/', views.cart_remove, name='cart_remove'),
    path('cart/json/', views.cart_json, name='cart_json'),
    
    # Checkout & Order
    path('checkout/', views.checkout, name='checkout'),
    path('order-success/<str:order_code>/', views.order_success, name='order_success'),
    path('order-lookup/', views.order_lookup, name='order_lookup'),
    
    # Features
    path('compare/', views.compare_cases, name='compare'),
    path('product/<int:product_id>/review/', views.submit_review, name='submit_review'),

    # User Account & Auth
    path('register/', views.user_register, name='user_register'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('account/', views.user_account, name='user_account'),
]
