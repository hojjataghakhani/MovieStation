from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth import login as a_login
from django.contrib.auth import logout as a_logout
from django.shortcuts import redirect
from django.shortcuts import HttpResponse
from django.contrib.auth.hashers import *
from django.contrib.auth.decorators import login_required
from django.template import RequestContext, loader

# import models
from .models import UserProfile

# import forms
from .forms import RegisterForm

# Create your views here.


@login_required(login_url='/signin')
def activation(request):
    user = UserProfile.objects.get(id=request.user.id)
    if user.activation_code == request.REQUEST.get('activation'):
        user.is_activate = True
    return redirect("/home")


def register(request):
    print("hi")
    if request.method == "POST":
        print(request.POST)
        form = RegisterForm(request.POST)
        print(form)
        if form.is_valid():
            user = UserProfile.objects.create_user(form.cleaned_data['username'], form.cleaned_data['email'],
                                                   form.cleaned_data['password'])
            user.birth_date = form.cleaned_data['birth_date']
            user.nickname = form.cleaned_data['username']
            user.activation_code = "1"
            # user.activation_code = hashlib.sha224(user.username + user.password).hexdigest()
            # send_mail('Simorgh Hotel Reservation', "127.0.0.1:8000/activation/?activation=" + user.activation_code,
            #           '', [user.email],
            #           fail_silently=False)
            user.save()
            return redirect("/home")
        else:
            print("not valid")
            form = RegisterForm()
            return render(request, "mysite/mainpage.html")
    else:
        form = RegisterForm()
        return render(request, "mysite/mainpage.html")


def login(request):
    if request.method == "POST":
        username = request.POST.get("UserName", "")
        password = request.POST.get("password", "")

        user = authenticate(username=username, password=password)

        if user is not None:
            a_login(request, user)
            return render(request, 'mysite/home.html')
        else:
            template = loader.get_template("mysite/mainpage.html")
            context = RequestContext(request, {
                'Alert': True
            })
            return HttpResponse(template.render(context))


def homepage(request):
    return render(request, "mysite/home.html")

@login_required(login_url='')
def show_profile(request, username):
    nowUser = UserProfile.objects.get(id=request.user)
    try:
        user = UserProfile.objects.get(username=username)
    except:
        user = None
    if user is not None:
        if user.username == nowUser.username:
            return render(request, "mysite/profile.html", {"User":user, "Owner":True})
        else:
            if user in nowUser.followings.all():
                return render(request, "mysite/profile.html", {"User": user, "Owner": False, "follows": True})
            else:
                return render(request, "mysite/profile.html", {"User": user, "Owner": False, "follows": False})
    else:
        return HttpResponse("Error : cant find requsted user")


