from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, get_user_model
from django.db import IntegrityError
from .serializers import SignupSerializer, LoginSerializer, UserSerializer, PasswordResetRequestSerializer, PasswordResetConfirmSerializer, UsernameRecoverySerializer, AccountDeletionSerializer
from .kakao_service import KakaoOAuthService
from .google_service import GoogleOAuthService
from .models import EmailVerificationToken, PasswordResetToken
from .email_utils import send_verification_email, send_password_reset_email, send_username_recovery_email

User = get_user_model()


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    """회원가입 API - 이메일 인증 필요"""
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()

        # 이메일 인증 토큰 생성 및 메일 발송
        try:
            verification_token = EmailVerificationToken.create_token(user)
            send_verification_email(user, verification_token)

            return Response({
                'username': user.username,
                'email': user.email,
                'message': '회원가입이 완료되었습니다. 이메일을 확인하여 인증을 완료해주세요.',
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            # 이메일 전송 실패 시에도 회원가입은 완료
            return Response({
                'username': user.username,
                'email': user.email,
                'message': '회원가입이 완료되었습니다. 이메일 전송에 실패했습니다.',
                'error': str(e)
            }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """로그인 API"""
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            # 일반 로그인 사용자의 경우 이메일 인증 확인
            if user.login_type == 'normal' and not user.is_email_verified:
                return Response({
                    'error': '이메일 인증이 필요합니다. 가입 시 받은 이메일을 확인해주세요.',
                    'email_verified': False
                }, status=status.HTTP_403_FORBIDDEN)

            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'username': user.username,
                'user_id': user.id,
                'email_verified': user.is_email_verified,
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'error': '아이디 또는 비밀번호가 올바르지 않습니다.'
            }, status=status.HTTP_401_UNAUTHORIZED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """로그아웃 API"""
    try:
        request.user.auth_token.delete()
        return Response({
            'message': '로그아웃되었습니다.'
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(generics.RetrieveUpdateAPIView):
    """사용자 프로필 조회/수정 API"""
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


@api_view(['POST'])
@permission_classes([AllowAny])
def kakao_login(request):
    """카카오 로그인 콜백 처리 API"""
    code = request.data.get('code')

    if not code:
        return Response({
            'error': '인가 코드가 필요합니다.'
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        # 1. 카카오 액세스 토큰 받기
        access_token = KakaoOAuthService.get_access_token(code)

        # 2. 카카오 사용자 정보 가져오기
        kakao_user_info = KakaoOAuthService.get_user_info(access_token)

        kakao_id = kakao_user_info['kakao_id']
        email = kakao_user_info['email']
        nickname = kakao_user_info['nickname']

        # 3. 카카오 ID로 기존 사용자 찾기
        try:
            user = User.objects.get(kakao_id=kakao_id)
        except User.DoesNotExist:
            # 4. 신규 사용자 생성 (회원가입)
            # 이메일이 없는 경우 기본값 설정
            if not email:
                email = f"kakao_{kakao_id}@kakao.user"

            # username 중복 방지를 위해 kakao_id 사용
            username = f"kakao_{kakao_id}"

            # 이메일 중복 체크
            if User.objects.filter(email=email).exists():
                email = f"kakao_{kakao_id}@kakao.user"

            try:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    kakao_id=kakao_id,
                    login_type='kakao',
                    is_email_verified=True,  # 소셜 로그인은 자동 인증
                )
                # 카카오 로그인은 비밀번호가 필요 없으므로 사용 불가능하게 설정
                user.set_unusable_password()
                user.save()

            except IntegrityError:
                return Response({
                    'error': '이미 존재하는 사용자입니다.'
                }, status=status.HTTP_400_BAD_REQUEST)

        # 5. 토큰 생성 및 반환
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key,
            'username': user.username,
            'user_id': user.id,
            'email': user.email,
            'login_type': user.login_type,
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({
            'error': f'카카오 로그인 처리 중 오류가 발생했습니다: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def google_login(request):
    """구글 로그인 콜백 처리 API"""
    code = request.data.get('code')

    if not code:
        return Response({
            'error': '인가 코드가 필요합니다.'
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        # 1. 구글 액세스 토큰 받기
        access_token = GoogleOAuthService.get_access_token(code)

        # 2. 구글 사용자 정보 가져오기
        google_user_info = GoogleOAuthService.get_user_info(access_token)

        google_id = google_user_info['google_id']
        email = google_user_info['email']
        name = google_user_info['name']

        # 3. 구글 ID로 기존 사용자 찾기
        try:
            user = User.objects.get(google_id=google_id)
        except User.DoesNotExist:
            # 4. 신규 사용자 생성 (회원가입)
            # 이메일이 없는 경우 기본값 설정
            if not email:
                email = f"google_{google_id}@google.user"

            # username 중복 방지를 위해 google_id 사용
            username = f"google_{google_id}"

            # 이메일 중복 체크
            if User.objects.filter(email=email).exists():
                email = f"google_{google_id}@google.user"

            try:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    google_id=google_id,
                    login_type='google',
                    is_email_verified=True,  # 소셜 로그인은 자동 인증
                )
                # 구글 로그인은 비밀번호가 필요 없으므로 사용 불가능하게 설정
                user.set_unusable_password()
                user.save()

            except IntegrityError:
                return Response({
                    'error': '이미 존재하는 사용자입니다.'
                }, status=status.HTTP_400_BAD_REQUEST)

        # 5. 토큰 생성 및 반환
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key,
            'username': user.username,
            'user_id': user.id,
            'email': user.email,
            'login_type': user.login_type,
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({
            'error': f'구글 로그인 처리 중 오류가 발생했습니다: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def verify_email(request):
    """이메일 인증 처리 API"""
    token = request.query_params.get('token')

    if not token:
        return Response({
            'error': '토큰이 필요합니다.'
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        verification_token = EmailVerificationToken.objects.get(token=token)

        if not verification_token.is_valid():
            return Response({
                'error': '토큰이 만료되었거나 이미 사용되었습니다.'
            }, status=status.HTTP_400_BAD_REQUEST)

        # 이메일 인증 완료
        user = verification_token.user
        user.is_email_verified = True
        user.save()

        verification_token.is_used = True
        verification_token.save()

        return Response({
            'message': '이메일 인증이 완료되었습니다. 로그인해주세요.',
            'username': user.username
        }, status=status.HTTP_200_OK)

    except EmailVerificationToken.DoesNotExist:
        return Response({
            'error': '유효하지 않은 토큰입니다.'
        }, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([AllowAny])
def resend_verification_email(request):
    """이메일 인증 메일 재발송 API"""
    email = request.data.get('email')

    if not email:
        return Response({
            'error': '이메일이 필요합니다.'
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email=email)

        if user.is_email_verified:
            return Response({
                'error': '이미 인증된 이메일입니다.'
            }, status=status.HTTP_400_BAD_REQUEST)

        # 새 인증 토큰 생성 및 메일 발송
        verification_token = EmailVerificationToken.create_token(user)
        send_verification_email(user, verification_token)

        return Response({
            'message': '인증 메일이 재발송되었습니다.'
        }, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        return Response({
            'error': '해당 이메일로 가입된 사용자가 없습니다.'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'error': f'메일 발송 중 오류가 발생했습니다: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def request_password_reset(request):
    """비밀번호 재설정 요청 API"""
    serializer = PasswordResetRequestSerializer(data=request.data)

    if serializer.is_valid():
        email = serializer.validated_data['email']

        try:
            user = User.objects.get(email=email, login_type='normal')

            # 비밀번호 재설정 토큰 생성 및 메일 발송
            reset_token = PasswordResetToken.create_token(user)
            send_password_reset_email(user, reset_token)

            return Response({
                'message': '비밀번호 재설정 링크가 이메일로 전송되었습니다.'
            }, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            # 보안을 위해 사용자가 없어도 동일한 메시지 반환
            return Response({
                'message': '비밀번호 재설정 링크가 이메일로 전송되었습니다.'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': f'메일 발송 중 오류가 발생했습니다: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password_confirm(request):
    """비밀번호 재설정 확인 API"""
    serializer = PasswordResetConfirmSerializer(data=request.data)

    if serializer.is_valid():
        token = serializer.validated_data['token']
        new_password = serializer.validated_data['new_password']

        try:
            reset_token = PasswordResetToken.objects.get(token=token)

            if not reset_token.is_valid():
                return Response({
                    'error': '토큰이 만료되었거나 이미 사용되었습니다.'
                }, status=status.HTTP_400_BAD_REQUEST)

            # 비밀번호 재설정
            user = reset_token.user
            user.set_password(new_password)
            user.save()

            reset_token.is_used = True
            reset_token.save()

            return Response({
                'message': '비밀번호가 성공적으로 재설정되었습니다.'
            }, status=status.HTTP_200_OK)

        except PasswordResetToken.DoesNotExist:
            return Response({
                'error': '유효하지 않은 토큰입니다.'
            }, status=status.HTTP_404_NOT_FOUND)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def recover_username(request):
    """아이디 찾기 API"""
    serializer = UsernameRecoverySerializer(data=request.data)

    if serializer.is_valid():
        email = serializer.validated_data['email']

        try:
            user = User.objects.get(email=email, login_type='normal')

            # 아이디 찾기 메일 발송
            send_username_recovery_email(user)

            return Response({
                'message': '등록된 이메일로 아이디 정보가 전송되었습니다.'
            }, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            # 보안을 위해 사용자가 없어도 동일한 메시지 반환
            return Response({
                'message': '등록된 이메일로 아이디 정보가 전송되었습니다.'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': f'메일 발송 중 오류가 발생했습니다: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_account(request):
    """회원탈퇴 API"""
    user = request.user
    serializer = AccountDeletionSerializer(data=request.data, context={'request': request})

    if serializer.is_valid():
        # 일반 로그인 사용자는 비밀번호 확인 필요
        if user.login_type == 'normal':
            password = serializer.validated_data.get('password')
            if not password:
                return Response({
                    'error': '비밀번호를 입력해주세요.'
                }, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 토큰 삭제
            if hasattr(user, 'auth_token'):
                user.auth_token.delete()

            # 사용자 삭제
            username = user.username
            user.delete()

            return Response({
                'message': f'{username}님의 계정이 성공적으로 삭제되었습니다.'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'error': f'계정 삭제 중 오류가 발생했습니다: {str(e)}'
            }, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
