from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
import random
from .models import OneTimePassword

User = get_user_model()

def signup_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        name = request.POST.get('name')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'authentication/signup.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'authentication/signup.html')

        # Create inactive user
        user = User.objects.create_user(email=email, name=name, password=password1, is_active=False)

        # Generate OTP code
        passcode = '{:06d}'.format(random.randint(0, 999999))
        OneTimePassword.objects.create(user=user, passcode=passcode)

        # Send email with passcode
        send_mail(
            'Your verification code',
            f'Your verification code is {passcode}',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )

        messages.info(request, 'A verification code has been sent to your email.')

        # Redirect to verification page
        return redirect('verify_email', slug=user.slug)
    else:
        return render(request, 'authentication/signup.html')



def verify_email(request, slug):
    if request.method == 'POST':
        passcode_input = request.POST.get('passcode')
        try:
            user = User.objects.get(slug=slug)
            otp = user.otp  # OneToOneField related object
            if otp.passcode == passcode_input:
                user.is_active = True
                user.save()
                otp.delete()  # Remove OTP after successful verification
                messages.success(request, 'Email verified. You can now log in.')
                return redirect('login')
            else:
                messages.error(request, 'Invalid verification code.')
        except User.DoesNotExist:
            messages.error(request, 'User does not exist.')
        except OneTimePassword.DoesNotExist:
            messages.error(request, 'Verification code expired or invalid.')
    else:
        return render(request, 'authentication/verify_email.html', {'slug': slug})
    return render(request, 'authentication/verify_email.html', {'slug': slug})


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('root')  # Redirect to your desired home page
            else:
                messages.error(request, 'Account is inactive. Please verify your email.')
                return redirect('login')
        else:
            messages.error(request, 'Invalid email or password.')
            return redirect('login')
    else:
        return render(request, 'authentication/login.html')



@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')


@login_required
def user_profile(request, slug):
    profile = get_object_or_404(User, slug=slug)
    return render(request, 'authentication/user_profile.html', {'user_profile': profile})


# authentication/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
import uuid
from datetime import timedelta

from .models import OneTimePassword

User = get_user_model()

def password_reset_request(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        try:
            user = User.objects.get(email=email)
            # Generate a unique token
            reset_token = str(uuid.uuid4())
            # Optionally, set an expiration time (e.g., 1 hour)
            expiry_time = timezone.now() + timedelta(hours=1)

            # Create a OneTimePassword entry for password reset
            otp = OneTimePassword.objects.create(
                user=user,
                passcode=reset_token,
                purpose='password_reset',
                expiry=expiry_time
            )

            # Build password reset URL
            reset_url = request.build_absolute_uri(
                reverse('password_reset_confirm', kwargs={'token': reset_token})
            )

            # Send email with reset link
            subject = 'Password Reset Request'
            message = render_to_string('authentication/password_reset_email.html', {
                'user': user,
                'reset_url': reset_url,
            })

            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )

            messages.info(request, 'A password reset link has been sent to your email.')
            return redirect('login')

        except User.DoesNotExist:
            messages.error(request, 'No account found with that email.')
            return render(request, 'authentication/password_reset_request.html')

    return render(request, 'authentication/password_reset_request.html')


def password_reset_confirm(request, token):
    try:
        otp = OneTimePassword.objects.get(passcode=token, purpose='password_reset')
        if otp.expiry < timezone.now():
            otp.delete()
            messages.error(request, 'Password reset link has expired.')
            return redirect('password_reset_request')
    except OneTimePassword.DoesNotExist:
        messages.error(request, 'Invalid password reset link.')
        return redirect('password_reset_request')

    if request.method == 'POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'authentication/password_reset_confirm.html', {'token': token})

        if len(password1) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
            return render(request, 'authentication/password_reset_confirm.html', {'token': token})

        # Update user's password
        user = otp.user
        user.set_password(password1)
        user.save()

        # Delete the OTP after successful reset
        otp.delete()

        messages.success(request, 'Your password has been reset successfully. You can now log in.')
        return redirect('login')

    return render(request, 'authentication/password_reset_confirm.html', {'token': token})
