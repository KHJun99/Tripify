from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Place, Bookmark
from .serializers import PlaceSerializer, BookmarkSerializer, KakaoPlaceCreateSerializer
from django.db.models import Q


class PlaceViewSet(viewsets.ReadOnlyModelViewSet):
    """장소 ViewSet"""
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Place.objects.all()

        # 검색어 필터링
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(address__icontains=search) |
                Q(region__icontains=search)
            )

        # 지역 필터링
        region = self.request.query_params.get('region', None)
        if region:
            queryset = queryset.filter(region__icontains=region)

        # 타입 필터링
        place_type = self.request.query_params.get('type', None)
        if place_type:
            queryset = queryset.filter(place_type=place_type)

        return queryset

    @action(detail=False, methods=['get'], url_path='festivals')
    def festivals(self, request):
        """축제/행사 목록 조회"""
        month = request.query_params.get('month', None)
        region = request.query_params.get('region', None)

        queryset = Place.objects.filter(place_type='festival')

        if month:
            queryset = queryset.filter(
                Q(event_start_date__month=month) |
                Q(event_end_date__month=month)
            )

        if region:
            queryset = queryset.filter(region__icontains=region)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class BookmarkViewSet(viewsets.ModelViewSet):
    """북마크 ViewSet"""
    serializer_class = BookmarkSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Bookmark.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_place_from_kakao(request):
    """카카오맵 장소를 Place로 저장"""
    try:
        serializer = KakaoPlaceCreateSerializer(data=request.data)
        if serializer.is_valid():
            place = serializer.save()
            return Response(PlaceSerializer(place).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        import traceback
        print(f"카카오맵 장소 저장 오류: {str(e)}")
        print(traceback.format_exc())
        return Response({
            'error': f'장소 저장 중 오류가 발생했습니다: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)