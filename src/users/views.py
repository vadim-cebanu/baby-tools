from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from .forms import LoginForm, RegisterForm


def user_register(request: HttpRequest) -> HttpResponse:
    """Handle user registration.

    Args:
        request: The current HTTP request.

    Returns:
        HttpResponse: The registration page, or a redirect to the
        login page after a successful registration.
    """
    if request.method == "POST":
        form: RegisterForm = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})


def user_login(request: HttpRequest) -> HttpResponse:
    """Handle user login.

    Args:
        request: The current HTTP request.

    Returns:
        HttpResponse: The login page, or a redirect to the home page
        after a successful login.
    """
    if request.method == "POST":
        form: LoginForm = LoginForm(request.POST)
        if form.is_valid():
            username: str = form.cleaned_data["username"]
            password: str = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect("/")
                messages.info(request, "User is not active")
            else:
                messages.info(
                    request,
                    "Something went wrong, maybe check your provided " "credentials or try again.",
                )
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})


def user_logout(request: HttpRequest) -> HttpResponse:
    """Log out the current user.

    Args:
        request: The current HTTP request.

    Returns:
        HttpResponse: A redirect to the home page.
    """
    logout(request)
    return redirect("/")
