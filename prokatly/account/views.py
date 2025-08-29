from django.shortcuts import render, redirect , get_object_or_404
from .forms import RegisterForm , LoginForm
from django.contrib.auth import authenticate , login , logout
from .models import User
from product.models import Product

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("login")
        
    else:
        form = RegisterForm()
        
    context = {
        'form': form
    }
    return render(request, 'account/register.html', context)



def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("index")
            else:
                form.add_error(None, "Неверное имя пользователя или пароль ")
    else:
        form = LoginForm()
    context = {
        'form': form
    }
    return render(request, 'account/login.html', context)



def logout_view(request):
    logout(request)
    return redirect("login")



def profile(request, username):
    user = get_object_or_404(User,username=username)
    products = Product.objects.filter(owner=user)
    context = {
        "profile_user": user,
        'products':products
    }
    return render(request, "account/profile.html", context)