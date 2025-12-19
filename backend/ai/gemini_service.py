import os
import json
import requests
from dotenv import load_dotenv
from places.models import Place
from festivals.models import Festival

load_dotenv()


class GeminiService:
    """SSAFY GMS를 통한 Google Gemini AI 서비스"""

    def __init__(self):
        self.api_key = os.getenv('GMS_API_KEY', '')
        self.base_url = 'https://gms.ssafy.io/gmsapi/generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-lite:generateContent'

    def generate_itinerary(self, budget, start_date, end_date, region, travel_style, accommodation_type):
        """
        SSAFY GMS API를 사용하여 여행 일정을 생성
        """
        # 여행 일수 계산
        days = (end_date - start_date).days + 1

        # 데이터베이스에서 해당 지역의 실제 장소 정보 가져오기
        tourist_spots = self._get_places_by_region(region, 'tourist', limit=15)
        restaurants = self._get_places_by_region(region, 'restaurant', limit=10)
        accommodations = self._get_places_by_region(region, 'accommodation', limit=5)
        festivals = self._get_festivals_by_region(region, start_date, end_date)

        # 장소 정보를 문자열로 포맷팅
        tourist_spots_str = self._format_places(tourist_spots)
        restaurants_str = self._format_places(restaurants)
        accommodations_str = self._format_places(accommodations)
        festivals_str = self._format_festivals(festivals)

        # 프롬프트 생성
        prompt = f"""
다음 조건으로 {days}일 여행 계획을 상세한 JSON 형식으로 작성해주세요:
- 예산: {budget:,}원
- 여행 기간: {start_date} ~ {end_date} ({days}일)
- 지역: {region}
- 여행 스타일: {travel_style}
- 숙박 타입: {accommodation_type}

**{region} 지역의 실제 데이터베이스 정보를 활용하세요:**

📍 추천 관광지 (이 중에서 선택하세요):
{tourist_spots_str}

🍽️ 추천 음식점 (이 중에서 선택하세요):
{restaurants_str}

🏨 추천 숙박시설 (이 중에서 선택하세요):
{accommodations_str}

🎉 해당 기간의 축제/행사:
{festivals_str}

각 일차별로 다음 정보를 **매우 구체적으로** 포함해주세요:

1. **관광지 정보** (attractions):
   - 위의 추천 관광지 목록에서 선택하여 사용하세요
   - 각 관광지의 정확한 명칭, 방문 시간, 소요 시간, 간단한 설명 포함
   - 이동 동선을 고려하여 효율적으로 배치하세요

2. **교통수단 정보** (transportation_info):
   - 주요 이동 구간별 교통수단 (버스, 지하철, 택시, 렌터카 등)
   - 예상 이동 시간 및 비용

3. **숙소 정보** (accommodation_info):
   - {accommodation_type} 타입의 추천 숙소명 또는 숙소 지역
   - 예상 숙박비
   - 체크인/체크아웃 시간

4. **식사 정보** (meals_info):
   - 위의 추천 음식점 목록에서 선택하여 사용하세요
   - 아침, 점심, 저녁 각각의 추천 식당명 또는 음식 종류
   - 예상 식사 비용

5. **축제/행사 정보** (events_info):
   - 위에 나열된 축제/행사 정보가 있다면 일정에 포함하세요
   - 축제명, 시간, 위치 등을 정확히 기재

6. **예상 비용** (estimated_cost):
   - 해당 일차의 총 예상 비용 (교통비 + 식비 + 입장료 + 숙박비 등)

JSON 형식 (정확히 이 구조를 따라주세요):
{{
  "days": [
    {{
      "day_number": 1,
      "description": "일정 전체 요약 (예: 서울 도심 투어 및 전통문화 체험)",
      "attractions": [
        {{
          "name": "경복궁",
          "time": "09:00",
          "duration": "2시간",
          "description": "조선시대 궁궐, 경회루와 근정전 관람"
        }},
        {{
          "name": "북촌 한옥마을",
          "time": "11:30",
          "duration": "1.5시간",
          "description": "전통 한옥 거리 산책 및 사진 촬영"
        }}
      ],
      "transportation_info": {{
        "morning": "지하철 3호선 경복궁역 하차 (1,400원)",
        "afternoon": "도보 이동 (경복궁→북촌)",
        "evening": "택시 이용 (약 8,000원)"
      }},
      "accommodation_info": {{
        "name": "명동 ○○호텔 또는 비슷한 등급",
        "cost": 80000,
        "check_in": "15:00",
        "check_out": "11:00"
      }},
      "meals_info": {{
        "breakfast": {{
          "restaurant": "호텔 조식 또는 근처 카페",
          "cost": 10000
        }},
        "lunch": {{
          "restaurant": "삼청동 전통 한정식 (예: ○○식당)",
          "cost": 15000
        }},
        "dinner": {{
          "restaurant": "명동 칼국수 맛집 (예: ○○집)",
          "cost": 12000
        }}
      }},
      "events_info": [
        {{
          "name": "경복궁 수문장 교대식",
          "time": "10:00, 14:00",
          "location": "경복궁 광화문",
          "description": "전통 수문장 교대 의식 관람 (무료)"
        }}
      ],
      "estimated_cost": 136400
    }}
  ]
}}

**중요**:
- 반드시 위에 제공된 실제 데이터베이스의 장소/음식점 목록에서 선택하여 사용하세요
- 장소명은 데이터베이스의 정확한 명칭을 그대로 사용하세요
- 예산 {budget:,}원을 {days}일로 나누어 각 일차별로 합리적으로 배분해주세요
- 이동 동선이 효율적이도록 근처 장소들을 묶어서 계획해주세요
- 축제/행사 정보가 있다면 일정에 우선적으로 포함하세요
"""

        # API 키가 없으면 샘플 데이터 반환
        if not self.api_key:
            print('경고: GMS_API_KEY가 설정되지 않았습니다. 샘플 데이터를 반환합니다.')
            return self._get_sample_data(days, region, travel_style)

        # SSAFY GMS API 호출
        try:
            url = f'{self.base_url}?key={self.api_key}'
            headers = {
                'Content-Type': 'application/json'
            }
            payload = {
                'contents': [
                    {
                        'parts': [
                            {'text': prompt}
                        ]
                    }
                ]
            }

            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()

            result = response.json()

            # Gemini API 응답 파싱
            if 'candidates' in result and len(result['candidates']) > 0:
                content = result['candidates'][0]['content']
                if 'parts' in content and len(content['parts']) > 0:
                    text = content['parts'][0]['text']

                    print('=== Gemini API 원본 응답 ===')
                    print(f'응답 길이: {len(text)} 글자')
                    print(f'첫 200자: {text[:200]}')
                    print('=' * 50)

                    # JSON 파싱 시도
                    try:
                        # 코드 블록 제거 (```json ... ``` 형식)
                        original_text = text
                        if '```json' in text:
                            text = text.split('```json')[1].split('```')[0].strip()
                        elif '```' in text:
                            text = text.split('```')[1].split('```')[0].strip()

                        itinerary_data = json.loads(text)
                        print(f'✓ JSON 파싱 성공! Days: {len(itinerary_data.get("days", []))}')
                        return itinerary_data
                    except json.JSONDecodeError as e:
                        # JSON 파싱 실패 시 텍스트 기반 응답 처리
                        print(f'✗ JSON 파싱 실패: {e}')
                        print(f'파싱 시도한 텍스트 (첫 500자):\n{text[:500]}')
                        return self._parse_text_response(text, days, region, travel_style)

            # 응답이 비정상인 경우 샘플 데이터 반환
            return self._get_sample_data(days, region, travel_style)

        except requests.exceptions.RequestException as e:
            print(f'GMS API 호출 오류: {e}')
            return self._get_sample_data(days, region, travel_style)

    def _parse_text_response(self, text, days, region, travel_style):
        """텍스트 응답을 파싱하여 구조화된 데이터로 변환"""
        return {
            'days': [
                {
                    'day_number': i + 1,
                    'description': f'{region} {travel_style} 여행 {i + 1}일차 - AI 추천 일정'
                }
                for i in range(days)
            ]
        }

    def _get_sample_data(self, days, region, travel_style):
        """샘플 데이터 반환 (API 키가 없거나 오류 발생 시)"""
        sample_days = []
        for i in range(days):
            sample_days.append({
                'day_number': i + 1,
                'description': f'{region} {travel_style} 여행 {i + 1}일차',
                'attractions': [
                    {
                        'name': f'{region} 대표 관광지 {j + 1}',
                        'time': f'{9 + j * 2}:00',
                        'duration': '2시간',
                        'description': f'{region}의 유명한 명소'
                    }
                    for j in range(3)
                ],
                'transportation_info': {
                    'morning': '대중교통 이용 (예상 비용: 5,000원)',
                    'afternoon': '도보 또는 택시',
                    'evening': '대중교통'
                },
                'accommodation_info': {
                    'name': f'{region} 지역 숙소',
                    'cost': 80000,
                    'check_in': '15:00',
                    'check_out': '11:00'
                },
                'meals_info': {
                    'breakfast': {
                        'restaurant': '호텔 조식 또는 근처 식당',
                        'cost': 10000
                    },
                    'lunch': {
                        'restaurant': f'{region} 맛집',
                        'cost': 15000
                    },
                    'dinner': {
                        'restaurant': f'{region} 특선 요리',
                        'cost': 20000
                    }
                },
                'events_info': [],
                'estimated_cost': 130000
            })
        return {'days': sample_days}

    def _get_places_by_region(self, region, place_type, limit=10):
        """지역과 타입으로 장소 검색"""
        try:
            places = Place.objects.filter(
                region__icontains=region,
                place_type=place_type
            )[:limit]
            return list(places)
        except Exception as e:
            print(f'장소 조회 오류: {e}')
            return []

    def _get_festivals_by_region(self, region, start_date, end_date):
        """지역과 기간으로 축제 검색"""
        try:
            # 여행 시작 월 기준으로 축제 검색
            month = start_date.month
            festivals = Festival.objects.filter(
                region__icontains=region,
                start_month=month,
                is_active=True
            )[:5]
            return list(festivals)
        except Exception as e:
            print(f'축제 조회 오류: {e}')
            return []

    def _format_places(self, places):
        """장소 목록을 프롬프트용 문자열로 포맷"""
        if not places:
            return "해당 지역의 데이터가 없습니다."

        formatted = []
        for place in places:
            category = f" ({place.category})" if place.category else ""
            formatted.append(f"- {place.title}{category}: {place.address}")

        return "\n".join(formatted)

    def _format_festivals(self, festivals):
        """축제 목록을 프롬프트용 문자열로 포맷"""
        if not festivals:
            return "해당 기간에 축제/행사가 없습니다."

        formatted = []
        for festival in festivals:
            period = f"{festival.event_start_date} ~ {festival.event_end_date}" if festival.event_start_date else "날짜 미정"
            formatted.append(f"- {festival.title} ({festival.category}): {period} @ {festival.address}")

        return "\n".join(formatted)
