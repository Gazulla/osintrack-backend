from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models import Narrative
from ..serializers import NarrativeSerializer

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getNarratives(request):
    narratives = Narrative.objects.all()
    serializer = NarrativeSerializer(narratives, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getNarrative(request, pk):
    try:
        narrative = Narrative.objects.get(_id=pk)
        serializer = NarrativeSerializer(narrative, many=False, context={'request': request})
        return Response(serializer.data)
    except: 
        message = {"detail": "Narrative not found."}
        return Response(message, status=status.HTTP_404_NOT_FOUND)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def createNarrative(request):
    data = request.data
    user = request.user
    image = request.FILES.get('image')
    try:
        narrative = Narrative.objects.create(
            title = data["title"],
            description = data["description"],
            image = image if image else "/placeholder.png",
            user = user)
        serializer = NarrativeSerializer(narrative, many=False, context={'request': request})
        return Response(serializer.data)
    except:
        message = {"detail": "Could not create a new narrative."}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def updateNarrative(request, pk):
    data = request.data
    user = request.user
    image = request.FILES.get('image')
    try:
        narrative = Narrative.objects.get(_id=pk)
        narrative.title = data["title"]
        narrative.description = data["description"]
        if (image):
            narrative.image = image
        narrative.user = user
        narrative.save()     
        serializer = NarrativeSerializer(narrative, many=False, context={'request': request})
        return Response(serializer.data)
    except:
        message = {"detail": "Could not update the selected narrative."}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def deleteNarrative(request, pk):
    try:
        narrative = Narrative.objects.get(_id=pk)
        deletedId = pk
        narrative.delete()     
        return Response(deletedId)
    except:
        message = {"detail": "Could not delete the selected narrative."}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)