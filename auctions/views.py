from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Category, AuctionListing


def index(request):
    return render(request, "auctions/index.html", {
        "lists": AuctionListing.objects.all()
    })


def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def newlist(request):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return render(request, "auctions/login.html")
        if request.POST["title"] == '' or request.POST["description"] == '' or request.POST["intialbid"] == '':
            return render(request, "auctions/newlist.html", {
                #  'categories': Category,
                'message': "Please Fill all mandatory Fields"
            })

        title = request.POST["title"]
        description = request.POST["description"]
        initial_bid = request.POST["intialbid"]
        photo = request.POST["photo"]
        print(title, description, initial_bid, photo)
        newlist = AuctionListing(
            title=title, description=description, startingbid=initial_bid, imageurl=photo, user=request.user)
        print(newlist)
        newlist.save()
        return HttpResponseRedirect(reverse('index'))
    return render(request, "auctions/newlist.html", {
        # 'categories': Category
    })
