import qrcode
import pyotp
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth import update_session_auth_hash
from django.core.mail import send_mail
from django.contrib.auth import logout
from django.contrib import messages
from .forms import UserRegistrationForm
import random
from .forms import ProfileUpdateForm, TwoFactorForm
from .models import UserProfile
from django.conf import settings
from io import BytesIO
import base64
import io






def register(request):
    form = UserRegistrationForm()
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!You can now log in.')
            return redirect('login')
            
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')


        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome {username}! You are now logged in.")
            return redirect('profile') #Redirects to the profile page
        else:
            messages.error(request, 'Invalid Username or Password')
    return render(request, 'users/login.html')

def logout_view(request):
    logout(request) #Ends user session
    return redirect('login')   # Redirects to Login Page after logout


@login_required
def profile_view(request):
    return render(request, 'users/profile.html')

@login_required
def edit_profile(request):
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect("edit_profile")
    else:
        form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, "edit_profile.html", {"form": form})


@login_required
def send_otp(request):
    otp = random.randint(100000, 999999)
    request.session["otp"] = otp  # Store OTP in session
    email = request.user.email

    send_mail(
        "Your 2FA OTP Code",
        f"Your OTP is: {otp}",
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )
    messages.info(request, "OTP sent to your email.")
    return redirect("verify_otp")


@login_required
def verify_otp(request):
    if request.method == "POST":
        form = TwoFactorForm(request.POST)
        if form.is_valid():
            entered_otp = form.cleaned_data["otp"]
            if entered_otp == str(request.session.get("otp")):
                messages.success(request, "2FA verification successful!")
                return redirect("dashboard")
            else:
                messages.error(request, "Invalid OTP. Try again.")

    else:
        form = TwoFactorForm()

    return render(request, "verify_otp.html", {"form": form})

@login_required
def enable_2fa(request):
    user = request.user

    profile, created = UserProfile.objects.get_or_create(user=user)
    
    if not profile.otp_secret:
        profile.otp_secret = pyotp.random_base32()
        profile.save()

    totp = pyotp.TOTP(profile.otp_secret)
    otp_url = totp.provisioning_uri(user.username, issuer_name="My Django App")

    # Generate QR code
    qr = qrcode.make(otp_url)
    qr_io = io.BytesIO()
    qr.save(qr_io, format="PNG")
    qr_base64 = base64.b64encode(qr_io.getvalue()).decode()

    return render(request, "users/enable_2fa.html", {"qr_base64": qr_base64})




# Create your views here.
