from django.contrib.auth.models import User
from django.db import models

class AppSettings(models.Model):
    telegramApiId = models.CharField(max_length=50, null=True, blank=True)
    telegramApiHash = models.CharField(max_length=100, null=True, blank=True)
    telegramPhone = models.CharField(max_length=100, null=True, blank=True)
    def __str__(self):
        return "app-settings"

class TelegramGroup(models.Model):
    name = models.CharField(max_length=100, unique=True)
    telegramId = models.IntegerField(blank=False, null=False, unique=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    _id = models.AutoField(primary_key=True, editable=False)
    addedAt = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(null=True, blank=True, default='/placeholder.png')
    parse= models.BooleanField(default=True)
    def __str__(self):
        return self.title

class TelegramGroupSnapshot(models.Model):
    telegramGroup = models.ForeignKey(TelegramGroup, on_delete=models.CASCADE, null=True, related_name='telegram_group_snapshots')
    title = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    _id = models.AutoField(primary_key=True, editable=False)
    snapshotDate = models.DateTimeField(auto_now_add=True)
    subs = models.IntegerField(blank=True, null=True)
    numMessages = models.IntegerField(blank=True, null=True)
    def __str__(self):
        return str(self.snapshotDate)

class TelegramMessage(models.Model):
    telegramGroup = models.ForeignKey(TelegramGroup, on_delete=models.CASCADE, null=True, related_name='telegram_group_messages')
    _id = models.AutoField(primary_key=True, editable=False)
    text = models.TextField(null=True, blank=True)
    hasImage = models.BooleanField(default=False)
    hasVideo = models.BooleanField(default=False)
    image = models.ImageField(null=True, blank=True, default='/placeholder.png')
    def __str__(self):
        return self._id

class TelegramMessageSnapshot(models.Model):
    telegramMessage = models.ForeignKey(TelegramMessage, on_delete=models.CASCADE, null=True, related_name='telegram_message_snapshots')
    _id = models.AutoField(primary_key=True, editable=False)
    snapshotDate = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(blank=True, null=True)
    # reactions = TO DO
    def __str__(self):
        return self.snapshotDate

class Narrative(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    _id = models.AutoField(primary_key=True, editable=False)
    image = models.ImageField(null=True, blank=True, default='/placeholder.png')
    telegramGroups = models.ManyToManyField(TelegramGroup, related_name="telegram_groups", blank=True)
    def __str__(self):
        return self.title

class UserData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='user_data')
    image = models.ImageField(null=True, blank=True, default='/placeholder.png')
    _id = models.AutoField(primary_key=True, editable=False)