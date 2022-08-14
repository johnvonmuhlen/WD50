from django.contrib import admin

from .models import Post, User

# Register your models here.

#class ListingAdmin(admin.ModelAdmin):
#    list_display = ("id", "title", "owner", "current_bid")
#    filter_horizontal = ("category", )
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "email")

class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "likes", "total_comments", "content")



# Register your models here.
admin.site.register(Post, PostAdmin)
admin.site.register(User, UserAdmin)
