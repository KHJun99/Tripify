from django.db import models


class Festival(models.Model):
    """축제 모델"""
    name = models.CharField(max_length=200, verbose_name='축제명')
    region = models.CharField(max_length=50, verbose_name='지역')
    location = models.CharField(max_length=300, verbose_name='장소')
    period = models.CharField(max_length=100, verbose_name='개최 기간')
    month = models.IntegerField(verbose_name='시작 월', help_text='1-12')
    description = models.TextField(verbose_name='간단 설명')
    detailed_description = models.TextField(verbose_name='상세 설명', blank=True)
    image = models.URLField(max_length=500, verbose_name='이미지 URL')

    # 추가 정보
    fee = models.CharField(max_length=100, verbose_name='입장료', default='무료')
    contact = models.CharField(max_length=100, verbose_name='연락처', blank=True)
    website = models.URLField(max_length=500, verbose_name='웹사이트', blank=True)

    # JSON 필드
    tags = models.JSONField(default=list, verbose_name='태그')
    programs = models.JSONField(default=list, verbose_name='프로그램', blank=True)
    transportation = models.JSONField(default=dict, verbose_name='교통 정보', blank=True)

    # 메타 정보
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')
    is_active = models.BooleanField(default=True, verbose_name='활성화 여부')

    class Meta:
        db_table = 'festivals'
        verbose_name = '축제'
        verbose_name_plural = '축제 목록'
        ordering = ['month', 'name']

    def __str__(self):
        return f"{self.name} ({self.region})"
