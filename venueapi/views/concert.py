from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from venueapi.models import Concert, Favorite, Venue, Band
from venueapi.views.opener import OpenerSerializer
from venueapi.views.band import BandSerializer
from venueapi.views.venue import VenueSerializer
from django.contrib.auth.models import User


class ConcertSerializer(serializers.ModelSerializer):
    opening_bands = BandSerializer(many=True)
    band = BandSerializer(many=False)
    venue = VenueSerializer(many=False)
    current_user_is_favorited = serializers.SerializerMethodField()

    def get_current_user_is_favorited(self, obj):
        # get the current user id through the request
        current_user_id = self.context['request'].user.id

        # Check the Users who have Favorited each Concert through related_name
        user_favorite = obj.users_who_favorited.filter(id=current_user_id)

        if user_favorite.exists():
            return True
        else:
            return False

    class Meta:
        model = Concert
        fields = ['id', 'venue', 'band', 'doors_open',
                   'show_starts', 'active', 'opening_bands', 'current_user_is_favorited']
        
class ConcertViewSet(ViewSet):
    def list(self, request):
        concerts = Concert.objects.order_by('show_starts').all()
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
        doors_open = request.data.get('doors_open')
        show_starts = request.data.get('show_starts')
        
        concert = Concert.objects.create(
            venue = venue,
            band = band,
            doors_open = doors_open,
            show_starts = show_starts,
            active = True
        )

        opener_ids = request.data.get('opening_bands', [])
        concert.opening_bands.set(opener_ids)

        try:
            serializer = ConcertSerializer(concert, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response(None, status=status.HTTP_404_NOT_FOUND)
        
    def update(self, request, pk=None):
        try:
            concert = Concert.objects.get(pk=pk)
            band = Band.objects.get(pk=request.data['band'])
            venue= Venue.objects.get(pk=request.data['venue'])

            concert.venue = venue
            concert.band = band
            concert.doors_open = request.data.get('doors_open')
            concert.show_starts = request.data.get('show_starts')
            concert.active = request.data.get('active')
            concert.save()

            opener_ids = request.data.get('opening_bands', [])
            concert.opening_bands.set(opener_ids)

            updated_serializer = ConcertSerializer(concert, context={'request': request})
            return Response(updated_serializer.data, status.HTTP_200_OK)
            
                    
        except Concert.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


        

