# 이메일 인증 설정 가이드

Tripify는 Gmail SMTP를 사용하여 사용자 이메일 인증, 비밀번호 재설정, 아이디 찾기 기능을 제공합니다.

## 기능 목록

1. **회원가입 시 이메일 인증**
   - 회원가입 시 인증 메일 발송
   - 이메일 인증 완료 후 로그인 가능
   - 소셜 로그인(카카오, 구글)은 자동 인증

2. **비밀번호 찾기**
   - 이메일로 비밀번호 재설정 링크 발송
   - 보안을 위한 1시간 유효 토큰

3. **아이디 찾기**
   - 이메일로 가입한 아이디 정보 발송

## Gmail SMTP 설정 방법

### 1. Gmail 앱 비밀번호 생성

Gmail의 2단계 인증을 사용하는 경우 앱 비밀번호를 생성해야 합니다.

1. Google 계정 페이지로 이동: https://myaccount.google.com/
2. 좌측 메뉴에서 "보안" 클릭
3. "Google에 로그인" 섹션에서 "2단계 인증" 활성화 (아직 활성화하지 않은 경우)
4. "앱 비밀번호" 검색 또는 다음 링크 접속: https://myaccount.google.com/apppasswords
5. 앱 선택: "메일"
6. 기기 선택: "기타(맞춤 이름)" - 예: "Tripify"
7. "생성" 클릭
8. 생성된 16자리 비밀번호 복사 (공백 제외)

### 2. 환경 변수 설정

`backend/.env` 파일을 생성하고 다음 내용을 추가하세요:

```bash
# Gmail SMTP 설정
EMAIL_HOST_USER=your_gmail_address@gmail.com
EMAIL_HOST_PASSWORD=your_16_digit_app_password_here

# Frontend URL (이메일 링크에 사용)
FRONTEND_URL=http://localhost:5173
```

**주의사항:**
- `EMAIL_HOST_USER`: Gmail 주소 입력
- `EMAIL_HOST_PASSWORD`: 위에서 생성한 16자리 앱 비밀번호 입력 (공백 없이)
- `.env` 파일은 절대 git에 커밋하지 마세요!

### 3. 데이터베이스 마이그레이션

```bash
cd backend
python manage.py migrate
```

### 4. 서버 실행 및 테스트

```bash
# Backend 서버 실행
cd backend
python manage.py runserver

# Frontend 서버 실행 (새 터미널)
cd frontend
npm run dev
```

## 이메일 템플릿

모든 이메일은 HTML 형식으로 발송되며, 다음과 같은 정보를 포함합니다:

### 이메일 인증
- 인증 링크 (24시간 유효)
- 사용자 이름
- 안내 메시지

### 비밀번호 재설정
- 재설정 링크 (1시간 유효)
- 사용자 이름
- 보안 안내

### 아이디 찾기
- 가입한 아이디
- 가입일
- 보안 안내

## API 엔드포인트

### 이메일 인증
- `POST /api/accounts/signup/` - 회원가입 (이메일 발송)
- `GET /api/accounts/verify-email/?token=<token>` - 이메일 인증
- `POST /api/accounts/resend-verification/` - 인증 메일 재발송

### 비밀번호 재설정
- `POST /api/accounts/password-reset/request/` - 재설정 요청
- `POST /api/accounts/password-reset/confirm/` - 새 비밀번호 설정

### 아이디 찾기
- `POST /api/accounts/recover-username/` - 아이디 찾기

## 프론트엔드 라우트

- `/login` - 로그인 (아이디/비밀번호 찾기 링크 포함)
- `/signup` - 회원가입
- `/auth/verify-email?token=<token>` - 이메일 인증
- `/auth/find-username` - 아이디 찾기
- `/auth/reset-password` - 비밀번호 재설정 요청
- `/auth/reset-password/confirm?token=<token>` - 비밀번호 재설정

## 트러블슈팅

### 이메일이 발송되지 않는 경우

1. **앱 비밀번호 확인**
   - 16자리 비밀번호를 공백 없이 정확히 입력했는지 확인
   - Gmail 계정 비밀번호가 아닌 앱 비밀번호를 사용해야 함

2. **2단계 인증 확인**
   - Gmail 계정에서 2단계 인증이 활성화되어 있는지 확인

3. **Gmail 보안 설정**
   - Gmail 계정의 "보안 수준이 낮은 앱의 액세스" 설정 확인
   - 최신 Gmail은 앱 비밀번호 사용을 권장

4. **방화벽 설정**
   - 포트 587 (TLS)가 열려있는지 확인

5. **환경 변수 로드 확인**
   ```python
   # Django shell에서 확인
   python manage.py shell
   >>> from django.conf import settings
   >>> print(settings.EMAIL_HOST_USER)
   >>> print(settings.EMAIL_HOST_PASSWORD)
   ```

### 이메일이 스팸으로 분류되는 경우

- Gmail 설정에서 Tripify 이메일을 "스팸 아님"으로 표시
- 발신자 이메일 주소를 연락처에 추가

## 보안 권장사항

1. **환경 변수 관리**
   - `.env` 파일을 `.gitignore`에 추가
   - 프로덕션 환경에서는 환경 변수 또는 비밀 관리 서비스 사용

2. **토큰 유효 시간**
   - 이메일 인증: 24시간 (설정 가능)
   - 비밀번호 재설정: 1시간 (설정 가능)

3. **HTTPS 사용**
   - 프로덕션 환경에서는 반드시 HTTPS 사용
   - 이메일 링크의 FRONTEND_URL을 https로 설정

4. **Rate Limiting**
   - 프로덕션 환경에서는 이메일 발송 횟수 제한 권장

## 프로덕션 배포 시 추가 설정

프로덕션 환경에서는 다음 설정을 권장합니다:

```python
# settings.py
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.getenv('EMAIL_HOST_USER')

# 프로덕션 URL 설정
FRONTEND_URL = os.getenv('FRONTEND_URL', 'https://yourdomain.com')
```

## 문의

설정에 문제가 있거나 질문이 있으시면 이슈를 생성해주세요.
