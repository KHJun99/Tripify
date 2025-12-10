from django.db import models
from django.conf import settings

class Place(models.Model):
    """여행지 모델"""
    PLACE_TYPE_CHOICES = [
        ('tourist', '관광지'),
        ('festival', '축제/행사'),
        ('restaurant', '맛집'),
        ('cafe', '카페'),
        ('accommodation', '숙박'),
    ]

    title = models.CharField(max_length=255, help_text="장소명")
    place_type = models.CharField(max_length=20, choices=PLACE_TYPE_CHOICES, default='tourist')
    address = models.CharField(max_length=500, help_text="주소")
    latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    description = models.TextField(blank=True)
    image_url = models.URLField(blank=True)
    tel = models.CharField(max_length=20, blank=True)
    content_id = models.CharField(max_length=50, unique=True, help_text="외부 API Content ID")
    region = models.CharField(max_length=100, help_text="지역")
    event_start_date = models.DateField(null=True, blank=True, help_text="행사 시작일")
    event_end_date = models.DateField(null=True, blank=True, help_text="행사 종료일")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'places'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Bookmark(models.Model):
    """북마크 모델"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookmarks')
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='bookmarks')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'bookmarks'
        unique_together = ['user', 'place']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.place.title}"
