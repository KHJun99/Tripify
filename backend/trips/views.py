from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import TravelPlan, Itinerary, ItineraryPlace
from .serializers import TravelPlanSerializer, TravelPlanCreateSerializer, ItinerarySerializer
from ai.gemini_service import GeminiService
from datetime import timedelta


class TravelPlanViewSet(viewsets.ModelViewSet):
    """여행 계획 ViewSet"""
    serializer_class = TravelPlanSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TravelPlan.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'], url_path='generate')
    def generate_itinerary(self, request):
        """AI 여행 코스 생성 API"""
        serializer = TravelPlanCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data

        # AI 서비스를 통해 여행 계획 생성
        try:
            gemini_service = GeminiService()
            itinerary_data = gemini_service.generate_itinerary(
                budget=data['budget'],
                start_date=data['start_date'],
                end_date=data['end_date'],
                region=data['region'],
                travel_style=data['travel_style'],
                accommodation_type=data['accommodation_type']
            )

            # TravelPlan 생성
            travel_plan = TravelPlan.objects.create(
                user=request.user,
                title=f"{data['region']} {data['travel_style']} 여행",
                budget=data['budget'],
                start_date=data['start_date'],
                end_date=data['end_date'],
                region=data['region'],
                travel_style=data['travel_style'],
                accommodation_type=data['accommodation_type'],
                is_generated=True
            )

            # 일정 데이터 저장 (itinerary_data가 있는 경우)
            if itinerary_data and 'days' in itinerary_data:
                for day_data in itinerary_data['days']:
                    Itinerary.objects.create(
                        travel_plan=travel_plan,
                        day_number=day_data['day_number'],
                        date=data['start_date'] + timedelta(days=day_data['day_number'] - 1),
                        description=day_data.get('description', '')
                    )

            response_serializer = TravelPlanSerializer(travel_plan)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                'error': f'여행 계획 생성 중 오류가 발생했습니다: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
