import re

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password

from ..models import UserData
from ..serializers import UserProfileSerializer

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getProfile(request):
    user = request.user
    try:
        serializer = UserProfileSerializer(user, many=False, context={'request': request})
        return Response(serializer.data)
    except: 
        message = {"detail": "User profile not found."}
        return Response(message, status=status.HTTP_404_NOT_FOUND)
    
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def updateProfile(request):
    user = request.user
    data = request.data
    try:
        firstName = data["firstName"].strip()
        lastName = data["lastName"].strip()
        email = data["email"].strip()
        
        if len(firstName) > 50:
            return Response({"detail": "First name is too long (max length 50 characters)"}, status=status.HTTP_400_BAD_REQUEST)
        if len(lastName) > 50:
            return Response({"detail": "Last name is too long (max length 50 characters)"}, status=status.HTTP_400_BAD_REQUEST)
        if len(email) > 100:
            return Response({"detail": "Email is too long (max length 100 characters)"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Email regular expression
        regexp = re.compile("^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$")
        if not regexp.match(email):
            return Response({"detail": "Invalid email format"}, status=status.HTTP_400_BAD_REQUEST)
        
        user.first_name = firstName
        user.last_name = lastName
        user.email = email
        user.save()
        serializer = UserProfileSerializer(user, many=False, context={'request': request})
        return Response(serializer.data)
    except Exception as exc:

        message = {"detail": "Unable to update password."}
        return Response(message, status=status.HTTP_404_NOT_FOUND)

@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def updateProfileImage(request):
    user = request.user
    image = request.FILES.get('image')
    try:
        userData = UserData.objects.get(user=user)
        if (image):
            userData.image = image
        userData.save()     
        serializer = UserProfileSerializer(user, many=False, context={'request': request})
        return Response(serializer.data)
    except:
        message = {"detail": "Unable to update profile picture."}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)

@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def updatePassword(request):
    user = request.user
    data = request.data
    try:
        oldPassword = data["oldPassword"].strip()
        newPassword = data["newPassword"].strip()
        newPasswordConfirm = data["newPasswordConfirm"].strip()
        
        if oldPassword == "":
            return Response({"detail": "Old password cannot be empty"}, status=status.HTTP_400_BAD_REQUEST)
        if not user.check_password(oldPassword):
            return Response({"detail": "Old password is not correct"}, status=status.HTTP_400_BAD_REQUEST)
        if newPassword == "":
            return Response({"detail": "New password cannot be empty"}, status=status.HTTP_400_BAD_REQUEST)
        if newPassword != newPasswordConfirm:
            return Response({"detail": "Password confirmation does not match"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Minimum eight characters, at least one uppercase letter, one lowercase letter and one number
        regexp = re.compile("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$")
        if not regexp.match(newPassword):
            return Response({"detail": "New password must have a minimum of eight characters, at least one uppercase letter, one lowercase letter and one number"}, status=status.HTTP_400_BAD_REQUEST)

        user.password = make_password(newPassword)
        user.save()
        return Response({"detail": "Password successfully updated"}, status=status.HTTP_200_OK)
    except Exception as exc:

        message = {"detail": "Unable to update password."}
        return Response(message, status=status.HTTP_404_NOT_FOUND)   