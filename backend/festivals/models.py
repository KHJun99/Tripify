from django.db import models


class Festival(models.Model):
    """축제 모델"""
    title = models.CharField(max_length=255, verbose_name='축제명')
    category = models.CharField(max_length=100, blank=True, verbose_name='카테고리')
    address = models.CharField(max_length=500, verbose_name='주소')
    phone = models.CharField(max_length=100, blank=True, verbose_name='연락처')
    latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    image_url = models.URLField(max_length=500, blank=True, verbose_name='이미지 URL')

    # 축제 날짜 정보
    event_start_date = models.CharField(max_length=20, blank=True, verbose_name='행사 시작일')  # YYYYMMDD
    event_end_date = models.CharField(max_length=20, blank=True, verbose_name='행사 종료일')    # YYYYMMDD
    start_month = models.IntegerField(null=True, blank=True, verbose_name='시작 월', help_text='1-12')
    end_month = models.IntegerField(null=True, blank=True, verbose_name='종료 월', help_text='1-12')

    # 지역 정보
    region = models.CharField(max_length=100, verbose_name='지역')

    # 외부 API ID
    content_id = models.CharField(max_length=50, unique=True, help_text="외부 API Content ID")

    # 메타 정보
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')
    is_active = models.BooleanField(default=True, verbose_name='활성화 여부')

    class Meta:
        db_table = 'festivals'
        verbose_name = '축제'
        verbose_name_plural = '축제 목록'
        ordering = ['start_month', 'title']

    def __str__(self):
        return f"{self.title} ({self.region})"
