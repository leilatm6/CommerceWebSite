from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    def __str__(self):
        return f"{self.username}"


class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"


class Bid(models.Model):
    initialbid = models.IntegerField()
    numberofbids = models.IntegerField(default=0)
    lastbid = models.IntegerField(default=0)
    biddatetime = models.DateTimeField(null=True)
    lastbiduser = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="activebids", null=True)


class AuctionListing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    bid = models.ForeignKey(Bid, on_delete=models.CASCADE,
                            related_name='lastuser')
    imageurl = models.URLField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='sellingproduct')
    """category = models.ForeignKey(
        Category, on_delete=models.DO_NOTHING, blank=True)"""
    watchedby = models.ManyToManyField(
        User, related_name='watchlist', blank='True')

    def __str__(self):
        return f"{self.title}: {self.description} with price {self.bid.initialbid} and user {self.user}"
