from rest_framework import serializers
from .models import Festival


class FestivalListSerializer(serializers.ModelSerializer):
    """축제 목록용 Serializer (간단한 정보)"""
    class Meta:
        model = Festival
        fields = [
            'id', 'name', 'region', 'location', 'period', 'month',
            'description', 'image', 'tags'
        ]


class FestivalDetailSerializer(serializers.ModelSerializer):
    """축제 상세 정보용 Serializer (모든 정보)"""
    class Meta:
        model = Festival
        fields = [
            'id', 'name', 'region', 'location', 'period', 'month',
            'description', 'detailed_description', 'image', 'fee',
            'contact', 'website', 'tags', 'programs', 'transportation',
            'created_at', 'updated_at'
        ]
