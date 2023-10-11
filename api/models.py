from django.contrib.auth.models import User
from django.db import models

class Narrative(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    _id = models.AutoField(primary_key=True, editable=False)
    image = models.ImageField(null=True, blank=True, default='/placeholder.png')

    def __str__(self):
        return self.title
