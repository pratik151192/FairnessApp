from django.contrib import admin
from .models import UserProfile, UserValues, Robots
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(UserValues)
admin.site.register(Robots)