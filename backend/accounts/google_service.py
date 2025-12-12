import requests
from django.conf import settings
from rest_framework.exceptions import ValidationError


class GoogleOAuthService:
    """구글 OAuth 인증 서비스"""

    GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
    GOOGLE_USER_INFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"

    @classmethod
    def get_access_token(cls, code):
        """인가 코드로 액세스 토큰 받기"""
        data = {
            'code': code,
            'client_id': settings.GOOGLE_CLIENT_ID,
            'client_secret': settings.GOOGLE_CLIENT_SECRET,
            'redirect_uri': settings.GOOGLE_REDIRECT_URI,
            'grant_type': 'authorization_code',
        }

        try:
            response = requests.post(cls.GOOGLE_TOKEN_URL, data=data)
            response.raise_for_status()
            token_data = response.json()
            return token_data['access_token']
        except requests.exceptions.RequestException as e:
            raise ValidationError(f"구글 토큰 발급 실패: {str(e)}")

    @classmethod
    def get_user_info(cls, access_token):
        """액세스 토큰으로 사용자 정보 가져오기"""
        headers = {
            'Authorization': f'Bearer {access_token}',
        }

        try:
            response = requests.get(cls.GOOGLE_USER_INFO_URL, headers=headers)
            response.raise_for_status()
            user_data = response.json()

            return {
                'google_id': str(user_data.get('id')),
                'email': user_data.get('email', ''),
                'name': user_data.get('name', ''),
                'picture': user_data.get('picture', ''),
            }
        except requests.exceptions.RequestException as e:
            raise ValidationError(f"구글 사용자 정보 조회 실패: {str(e)}")

    @classmethod
    def revoke_token(cls, access_token):
        """구글 액세스 토큰 취소"""
        try:
            response = requests.post(
                f'https://oauth2.googleapis.com/revoke?token={access_token}'
            )
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as e:
            raise ValidationError(f"구글 토큰 취소 실패: {str(e)}")
