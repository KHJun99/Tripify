from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.core.management import call_command
from .models import Festival
from .serializers import FestivalListSerializer, FestivalDetailSerializer
from io import StringIO


class FestivalViewSet(viewsets.ReadOnlyModelViewSet):
    """
    축제 ViewSet (읽기 전용)

    list: 축제 목록 조회 (필터링 가능 - month, region)
    retrieve: 축제 상세 정보 조회
    sync: 한국관광공사 API에서 축제 데이터 동기화 (POST /api/festivals/sync/)
    """
    queryset = Festival.objects.filter(is_active=True)
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['month', 'region']
    search_fields = ['name', 'description', 'location']
    ordering_fields = ['month', 'name', 'created_at']
    ordering = ['month', 'name']

    def get_serializer_class(self):
        """액션에 따라 다른 Serializer 사용"""
        if self.action == 'retrieve':
            return FestivalDetailSerializer
        return FestivalListSerializer

    @action(detail=False, methods=['post'])
    def sync(self, request):
        """
        한국관광공사 API에서 축제 데이터를 동기화합니다.

        Query Parameters:
        - clear: true/false (기존 데이터 삭제 여부)
        - month: 1-12 (특정 월만 동기화)
        """
        try:
            # 명령 출력 캡처
            out = StringIO()

            # 옵션 파싱
            options = {}
            if request.query_params.get('clear') == 'true':
                options['clear'] = True
            if request.query_params.get('month'):
                try:
                    options['month'] = int(request.query_params.get('month'))
                except ValueError:
                    return Response(
                        {'error': 'month는 1-12 사이의 숫자여야 합니다.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            # 동기화 명령 실행
            call_command('sync_festivals', stdout=out, **options)

            # 결과 반환
            return Response({
                'message': '축제 데이터 동기화가 완료되었습니다.',
                'total_count': Festival.objects.filter(is_active=True).count(),
                'output': out.getvalue()
            })

        except Exception as e:
            return Response(
                {'error': f'동기화 중 오류 발생: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
