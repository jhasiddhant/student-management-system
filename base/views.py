from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from base.EmailBackEnd import EmailBackEnd


def ShowLoginPage(request):
    return render(request, "login_page.html")


def doLogin(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>", status=405)
    else:
        user = EmailBackEnd.authenticate(request, username=request.POST.get("email"),
                                         password=request.POST.get("password"))
        if user is not None:
            login(request, user)
            if str(user.user_type) == "1":
                return HttpResponseRedirect('/admin_home')
            elif str(user.user_type) == "2":
                return HttpResponseRedirect(reverse("staff_home"))
            else:
                return HttpResponseRedirect(reverse("student_home"))
        else:
            messages.error(request, "Invalid Login Details")
            return HttpResponseRedirect("/")


@login_required(login_url='/')
def GetUserDetails(request):
    return HttpResponse("User : " + request.user.email + " usertype : " + str(request.user.user_type))


def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")
