from django.contrib import admin

from .models import TelegramUser, Commands, Feedback

admin.site.register(TelegramUser)
admin.site.register(Commands)
admin.site.register(Feedback)