from django.contrib import admin
from .models import *

admin.site.register(Bid)
admin.site.register(User)
admin.site.register(AuctionListing)
admin.site.register(Category)

# Register your models here.
