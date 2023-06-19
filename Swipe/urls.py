"""Swipe URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from allauth.account.views import ConfirmEmailView
from dj_rest_auth.registration.views import RegisterView, VerifyEmailView, ResendEmailVerificationView
from dj_rest_auth.views import LoginView, LogoutView
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from Swipe import settings

from Swipe.users.views import BuilderRegisterView, CustomConfirmEmailView, OwnerRegisterView

urlpatterns = [
    path('admin/', admin.site.urls),
    # Swagger UI
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # Apps
    path('users/', include('Swipe.users.urls')),
    path('notaries/', include('Swipe.notaries.urls')),
    path('residential-complexes/', include('Swipe.residential_complexes.urls')),
    path('announcements/', include('Swipe.announcements.urls')),
    path('promotions/', include('Swipe.promotions.urls')),
    path('chessboards/', include('Swipe.chessboard.urls')),
    path('saved-filters/', include('Swipe.saved_filters.urls')),

    # auth
    path('register/builder/', BuilderRegisterView.as_view()),
    path('register/owner/', OwnerRegisterView.as_view()),
    re_path(r'^account-confirm-email/(?P<key>[-:\w]+)/$', CustomConfirmEmailView.as_view(),
            name='account_confirm_email'),

    # Simple JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),



    # dj-rest-auth
    path('login/', LoginView.as_view(), name='rest_login'),
    path('logout/', LogoutView.as_view()),
    path('verify-email/', VerifyEmailView.as_view(), name='rest_verify_email'),
    path('resend-email/', ResendEmailVerificationView.as_view(), name="rest_resend_email"),
    re_path(r'^account-email-verification-sent/', VerifyEmailView.as_view(),
            name='account_email_verification_sent'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
               + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
