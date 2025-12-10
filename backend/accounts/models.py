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

    class Meta:
        db_table = 'users'
        ordering = ['-created_at']

    def __str__(self):
        return self.username
