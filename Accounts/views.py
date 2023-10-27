from django.shortcuts import redirect, render
from django.utils.text import slugify
from django.contrib.auth import authenticate, login as auth_login, logout
from .models import Account

# Create your views here.
def register(request):
    if request.method == 'POST':
        first_name      = request.POST.get('first_name')
        last_name       = request.POST.get('last_name')
        email           = request.POST.get('email')
        phone_number    = request.POST.get('phone_number')
        country         = request.POST.get('country')
        password        = request.POST.get('password')
        re_password     = request.POST.get('re_password')



        if Account.objects.filter(email=email).exists():
            error_message = "Email already exist use another email"
            return render(request,'register.html',{'error_message':error_message})
      
        if Account.objects.filter(phone_number=phone_number).exists():
            error_message = "Number already exist use another number"
            return render(request,'register.html',{'error_message':error_message})
        
        username = slugify(f"{first_name}-{last_name}")

        if password == re_password :
            user = Account.objects.create(
                first_name = first_name,
                last_name = last_name,
                email=email,
                username = username,
                phone_number=phone_number,
                country=country,
            )

            user.set_password(password)
            user.save()

            return redirect('login')

        else:
            error_message = 'both password doesnt match please type correctly'
            return render(request,'register.html',{'error_message':error_message})

    return render(request,'register.html')


def login(request):
    # if request.method == 'POST':
    #     email = request.POST.get('email')
    #     password = request.POST.get('password')

    #     user = authenticate(request, email=email, password=password)

    #     if  user is not None:
    #         auth_login(request,user)
    #         return redirect('home')
        
    #     else:
    #         error_message = 'Invalid email or password. Please try again.'
    #         return render(request,'login.html',{'error_message':error_message})

    return render(request,'login.html')