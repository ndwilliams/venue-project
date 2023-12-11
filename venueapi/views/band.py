from rest_framework import viewsets, status
from rest_framework import serializers
from rest_framework.response import Response
from venueapi.models import Band

class BandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Band
        fields = ['id', 'name', 'genre']

class BandViewSet(viewsets.ViewSet):

    def list(self, request):
        bands = Band.objects.all()
        serializer = BandSerializer(bands, many=True, context={'request': request})
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        try:
            band = Band.objects.get(pk=pk)
            serializer = BandSerializer(band)
            return Response(serializer.data)
        except Band.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    def create(self, request):

        band = Band()
        band.name = request.data.get('name')
        band.genre = request.data.get('genre')
        band.save()

        try:
            serializer = BandSerializer(band, many=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response(None, status=status.HTTP_404_NOT_FOUND)

