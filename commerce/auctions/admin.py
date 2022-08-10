from django.contrib import admin
from .models import User, Listing, Bid, Comment, Categorie

class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "owner", "current_bid")
    filter_horizontal = ("category", )
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "date_joined", "last_login")
    



# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Categorie)