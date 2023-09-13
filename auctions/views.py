from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Category, AuctionListing, Bid
from datetime import datetime


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
        print(request.POST)
        if not request.user.is_authenticated:
            return render(request, "auctions/login.html")
        if request.POST["title"] == '' or request.POST["description"] == '' or request.POST["initialbid"] == '':

            return render(request, "auctions/newlist.html", {
                #  'categories': Category,
                'message': "Please Fill all mandatory Fields"
            })

        title = request.POST["title"]
        description = request.POST["description"]
        biddatetime = datetime.now()
        initial_bid = Bid(
            initialbid=request.POST["initialbid"], biddatetime=biddatetime)
        initial_bid.save()
        photo = request.POST["photo"]
        # print(title, description, initial_bid, photo)
        newlist = AuctionListing(
            title=title, description=description, bid=initial_bid, imageurl=photo, user=request.user)
        newlist.save()
        return HttpResponseRedirect(reverse('index'))
    return render(request, "auctions/newlist.html", {
        # 'categories': Category
    })


def list(request, listid):
    list = AuctionListing.objects.get(pk=listid)
    messageforbid = "The amount shoud be more than {list.bid.lastbid}" if list.bid.numberofbids > 0 else "The amount shoud be more than or equal{list.bid.initialbid}"
    if not list:
        return print('????????????????????')
    if request.method == "POST":
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("login"))
        if "addremovebutton" in request.POST:
            if request.user in list.watchedby.all():
                list.watchedby.remove(request.user)
                return render(request, "auctions/list.html", {
                    "list": list,
                })
            list.watchedby.add(request.user)

            return render(request, "auctions/list.html", {
                "list": list,
                #   "watchlist": 'True'
            })
        if "bidbutton" in request.POST:
            newbid = float(request.POST["bidinput"])
            if list.bid.numberofbids == 0:
                if newbid < list.bid.initialbid:
                    return render(request, "auctions/list.html", {
                        "list": list,
                        "message": "The bid should not be less than starting bid"
                    })
            elif newbid <= list.bid.lastbid:
                return render(request, "auctions/list.html", {
                    "list": list,
                    "message": "The bid should  be greate than current bid"
                })
            list.bid.lastbid = newbid
            list.bid.numberofbids += 1
            list.bid.lastbiduser = request.user
            list.bid.save()
            return render(request, "auctions/list.html", {
                "list": list,
            })

    if request.user.is_authenticated and list in request.user.watchlist.all():
        return render(request, "auctions/list.html", {
            "list": list,
            # "watchlist": True,

        })
    return render(request, "auctions/list.html", {
        "list": list,

    })
