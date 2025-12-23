import os
import json
import requests
from dotenv import load_dotenv
from places.models import Place
from festivals.models import Festival

load_dotenv()


class GeminiService:
    """SSAFY GMS를 통한 Claude Sonnet 4 AI 서비스"""

    def __init__(self):
        self.api_key = os.getenv('GMS_API_KEY', '')
        # Anthropic Claude Sonnet 4 모델 (SSAFY GMS 프록시 경유)
        self.base_url = 'https://gms.ssafy.io/gmsapi/api.anthropic.com/v1/messages'
        self.model = 'claude-sonnet-4-20250514'

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

7. **일정 다양성 규칙 (중요)**:
   - 각 day_number(1일차, 2일차, 3일차 ...)의 일정은 서로 다른 코스로 구성해야 합니다
   - 단순히 동일한 일정을 복사하여 day_number만 바꾸면 안 됩니다
   - attractions, transportation_info, meals_info, events_info, estimated_cost를 각 일차마다 의미 있게 다르게 구성하세요
   - 예를 들어 1일차와 2일차의 관광지 목록과 식사 장소는 반드시 달라야 합니다

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

**반복/복사 금지 규칙 (매우 중요)**:
- 각 일차의 내용을 그대로 복사해서 붙여넣지 마세요
- 특히 attractions, meals_info, transportation_info는 각 일차마다 다른 장소/내용을 사용하세요
- 같은 장소를 여러 날에 사용할 수는 있지만, 그 경우에도 시간대나 동선, 함께 방문하는 다른 장소를 달리 구성하세요

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

        # SSAFY GMS API 호출 (Claude Sonnet 4)
        try:
            url = self.base_url
            headers = {
                'Content-Type': 'application/json',
                'x-api-key': self.api_key,
                'anthropic-version': '2023-06-01',
            }
            payload = {
                'model': self.model,
                'max_tokens': 4096,
                'messages': [
                    {
                        'role': 'user',
                        'content': prompt,
                    }
                ],
            }

            response = requests.post(url, headers=headers, json=payload, timeout=60)
            response.raise_for_status()

            result = response.json()

            # Claude API 응답 파싱
            if 'content' in result and isinstance(result['content'], list):
                # 여러 블록 중 text 타입만 이어붙이기
                text_parts = []
                for block in result['content']:
                    if isinstance(block, dict):
                        # SSAFY GMS는 { "type": "text", "text": "..." } 형태 사용
                        if block.get('type') == 'text' and 'text' in block:
                            text_parts.append(block['text'])
                text = ''.join(text_parts).strip()

                if text:

                    print('=== Claude API 원본 응답 ===')
                    print(f'응답 길이: {len(text)} 글자')
                    print(f'첫 200자: {text[:200]}')
                    print('=' * 50)

                    # JSON 파싱 시도
                    try:
                        # 텍스트에서 JSON 부분만 추출하여 파싱
                        itinerary_data = self._extract_json_from_text(text)
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

                        # 일정 다양성 검증: 모든 일차의 일정이 거의 동일하면 실패로 간주
                        if self._all_days_almost_same(itinerary_data):
                            print('⚠️ 모든 일차의 일정이 거의 동일합니다. 샘플(DB 기반) 데이터를 사용해 대체합니다.')
                            return self._get_sample_data(days, region, travel_style, people_count, departure_location)

                        # 예산 검증
                        if not self._validate_budget(itinerary_data, budget, budget_min, budget_max):
                            print('⚠️  예산 초과! 재생성을 시도합니다...')
                            # 재생성 시도 (최대 5회 반복)
                            max_retries = 5
                            retry_count = 0
                            
                            while retry_count < max_retries:
                                retry_count += 1
                                print(f'재생성 시도 {retry_count}/{max_retries}...')
                                
                                regenerated_data = self._regenerate_with_budget_constraint(
                                    budget, people_count, start_date, end_date, departure_location, region,
                                    travel_style, accommodation_type, days,
                                    daily_budget, budget_min, budget_max,
                                    tourist_spots_str, restaurants_str, accommodations_str, festivals_str,
                                    retry_count=retry_count - 1
                                )
                                
                                # 재생성된 데이터의 예산 검증
                                if regenerated_data and self._validate_budget(regenerated_data, budget, budget_min, budget_max):
                                    print(f'✓ 재생성 성공! ({retry_count}회 시도)')
                                    return regenerated_data
                                else:
                                    if retry_count < max_retries:
                                        print(f'⚠️ 재생성 {retry_count}회차도 예산 초과. 다시 시도합니다...')
                                    else:
                                        print(f'⚠️ 최대 재시도 횟수({max_retries}회)에 도달했습니다. 마지막 결과를 반환합니다.')
                                        return regenerated_data if regenerated_data else itinerary_data
                            
                            # 루프를 빠져나온 경우 (이론적으로는 발생하지 않음)
                            return regenerated_data if 'regenerated_data' in locals() else itinerary_data

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
                                          tourist_spots_str, restaurants_str, accommodations_str, festivals_str,
                                          retry_count=0):
        """예산 제약을 더 강조하여 재생성 (재시도 횟수 포함)"""
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

7. **일정 다양성 규칙 (중요)**:
   - 각 day_number의 일정은 서로 다른 코스로 구성해야 합니다
   - 단순 복사/붙여넣기 형태의 동일한 일정을 여러 날에 반복해서 사용하면 안 됩니다

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
- **이전 시도에서 예산을 초과했으므로, 이번에는 반드시 더 저렴한 옵션을 선택하세요** (재시도 횟수: {retry_count + 1}회):
  * 게스트하우스나 모텔 등 저렴한 숙소 선택 (호텔 피하기)
  * 대중교통 이용 (택시 최소화, 가능하면 도보)
  * 가성비 좋은 음식점 선택 (고급 레스토랑 피하기)
  * 무료 관광지 우선 포함 (유료 입장료 최소화)
  * 각 일차별 비용을 {daily_budget:,}원 이하로 유지
- **총 비용 합계가 {budget_max:,}원을 넘지 않도록 각 일차의 estimated_cost를 신중하게 계산하세요**

**반복/복사 금지 규칙 (매우 중요)**:
- 각 일차의 attractions, meals_info, transportation_info를 그대로 복사하지 마세요
- 재생성 시에도 1일차, 2일차, 3일차 등은 서로 다른 일정이 되도록 구성하세요

**기타 중요 사항**:
- 반드시 위에 제공된 실제 데이터베이스의 장소/음식점 목록에서 선택하여 사용하세요
- 장소명은 데이터베이스의 정확한 명칭을 그대로 사용하세요
- 모든 비용은 {people_count}명 전체를 기준으로 계산해주세요
- 이동 동선이 효율적이도록 근처 장소들을 묶어서 계획해주세요
- **각 일차마다 meals_info에 아침, 점심, 저녁 식사 정보를 반드시 포함해야 합니다. 이는 선택 사항이 아닌 필수 항목입니다.**
"""

        try:
            url = self.base_url
            headers = {
                'Content-Type': 'application/json',
                'x-api-key': self.api_key,
                'anthropic-version': '2023-06-01',
            }
            payload = {
                'model': self.model,
                'max_tokens': 4096,
                'messages': [
                    {
                        'role': 'user',
                        'content': prompt,
                    }
                ],
            }

            response = requests.post(url, headers=headers, json=payload, timeout=60)
            response.raise_for_status()
            result = response.json()

            # Claude API 응답 파싱
            if 'content' in result and isinstance(result['content'], list):
                text_parts = []
                for block in result['content']:
                    if isinstance(block, dict) and block.get('type') == 'text' and 'text' in block:
                        text_parts.append(block['text'])
                text = ''.join(text_parts).strip()

                if text:

                    # 텍스트에서 JSON 부분만 추출하여 파싱
                    itinerary_data = self._extract_json_from_text(text)
                    if isinstance(itinerary_data, list):
                        itinerary_data = {'days': itinerary_data}
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

                    # 재생성된 데이터도 예산 검증
                    if self._validate_budget(itinerary_data, budget, budget_min, budget_max):
                        print(f'✓ 재생성된 계획이 예산 범위 내입니다.')
                    else:
                        print(f'⚠️ 재생성된 계획도 여전히 예산을 초과합니다.')
                    
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
        """
        샘플 데이터 반환 (API 키가 없거나 오류 발생 시)
        - 실제 DB의 장소/음식점/숙소/축제 데이터를 사용
        - 각 일차마다 다른 코스로 구성하여 "복붙"처럼 보이지 않도록 함
        """
        try:
            tourist_spots = self._get_places_by_region(region, 'tourist', limit=30)
            restaurants = self._get_places_by_region(region, 'restaurant', limit=30)
            accommodations = self._get_places_by_region(region, 'accommodation', limit=10)
            # 축제는 대략적인 기간 정보만 사용
            festivals = self._get_festivals_by_region(region, days and days >= 1 and None or None, None, None)
        except Exception:
            tourist_spots, restaurants, accommodations, festivals = [], [], [], []

        # 이름 리스트로 변환
        tourist_list = list(tourist_spots)
        restaurant_list = list(restaurants)
        accommodation_list = list(accommodations)

        sample_days = []
        for i in range(days):
            day_number = i + 1

            # 첫날에는 출발지 → 지역 이동 포함
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

            # 관광지: 날짜마다 시작 인덱스를 다르게 해서 다른 조합 사용
            day_attractions = []
            if tourist_list:
                for j in range(3):
                    idx = (i * 3 + j) % len(tourist_list)
                    place = tourist_list[idx]
                    day_attractions.append({
                        'name': place.title,
                        'time': f'{9 + j * 2}:00',
                        'duration': '2시간',
                        'description': place.address,
                    })
            else:
                # DB에 데이터가 없을 때의 최소한의 더미
                for j in range(3):
                    day_attractions.append({
                        'name': f'{region} 대표 관광지 {day_number}-{j + 1}',
                        'time': f'{9 + j * 2}:00',
                        'duration': '2시간',
                        'description': f'{region}의 유명한 명소',
                    })

            # 식사: 각 일차마다 다른 식당을 쓰도록 인덱스 회전
            def _pick_restaurant(offset):
                if restaurant_list:
                    place = restaurant_list[(i + offset) % len(restaurant_list)]
                    return {
                        'restaurant': place.title,
                        'cost': 15000,
                    }
                return {
                    'restaurant': f'{region} 맛집 {day_number}-{offset + 1}',
                    'cost': 15000,
                }

            meals_info = {
                '아침': {
                    'restaurant': '호텔 조식 또는 근처 식당',
                    'cost': 10000,
                },
                '점심': _pick_restaurant(0),
                '저녁': _pick_restaurant(1),
            }

            # 숙소: 여러 개가 있으면 날짜별로 다른 숙소 사용
            if accommodation_list:
                acc = accommodation_list[i % len(accommodation_list)]
                accommodation_info = {
                    'name': acc.title,
                    'cost': 80000,
                    'check_in': '15:00',
                    'check_out': '11:00',
                }
            else:
                accommodation_info = {
                    'name': f'{region} 지역 숙소 {day_number}',
                    'cost': 80000,
                    'check_in': '15:00',
                    'check_out': '11:00',
                }

            sample_days.append({
                'day_number': day_number,
                'description': f'{region} {travel_style} 여행 {day_number}일차 - 추천 코스',
                'attractions': day_attractions,
                'transportation_info': transportation_info,
                'accommodation_info': accommodation_info,
                'meals_info': meals_info,
                'events_info': [],
                'estimated_cost': 130000,
            })

        return {'days': sample_days}

    def _extract_json_from_text(self, text):
        """
        LLM 응답 텍스트에서 JSON 부분만 안전하게 추출하여 dict로 반환
        - ```json ... ``` 코드블록 우선 사용
        - 없으면 첫 '{'부터 마지막 '}'까지를 잘라서 파싱 시도
        """
        original_text = text

        # 0) 전체 텍스트를 그대로 JSON으로 해석해보기 (이미 순수 JSON일 수 있음)
        try:
            stripped = text.strip()
            if stripped:
                return json.loads(stripped)
        except Exception:
            # 실패하면 아래 단계들 진행
            pass

        # 1) ```json 코드블록 처리
        if '```json' in text:
            try:
                body = text.split('```json', 1)[1].split('```', 1)[0].strip()
                return json.loads(body)
            except Exception:
                text = original_text

        # 2) 일반 ``` 코드블록 처리
        if '```' in text:
            try:
                body = text.split('```', 1)[1].split('```', 1)[0].strip()
                return json.loads(body)
            except Exception:
                text = original_text

        # 3) 자연어 설명 + JSON 형태: 첫 '{' ~ 마지막 '}' 구간만 추출
        first_brace = text.find('{')
        last_brace = text.rfind('}')
        if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
            candidate = text[first_brace:last_brace + 1].strip()
            try:
                return json.loads(candidate)
            except json.JSONDecodeError as e:
                print('✗ _extract_json_from_text JSONDecodeError:', e)
                print('추출된 candidate 앞 300자:\n', candidate[:300])
                raise

        # 어떤 형태로도 JSON을 찾지 못한 경우
        raise json.JSONDecodeError('No valid JSON object found in text', original_text, 0)

    def _all_days_almost_same(self, itinerary_data):
        """
        모든 일차의 내용이 거의 동일한지 검사
        - day_number, description을 제외한 나머지 필드가 모두 동일하면 "복붙"으로 간주
        """
        days = itinerary_data.get('days') or []
        if len(days) <= 1:
            return False

        normalized = []
        for day in days:
            # 비교에 사용하지 않을 키 제거
            cmp_day = dict(day)
            cmp_day.pop('day_number', None)
            cmp_day.pop('description', None)
            # 정렬된 JSON 문자열로 변환하여 비교
            try:
                normalized.append(json.dumps(cmp_day, sort_keys=True, ensure_ascii=False))
            except TypeError:
                # JSON으로 직렬화 안 되는 값이 있으면 문자열 변환
                normalized.append(str(cmp_day))

        return len(set(normalized)) == 1

    def _build_region_candidates(self, region: str):
        """
        지역 문자열에서 검색에 사용할 후보 키워드 목록 생성
        예) "부산광역시" -> ["부산광역시", "부산"]
            "서울특별시 강남구" -> ["서울특별시 강남구", "서울특별시", "서울", "강남구", "강남"]
        """
        if not region:
            return []

        region = region.strip()
        candidates = set()

        # 1차: 전체 문자열
        candidates.add(region)

        # 2차: 공백으로 나눈 토큰들
        parts = [p for p in region.split() if p]
        if parts:
            for p in parts:
                candidates.add(p)

        # 3차: 행정구역 접미사 제거 버전
        suffixes = ['광역시', '특별시', '시', '군', '구', '도']
        for text in list(candidates):
            for suf in suffixes:
                if text.endswith(suf) and len(text) > len(suf):
                    candidates.add(text[: -len(suf)])

        # 빈 문자열 제거
        return [c for c in candidates if c]

    def _get_places_by_region(self, region, place_type, limit=10):
        """지역과 타입으로 장소 검색 (여러 후보 키워드로 순차 검색)"""
        try:
            candidates = self._build_region_candidates(region)
            print(f'[Place 검색] region="{region}", candidates={candidates}, type={place_type}')

            for keyword in candidates:
                qs = Place.objects.filter(
                    region__icontains=keyword,
                    place_type=place_type
                )[:limit]
                places = list(qs)
                if places:
                    print(f'[Place 검색] "{keyword}" 로 {len(places)}개 찾음')
                    return places

            print(f'[Place 검색] "{region}" 에 대한 장소를 찾지 못했습니다. place_type={place_type}')
            return []
        except Exception as e:
            print(f'장소 조회 오류: {e}')
            return []

    def _get_festivals_by_region(self, region, start_date, end_date):
        """지역과 기간으로 축제 검색 (여러 후보 키워드로 순차 검색)"""
        try:
            month = start_date.month
            candidates = self._build_region_candidates(region)
            print(f'[Festival 검색] region="{region}", candidates={candidates}, month={month}')

            for keyword in candidates:
                qs = Festival.objects.filter(
                    region__icontains=keyword,
                    start_month=month,
                    is_active=True
                )[:5]
                festivals = list(qs)
                if festivals:
                    print(f'[Festival 검색] "{keyword}" 로 {len(festivals)}개 찾음')
                    return festivals

            print(f'[Festival 검색] "{region}" 에 대한 축제를 찾지 못했습니다. month={month}')
            return []
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

    def modify_itinerary(self, existing_plan, requirements, budget, people_count, start_date, end_date, departure_location, region, travel_style, accommodation_type):
        """
        기존 여행 계획을 사용자 요구사항에 맞게 수정
        """
        # 여행 일수 계산
        days = (end_date - start_date).days + 1
        
        # 기존 일정을 JSON 형식으로 포맷팅
        existing_itinerary_str = self._format_existing_itinerary(existing_plan)
        
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
        
        # 일일 예산 계산
        daily_budget = budget // days
        budget_max = int(budget * 1.1)
        
        # 기존 일정을 JSON 형식으로 변환
        existing_days_data = []
        for itinerary in existing_plan.itineraries.all().order_by('day_number'):
            existing_days_data.append({
                'day_number': itinerary.day_number,
                'description': itinerary.description,
                'attractions': itinerary.attractions or [],
                'transportation_info': itinerary.transportation_info or {},
                'accommodation_info': itinerary.accommodation_info or {},
                'meals_info': itinerary.meals_info or {},
                'events_info': itinerary.events_info or [],
                'estimated_cost': itinerary.estimated_cost or 0
            })
        
        existing_json = json.dumps(existing_days_data, ensure_ascii=False, indent=2)
        
        # 프롬프트 생성
        prompt = f"""
다음은 기존 여행 계획입니다. **기존 계획을 최대한 유지하면서** 사용자의 요구사항에 맞게 **부분적으로만 수정**해주세요.

**⚠️ 매우 중요: 기존 계획의 구조와 내용을 최대한 유지하세요. 요구사항에 명시되지 않은 부분은 그대로 유지해야 합니다.**

**기존 여행 계획 (JSON 형식):**
```json
{existing_json}
```

**사용자 요구사항:**
{requirements}

**기본 여행 정보:**
- 총 예산: {budget:,}원 (총 {people_count}명, 1인당 약 {budget // people_count:,}원)
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

**수정 지침 (매우 중요):**
1. **기존 계획의 구조를 그대로 유지하세요** - day_number, 일정 순서, 전체적인 흐름은 변경하지 마세요
2. **요구사항에 명시된 부분만 수정하세요** - 예를 들어 "2일차 저녁 식사"만 언급되었다면, 2일차 저녁 식사만 변경하고 나머지는 그대로 유지
3. **요구사항에 해당하지 않는 일정은 기존 내용을 그대로 반환하세요**
4. 예산은 {budget:,}원을 초과하지 않도록 주의하세요 (최대 {budget_max:,}원)
5. **반드시 {days}일치 일정을 모두 반환해야 하며, 각 일정의 day_number는 기존과 동일해야 합니다**
6. 각 일차마다 meals_info에 아침, 점심, 저녁 식사 정보를 반드시 포함하세요
7. **기존 계획에서 좋은 부분(요구사항과 무관한 부분)은 절대 변경하지 마세요**
8. **설명 문장, 해설, 코드블록(```` ````, ```json```)은 절대 출력하지 말고, 오직 하나의 JSON 객체만 출력하세요.**
9. **"meals_info" 일부만 출력하거나 특정 일차만 따로 출력하지 말고, 항상 전체 일차를 포함한 완전한 JSON 객체를 출력해야 합니다.**

JSON 형식 (정확히 이 구조를 따라주세요):
{{
  "days": [
    {{
      "day_number": 1,
      "description": "수정된 일정 전체 요약",
      "attractions": [
        {{
          "name": "관광지명",
          "time": "09:00",
          "duration": "2시간",
          "description": "관광지 설명"
        }}
      ],
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
      "description": "수정된 {days}일차 일정 요약",
      "attractions": [...],
      "transportation_info": {{...}},
      "accommodation_info": {{...}},
      "meals_info": {{...}},
      "events_info": [],
      "estimated_cost": {daily_budget}
    }}''' if days > 1 else ''}
  ]
}}

**중요 출력 규칙:**
- 출력은 반드시 **위 JSON 객체 하나만** 포함해야 합니다.
- JSON 앞뒤에 자연어 설명, 요약 문장, 마크다운, 코드블록 기호( ``` ) 등을 절대 추가하지 마세요.
- transportation_info의 키: "오전", "오후", "저녁" 사용
- meals_info는 반드시 "아침", "점심", "저녁" 키를 모두 가져야 합니다
- 사용자 요구사항을 반드시 반영하세요
- 예산을 준수하세요
"""

        # API 키가 없으면 기존 계획 반환
        if not self.api_key:
            print('경고: GMS_API_KEY가 설정되지 않았습니다. 기존 계획을 반환합니다.')
            return self._get_existing_itinerary_data(existing_plan)
        
        # SSAFY GMS API 호출 (Claude Sonnet 4)
        try:
            url = self.base_url
            headers = {
                'Content-Type': 'application/json',
                'x-api-key': self.api_key,
                'anthropic-version': '2023-06-01',
            }
            payload = {
                'model': self.model,
                'max_tokens': 4096,
                'messages': [
                    {
                        'role': 'user',
                        'content': prompt,
                    }
                ],
            }
            
            response = requests.post(url, headers=headers, json=payload, timeout=60)
            response.raise_for_status()
            
            result = response.json()
            
            # Claude API 응답 파싱
            if 'content' in result and isinstance(result['content'], list):
                text_parts = []
                for block in result['content']:
                    if isinstance(block, dict) and block.get('type') == 'text' and 'text' in block:
                        text_parts.append(block['text'])
                text = ''.join(text_parts).strip()
                
                if text:
                    
                    print('=== 수정된 계획 API 원본 응답 ===')
                    print(f'응답 길이: {len(text)} 글자')
                    print(f'첫 200자: {text[:200]}')
                    print('=' * 50)
                    
                    # JSON 파싱 시도
                    try:
                        # 텍스트에서 JSON 부분만 추출하여 파싱
                        itinerary_data = self._extract_json_from_text(text)
                        if isinstance(itinerary_data, list):
                            itinerary_data = {'days': itinerary_data}
                        # 모델이 [ {...}, {...} ] 형태의 배열만 보낸 경우 보정
                        if isinstance(itinerary_data, list):
                            itinerary_data = {'days': itinerary_data}
                        days_count = len(itinerary_data.get("days", []))
                        print(f'✓ 수정된 계획 JSON 파싱 성공! Days: {days_count}개 (요청: {days}일)')
                        
                        # 일수 검증
                        if days_count != days:
                            print(f'⚠️ 일수 불일치! 요청: {days}일, 생성: {days_count}일')
                        
                        # 예산 검증
                        self._validate_budget(itinerary_data, budget, int(budget * 0.9), budget_max)
                        
                        return itinerary_data
                    except json.JSONDecodeError as e:
                        print(f'✗ JSON 파싱 실패: {e}')
                        print(f'파싱 시도한 텍스트 (첫 500자):\n{text[:500]}')
                        return self._get_existing_itinerary_data(existing_plan)
            
            # 응답이 비정상인 경우 기존 계획 반환
            return self._get_existing_itinerary_data(existing_plan)
            
        except requests.exceptions.RequestException as e:
            print(f'GMS API 호출 오류: {e}')
            return self._get_existing_itinerary_data(existing_plan)

    def _format_existing_itinerary(self, travel_plan):
        """기존 여행 계획을 프롬프트용 문자열로 포맷팅"""
        if not travel_plan or not hasattr(travel_plan, 'itineraries'):
            return "기존 계획 정보가 없습니다."
        
        formatted = []
        formatted.append(f"제목: {travel_plan.title}")
        formatted.append(f"예산: {travel_plan.budget:,}원")
        formatted.append(f"인원: {travel_plan.people_count}명")
        formatted.append(f"기간: {travel_plan.start_date} ~ {travel_plan.end_date}")
        formatted.append(f"지역: {travel_plan.region}")
        formatted.append(f"스타일: {travel_plan.travel_style}")
        formatted.append(f"숙박: {travel_plan.accommodation_type}")
        formatted.append("")
        formatted.append("일정:")
        
        for itinerary in travel_plan.itineraries.all().order_by('day_number'):
            formatted.append(f"\n[Day {itinerary.day_number}] {itinerary.date}")
            formatted.append(f"설명: {itinerary.description}")
            
            if itinerary.attractions:
                formatted.append("관광지:")
                for attr in itinerary.attractions:
                    if isinstance(attr, dict):
                        formatted.append(f"  - {attr.get('name', '')} ({attr.get('time', '')}, {attr.get('duration', '')})")
            
            if itinerary.transportation_info:
                formatted.append("교통:")
                for key, value in itinerary.transportation_info.items():
                    formatted.append(f"  - {key}: {value}")
            
            if itinerary.accommodation_info:
                acc = itinerary.accommodation_info
                if isinstance(acc, dict):
                    formatted.append(f"숙소: {acc.get('name', '')} ({acc.get('cost', 0):,}원)")
            
            if itinerary.meals_info:
                formatted.append("식사:")
                for meal_time, meal_info in itinerary.meals_info.items():
                    if isinstance(meal_info, dict):
                        formatted.append(f"  - {meal_time}: {meal_info.get('restaurant', '')} ({meal_info.get('cost', 0):,}원)")
                    else:
                        formatted.append(f"  - {meal_time}: {meal_info}")
            
            if itinerary.estimated_cost:
                formatted.append(f"예상 비용: {itinerary.estimated_cost:,}원")
        
        return "\n".join(formatted)

    def _get_existing_itinerary_data(self, travel_plan):
        """기존 여행 계획을 JSON 형식으로 변환"""
        days = []
        for itinerary in travel_plan.itineraries.all().order_by('day_number'):
            days.append({
                'day_number': itinerary.day_number,
                'description': itinerary.description,
                'attractions': itinerary.attractions or [],
                'transportation_info': itinerary.transportation_info or {},
                'accommodation_info': itinerary.accommodation_info or {},
                'meals_info': itinerary.meals_info or {},
                'events_info': itinerary.events_info or [],
                'estimated_cost': itinerary.estimated_cost or 0
            })
        return {'days': days}


