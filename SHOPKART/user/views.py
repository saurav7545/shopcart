from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import UserProfile
from django.contrib.auth.decorators import login_required


@login_required
def profile(request):

    profile, _ = UserProfile.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":

        request.user.email = request.POST.get(
            "email"
        )

        request.user.save()

        profile.phone = request.POST.get(
            "phone"
        )

        profile.address = request.POST.get(
            "address"
        )

        profile.city = request.POST.get(
            "city"
        )

        profile.state = request.POST.get(
            "state"
        )

        profile.pincode = request.POST.get(
            "pincode"
        )

        profile.save()

        messages.success(
            request,
            "Profile updated successfully."
        )

        return redirect("profile")

    return render(
        request,
        "profile.html",
        {
            "profile": profile
        }
    )


def register(request):

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")


        # Empty field check
        if not username or not email or not password or not confirm_password:

            messages.error(
                request,
                "All fields are required."
            )

            return redirect("register")


        # Password match
        if password != confirm_password:

            messages.error(
                request,
                "Passwords do not match."
            )

            return redirect("register")


        # Username already exists
        if User.objects.filter(username=username).exists():

            messages.error(
                request,
                "Username already exists."
            )

            return redirect("register")


        # Email already exists
        if User.objects.filter(email=email).exists():

            messages.error(
                request,
                "Email already exists."
            )

            return redirect("register")


        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )


        messages.success(
            request,
            "Registration successful. Please login."
        )

        return redirect("login")


    return render(
        request,
        "register.html"
    )



def login_view(request):

    if request.user.is_authenticated:
        return redirect("home")


    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")


        user = authenticate(
            request,
            username=username,
            password=password
        )


        if user is not None:

            login(request, user)

            messages.success(
                request,
                f"Welcome {user.username}!"
            )

            return redirect("home")


        else:

            messages.error(
                request,
                "Invalid username or password."
            )

            return redirect("login")


    return render(
        request,
        "login.html"
    )



def logout_view(request):

    logout(request)

    messages.success(
        request,
        "You have been logged out."
    )

    return redirect("home")