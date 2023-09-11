from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    def __str__(self):
        return f"{self.username}"


class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"


class AuctionListing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    startingbid = models.IntegerField()
    imageurl = models.URLField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='sellingproduct')
    category = models.ForeignKey(
        Category, on_delete=models.DO_NOTHING, blank=True)
    watchedby = models.ManyToManyField(
        User, related_name='watchlist', blank='True')


class Bids(models.Model):
    amount = models.IntegerField()
