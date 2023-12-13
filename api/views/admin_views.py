from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from ..models import AppSettings
from ..serializers import AppSettingsSerializer

@api_view(["GET"])
@permission_classes([IsAuthenticated, IsAdminUser])
def getAppSettings(request):
    appSettings = AppSettings.objects.all()
    if len(appSettings) == 0:
         settings = AppSettings.objects.create(
            telegramApiId = "",
            telegramApiHash = "",
            telegramPhone = "")
    else:
         settings = appSettings[0]
    serializer = AppSettingsSerializer(settings, many=False)
    return Response(serializer.data)

@api_view(["PUT"])
@permission_classes([IsAuthenticated, IsAdminUser])
def updateAppSettings(request):
    data = request.data

    try:
        settings = AppSettings.objects.all()[0]
        settings.telegramApiId = data["telegramApiId"]
        settings.telegramApiHash = data["telegramApiHash"]
        settings.telegramPhone = data["telegramPhone"]
        settings.save()     
        serializer = AppSettingsSerializer(settings, many=False)
        return Response(serializer.data)
    except:
        message = {"detail": "Could not update settings."}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)