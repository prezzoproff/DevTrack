from django.shortcuts import render, redirect
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

# Create your views here.
