from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from venueapi.models import Concert, Favorite
from django.contrib.auth.models import User

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields= ['id', 'concert_id', 'user_id']

class FavoriteViewSet(ViewSet):
    def list(self, request):
        favorites = Favorite.objects.all()
        serializer = FavoriteSerializer(favorites, many=True, context={'request': request})
        return Response(serializer.data)
    
    def create(self, request):
        user = User.objects.get(pk=request.user.id)
        concert = Concert.objects.get(pk=request.data['concert'])

        favorite = Favorite.objects.create(
            user = user,
            concert = concert
        )
        favorite.save()

        try:
            serializer = FavoriteSerializer(favorite, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as ex:
            return Response(None, status=status.HTTP_404_NOT_FOUND)
        
    def destroy(self, request, pk=None):
        try:
            favorite = Favorite.objects.get(pk=pk)
            self.check_object_permissions(request, favorite)
            favorite.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        
        except Favorite.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)