from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from .models import Profile
from django.contrib.auth import login

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            display_name = form.cleaned_data.get('display_name')
            # Сохраняем отображаемое имя в профиль
            user.profile.display_name = display_name
            user.profile.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/signup.html', {'form': form})


from django.contrib.auth.decorators import login_required

@login_required
def home_view(request):
    return render(request, 'users/home.html')
