from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.UserDetailView.as_view(), name='profile'),
    path('kakao/callback/', views.kakao_login, name='kakao_login'),
    path('google/callback/', views.google_login, name='google_login'),

    # 이메일 인증
    path('verify-email/', views.verify_email, name='verify_email'),
    path('resend-verification/', views.resend_verification_email, name='resend_verification'),

    # 비밀번호 재설정
    path('password-reset/request/', views.request_password_reset, name='request_password_reset'),
    path('password-reset/confirm/', views.reset_password_confirm, name='reset_password_confirm'),

    # 비밀번호 확인
    path('password-verify/', views.verify_password, name='verify_password'),

    # 비밀번호 변경
    path('password-change/', views.change_password, name='change_password'),

    # 아이디 찾기
    path('recover-username/', views.recover_username, name='recover_username'),

    # 회원탈퇴
    path('delete/', views.delete_account, name='delete_account'),
]
