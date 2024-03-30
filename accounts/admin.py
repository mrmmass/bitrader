from django.contrib import admin
from .models import User   , UserProfile
from django.contrib.sessions.models import Session


# Register your models here.


admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(Session)
