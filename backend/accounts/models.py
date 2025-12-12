from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import secrets
import hashlib


class User(AbstractUser):
    """커스텀 사용자 모델"""
    email = models.EmailField(unique=True)
    profile_image = models.ImageField(upload_to='profiles/', null=True, blank=True)
    preferred_region = models.CharField(max_length=100, blank=True, help_text="선호 지역")
    travel_style = models.CharField(max_length=100, blank=True, help_text="여행 스타일")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # 소셜 로그인 관련 필드
    kakao_id = models.CharField(max_length=100, unique=True, null=True, blank=True, help_text="카카오 고유 ID")
    google_id = models.CharField(max_length=100, unique=True, null=True, blank=True, help_text="구글 고유 ID")
    login_type = models.CharField(max_length=20, default='normal', choices=[
        ('normal', 'Normal'),
        ('kakao', 'Kakao'),
        ('google', 'Google'),
    ], help_text="로그인 타입")

    # 이메일 인증 관련 필드
    is_email_verified = models.BooleanField(default=False, help_text="이메일 인증 여부")

    class Meta:
        db_table = 'users'
        ordering = ['-created_at']

    def __str__(self):
        return self.username


class EmailVerificationToken(models.Model):
    """이메일 인증 토큰"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='email_verification_tokens')
    token = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    class Meta:
        db_table = 'email_verification_tokens'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.token[:8]}..."

    @classmethod
    def create_token(cls, user):
        """새로운 인증 토큰 생성"""
        from django.conf import settings
        from datetime import timedelta

        # 기존 미사용 토큰 삭제
        cls.objects.filter(user=user, is_used=False).delete()

        # 새 토큰 생성
        token = secrets.token_urlsafe(32)
        expires_at = timezone.now() + timedelta(hours=settings.EMAIL_VERIFICATION_EXPIRE_HOURS)

        return cls.objects.create(
            user=user,
            token=token,
            expires_at=expires_at
        )

    def is_valid(self):
        """토큰 유효성 검사"""
        return not self.is_used and timezone.now() < self.expires_at


class PasswordResetToken(models.Model):
    """비밀번호 재설정 토큰"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='password_reset_tokens')
    token = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    class Meta:
        db_table = 'password_reset_tokens'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.token[:8]}..."

    @classmethod
    def create_token(cls, user):
        """새로운 비밀번호 재설정 토큰 생성"""
        from django.conf import settings
        from datetime import timedelta

        # 기존 미사용 토큰 삭제
        cls.objects.filter(user=user, is_used=False).delete()

        # 새 토큰 생성
        token = secrets.token_urlsafe(32)
        expires_at = timezone.now() + timedelta(seconds=settings.PASSWORD_RESET_TIMEOUT)

        return cls.objects.create(
            user=user,
            token=token,
            expires_at=expires_at
        )

    def is_valid(self):
        """토큰 유효성 검사"""
        return not self.is_used and timezone.now() < self.expires_at
