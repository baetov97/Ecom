from django.urls import reverse
from rest_framework import serializers
from django.contrib import auth
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from ..models import User
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework_simplejwt.serializers import (
    login_rule, user_eligible_for_login,
    PasswordField, TokenRefreshSerializer as BaseRefreshSerializer
)
from rest_framework.exceptions import (
    AuthenticationFailed,
    ValidationError
)
from rest_framework_simplejwt.settings import api_settings
from django.utils.translation import gettext_lazy as _


class TokenPairObtainSerializer(serializers.Serializer):
    default_error_messages = {
        'no_active_account': _('No active account found with the given credentials')
    }
    email = serializers.EmailField(required=False)
    password = PasswordField()

    def update(self, instance, validated_data):
        raise NotImplementedError

    def create(self, validated_data):
        raise NotImplementedError

    # TODO: Add additional claims
    @classmethod
    def get_token(cls, user):
        token = RefreshToken.for_user(user)
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['username'] = user.email
        return token

    def validate(self, attrs):
        email = attrs.get('email')
        if not email:
            raise ValidationError(
                _('Provide at least phone or email')
            )
        password = attrs.get('password')
        request = self.context.get('request')
        user = authenticate(
            request=request,
            email=email,
            password=password
        )
        if not getattr(login_rule, user_eligible_for_login)(user):
            raise AuthenticationFailed(
                self.error_messages['no_active_account'],
                'no_active_account',
            )
        refresh = self.get_token(user)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, user)
        return data


class TokenRefreshSerializer(BaseRefreshSerializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')

        if not username.isalnum():
            raise serializers.ValidationError("The should only contain alphanumeric characters")
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']

    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    username = serializers.CharField(max_length=255, min_length=3, read_only=True)
    tokens = serializers.SerializerMethodField('get_tokens')

    def get_tokens(self, obj):
        user = User.objects.get(email=obj['email'])
        return {
            'access': user.tokens()['access'],
            'refresh': user.tokens()['refresh']
        }

    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        user = auth.authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        if not user.is_active:
            raise AuthenticationFailed('Email is not verified')
        return {'email': user.email, 'username': user.username, 'tokens': user.tokens()}


class ResetPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)
    redirect_url = serializers.CharField(max_length=500, required=False)

    class Meta:
        fields = ['email']


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = urlsafe_base64_decode(uidb64)
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)
            user.set_password(password)
            user.save()
        except DjangoUnicodeDecodeError:
            raise AuthenticationFailed('The reset link is invalid', 401)
        return super().validate(attrs)
