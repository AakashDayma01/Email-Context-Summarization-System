from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
# Create your views here.


def login_view(request):

    if request.method == "POST":

        email = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=email,
            password=password
        )

        if user:
            login(request, user)
            return redirect("dashboard")

        return render(
            request,
            "login.html",
            {"error": "Invalid credentials"}
        )

    return render(request, "login.html")



def logout_view(request):

    logout(request)

    return redirect("login")


