from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings
from . import views

# Custom authentication form for email login
class EmailAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Email'

urlpatterns = [
    path('', views.users_index, name='users_index'),
    path('register/', views.register, name='register'),
    path('verify/<str:uidb64>/<str:token>/', views.verify_email, name='verify_email'),
    path('resend-verification/', views.resend_verification, name='resend_verification'),
    path('login/', auth_views.LoginView.as_view(
        template_name='users/login.html',
        form_class=EmailAuthenticationForm
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        template_name='users/logout.html',
    ), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('change-password/', views.change_password, name='change_password'),
    
    # Password reset URLs
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='users/password_reset.html',
             html_email_template_name='users/password_reset_email.html',
             subject_template_name='users/password_reset_subject.txt',
             from_email=settings.DEFAULT_FROM_EMAIL,
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
]
