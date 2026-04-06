from django.urls import path
from . import views
app_name = 'billing'
urlpatterns = [
    path('checkout/', views.create_checkout_session, name='checkout'),
    path('success/', views.checkout_success, name='success'),
    path('status/', views.subscription_status, name='subscription_status'),
    path('webhook/', views.webhook, name='webhook'),
    path('pricing/', views.pricing, name='pricing'),
]
