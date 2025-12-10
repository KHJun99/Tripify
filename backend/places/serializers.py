from rest_framework import serializers
from .models import Place, Bookmark

class PlaceSerializer(serializers.ModelSerializer):
    """장소 Serializer"""
    class Meta:
        model = Place
        fields = ['id', 'title', 'place_type', 'address', 'latitude', 'longitude',
                  'description', 'image_url', 'tel', 'content_id', 'region',
                  'event_start_date', 'event_end_date', 'created_at']
        read_only_fields = ['id', 'created_at']


class BookmarkSerializer(serializers.ModelSerializer):
    """북마크 Serializer"""
    place = PlaceSerializer(read_only=True)
    place_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Bookmark
        fields = ['id', 'place', 'place_id', 'created_at']
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
