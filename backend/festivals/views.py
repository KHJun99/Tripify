from rest_framework import viewsets, filters
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .models import Festival
from .serializers import FestivalListSerializer, FestivalDetailSerializer


class FestivalViewSet(viewsets.ReadOnlyModelViewSet):
    """
    축제 ViewSet (읽기 전용)

    list: 축제 목록 조회 (필터링 가능 - start_month, end_month, region, category)
    retrieve: 축제 상세 정보 조회
    """
    queryset = Festival.objects.filter(is_active=True)
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['start_month', 'end_month', 'region', 'category']
    search_fields = ['title', 'address', 'category']
    ordering_fields = ['start_month', 'title', 'created_at']
    ordering = ['start_month', 'title']

    def get_serializer_class(self):
        """액션에 따라 다른 Serializer 사용"""
        if self.action == 'retrieve':
            return FestivalDetailSerializer
        return FestivalListSerializer
