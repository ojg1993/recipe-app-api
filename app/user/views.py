from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user import serializers



class CreateUserView(generics.CreateAPIView):
    # Create a new user
    serializer_class = serializers.UserSerializer


class CreateTokenView(ObtainAuthToken):
    # Create a new auth token for user
    serializer_class = serializers.AuthTokenSerializer
    # Add this view to the browsable api
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES