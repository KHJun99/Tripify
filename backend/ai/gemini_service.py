import os
import json
import requests
from dotenv import load_dotenv

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

        # 프롬프트 생성
        prompt = f"""
다음 조건으로 {days}일 여행 계획을 JSON 형식으로 작성해주세요:
- 예산: {budget:,}원
- 여행 기간: {start_date} ~ {end_date} ({days}일)
- 지역: {region}
- 여행 스타일: {travel_style}
- 숙박 타입: {accommodation_type}

각 일차별로 다음 정보를 포함해주세요:
1. 방문할 관광지 3-5곳
2. 추천 식당 (점심, 저녁)
3. 예상 소요 시간
4. 대략적인 일정 예산

JSON 형식:
{{
  "days": [
    {{
      "day_number": 1,
      "description": "일정 요약",
      "places": ["장소1", "장소2", "장소3"],
      "meals": {{"lunch": "점심 식당", "dinner": "저녁 식당"}},
      "budget": 예상금액
    }}
  ]
}}
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

                    # JSON 파싱 시도
                    try:
                        # 코드 블록 제거 (```json ... ``` 형식)
                        if '```json' in text:
                            text = text.split('```json')[1].split('```')[0].strip()
                        elif '```' in text:
                            text = text.split('```')[1].split('```')[0].strip()

                        itinerary_data = json.loads(text)
                        return itinerary_data
                    except json.JSONDecodeError:
                        # JSON 파싱 실패 시 텍스트 기반 응답 처리
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
        return {
            'days': [
                {
                    'day_number': i + 1,
                    'description': f'{region} {travel_style} 여행 {i + 1}일차'
                }
                for i in range(days)
            ]
        }
