from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """사용자 정보 Serializer"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'nickname', 'profile_image', 'preferred_region',
                  'travel_style', 'login_type', 'created_at']
        read_only_fields = ['id', 'login_type', 'created_at']


class SignupSerializer(serializers.ModelSerializer):
    """회원가입 Serializer"""
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'password_confirm', 'email', 'nickname',
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
        
        # 토큰으로 사용자 찾기
        from .models import PasswordResetToken
        from django.contrib.auth.hashers import check_password
        
        try:
            reset_token = PasswordResetToken.objects.get(token=attrs['token'])
            if reset_token.is_valid():
                user = reset_token.user
                
                # 새 비밀번호가 현재 비밀번호와 동일한지 확인
                if check_password(attrs['new_password'], user.password):
                    raise serializers.ValidationError({
                        "new_password": "새 비밀번호는 현재 비밀번호와 동일할 수 없습니다. 다른 비밀번호를 입력해주세요."
                    })
        except PasswordResetToken.DoesNotExist:
            # 토큰이 없어도 여기서는 에러를 발생시키지 않음 (나중에 views에서 처리)
            pass
        
        return attrs


class UsernameRecoverySerializer(serializers.Serializer):
    """아이디 찾기 Serializer"""
    email = serializers.EmailField(required=True)


class AccountDeletionSerializer(serializers.Serializer):
    """회원탈퇴 Serializer"""
    password = serializers.CharField(required=False, write_only=True)

    def validate_password(self, value):
        user = self.context['request'].user
        # 일반 로그인 사용자는 비밀번호 확인 필요
        if user.login_type == 'normal' and not user.check_password(value):
            raise serializers.ValidationError("비밀번호가 올바르지 않습니다.")
        return value


class PasswordChangeSerializer(serializers.Serializer):
    """비밀번호 변경 Serializer"""
    current_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(required=True, write_only=True)

    def validate_current_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("현재 비밀번호가 올바르지 않습니다.")
        return value

    def validate(self, attrs):
        user = self.context['request'].user
        
        # 사용자 확인
        if not user or not user.is_authenticated:
            raise serializers.ValidationError({
                "current_password": "인증된 사용자만 비밀번호를 변경할 수 있습니다."
            })
        
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({"new_password": "새 비밀번호가 일치하지 않습니다."})
        
        # 현재 비밀번호와 동일한지 확인
        from django.contrib.auth.hashers import check_password
        
        # 현재 비밀번호와 동일한지 확인 (2가지 방법으로 검증)
        
        # 방법 1: 사용자가 입력한 현재 비밀번호와 새 비밀번호 평문 비교
        # validate_current_password에서 이미 현재 비밀번호가 맞는지 확인했으므로,
        # current_password와 new_password가 같으면 동일한 비밀번호입니다.
        if attrs['current_password'] == attrs['new_password']:
            print(f"[비밀번호 검증] 평문 비교: 현재 비밀번호와 새 비밀번호가 동일함")
            raise serializers.ValidationError({
                "new_password": "새 비밀번호는 현재 비밀번호와 동일할 수 없습니다. 다른 비밀번호를 입력해주세요."
            })
        
        # 방법 2: 현재 로그인한 사용자의 비밀번호 해시와 새 비밀번호 비교
        # user.password는 현재 로그인한 사용자(request.user)의 비밀번호 해시입니다
        if check_password(attrs['new_password'], user.password):
            print(f"[비밀번호 검증] 해시 비교: 새 비밀번호가 현재 비밀번호 해시와 일치함")
            raise serializers.ValidationError({
                "new_password": "새 비밀번호는 현재 비밀번호와 동일할 수 없습니다. 다른 비밀번호를 입력해주세요."
            })
        
        print(f"[비밀번호 검증] 통과: 새 비밀번호가 현재 비밀번호와 다름")
        
        return attrs


class PasswordVerifySerializer(serializers.Serializer):
    """비밀번호 확인 Serializer"""
    password = serializers.CharField(required=True, write_only=True)

    def validate_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("비밀번호가 올바르지 않습니다.")
        return value
