from django.db import models
from django.contrib.auth.models import AbstractUser

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

    class Meta:
        db_table = 'users'
        ordering = ['-created_at']

    def __str__(self):
        return self.username
