import os
import requests
from dotenv import load_dotenv

load_dotenv()


class TourAPI:
    """한국관광공사 TourAPI 서비스"""

    def __init__(self):
        self.api_key = os.getenv('TOUR_API_KEY', '')
        self.base_url = 'http://apis.data.go.kr/B551011/KorService1'

    def search_tourist_spots(self, region=None, keyword=None):
        """관광지 검색"""
        endpoint = f'{self.base_url}/searchKeyword1'
        params = {
            'serviceKey': self.api_key,
            'numOfRows': 10,
            'pageNo': 1,
            'MobileOS': 'ETC',
            'MobileApp': 'Tripify',
            '_type': 'json'
        }

        if keyword:
            params['keyword'] = keyword

        if region:
            params['areaCode'] = self._get_area_code(region)

        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f'TourAPI 오류: {e}')
            return None

    def get_detail(self, content_id):
        """관광지 상세 정보 조회"""
        endpoint = f'{self.base_url}/detailCommon1'
        params = {
            'serviceKey': self.api_key,
            'contentId': content_id,
            'MobileOS': 'ETC',
            'MobileApp': 'Tripify',
            '_type': 'json',
            'defaultYN': 'Y',
            'firstImageYN': 'Y',
            'addrinfoYN': 'Y',
            'mapinfoYN': 'Y',
            'overviewYN': 'Y'
        }

        try:
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f'TourAPI 상세 조회 오류: {e}')
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
