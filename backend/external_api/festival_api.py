import os
import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()


class FestivalAPI:
    """축제/행사 정보 API 서비스"""

    def __init__(self):
        self.api_key = os.getenv('TOUR_API_KEY', '')
        self.base_url = 'http://apis.data.go.kr/B551011/KorService1'

    def search_festivals(self, month=None, region=None, year=None):
        """축제/행사 검색"""
        # areaBasedList1 엔드포인트 사용 (더 안정적)
        endpoint = f'{self.base_url}/areaBasedList1'

        # 연도 설정 (기본값: 현재 연도)
        if year is None:
            year = datetime.now().year

        params = {
            'serviceKey': self.api_key,
            'numOfRows': 100,
            'pageNo': 1,
            'MobileOS': 'ETC',
            'MobileApp': 'Tripify',
            '_type': 'json',
            'listYN': 'Y',
            'arrange': 'O',  # 제목순 정렬
            'contentTypeId': 15  # 15 = 축제/공연/행사
        }

        if region:
            params['areaCode'] = self._get_area_code(region)

        try:
            response = requests.get(endpoint, params=params, timeout=10)

            # 상태 코드 확인
            if response.status_code != 200:
                print(f'API 오류 (HTTP {response.status_code}): {response.text[:200]}')
                return None

            # JSON 응답 파싱
            try:
                data = response.json()

                # 응답 구조 확인
                if 'response' not in data:
                    print(f'예상치 못한 응답 구조: {str(data)[:200]}')
                    return None

                # 에러 코드 확인
                header = data.get('response', {}).get('header', {})
                result_code = header.get('resultCode', '')
                result_msg = header.get('resultMsg', '')

                if result_code != '0000':
                    print(f'API 에러 코드: {result_code}, 메시지: {result_msg}')
                    return None

                return data

            except ValueError as e:
                print(f'JSON 파싱 오류: {e}')
                print(f'응답 내용: {response.text[:500]}')
                return None

        except requests.exceptions.Timeout:
            print('FestivalAPI 오류: 요청 시간 초과')
            return None
        except requests.exceptions.RequestException as e:
            print(f'FestivalAPI 오류: {e}')
            return None
        except Exception as e:
            print(f'FestivalAPI 예상치 못한 오류: {e}')
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
