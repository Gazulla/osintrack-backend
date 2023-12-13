from django.urls import path
from api.views import telegram_views as views

urlpatterns = [
    path("groups/check/", views.checkTelegramGroup, name="check-telegram-group"),
    path("connect/", views.connectTelegram, name="connect-telegram"),
    path("inputphonecode/", views.inputPhoneCodeTelegram, name="input-phone-code-telegram"),
    path("disconnect/", views.disconnectTelegram, name="disconnect-telegram"),
    path("checksession/", views.checkTelegramSession, name="check-telegram-session"),
]