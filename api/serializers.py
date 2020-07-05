
from rest_framework import serializers
from rest_framework.serializers import (
    ModelSerializer, PrimaryKeyRelatedField,
    SerializerMethodField
)
from books.models import *
from django.contrib.auth.models import User, Permission
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token



class UserSerializer(ModelSerializer):
    """ serializer for User
    """
    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    default_error_messages = {
        'inactive_account': 'User account is disabled.',
        'invalid_credentials': 'Unable to login with provided credentials.'
    }

    def __init__(self, *args, **kwargs):
        super(UserLoginSerializer, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self, attrs):
        self.user = authenticate(username=attrs.get("username"), password=attrs.get('password'))
        if self.user:
            if not self.user.is_active:
                raise serializers.ValidationError(self.error_messages['inactive_account'])
            return attrs
        else:
            raise serializers.ValidationError(self.error_messages['invalid_credentials'])


class TokenSerializer(serializers.ModelSerializer):
    auth_token = serializers.CharField(source='key')

    class Meta:
        model = Token
        fields = ("auth_token", "created")

class BookSerializer(ModelSerializer):
    """ serializer for book
    """
    class Meta:
        model = Book
        fields = ('name', 'author', 'image')



class BorrowBookSerializer(ModelSerializer):

    class Meta:
        model = BorrowedBook
        fields = ('book', 'date')