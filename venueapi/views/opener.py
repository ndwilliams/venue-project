from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from venueapi.models import Opener, Band, Concert

class OpenerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Opener
        fields = ['id', 'concert', 'band']

class OpenerViewSet(ViewSet):
    
    def list(self, request):
        openers = Opener.objects.all()
        serializer = OpenerSerializer(openers, many=True, context={'request': request})
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        try:
            opener = Opener.objects.get(pk=pk)
            serializer = OpenerSerializer(opener, context={'request': request})
            return Response(serializer.data)
        except Opener.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    def create(self, request):
        concert = Concert.objects.get(pk=request.data['concert'])
        band = Band.objects.get(pk=request.data['band'])

        opener = Opener.objects.create(
            concert = concert,
            band = band
        )
        opener.save()

        try:
            serializer = OpenerSerializer(opener, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response(None, status=status.HTTP_404_NOT_FOUND)
        
    def destroy(self, request, pk=None):
        try:
            opener = Opener.objects.get(pk=pk)
            opener.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        
        except Opener.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)