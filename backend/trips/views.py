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

    def get_object(self):
        """객체 조회 - 추천된 계획은 누구나 볼 수 있도록"""
        queryset = self.filter_queryset(self.get_queryset())
        
        # URL에서 pk 가져오기
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        lookup_value = self.kwargs[lookup_url_kwarg]
        
        try:
            # 먼저 본인 계획에서 찾기
            obj = queryset.get(pk=lookup_value)
            return obj
        except TravelPlan.DoesNotExist:
            # 본인 계획이 아니면 추천된 계획인지 확인
            try:
                obj = TravelPlan.objects.get(pk=lookup_value, is_recommended=True)
                return obj
            except TravelPlan.DoesNotExist:
                from rest_framework.exceptions import NotFound
                raise NotFound('여행 계획을 찾을 수 없습니다.')

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
                people_count=data['people_count'],
                start_date=data['start_date'],
                end_date=data['end_date'],
                departure_location=data['departure_location'],
                region=data['region'],
                travel_style=data['travel_style'],
                accommodation_type=data['accommodation_type']
            )

            # TravelPlan 생성
            travel_plan = TravelPlan.objects.create(
                user=request.user,
                title=f"{data['region']} {data['travel_style']} 여행",
                budget=data['budget'],
                people_count=data['people_count'],
                start_date=data['start_date'],
                end_date=data['end_date'],
                departure_location=data['departure_location'],
                region=data['region'],
                travel_style=data['travel_style'],
                accommodation_type=data['accommodation_type'],
                is_generated=True
            )

            # 일정 데이터 저장 (itinerary_data가 있는 경우)
            created_count = 0
            print(f'=== Itinerary 데이터 확인 ===')
            print(f'itinerary_data 존재: {itinerary_data is not None}')
            if itinerary_data:
                print(f'itinerary_data 타입: {type(itinerary_data)}')
                print(f'itinerary_data 키: {itinerary_data.keys() if isinstance(itinerary_data, dict) else "N/A"}')
                print(f'"days" 키 존재: {"days" in itinerary_data if isinstance(itinerary_data, dict) else False}')
                if isinstance(itinerary_data, dict) and 'days' in itinerary_data:
                    print(f'days 개수: {len(itinerary_data["days"])}')
            
            if itinerary_data and isinstance(itinerary_data, dict) and 'days' in itinerary_data:
                for day_data in itinerary_data['days']:
                    try:
                        day_num = day_data.get('day_number', '?')
                        meals_info = day_data.get('meals_info', {})
                        
                        # 식사 정보 확인 로그
                        print(f'Day {day_num} - meals_info 존재: {meals_info is not None and meals_info != {}}')
                        if meals_info:
                            print(f'Day {day_num} - meals_info 키: {list(meals_info.keys()) if isinstance(meals_info, dict) else "N/A"}')
                            print(f'Day {day_num} - meals_info 내용: {meals_info}')
                        else:
                            print(f'⚠️ Day {day_num} - meals_info가 비어있습니다!')
                        
                        Itinerary.objects.create(
                            travel_plan=travel_plan,
                            day_number=day_data['day_number'],
                            date=data['start_date'] + timedelta(days=day_data['day_number'] - 1),
                            description=day_data.get('description', ''),
                            attractions=day_data.get('attractions', []),
                            transportation_info=day_data.get('transportation_info', {}),
                            accommodation_info=day_data.get('accommodation_info', {}),
                            meals_info=meals_info,
                            events_info=day_data.get('events_info', []),
                            estimated_cost=day_data.get('estimated_cost', None)
                        )
                        created_count += 1
                    except Exception as e:
                        print(f'✗ 일정 생성 오류 (day {day_data.get("day_number", "?")}): {e}')
                        import traceback
                        traceback.print_exc()
            else:
                print(f'⚠️ 일정 데이터가 없거나 형식이 올바르지 않습니다.')
                print(f'itinerary_data: {itinerary_data}')

            print(f'✓ Itinerary 생성 완료: {created_count}개')

            # Refresh to get itineraries
            travel_plan.refresh_from_db()
            itinerary_count = travel_plan.itineraries.count()
            print(f'✓ TravelPlan의 itineraries 개수: {itinerary_count}')

            response_serializer = TravelPlanSerializer(travel_plan)
            print(f'✓ Serialized data에 itineraries 포함: {"itineraries" in response_serializer.data}')
            if 'itineraries' in response_serializer.data:
                print(f'✓ Serialized itineraries 개수: {len(response_serializer.data["itineraries"])}')

            return Response(response_serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                'error': f'여행 계획 생성 중 오류가 발생했습니다: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'], url_path='recommend')
    def recommend_plan(self, request, pk=None):
        """여행 계획 추천 API"""
        from .serializers import TravelPlanRecommendSerializer
        from django.utils import timezone
        
        travel_plan = self.get_object()
        
        # 본인의 계획만 추천 가능
        if travel_plan.user != request.user:
            return Response({
                'error': '본인의 여행 계획만 추천할 수 있습니다.'
            }, status=status.HTTP_403_FORBIDDEN)
        
        serializer = TravelPlanRecommendSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        travel_plan.is_recommended = True
        travel_plan.review = data['review']
        travel_plan.rating = data['rating']
        travel_plan.recommended_at = timezone.now()
        travel_plan.save()
        
        response_serializer = TravelPlanSerializer(travel_plan)
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['delete'], url_path='recommend')
    def unrecommend_plan(self, request, pk=None):
        """여행 계획 추천 취소 API"""
        travel_plan = self.get_object()
        
        # 본인의 계획만 추천 취소 가능
        if travel_plan.user != request.user:
            return Response({
                'error': '본인의 여행 계획만 추천 취소할 수 있습니다.'
            }, status=status.HTTP_403_FORBIDDEN)
        
        travel_plan.is_recommended = False
        travel_plan.review = ''
        travel_plan.rating = None
        travel_plan.recommended_at = None
        travel_plan.save()
        
        response_serializer = TravelPlanSerializer(travel_plan)
        return Response(response_serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def recommended_plans(request):
    """추천된 여행 계획 목록 API"""
    from .serializers import TravelPlanSerializer
    
    plans = TravelPlan.objects.filter(is_recommended=True).order_by('-recommended_at')
    serializer = TravelPlanSerializer(plans, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

