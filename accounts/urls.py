from django.urls import path
from . import views
app_name = 'accounts'
urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('social-accounts/', views.social_accounts_view, name='social_accounts'),
    path('social-accounts/disconnect/<str:provider>/', views.disconnect_social_account, name='disconnect_social_account'),
]
