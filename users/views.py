from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib import messages
from .forms import UserRegistrationForm




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
    return render(request, 'profile.html')



# Create your views here.
