from rest_framework import serializers
from .models import Place, Bookmark
import uuid

class PlaceSerializer(serializers.ModelSerializer):
    """장소 Serializer"""
    class Meta:
        model = Place
        fields = ['id', 'title', 'place_type', 'address', 'latitude', 'longitude',
                  'description', 'image_url', 'tel', 'content_id', 'region',
                  'event_start_date', 'event_end_date', 'created_at']
        read_only_fields = ['id', 'created_at']


class KakaoPlaceCreateSerializer(serializers.Serializer):
    """카카오맵 장소 생성 Serializer"""
    id = serializers.CharField(help_text="카카오맵 장소 ID")
    place_name = serializers.CharField(help_text="장소명")
    address_name = serializers.CharField(help_text="주소")
    road_address_name = serializers.CharField(required=False, allow_blank=True, help_text="도로명 주소")
    x = serializers.CharField(help_text="경도")
    y = serializers.CharField(help_text="위도")
    category_name = serializers.CharField(required=False, allow_blank=True, help_text="카테고리")
    phone = serializers.CharField(required=False, allow_blank=True, help_text="전화번호")
    place_url = serializers.URLField(required=False, allow_blank=True, help_text="장소 URL")
    
    def create(self, validated_data):
        # 카카오맵 장소 ID를 content_id로 사용
        kakao_id = validated_data['id']
        
        # 이미 존재하는 장소인지 확인
        place, created = Place.objects.get_or_create(
            content_id=f"kakao_{kakao_id}",
            defaults={
                'title': validated_data['place_name'],
                'address': validated_data.get('road_address_name') or validated_data['address_name'],
                'latitude': validated_data['y'],
                'longitude': validated_data['x'],
                'tel': validated_data.get('phone', ''),
                'region': self._extract_region(validated_data['address_name']),
                'place_type': self._determine_place_type(validated_data.get('category_name', '')),
                'category': validated_data.get('category_name', ''),
                'description': f"카카오맵에서 저장된 장소: {validated_data.get('category_name', '')}",
            }
        )
        return place
    
    def _extract_region(self, address):
        """주소에서 지역 추출"""
        # 주소에서 첫 번째 공백 전까지가 지역 (예: "서울특별시 강남구" -> "서울특별시")
        parts = address.split()
        if parts:
            region = parts[0]
            # "특별시", "광역시", "시", "도" 제거
            region = region.replace('특별시', '').replace('광역시', '').replace('시', '').replace('도', '')
            return region
        return "기타"
    
    def _determine_place_type(self, category_name):
        """카테고리명으로 장소 타입 결정"""
        category_lower = category_name.lower()
        if '음식점' in category_name or '맛집' in category_name or '식당' in category_name:
            return 'restaurant'
        elif '카페' in category_name or '커피' in category_name:
            return 'cafe'
        elif '숙박' in category_name or '호텔' in category_name or '모텔' in category_name:
            return 'accommodation'
        elif '축제' in category_name or '행사' in category_name:
            return 'festival'
        else:
            return 'tourist'


class BookmarkSerializer(serializers.ModelSerializer):
    """북마크 Serializer"""
    place = PlaceSerializer(read_only=True)
    place_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Bookmark
        fields = ['id', 'place', 'place_id', 'created_at']
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        place_id = validated_data.pop('place_id')
        try:
            place = Place.objects.get(id=place_id)
        except Place.DoesNotExist:
            raise serializers.ValidationError({'place_id': '존재하지 않는 장소입니다.'})
        
        validated_data['user'] = self.context['request'].user
        validated_data['place'] = place
        
        # 중복 체크
        if Bookmark.objects.filter(user=validated_data['user'], place=place).exists():
            raise serializers.ValidationError({'place_id': '이미 북마크된 장소입니다.'})
        
        return super().create(validated_data)
