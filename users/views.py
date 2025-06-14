import qrcode
import pyotp
from django.contrib.auth.forms import AuthenticationForm
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
from .forms import ProfileForm
from issues.models import Issues 
from django.shortcuts import render





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
    form = AuthenticationForm(request, data=request.POST) if request.method == 'POST' else AuthenticationForm()

    if request.method == 'POST' and form.is_valid():
        user = form.get_user()  # Get authenticated user
        login(request, user)
        messages.success(request, f"Welcome {user.username}! You are now logged in.")
        return redirect('profile')  # Ensure 'profile' exists in urls.py

    return render(request, 'users/login.html', {'form': form}) 

def logout_view(request):
    logout(request) #Ends user session
    return redirect('login')   # Redirects to Login Page after logout


@login_required
def profile_view(request):
    return render(request, 'users/profile.html')

@login_required
def edit_profile(request):
    # Get or create the user's profile
    profile = request.user.userprofile


    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            form.save()  # Save profile data including profile picture
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')  # Redirect to profile page after update

    else:
        form = ProfileForm(instance=profile)

    return render(request, 'users/edit_profile.html', {'form': form, 'profile': profile})



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

    profile  = request.user.userprofile

    
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


    if request.method == "POST":
        otp = request.POST.get("otp")
        if profile.verify_token(otp):
            profile.two_factor_enabled = True 
            profile.save()
            messages.success(request, "2FA has been enabled successfully.")
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid OTP. Please try again.")

    return render(request, "users/enable_2fa.html", {"qr_base64": qr_base64})




@login_required
def dashboard(request):
    user = request.user
    issues = Issues.objects.filter(reporter=user)
    profile = user.userprofile  # Get user profile for 2FA

    return render(request, 'users/dashboard.html', {
        'issues': issues,
        'profile': profile,
        'two_factor_status': profile.two_factor_enabled
    })


@login_required
def disable_2fa(request):
    profile = request.user.userprofile
    profile.two_factor_enabled = False
    profile.otp_secret = ''
    profile.save()
    messages.success(request, "2FA has been disabled.")
    return redirect('profile')





# Create your views here.
