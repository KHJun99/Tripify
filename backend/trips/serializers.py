from rest_framework import serializers
from .models import TravelPlan, Itinerary, ItineraryPlace, Wishlist
from places.serializers import PlaceSerializer

class ItineraryPlaceSerializer(serializers.ModelSerializer):
    """일정별 장소 Serializer"""
    place = PlaceSerializer(read_only=True)
    place_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = ItineraryPlace
        fields = ['id', 'place', 'place_id', 'order', 'visit_time', 'duration', 'notes']
        read_only_fields = ['id']


class ItinerarySerializer(serializers.ModelSerializer):
    """여행 일정 Serializer"""
    places = ItineraryPlaceSerializer(many=True, read_only=True)

    class Meta:
        model = Itinerary
        fields = [
            'id', 'day_number', 'date', 'description', 'places',
            'attractions', 'transportation_info', 'accommodation_info',
            'meals_info', 'events_info', 'estimated_cost'
        ]
        read_only_fields = ['id']


class TravelPlanSerializer(serializers.ModelSerializer):
    """여행 계획 Serializer"""
    itineraries = ItinerarySerializer(many=True, read_only=True)
    user = serializers.SerializerMethodField()
    user_id = serializers.IntegerField(source='user.id', read_only=True)

    def get_user(self, obj):
        """사용자 닉네임 반환 (닉네임이 없으면 username)"""
        if obj.user.nickname:
            return obj.user.nickname
        return obj.user.username

    class Meta:
        model = TravelPlan
        fields = ['id', 'user', 'user_id', 'title', 'budget', 'people_count', 'start_date', 'end_date',
                  'departure_location', 'region', 'travel_style', 'accommodation_type', 'is_generated',
                  'is_recommended', 'review', 'rating', 'recommended_at',
                  'itineraries', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at', 'is_generated', 'recommended_at']


class TravelPlanRecommendSerializer(serializers.Serializer):
    """여행 계획 추천 Serializer"""
    review = serializers.CharField(required=True, max_length=2000, help_text="후기")
    rating = serializers.IntegerField(required=True, min_value=1, max_value=5, help_text="평점 (1-5)")


class TravelPlanModifySerializer(serializers.Serializer):
    """여행 계획 수정 요청 Serializer"""
    requirements = serializers.CharField(required=True, max_length=2000, help_text="수정 요구사항")


class TravelPlanCreateSerializer(serializers.Serializer):
    """AI 여행 계획 생성 요청 Serializer"""
    budget = serializers.IntegerField(required=True, min_value=0)
    people_count = serializers.IntegerField(required=True, min_value=1)
    start_date = serializers.DateField(required=True)
    end_date = serializers.DateField(required=True)
    departure_location = serializers.CharField(required=True, max_length=100)
    region = serializers.CharField(required=True, max_length=100)
    travel_style = serializers.CharField(required=True, max_length=100)
    accommodation_type = serializers.ChoiceField(
        choices=['hotel', 'motel', 'pension', 'guesthouse'],
        required=True
    )

    def validate(self, attrs):
        if attrs['start_date'] >= attrs['end_date']:
            raise serializers.ValidationError("종료일은 시작일보다 이후여야 합니다.")
        return attrs


class WishlistSerializer(serializers.ModelSerializer):
    """여행 위시리스트 Serializer"""
    
    class Meta:
        model = Wishlist
        fields = ['id', 'text', 'checked', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
