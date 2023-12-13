from rest_framework import serializers
from django.contrib.auth.models import User
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Narrative, AppSettings, UserData

class AppSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppSettings
        fields = ['telegramApiId', 'telegramApiHash', 'telegramPhone']

class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = ['_id', 'image']

class UserProfileSerializer(serializers.ModelSerializer):
    _id = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)
    firstName = serializers.SerializerMethodField(read_only=True)
    lastName = serializers.SerializerMethodField(read_only=True)
    dateJoined = serializers.SerializerMethodField(read_only=True)
    image = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ["id", "_id", "username", "firstName", "lastName", "email", "isAdmin", "dateJoined", "image"]
    
    def get_isAdmin(self, obj):
        return obj.is_staff

    def get__id(self, obj):
        return obj.id
    
    def get_firstName(self, obj):
        return obj.first_name
    
    def get_lastName(self, obj):
        return obj.last_name
    
    def get_dateJoined(self, obj):
        return obj.date_joined
    
    def get_image(self, obj):
        img = UserData.objects.filter(user=obj)[0].image
        request = self.context.get('request')
        full_url = ''.join(['http://', request.META['HTTP_HOST'],settings.MEDIA_URL, str(img)])
        return full_url
    
class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    _id = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = User
        fields = ["id", "_id", "username","email", "name", "isAdmin", "date_joined"]
 
    def get_isAdmin(self, obj):
        return obj.is_staff

    def get__id(self, obj):
        return obj.id

    def get_name(self, obj):
        name = obj.first_name
        if name == "":
            name = obj.email
        return name


class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = ["id", "_id", "username", "isAdmin", "token"]

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)

class NarrativeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Narrative
        fields = ['_id', 'title', 'description', 'image', 'createdAt']