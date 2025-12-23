import requests
from django.conf import settings
from rest_framework.exceptions import ValidationError


class NaverOAuthService:
    """네이버 OAuth 인증 서비스"""

    NAVER_TOKEN_URL = "https://nid.naver.com/oauth2.0/token"
    NAVER_USER_INFO_URL = "https://openapi.naver.com/v1/nid/me"

    @classmethod
    def get_access_token(cls, code, state):
        """인가 코드로 액세스 토큰 받기"""
        data = {
            'grant_type': 'authorization_code',
            'client_id': settings.NAVER_CLIENT_ID,
            'client_secret': settings.NAVER_CLIENT_SECRET,
            'code': code,
            'state': state,
        }

        try:
            response = requests.post(cls.NAVER_TOKEN_URL, data=data)
            response.raise_for_status()
            token_data = response.json()
            
            # 에러 체크
            if 'error' in token_data:
                raise ValidationError(f"네이버 토큰 발급 실패: {token_data.get('error_description', token_data.get('error'))}")
            
            return token_data['access_token']
        except requests.exceptions.RequestException as e:
            raise ValidationError(f"네이버 토큰 발급 실패: {str(e)}")

    @classmethod
    def get_user_info(cls, access_token):
        """액세스 토큰으로 사용자 정보 가져오기"""
        headers = {
            'Authorization': f'Bearer {access_token}',
        }

        try:
            response = requests.get(cls.NAVER_USER_INFO_URL, headers=headers)
            response.raise_for_status()
            user_data = response.json()
            
            # 네이버 API 응답 구조: {"resultcode": "00", "message": "success", "response": {...}}
            if user_data.get('resultcode') != '00':
                raise ValidationError(f"네이버 사용자 정보 조회 실패: {user_data.get('message', 'Unknown error')}")
            
            naver_user = user_data.get('response', {})
            
            return {
                'naver_id': str(naver_user.get('id')),
                'email': naver_user.get('email', ''),
                'nickname': naver_user.get('nickname', ''),
                'name': naver_user.get('name', ''),
                'profile_image': naver_user.get('profile_image', ''),
            }
        except requests.exceptions.RequestException as e:
            raise ValidationError(f"네이버 사용자 정보 조회 실패: {str(e)}")

    @classmethod
    def revoke_token(cls, access_token):
        """네이버 액세스 토큰 취소"""
        try:
            response = requests.post(
                f'https://nid.naver.com/oauth2.0/token?grant_type=delete&client_id={settings.NAVER_CLIENT_ID}&client_secret={settings.NAVER_CLIENT_SECRET}&access_token={access_token}&service_provider=NAVER'
            )
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            raise ValidationError(f"네이버 토큰 취소 실패: {str(e)}")

