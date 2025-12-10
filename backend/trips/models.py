from django.db import models
from django.conf import settings
from places.models import Place

class TravelPlan(models.Model):
    """여행 계획 모델"""
    ACCOMMODATION_CHOICES = [
        ('hotel', '호텔'),
        ('motel', '모텔'),
        ('pension', '펜션'),
        ('guesthouse', '게스트하우스'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='travel_plans')
    title = models.CharField(max_length=255, help_text="여행 제목")
    budget = models.IntegerField(help_text="예산")
    start_date = models.DateField(help_text="여행 시작일")
    end_date = models.DateField(help_text="여행 종료일")
    region = models.CharField(max_length=100, help_text="여행 지역")
    travel_style = models.CharField(max_length=100, help_text="여행 스타일")
    accommodation_type = models.CharField(max_length=20, choices=ACCOMMODATION_CHOICES, default='motel')
    is_generated = models.BooleanField(default=False, help_text="AI 생성 여부")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'travel_plans'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.user.username})"


class Itinerary(models.Model):
    """여행 일정 모델 (일차별 계획)"""
    travel_plan = models.ForeignKey(TravelPlan, on_delete=models.CASCADE, related_name='itineraries')
    day_number = models.IntegerField(help_text="여행 일차")
    date = models.DateField(help_text="일정 날짜")
    description = models.TextField(blank=True, help_text="일정 설명")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'itineraries'
        ordering = ['day_number']
        unique_together = ['travel_plan', 'day_number']

    def __str__(self):
        return f"{self.travel_plan.title} - Day {self.day_number}"


class ItineraryPlace(models.Model):
    """일정별 장소 모델"""
    itinerary = models.ForeignKey(Itinerary, on_delete=models.CASCADE, related_name='places')
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='itinerary_places')
    order = models.IntegerField(help_text="방문 순서")
    visit_time = models.TimeField(null=True, blank=True, help_text="방문 시간")
    duration = models.IntegerField(null=True, blank=True, help_text="체류 시간 (분)")
    notes = models.TextField(blank=True, help_text="메모")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'itinerary_places'
        ordering = ['order']
        unique_together = ['itinerary', 'order']

    def __str__(self):
        return f"{self.itinerary} - {self.place.title}"
