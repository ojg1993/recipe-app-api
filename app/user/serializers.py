from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name']
        # Validate fields as below ->  returns 400 if doens't meet criteria
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        # Create and return a user with encrypted password
        return get_user_model().objects.create_user(**validated_data)


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email, # Using email as username
            password=password
        )
        if not user:
            msg = _('Unable to log in with provided credentials.')
            # Returning 400 bad request error
            raise serializers.ValidationError(msg, code='authorization')
        attrs['user'] = user
        return attrs