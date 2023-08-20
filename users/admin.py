from django.contrib import admin

from users.models import User, CallbackToken

admin.site.register(User)
