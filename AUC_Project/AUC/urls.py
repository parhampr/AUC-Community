import django
from django import template
from django.urls import path
from django.views.generic.base import TemplateView
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.testing, name='testing'),
    path("accounts/register/", views.register, name="register"),
    path("accounts/login/", views.login_view, name="login"),
    path("accounts/logout", views.logout_view, name="logout"),
    path("accounts/login/usercheck", views.userCheck, name='userAvailability'),
    path("reset_password/", auth_views.PasswordResetView.as_view(template_name="AUC/AuthenticateProfile.html", html_email_template_name="AUC/Auth/acc_pass_reset_email.html", subject_template_name="AUC/Auth/password_reset_custom_subject.txt"), name="reset_password"),
    path("reset_password_sent/", auth_views.PasswordResetDoneView.as_view(template_name="AUC/AuthenticateProfile.html"), name="password_reset_done"),
    path("accounts/user/password_reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name="AUC/AuthenticateProfile.html"), name="password_reset_confirm"),
    path("reset_password_complete/", views.password_reset_successfully, name="password_reset_complete"),
    path("accounts/user/confirm_email", views.Confirm_Email, name='activate'),
    path("accounts/user/send_verification/", views.ReVerificationEmail, name='send_verify'),
    path("xyx", views.ErrorHandler404)
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)