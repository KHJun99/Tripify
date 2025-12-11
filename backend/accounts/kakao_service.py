import requests
from django.conf import settings
from rest_framework.exceptions import ValidationError


class KakaoOAuthService:
    """카카오 OAuth 인증 서비스"""

    KAKAO_TOKEN_URL = "https://kauth.kakao.com/oauth/token"
    KAKAO_USER_INFO_URL = "https://kapi.kakao.com/v2/user/me"

    @classmethod
    def get_access_token(cls, code):
        """인가 코드로 액세스 토큰 받기"""
        data = {
            'grant_type': 'authorization_code',
            'client_id': settings.KAKAO_REST_API_KEY,
            'redirect_uri': settings.KAKAO_REDIRECT_URI,
            'code': code,
        }

        if settings.KAKAO_CLIENT_SECRET:
            data['client_secret'] = settings.KAKAO_CLIENT_SECRET

        try:
            response = requests.post(cls.KAKAO_TOKEN_URL, data=data)
            response.raise_for_status()
            token_data = response.json()
            return token_data['access_token']
        except requests.exceptions.RequestException as e:
            raise ValidationError(f"카카오 토큰 발급 실패: {str(e)}")

    @classmethod
    def get_user_info(cls, access_token):
        """액세스 토큰으로 사용자 정보 가져오기"""
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
        }

        try:
            response = requests.get(cls.KAKAO_USER_INFO_URL, headers=headers)
            response.raise_for_status()
            user_data = response.json()

            kakao_account = user_data.get('kakao_account', {})
            profile = kakao_account.get('profile', {})

            return {
                'kakao_id': str(user_data.get('id')),
                'email': kakao_account.get('email', ''),
                'nickname': profile.get('nickname', ''),
                'profile_image': profile.get('profile_image_url', ''),
            }
        except requests.exceptions.RequestException as e:
            raise ValidationError(f"카카오 사용자 정보 조회 실패: {str(e)}")

    @classmethod
    def unlink_user(cls, access_token):
        """카카오 연결 끊기"""
        headers = {
            'Authorization': f'Bearer {access_token}',
        }

        try:
            response = requests.post(
                'https://kapi.kakao.com/v1/user/unlink',
                headers=headers
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise ValidationError(f"카카오 연결 끊기 실패: {str(e)}")
