from django.contrib import admin
from .models import Festival


@admin.register(Festival)
class FestivalAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'region', 'start_month', 'event_start_date', 'is_active', 'created_at']
    list_filter = ['region', 'start_month', 'category', 'is_active']
    search_fields = ['title', 'address', 'category']
    list_editable = ['is_active']
    ordering = ['start_month', 'title']

    fieldsets = (
        ('기본 정보', {
            'fields': ('title', 'category', 'region', 'address', 'phone', 'is_active')
        }),
        ('날짜 정보', {
            'fields': ('event_start_date', 'event_end_date', 'start_month', 'end_month')
        }),
        ('위치 정보', {
            'fields': ('latitude', 'longitude', 'image_url')
        }),
        ('메타 정보', {
            'fields': ('content_id',),
            'classes': ('collapse',)
        }),
    )
