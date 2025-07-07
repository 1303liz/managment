from django.shortcuts import render, redirect
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from .forms import CustomUserCreationForm, CustomUserChangeForm, ProfileUpdateForm
from .models import CustomUser, Profile

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            
            # Create user profile
            Profile.objects.create(user=user)
            
            # Generate verification token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            verification_link = f"{request.scheme}://{request.get_host()}/users/verify/{uid}/{token}/"
            
            # Send verification email
            subject = 'Verify your email address - User Management System'
            html_message = render_to_string('users/verification_email.html', {
                'user': user,
                'verification_link': verification_link,
            })
            plain_message = strip_tags(html_message)
            
            try:
                send_mail(
                    subject,
                    plain_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    html_message=html_message,
                    fail_silently=False,
                )
                messages.success(request, 'Please check your email to verify your account.')
            except Exception as e:
                messages.error(request, f'Could not send verification email: {str(e)}. Please try again.')
                user.delete()
                return redirect('register')
            
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

def verify_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.is_email_verified = True
        user.save()
        
        # Send welcome email
        login_link = f"{request.scheme}://{request.get_host()}/users/login/"
        subject = 'Welcome to User Management System!'
        html_message = render_to_string('users/welcome_email.html', {
            'user': user,
            'login_link': login_link,
        })
        plain_message = strip_tags(html_message)
        
        try:
            send_mail(
                subject,
                plain_message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                html_message=html_message,
                fail_silently=False,
            )
        except Exception as e:
            # Log the error but don't interrupt the user flow
            print(f"Error sending welcome email: {str(e)}")
            
        messages.success(request, 'Your email has been verified. You can now log in.')
        return redirect('login')
    else:
        messages.error(request, 'The verification link is invalid or has expired.')
        return redirect('register')

@login_required
def profile(request):
    # Ensure the user has a profile
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        user_form = CustomUserChangeForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('profile')
    else:
        user_form = CustomUserChangeForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'users/profile.html', context)

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/change_password.html', {'form': form})

@login_required
def resend_verification(request):
    if request.method == 'POST' and not request.user.is_email_verified:
        user = request.user
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        verification_link = f"{request.scheme}://{request.get_host()}/users/verify/{uid}/{token}/"
        subject = 'Verify your email address - User Management System'
        html_message = render_to_string('users/verification_email.html', {
            'user': user,
            'verification_link': verification_link,
        })
        plain_message = strip_tags(html_message)
        try:
            send_mail(
                subject,
                plain_message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                html_message=html_message,
                fail_silently=False,
            )
            messages.success(request, 'Verification email sent! Please check your inbox.')
        except Exception as e:
            messages.error(request, f'Could not send verification email: {str(e)}. Please try again later.')
    return redirect('profile')

def users_index(request):
    return redirect('login')
