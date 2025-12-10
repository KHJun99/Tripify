import os
import json
from dotenv import load_dotenv

load_dotenv()


class GeminiService:
    """Google Gemini AI 서비스"""

    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY', '')

    def generate_itinerary(self, budget, start_date, end_date, region, travel_style, accommodation_type):
        """
        AI를 사용하여 여행 일정을 생성
        실제 환경에서는 Google Gemini API를 호출
        """
        # 여행 일수 계산
        days = (end_date - start_date).days + 1

        # 프롬프트 생성
        prompt = f"""
        다음 조건으로 {days}일 여행 계획을 추천해주세요:
        - 예산: {budget}원
        - 여행 기간: {start_date} ~ {end_date} ({days}일)
        - 지역: {region}
        - 여행 스타일: {travel_style}
        - 숙박 타입: {accommodation_type}

        각 일차별로 추천 장소와 활동을 포함해주세요.
        """

        # TODO: 실제 Gemini API 호출
        # 현재는 샘플 데이터 반환
        return {
            'days': [
                {
                    'day_number': i + 1,
                    'description': f'{region} {travel_style} 여행 {i + 1}일차'
                }
                for i in range(days)
            ]
        }
