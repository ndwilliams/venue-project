from rest_framework import viewsets, status
from rest_framework import serializers
from rest_framework.response import Response
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'username', 'is_staff', 
                  'is_superuser'] 
        
class UserViewSet(viewsets.ViewSet):

    def list(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True, context={'request': request})
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    def update(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)

            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                user.first_name = serializer.validated_data['first_name']
                user.first_name = serializer.validated_data['last_name']
                user.email = serializer.validated_data['email']
                user.username = serializer.validated_data['username']
                user.is_staff = serializer.validated_data['is_staff']
                user.is_superuser = serializer.validated_data['is_superuser']
                user.save()

                updated_serializer = UserSerializer(user, context={'request': request})
                return Response(updated_serializer.data, status.HTTP_200_OK)
            
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)