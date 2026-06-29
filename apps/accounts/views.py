from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect


def login_view(request):
    """
    Authenticate a user and create a new login session.

    For POST requests, the submitted email and password are validated
    using Django's authentication system. On successful authentication,
    the user is redirected to the dashboard. If authentication fails,
    the login page is re-rendered with an error message.

    For GET requests, the login page is displayed.
    """
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
    """
    Log out the currently authenticated user.

    This view terminates the user's session and redirects
    them to the login page.
    """
    logout(request)
    return redirect("login")