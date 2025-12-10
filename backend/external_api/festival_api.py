import os
import requests
from dotenv import load_dotenv

load_dotenv()


class FestivalAPI:
    """축제/행사 정보 API 서비스"""

    def __init__(self):
        self.api_key = os.getenv('TOUR_API_KEY', '')
        self.base_url = 'http://apis.data.go.kr/B551011/KorService1'

    def search_festivals(self, month=None, region=None):
        """축제/행사 검색"""
        endpoint = f'{self.base_url}/searchFestival1'
        params = {
            'serviceKey': self.api_key,
            'numOfRows': 20,
            'pageNo': 1,
            'MobileOS': 'ETC',
            'MobileApp': 'Tripify',
            '_type': 'json',
            'listYN': 'Y',
            'arrange': 'A'
        }

        if month:
            params['eventStartDate'] = f'2024{month:02d}01'

        if region:
            params['areaCode'] = self._get_area_code(region)

        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f'FestivalAPI 오류: {e}')
            return None

    def _get_area_code(self, region):
        """지역명을 area code로 변환"""
        area_codes = {
            '서울': 1,
            '인천': 2,
            '대전': 3,
            '대구': 4,
            '광주': 5,
            '부산': 6,
            '울산': 7,
            '세종': 8,
            '경기': 31,
            '강원': 32,
            '충북': 33,
            '충남': 34,
            '경북': 35,
            '경남': 36,
            '전북': 37,
            '전남': 38,
            '제주': 39
        }
        return area_codes.get(region, 1)
