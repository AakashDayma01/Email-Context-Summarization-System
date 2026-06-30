from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=email,
            password=password,
        )

        if user:
            login(request, user)
            return redirect("dashboard")

        return render(
            request,
            "login.html",
            {"error": "Invalid email or password"},
        )

    return render(request, "login.html")

def logout_view(request):
    """
    Log out the currently authenticated user.

    This view terminates the user's session and redirects
    them to the login page.
    """
    logout(request)
    return redirect("login")