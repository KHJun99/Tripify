from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """사용자 정보 Serializer"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile_image', 'preferred_region', 
                  'travel_style', 'created_at']
        read_only_fields = ['id', 'created_at']


class SignupSerializer(serializers.ModelSerializer):
    """회원가입 Serializer"""
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'password_confirm', 'email', 
                  'preferred_region', 'travel_style']

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "비밀번호가 일치하지 않습니다."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    """로그인 Serializer"""
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)


class PasswordResetRequestSerializer(serializers.Serializer):
    """비밀번호 재설정 요청 Serializer"""
    email = serializers.EmailField(required=True)


class PasswordResetConfirmSerializer(serializers.Serializer):
    """비밀번호 재설정 확인 Serializer"""
    token = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({"new_password": "비밀번호가 일치하지 않습니다."})
        return attrs


class UsernameRecoverySerializer(serializers.Serializer):
    """아이디 찾기 Serializer"""
    email = serializers.EmailField(required=True)
