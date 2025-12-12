from django.contrib import admin
from .models import Festival


@admin.register(Festival)
class FestivalAdmin(admin.ModelAdmin):
    list_display = ['name', 'region', 'month', 'period', 'is_active', 'created_at']
    list_filter = ['region', 'month', 'is_active']
    search_fields = ['name', 'location', 'description']
    list_editable = ['is_active']
    ordering = ['month', 'name']

    fieldsets = (
        ('기본 정보', {
            'fields': ('name', 'region', 'location', 'period', 'month', 'is_active')
        }),
        ('설명', {
            'fields': ('description', 'detailed_description', 'image')
        }),
        ('추가 정보', {
            'fields': ('fee', 'contact', 'website')
        }),
        ('상세 정보', {
            'fields': ('tags', 'programs', 'transportation'),
            'classes': ('collapse',)
        }),
    )
