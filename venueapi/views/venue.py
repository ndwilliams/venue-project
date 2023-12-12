from rest_framework import viewsets, status, serializers
from rest_framework.response import Response
from venueapi.models import Venue

class VenueSerializer(serializers.ModelSerializer):

    class Meta:
        model = Venue
        fields = ['id', 'venue_outside_image_url', 'venue_inside_image_url',
                   'name', 'address', 'capacity', 'about_section', 'active']

class VenueViewSet(viewsets.ViewSet):

    def list(self, request):
        venues = Venue.objects.all()
        serializer = VenueSerializer(venues, many=True, context={'request': request})
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        try:
            venue = Venue.objects.get(pk=pk)
            serializer = VenueSerializer(venue, context={'request': request})
            return Response(serializer.data)
        except Venue.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    def create(self,request):

        venue_outside_image_url = request.data.get('venue_outside_image_url')
        venue_inside_image_url = request.data.get('venue_inside_image_url')
        name = request.data.get('name')
        address = request.data.get('address')
        capacity = request.data.get('capacity')
        about_section = request.data.get('about_section')
        active = request.data.get('active')

        venue = Venue.objects.create(
            venue_inside_image_url=venue_inside_image_url,
            venue_outside_image_url=venue_outside_image_url,
            name=name,
            address=address,
            capacity=capacity,
            about_section=about_section,
            active=active
        )

        venue.save()

        try:
            serializer = VenueSerializer(venue, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response(None, status=status.HTTP_404_NOT_FOUND)
        
    def update(self, request, pk=None):
        try:
            venue = Venue.objects.get(pk=pk)
            serializer = VenueSerializer(venue, data=request.data)
            if serializer.is_valid():
                venue.venue_inside_image_url = serializer.validated_data['venue_inside_image_url']
                venue.venue_outside_image_url = serializer.validated_data['venue_outside_image_url']
                venue.name = serializer.validated_data['name']
                venue.address = serializer.validated_data['address']
                venue.capacity = serializer.validated_data['capacity']
                venue.about_section = serializer.validated_data['about_section']
                venue.active = serializer.validated_data['active']
                venue.save()

                serializer = VenueSerializer(venue, context={'request': request})
                return Response(None, status.HTTP_204_NO_CONTENT)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Venue.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)