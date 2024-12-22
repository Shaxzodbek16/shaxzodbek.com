from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password, make_password
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib import messages
from django.utils import timezone
from django.urls import reverse
import uuid
from datetime import timedelta

from .models import OneTimePassword, User
from .helpers import send_email


def signup_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        first_name = request.POST.get("name")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if User.objects.filter(email=email).exists():
            if not User.objects.get(email=email).is_active:
                user = User.objects.get(email=email)
                # Delete any existing OTPs for this user
                OneTimePassword.objects.filter(user=user).delete()
                passcode = user.generate_otp()
                OneTimePassword.objects.create(user=user, passcode=passcode)
                send_email(
                    user.email,
                    {"name": user.first_name, "content": passcode, "sign_up": True},
                )
                return redirect("verify_email", slug=user.slug)
            messages.error(request, "Email already exists with another account.")
            return render(
                request,
                "authentication/sign_up.html",
                context={
                    "email": email,
                    "name": first_name,
                    "password1": password1,
                    "password2": password2,
                },
            )

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return render(
                request,
                "authentication/sign_up.html",
                context={
                    "email": email,
                    "name": first_name,
                    "password1": password1,
                    "password2": password2,
                },
            )

        user = User.objects.create(
            email=email,
            first_name=first_name,
            password=make_password(password1),
            is_active=False,
        )

        passcode = user.generate_otp()
        OneTimePassword.objects.create(user=user, passcode=passcode)

        if not send_email(
            user.email,
            {"name": user.first_name, "content": passcode, "sign_up": True},
        ):
            messages.error(request, "Failed to send verification email.")
            return render(
                request,
                "authentication/sign_up.html",
                context={
                    "email": email,
                    "name": first_name,
                    "password1": password1,
                    "password2": password2,
                },
            )

        messages.info(request, "A verification code has been sent to your email.")
        return redirect("verify_email", slug=user.slug)

    return render(request, "authentication/sign_up.html")


# todo: should fix this view
def verify_email(request, slug):
    if request.method == "POST":
        code = request.POST.get("code")
        passcode = code.replace(" ", "").strip()

        try:
            user = User.objects.get(slug=slug)
            otp = OneTimePassword.objects.filter(
                user=user, purpose="verification"
            ).latest("created_at")

            if otp.expiry < timezone.now():
                otp.delete()
                messages.error(
                    request, "Verification code has expired. Please request a new one."
                )
                return render(
                    request, "authentication/verify_email.html", {"slug": slug}
                )

            if int(otp.passcode) == int(passcode):
                user.is_active = True
                user.save()
                otp.delete()
                login(request, user)
                return redirect("root")
            else:
                messages.error(request, "Invalid verification code.")
                return render(
                    request, "authentication/verify_email.html", {"slug": slug}
                )

        except User.DoesNotExist:
            messages.error(request, "User does not exist.")
        except OneTimePassword.DoesNotExist:
            messages.error(request, "Verification code expired or invalid.")
        except ValueError:
            messages.error(request, "Invalid verification code format.")

    return render(request, "authentication/verify_email.html", {"slug": slug})


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
            if not user.is_active:
                OneTimePassword.objects.filter(user=user).delete()
                passcode = user.generate_otp()
                OneTimePassword.objects.create(
                    user=user, passcode=passcode, purpose="verification"
                )
                send_email(
                    user.email,
                    {"name": user.first_name, "content": passcode, "sign_up": True},
                )
                messages.info(
                    request,
                    "Account is not activated. A verification code has been sent to your email.",
                )
                return render(
                    request,
                    "authentication/verify_email.html",
                    {"email": user.hash_email},
                )

            if check_password(password, user.password):
                login(request, user)
                return render(request, "blog/home.html", {"slug": user.slug})

            messages.error(request, "Invalid email or password.")

        except User.DoesNotExist:
            messages.error(request, "Invalid email or password.")

        return render(
            request,
            "authentication/log_in.html",
            context={"email": email, "password": password},
        )

    return render(request, "authentication/log_in.html")


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("root")


@login_required
def user_profile(request, slug):
    profile = get_object_or_404(User, slug=slug)

    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        date_of_birth = request.POST.get("date_of_birth")
        profile_picture = request.FILES.get("profile_picture")

        profile.first_name = first_name
        profile.last_name = last_name
        profile.date_of_birth = date_of_birth

        if profile_picture:
            profile.profile_picture = profile_picture

        profile.save()
        messages.success(request, "Profile updated successfully.")
        return redirect("profile", slug=profile.slug)

    return render(request, "authentication/profile.html", {"user_profile": profile})


def password_reset_request(request):
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            user = User.objects.get(email=email)
            reset_token = str(uuid.uuid4())
            expiry_time = timezone.now() + timedelta(hours=1)

            otp = OneTimePassword.objects.create(
                user=user,
                passcode=reset_token,
                purpose="password_reset",
                expiry=expiry_time,
            )

            reset_url = request.build_absolute_uri(
                reverse("password_reset_confirm", kwargs={"token": reset_token})
            )

            send_email(
                user.email,
                {
                    "name": user.first_name,
                    "content": reset_url,
                    "password_reset": True,
                },
            )

            messages.info(request, "A password reset link has been sent to your email.")
            return redirect("login")

        except User.DoesNotExist:
            messages.error(request, "No account found with that email.")
            return render(request, "authentication/forgot_password.html")

    return render(request, "authentication/forgot_password.html")


def password_reset_confirm(request, token):
    try:
        otp = OneTimePassword.objects.get(passcode=token, purpose="password_reset")
        if otp.expiry < timezone.now():
            otp.delete()
            messages.error(request, "Password reset link has expired.")
            return redirect("password_reset_request")
    except OneTimePassword.DoesNotExist:
        messages.error(request, "Invalid password reset link.")
        return redirect("password_reset_request")

    if request.method == "POST":
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return render(
                request, "authentication/password_reset_confirm.html", {"token": token}
            )

        if len(password1) < 8:
            messages.error(request, "Password must be at least 8 characters long.")
            return render(
                request, "authentication/password_reset_confirm.html", {"token": token}
            )

        user = otp.user
        user.set_password(password1)
        user.save()

        otp.delete()

        messages.success(
            request, "Your password has been reset successfully. You can now log in."
        )
        return redirect("login")

    return render(
        request, "authentication/password_reset_confirm.html", {"token": token}
    )
