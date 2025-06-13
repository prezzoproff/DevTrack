from django.urls import path
from . import views
from .views import edit_profile, send_otp, verify_otp
from .views import enable_2fa





urlpatterns = [
        path('register/', views.register, name = 'register'),
        path('login/', views.login_view, name = 'login'),
        path('logout/', views.logout_view, name = 'logout'),
        path('profile/', views.profile_view, name = 'profile'),
        path("edit-profile/", edit_profile, name="edit_profile"),
        path("send-otp/", send_otp, name="send_otp"),
        path("verify-otp/", verify_otp, name="verify_otp"),
        path('enable-2fa/', enable_2fa, name='enable_2fa'),
        path('dashboard/', views.dashboard, name='dashboard'),
        path('disable-2fa/', views.disable_2fa, name='disable_2fa'),
]
