from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from venueapi.models import Concert, Venue, Band
from django.contrib.auth.models import User


class ConcertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Concert
        fields = ['id', 'venue', 'band', 'doors_open',
                   'show_starts', 'active', 'opening_bands']
        
class ConcertViewSet(ViewSet):
    def list(self, request):
        concerts = Concert.objects.all()
        serializer = ConcertSerializer(concerts, many=True, context={'request': request})
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        try:
            concert = Concert.objects.get(pk=pk)
            serializer = ConcertSerializer(concert, context={'request': request})
            return Response(serializer.data)
        except Concert.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def create(self, request):
        venue = Venue.objects.get(pk=request.data['venue'])
        band = Band.objects.get(pk=request.data['band'])
        # opening_bands = OpenerSerializer(many=True)
        doors_open = request.data.get('doors_open')
        show_starts = request.data.get('show_starts')
        
        concert = Concert.objects.create(
            venue = venue,
            band = band,
            doors_open = doors_open,
            show_starts = show_starts,
            active = True
        )
        concert.save()

        try:
            serializer = ConcertSerializer(concert, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response(None, status=status.HTTP_404_NOT_FOUND)
        
    def update(self, request, pk=None):
        try:
            concert = Concert.objects.get(pk=pk)

            serializer = ConcertSerializer(data=request.data)
            if serializer.is_valid():
                concert.venue = serializer.validated_data['venue']
                concert.band = serializer.validated_data['band']
                concert.doors_open = serializer.validated_data['doors_open']
                concert.show_starts = serializer.validated_data['show_starts']
                concert.active = serializer.validated_data['active']
                # concert.opening_bands = serializer.validated_data['opening_bands']
                concert.save()

                updated_serializer = ConcertSerializer(concert, context={'request': request})
                return Response(updated_serializer.data, status.HTTP_200_OK)
            
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        
        except Concert.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


        

