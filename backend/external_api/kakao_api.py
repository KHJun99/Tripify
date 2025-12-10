import os
import requests
from dotenv import load_dotenv

load_dotenv()


class KakaoAPI:
    """카카오 API 서비스 (지도, 장소 검색)"""

    def __init__(self):
        self.rest_api_key = os.getenv('KAKAO_REST_API_KEY', '')
        self.base_url = 'https://dapi.kakao.com'

    def search_place(self, query, x=None, y=None, radius=None):
        """장소 검색"""
        endpoint = f'{self.base_url}/v2/local/search/keyword.json'
        headers = {
            'Authorization': f'KakaoAK {self.rest_api_key}'
        }
        params = {
            'query': query,
            'size': 15
        }

        if x and y:
            params['x'] = x
            params['y'] = y

        if radius:
            params['radius'] = radius

        try:
            response = requests.get(endpoint, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f'KakaoAPI 오류: {e}')
            return None

    def get_address(self, x, y):
        """좌표로 주소 조회"""
        endpoint = f'{self.base_url}/v2/local/geo/coord2address.json'
        headers = {
            'Authorization': f'KakaoAK {self.rest_api_key}'
        }
        params = {
            'x': x,
            'y': y
        }

        try:
            response = requests.get(endpoint, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f'KakaoAPI 주소 조회 오류: {e}')
            return None
