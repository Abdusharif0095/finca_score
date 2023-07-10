from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseAdmin
from .models import User
from .forms import UserChangeForm


class UserAdmin(BaseAdmin):
    form = UserChangeForm


admin.site.register(User, UserAdmin)
