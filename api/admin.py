from django.contrib import admin
from .models import *

admin.site.register(Narrative)
admin.site.register(TelegramGroup)
admin.site.register(TelegramGroupSnapshot)
admin.site.register(TelegramMessage)
admin.site.register(TelegramMessageSnapshot)
admin.site.register(UserData)