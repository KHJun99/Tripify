from rest_framework import serializers
from .models import Festival


class FestivalListSerializer(serializers.ModelSerializer):
    """축제 목록용 Serializer (간단한 정보)"""
    class Meta:
        model = Festival
        fields = [
            'id', 'title', 'category', 'address', 'region',
            'event_start_date', 'event_end_date', 'start_month', 'end_month',
            'image_url', 'phone'
        ]


class FestivalDetailSerializer(serializers.ModelSerializer):
    """축제 상세 정보용 Serializer (모든 정보)"""
    class Meta:
        model = Festival
        fields = [
            'id', 'title', 'category', 'address', 'region', 'phone',
            'latitude', 'longitude', 'image_url',
            'event_start_date', 'event_end_date', 'start_month', 'end_month',
            'content_id', 'is_active', 'created_at', 'updated_at'
        ]
