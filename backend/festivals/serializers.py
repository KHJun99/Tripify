from rest_framework import serializers
from .models import Festival


class FestivalListSerializer(serializers.ModelSerializer):
    """축제 목록용 Serializer (간단한 정보)"""
    event_start_date = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    event_end_date = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    
    def to_representation(self, instance):
        """빈 문자열을 null로 변환"""
        ret = super().to_representation(instance)
        # 빈 문자열을 None으로 변환
        if ret.get('event_start_date') == '':
            ret['event_start_date'] = None
        if ret.get('event_end_date') == '':
            ret['event_end_date'] = None
        return ret
    
    class Meta:
        model = Festival
        fields = [
            'id', 'title', 'category', 'address', 'region',
            'event_start_date', 'event_end_date', 'start_month', 'end_month',
            'image_url', 'phone'
        ]


class FestivalDetailSerializer(serializers.ModelSerializer):
    """축제 상세 정보용 Serializer (모든 정보)"""
    event_start_date = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    event_end_date = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    
    def to_representation(self, instance):
        """빈 문자열을 null로 변환"""
        ret = super().to_representation(instance)
        # 빈 문자열을 None으로 변환
        if ret.get('event_start_date') == '':
            ret['event_start_date'] = None
        if ret.get('event_end_date') == '':
            ret['event_end_date'] = None
        return ret
    
    class Meta:
        model = Festival
        fields = [
            'id', 'title', 'category', 'address', 'region', 'phone',
            'latitude', 'longitude', 'image_url',
            'event_start_date', 'event_end_date', 'start_month', 'end_month',
            'content_id', 'is_active', 'created_at', 'updated_at'
        ]
