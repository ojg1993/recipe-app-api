from rest_framework import generics
from user import serializers


class CreateUserView(generics.CreateAPIView):
    # Create a new user
    serializer_class = serializers.UserSerializer
