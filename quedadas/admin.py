from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Meeting, Friendship, Tracking, RoutePoint, Statistics, Zone
from .models import Profile


# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'employee'


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


# Define a new User admin
class RouteAdminInline(admin.TabularInline):
    model = RoutePoint


class TrackingPoint(admin.ModelAdmin):
    inlines = (RouteAdminInline,)


admin.site.register(Tracking, TrackingPoint)

admin.site.register(Meeting)
admin.site.register(Friendship)
admin.site.register(Statistics)
admin.site.register(Zone)