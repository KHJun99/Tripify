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

    def generate_itinerary(self, budget, people_count, start_date, end_date, departure_location, region, travel_style, accommodation_type):
        """
        SSAFY GMS API를 사용하여 여행 일정을 생성
        """
        # 여행 일수 계산
        days = (end_date - start_date).days + 1

        # 1인당 예산 계산
        budget_per_person = budget // people_count

        # 일일 예산 계산 (총 예산을 일수로 나눔)
        daily_budget = budget // days

        # 예산 허용 범위 (최대 10% 초과까지 허용)
        budget_min = int(budget * 0.9)  # 참고용 (현재는 사용하지 않음)
        budget_max = int(budget * 1.1)  # 예산의 110% 초과 시 재생성

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
다음 조건으로 **정확히 {days}일** 여행 계획을 상세한 JSON 형식으로 작성해주세요:
**중요: 반드시 {days}일치 일정을 모두 생성해야 합니다. {days-1}일이나 {days+1}일이 아닌 정확히 {days}일입니다.**
- 총 예산: {budget:,}원 (총 {people_count}명, 1인당 약 {budget_per_person:,}원)
- 여행 인원: {people_count}명
- 여행 기간: {start_date} ~ {end_date} ({days}일)
- 출발지: {departure_location}
- 여행 지역: {region}
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
   - 출발지({departure_location})에서 여행 지역({region})으로의 이동 방법을 첫날 일정에 포함하세요
   - 주요 이동 구간별 교통수단 (버스, 지하철, 택시, 렌터카, KTX, 고속버스 등)
   - 예상 이동 시간 및 비용
   - 첫날에는 "{departure_location} → {region}" 이동 경로와 비용을 명시하세요

3. **숙소 정보** (accommodation_info):
   - {accommodation_type} 타입의 추천 숙소명 또는 숙소 지역
   - 예상 숙박비
   - 체크인/체크아웃 시간

4. **식사 정보** (meals_info) - **필수 항목입니다**:
   - 위의 추천 음식점 목록에서 선택하여 사용하세요
   - **반드시 아침, 점심, 저녁 각각의 추천 식당명 또는 음식 종류를 포함하세요**
   - 각 식사마다 예상 식사 비용을 포함하세요
   - meals_info는 반드시 "아침", "점심", "저녁" 키를 가진 객체여야 합니다

5. **축제/행사 정보** (events_info):
   - 위에 나열된 축제/행사 정보가 있다면 일정에 포함하세요
   - 축제명, 시간, 위치 등을 정확히 기재

6. **예상 비용** (estimated_cost):
   - 해당 일차의 총 예상 비용 (교통비 + 식비 + 입장료 + 숙박비 등)

JSON 형식 (정확히 이 구조를 따라주세요):
**반드시 "days" 배열에 정확히 {days}개의 일정 객체를 포함해야 합니다. day_number는 1부터 {days}까지 순서대로여야 합니다.**

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
        "오전": "지하철 3호선 경복궁역 하차 (1,400원)",
        "오후": "도보 이동 (경복궁→북촌)",
        "저녁": "택시 이용 (약 8,000원)"
      }},
      "accommodation_info": {{
        "name": "명동 ○○호텔 또는 비슷한 등급",
        "cost": 80000,
        "check_in": "15:00",
        "check_out": "11:00"
      }},
      "meals_info": {{
        "아침": {{
          "restaurant": "호텔 조식 또는 근처 카페",
          "cost": 10000
        }},
        "점심": {{
          "restaurant": "삼청동 전통 한정식 (예: ○○식당)",
          "cost": 15000
        }},
        "저녁": {{
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
    }},
    {{
      "day_number": 2,
      "description": "2일차 일정 요약",
      "attractions": [...],
      "transportation_info": {{...}},
      "accommodation_info": {{...}},
      "meals_info": {{...}},
      "events_info": [],
      "estimated_cost": 120000
    }}{f''',
    {{
      "day_number": {days},
      "description": "{days}일차 일정 요약",
      "attractions": [...],
      "transportation_info": {{...}},
      "accommodation_info": {{...}},
      "meals_info": {{...}},
      "events_info": [],
      "estimated_cost": 110000
    }}''' if days > 2 else ''}
  ]
}}

**중요: 모든 텍스트는 한글로 작성하세요**
- transportation_info의 키: "오전", "오후", "저녁" 사용 (morning, afternoon, evening 사용 금지)
- **meals_info는 반드시 포함되어야 하며, "아침", "점심", "저녁" 키를 모두 가져야 합니다** (breakfast, lunch, dinner 사용 금지)
- 각 일차마다 meals_info에 아침, 점심, 저녁 식사 정보를 반드시 포함하세요
- 모든 설명과 내용은 한글로 작성
- 시간 표기: "09:00", "15:00" 등 숫자는 그대로 사용
- 장소명과 상호명은 데이터베이스에 있는 그대로 사용

**예산 준수 규칙 (매우 중요)**:
- 총 예산: {budget:,}원 ({people_count}명 전체 기준)
- 일일 목표 예산: 약 {daily_budget:,}원
- **전체 {days}일간 총 비용 합계는 {budget_max:,}원을 초과하지 않아야 합니다 (예산의 110% 이하)**
- 예산보다 작게 생성되는 것은 문제없지만, 예산을 10% 초과하면 안 됩니다
- 각 일차의 estimated_cost를 모두 합산했을 때 총 예산의 110%를 넘지 않도록 주의하세요
- 예산을 초과할 가능성이 있으면 저렴한 음식점/숙소를 선택하고, 불필요한 택시 이용을 줄이세요

**기타 중요 사항**:
- 반드시 위에 제공된 실제 데이터베이스의 장소/음식점 목록에서 선택하여 사용하세요
- 장소명은 데이터베이스의 정확한 명칭을 그대로 사용하세요
- 모든 비용은 {people_count}명 전체를 기준으로 계산해주세요 (예: 숙박비는 {people_count}명이 함께 사용, 식비는 {people_count}명분)
- 이동 동선이 효율적이도록 근처 장소들을 묶어서 계획해주세요
- 축제/행사 정보가 있다면 일정에 우선적으로 포함하세요
- **각 일차마다 meals_info에 아침, 점심, 저녁 식사 정보를 반드시 포함해야 합니다. 이는 선택 사항이 아닌 필수 항목입니다.**
"""

        # API 키가 없으면 샘플 데이터 반환
        if not self.api_key:
            print('경고: GMS_API_KEY가 설정되지 않았습니다. 샘플 데이터를 반환합니다.')
            return self._get_sample_data(days, region, travel_style, people_count, departure_location)

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
                        days_count = len(itinerary_data.get("days", []))
                        print(f'✓ JSON 파싱 성공! Days: {days_count}개 (요청: {days}일)')
                        
                        # 일수 검증
                        if days_count != days:
                            print(f'⚠️ 일수 불일치! 요청: {days}일, 생성: {days_count}일')
                            if days_count < days:
                                print(f'⚠️ 일정이 부족합니다. {days - days_count}일이 더 필요합니다.')
                        
                        # 식사 정보 검증
                        if 'days' in itinerary_data:
                            for i, day in enumerate(itinerary_data['days'], 1):
                                meals_info = day.get('meals_info', {})
                                if not meals_info or not isinstance(meals_info, dict):
                                    print(f'⚠️ Day {i} - meals_info가 없거나 형식이 잘못되었습니다: {meals_info}')
                                else:
                                    required_keys = ['아침', '점심', '저녁']
                                    missing_keys = [key for key in required_keys if key not in meals_info]
                                    if missing_keys:
                                        print(f'⚠️ Day {i} - meals_info에 누락된 키: {missing_keys}')
                                    else:
                                        print(f'✓ Day {i} - meals_info 정상: {list(meals_info.keys())}')

                        # 예산 검증
                        if not self._validate_budget(itinerary_data, budget, budget_min, budget_max):
                            print('⚠️  예산 초과! 재생성을 시도합니다...')
                            # 재생성 시도 (1회)
                            return self._regenerate_with_budget_constraint(
                                budget, people_count, start_date, end_date, departure_location, region,
                                travel_style, accommodation_type, days,
                                daily_budget, budget_min, budget_max,
                                tourist_spots_str, restaurants_str, accommodations_str, festivals_str
                            )

                        return itinerary_data
                    except json.JSONDecodeError as e:
                        # JSON 파싱 실패 시 텍스트 기반 응답 처리
                        print(f'✗ JSON 파싱 실패: {e}')
                        print(f'파싱 시도한 텍스트 (첫 500자):\n{text[:500]}')
                        # 파싱 실패 시 샘플 데이터 반환
                        return self._get_sample_data(days, region, travel_style, people_count, departure_location)

            # 응답이 비정상인 경우 샘플 데이터 반환
            return self._get_sample_data(days, region, travel_style, people_count, departure_location)

        except requests.exceptions.RequestException as e:
            print(f'GMS API 호출 오류: {e}')
            return self._get_sample_data(days, region, travel_style, people_count, departure_location)

    def _validate_budget(self, itinerary_data, budget, budget_min, budget_max):
        """예산 검증: 총 비용이 예산을 10% 초과했는지 확인"""
        if 'days' not in itinerary_data:
            return True  # 데이터가 없으면 검증 통과

        total_cost = 0
        for day in itinerary_data['days']:
            cost = day.get('estimated_cost', 0)
            if cost:
                total_cost += cost

        print(f'총 예상 비용: {total_cost:,}원 / 예산: {budget:,}원 (허용범위: 최대 {budget_max:,}원)')

        # 총 비용이 예산의 10%를 초과했을 때만 재생성 (예산보다 작으면 OK)
        if total_cost > budget_max:
            print(f'❌ 예산 초과! (예산 대비 {(total_cost / budget * 100):.1f}%, 초과 금액: {total_cost - budget:,}원)')
            return False

        print(f'✓ 예산 범위 내 ({(total_cost / budget * 100):.1f}%)')
        return True

    def _regenerate_with_budget_constraint(self, budget, people_count, start_date, end_date, departure_location,
                                          region, travel_style, accommodation_type, days,
                                          daily_budget, budget_min, budget_max,
                                          tourist_spots_str, restaurants_str, accommodations_str, festivals_str):
        """예산 제약을 더 강조하여 재생성"""
        budget_per_person = budget // people_count

        prompt = f"""
다음 조건으로 {days}일 여행 계획을 상세한 JSON 형식으로 작성해주세요:
- 총 예산: {budget:,}원 (총 {people_count}명, 1인당 약 {budget_per_person:,}원)
- 여행 인원: {people_count}명
- 여행 기간: {start_date} ~ {end_date} ({days}일)
- 출발지: {departure_location}
- 여행 지역: {region}
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
   - 출발지({departure_location})에서 여행 지역({region})으로의 이동 방법을 첫날 일정에 포함하세요
   - 주요 이동 구간별 교통수단 (버스, 지하철, 택시, 렌터카, KTX, 고속버스 등)
   - 예상 이동 시간 및 비용
   - 첫날에는 "{departure_location} → {region}" 이동 경로와 비용을 명시하세요

3. **숙소 정보** (accommodation_info):
   - {accommodation_type} 타입의 추천 숙소명 또는 숙소 지역
   - 예상 숙박비
   - 체크인/체크아웃 시간

4. **식사 정보** (meals_info) - **필수 항목입니다**:
   - 위의 추천 음식점 목록에서 선택하여 사용하세요
   - **반드시 아침, 점심, 저녁 각각의 추천 식당명 또는 음식 종류를 포함하세요**
   - 각 식사마다 예상 식사 비용을 포함하세요
   - meals_info는 반드시 "아침", "점심", "저녁" 키를 가진 객체여야 합니다

5. **축제/행사 정보** (events_info):
   - 위에 나열된 축제/행사 정보가 있다면 일정에 포함하세요
   - 축제명, 시간, 위치 등을 정확히 기재

6. **예상 비용** (estimated_cost):
   - 해당 일차의 총 예상 비용 (교통비 + 식비 + 입장료 + 숙박비 등)

JSON 형식 (정확히 이 구조를 따라주세요):
**반드시 "days" 배열에 정확히 {days}개의 일정 객체를 포함해야 합니다. day_number는 1부터 {days}까지 순서대로여야 합니다.**

{{
  "days": [
    {{
      "day_number": 1,
      "description": "일정 전체 요약",
      "attractions": [...],
      "transportation_info": {{
        "오전": "교통수단 및 비용",
        "오후": "교통수단 및 비용",
        "저녁": "교통수단 및 비용"
      }},
      "accommodation_info": {{
        "name": "숙소명",
        "cost": 80000,
        "check_in": "15:00",
        "check_out": "11:00"
      }},
      "meals_info": {{
        "아침": {{
          "restaurant": "식당명 또는 음식 종류",
          "cost": 10000
        }},
        "점심": {{
          "restaurant": "식당명 또는 음식 종류",
          "cost": 15000
        }},
        "저녁": {{
          "restaurant": "식당명 또는 음식 종류",
          "cost": 20000
        }}
      }},
      "events_info": [],
      "estimated_cost": {daily_budget}
    }}{f''',
    {{
      "day_number": {days},
      "description": "{days}일차 일정 요약",
      "attractions": [...],
      "transportation_info": {{...}},
      "accommodation_info": {{...}},
      "meals_info": {{...}},
      "events_info": [],
      "estimated_cost": {daily_budget}
    }}''' if days > 1 else ''}
  ]
}}

**중요: 모든 텍스트는 한글로 작성하세요**
- transportation_info의 키: "오전", "오후", "저녁" 사용 (morning, afternoon, evening 사용 금지)
- **meals_info는 반드시 포함되어야 하며, "아침", "점심", "저녁" 키를 모두 가져야 합니다** (breakfast, lunch, dinner 사용 금지)
- 각 일차마다 meals_info에 아침, 점심, 저녁 식사 정보를 반드시 포함하세요
- 모든 설명과 내용은 한글로 작성
- 시간 표기: "09:00", "15:00" 등 숫자는 그대로 사용
- 장소명과 상호명은 데이터베이스에 있는 그대로 사용

**⚠️ 예산 준수 규칙 (절대적으로 중요) ⚠️**:
- 총 예산: {budget:,}원 ({people_count}명 전체 기준)
- 일일 목표 예산: 약 {daily_budget:,}원
- **전체 {days}일간 총 비용 합계는 절대적으로 {budget_max:,}원을 초과하지 않아야 합니다 (예산의 110% 이하)**
- 예산보다 작게 생성되는 것은 문제없지만, 예산을 10% 초과하면 안 됩니다
- 첫 번째 시도에서 예산을 초과했으므로, 이번에는 더 저렴한 옵션을 선택하세요:
  * 게스트하우스나 모텔 등 저렴한 숙소 선택
  * 대중교통 이용 (택시 최소화)
  * 가성비 좋은 음식점 선택
  * 무료 관광지 우선 포함
- 각 일차별 비용이 {daily_budget:,}원을 크게 넘지 않도록 주의하세요

**기타 중요 사항**:
- 반드시 위에 제공된 실제 데이터베이스의 장소/음식점 목록에서 선택하여 사용하세요
- 장소명은 데이터베이스의 정확한 명칭을 그대로 사용하세요
- 모든 비용은 {people_count}명 전체를 기준으로 계산해주세요
- 이동 동선이 효율적이도록 근처 장소들을 묶어서 계획해주세요
- **각 일차마다 meals_info에 아침, 점심, 저녁 식사 정보를 반드시 포함해야 합니다. 이는 선택 사항이 아닌 필수 항목입니다.**
"""

        try:
            url = f'{self.base_url}?key={self.api_key}'
            headers = {'Content-Type': 'application/json'}
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

            if 'candidates' in result and len(result['candidates']) > 0:
                content = result['candidates'][0]['content']
                if 'parts' in content and len(content['parts']) > 0:
                    text = content['parts'][0]['text']

                    # 코드 블록 제거
                    if '```json' in text:
                        text = text.split('```json')[1].split('```')[0].strip()
                    elif '```' in text:
                        text = text.split('```')[1].split('```')[0].strip()

                    itinerary_data = json.loads(text)
                    days_count = len(itinerary_data.get("days", []))
                    print(f'✓ 재생성 성공! Days: {days_count}개 (요청: {days}일)')
                    
                    # 일수 검증
                    if days_count != days:
                        print(f'⚠️ 일수 불일치! 요청: {days}일, 생성: {days_count}일')
                        if days_count < days:
                            print(f'⚠️ 일정이 부족합니다. {days - days_count}일이 더 필요합니다.')
                    
                    # 식사 정보 검증
                    if 'days' in itinerary_data:
                        for i, day in enumerate(itinerary_data['days'], 1):
                            meals_info = day.get('meals_info', {})
                            if not meals_info or not isinstance(meals_info, dict):
                                print(f'⚠️ Day {i} - meals_info가 없거나 형식이 잘못되었습니다: {meals_info}')
                            else:
                                required_keys = ['아침', '점심', '저녁']
                                missing_keys = [key for key in required_keys if key not in meals_info]
                                if missing_keys:
                                    print(f'⚠️ Day {i} - meals_info에 누락된 키: {missing_keys}')
                                else:
                                    print(f'✓ Day {i} - meals_info 정상: {list(meals_info.keys())}')

                    # 재생성된 데이터도 예산 검증 (통과 여부와 관계없이 반환)
                    self._validate_budget(itinerary_data, budget, budget_min, budget_max)
                    return itinerary_data

        except Exception as e:
            print(f'재생성 실패: {e}')

        # 재생성 실패 시 샘플 데이터 반환
        return self._get_sample_data(days, region, travel_style, people_count, departure_location)

    def _parse_text_response(self, text, days, region, travel_style, people_count):
        """텍스트 응답을 파싱하여 구조화된 데이터로 변환"""
        return {
            'days': [
                {
                    'day_number': i + 1,
                    'description': f'{region} {travel_style} 여행 {i + 1}일차 - AI 추천 일정 ({people_count}명)'
                }
                for i in range(days)
            ]
        }

    def _get_sample_data(self, days, region, travel_style, people_count, departure_location='서울특별시'):
        """샘플 데이터 반환 (API 키가 없거나 오류 발생 시)"""
        sample_days = []
        for i in range(days):
            # 첫날에는 출발지에서 여행 지역으로의 이동 정보 포함
            if i == 0:
                transportation_info = {
                    '오전': f'{departure_location} → {region} 이동 (KTX 또는 고속버스, 예상 비용: 50,000원)',
                    '오후': '대중교통 이용 (예상 비용: 5,000원)',
                    '저녁': '도보 또는 택시'
                }
            else:
                transportation_info = {
                    '오전': '대중교통 이용 (예상 비용: 5,000원)',
                    '오후': '도보 또는 택시',
                    '저녁': '대중교통'
                }
            
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
                'transportation_info': transportation_info,
                'accommodation_info': {
                    'name': f'{region} 지역 숙소',
                    'cost': 80000,
                    'check_in': '15:00',
                    'check_out': '11:00'
                },
                'meals_info': {
                    '아침': {
                        'restaurant': '호텔 조식 또는 근처 식당',
                        'cost': 10000
                    },
                    '점심': {
                        'restaurant': f'{region} 맛집',
                        'cost': 15000
                    },
                    '저녁': {
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
