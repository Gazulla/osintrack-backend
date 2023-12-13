from rest_framework import status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models import AppSettings
from ..services.telegram import getTelegramGroup, checkTelegramConnection, connectTelegramRequest, connectTelegramInputCode, logOutTelegram

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def checkTelegramGroup(request):
    try:
        data = request.data
        groupIdentifier = data["telegramGroupIdentifier"]
        phone = '34636868168'
        appSettings = AppSettings.objects.all()
        settings = appSettings[0]
        apiId = int(settings.telegramApiId)
        apiHash = settings.telegramApiHash
        disconnectTelegram(apiId,apiHash)
        #getTelegramGroup(groupIdentifier,apiId,apiHash)
        #connectTelegramRequest(apiId,apiHash,phone)
        #group = Narrative.objects.get()
        #connectTelegramInputCode(apiId,apiHash,phone,code=90527,phone_code_hash='4c7a327afcfeac00a4')
        #checkTelegramConnection(apiId,apiHash)
        return Response("no Fail")
    except: 
        message = {"detail": "Error checking Telegram group."}
        return Response(message, status=status.HTTP_404_NOT_FOUND)
    

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def connectTelegram(request):
    try:
        data = request.data
        apiId = int(data["telegramApiId"])
        apiHash = data["telegramApiHash"]
        phone = data["telegramPhone"]
        result =  connectTelegramRequest(apiId,apiHash,phone)
        if result["success"]:
           return Response(result["detail"], status=status.HTTP_200_OK)
        else:
           return Response(result["detail"], status=status.HTTP_400_BAD_REQUEST)
    except Exception as exc:
        message = {"detail": "Error connecting to Telegram."}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def inputPhoneCodeTelegram(request):
    try:
        data = request.data
        apiId = int(data["telegramApiId"])
        apiHash = data["telegramApiHash"]
        phone = data["telegramPhone"]
        code = data["code"]
        phone_code_hash = data["phoneCodeHash"]
        result = connectTelegramInputCode(apiId,apiHash,phone,code,phone_code_hash)
        if result["success"]:
           return Response(result, status=status.HTTP_200_OK)
        else:
           return Response(result, status=status.HTTP_400_BAD_REQUEST)
    except: 
        message = {"detail": "Error sending the verification code."}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def disconnectTelegram(request):
    try:
        appSettings = AppSettings.objects.all()
        settings = appSettings[0]
        apiId = int(settings.telegramApiId)
        apiHash = settings.telegramApiHash
        logOutTelegram(apiId,apiHash)
        return Response("Disconnected!")
    except Exception as exc:
        message = {"detail": "Error disconnecting to Telegram."}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def checkTelegramSession(request):
    try:
        appSettings = AppSettings.objects.all()
        settings = appSettings[0]
        apiId = int(settings.telegramApiId)
        apiHash = settings.telegramApiHash
        connected = checkTelegramConnection(apiId,apiHash)
        return Response(connected)
    except Exception as exc:
        message = {"detail": "Error checking Telegram session."}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)