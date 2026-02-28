# GOOGLE_LOGIN_SETUP.md

# 구글 로그인 설정 가이드

## 개요
이 문서는 Tripify 프로젝트에서 구글 OAuth 로그인 기능을 설정하는 방법을 안내합니다.

## 1. Google Cloud Console 계정 및 프로젝트 생성

### 1.1 Google Cloud Console 접속
1. [Google Cloud Console](https://console.cloud.google.com/)에 접속합니다.
2. Google 계정으로 로그인합니다.

### 1.2 새 프로젝트 생성
1. 상단의 프로젝트 선택 드롭다운을 클릭합니다.
2. **새 프로젝트** 버튼을 클릭합니다.
3. 프로젝트 정보를 입력합니다:
   - **프로젝트 이름**: Tripify (원하는 이름)
   - **위치**: 조직 없음 (개인 프로젝트의 경우)
4. **만들기** 버튼을 클릭합니다.

## 2. OAuth 동의 화면 설정

### 2.1 OAuth 동의 화면 구성
1. 좌측 메뉴에서 **API 및 서비스** > **OAuth 동의 화면**을 선택합니다.
2. 사용자 유형을 선택합니다:
   - 개발/테스트: **외부** 선택
   - 조직 내부용: **내부** 선택
3. **만들기** 버튼을 클릭합니다.

### 2.2 앱 정보 입력
1. **OAuth 동의 화면** 탭에서 다음 정보를 입력합니다:
   - **앱 이름**: Tripify
   - **사용자 지원 이메일**: 본인의 이메일 주소
   - **앱 로고**: (선택사항) 앱 로고 이미지
   - **앱 도메인**: (선택사항)
     - 애플리케이션 홈페이지: `http://localhost:5173`
   - **승인된 도메인**: (선택사항, 운영 환경 시)
   - **개발자 연락처 정보**: 본인의 이메일 주소
2. **저장 후 계속** 버튼을 클릭합니다.

### 2.3 범위 설정
1. **범위** 탭에서 **범위 추가 또는 삭제** 버튼을 클릭합니다.
2. 다음 범위를 선택합니다:
   - `.../auth/userinfo.email`
   - `.../auth/userinfo.profile`
   - `openid`
3. **업데이트** 버튼을 클릭합니다.
4. **저장 후 계속** 버튼을 클릭합니다.

### 2.4 테스트 사용자 추가 (외부 앱인 경우)
1. **테스트 사용자** 탭에서 **ADD USERS** 버튼을 클릭합니다.
2. 테스트에 사용할 Google 계정 이메일을 입력합니다.
3. **저장** 버튼을 클릭합니다.

## 3. OAuth 2.0 클라이언트 ID 생성

### 3.1 사용자 인증 정보 만들기
1. 좌측 메뉴에서 **API 및 서비스** > **사용자 인증 정보**를 선택합니다.
2. 상단의 **사용자 인증 정보 만들기** > **OAuth 클라이언트 ID**를 클릭합니다.

### 3.2 OAuth 클라이언트 ID 구성
1. 애플리케이션 유형을 선택합니다: **웹 애플리케이션**
2. 이름을 입력합니다: **Tripify Web Client**
3. **승인된 자바스크립트 원본**에 다음을 추가합니다:
   - 개발 환경: `http://localhost:5173`
   - 운영 환경: 실제 도메인 (예: `https://tripify.com`)
4. **승인된 리디렉션 URI**에 다음을 추가합니다:
   - 개발 환경: `http://localhost:5173/auth/google/callback`
   - 운영 환경: `https://your-domain.com/auth/google/callback`
5. **만들기** 버튼을 클릭합니다.

### 3.3 클라이언트 ID 및 보안 비밀번호 저장
1. 생성된 OAuth 클라이언트의 **클라이언트 ID**와 **클라이언트 보안 비밀번호**를 복사합니다.
2. 안전한 곳에 저장합니다.

## 4. 환경 변수 설정

### 4.1 백엔드 환경 변수
`backend/.env` 파일을 생성하거나 기존 파일에 다음 내용을 추가합니다:

```env
# 기존 설정...
KAKAO_REST_API_KEY=your_kakao_rest_api_key_here
KAKAO_REDIRECT_URI=http://localhost:5173/auth/kakao/callback
KAKAO_CLIENT_SECRET=your_kakao_client_secret_here

# Google OAuth Settings
GOOGLE_CLIENT_ID=your_google_client_id_here.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your_google_client_secret_here
GOOGLE_REDIRECT_URI=http://localhost:5173/auth/google/callback
```

### 4.2 프론트엔드 환경 변수
`frontend/.env` 파일을 생성하거나 기존 파일에 다음 내용을 추가합니다:

```env
# 기존 설정...
VITE_KAKAO_REST_API_KEY=your_kakao_rest_api_key_here
VITE_KAKAO_REDIRECT_URI=http://localhost:5173/auth/kakao/callback

# Google OAuth Settings
VITE_GOOGLE_CLIENT_ID=your_google_client_id_here.apps.googleusercontent.com
VITE_GOOGLE_REDIRECT_URI=http://localhost:5173/auth/google/callback
```

## 5. 데이터베이스 마이그레이션

User 모델에 구글 로그인 관련 필드가 추가되었으므로 마이그레이션을 실행해야 합니다.

```bash
cd backend
python manage.py makemigrations
python manage.py migrate
```

## 6. 패키지 설치

### 6.1 백엔드
백엔드는 추가 패키지 설치가 필요하지 않습니다. (기존 `requests` 라이브러리 사용)

```bash
cd backend
pip install -r requirements.txt
```

### 6.2 프론트엔드
프론트엔드는 추가 패키지 설치가 필요하지 않습니다. (기존 패키지 사용)

```bash
cd frontend
npm install
```

## 7. 애플리케이션 실행

### 7.1 백엔드 서버 실행
```bash
cd backend
python manage.py runserver
```

### 7.2 프론트엔드 서버 실행
```bash
cd frontend
npm run dev
```

## 8. 테스트

1. 브라우저에서 `http://localhost:5173/login`에 접속합니다.
2. **구글로 시작하기** 버튼을 클릭합니다.
3. Google 계정으로 로그인하고 권한을 허용합니다.
4. 로그인 성공 후 메인 페이지로 리다이렉트되는지 확인합니다.

## 9. 주의사항

- **보안**: `.env` 파일은 절대 Git에 커밋하지 마세요. `.gitignore`에 포함되어 있는지 확인하세요.
- **Redirect URI**: Google Cloud Console에 등록한 Redirect URI와 환경 변수의 URI가 정확히 일치해야 합니다.
- **도메인 등록**: 운영 환경에서는 반드시 실제 도메인을 Google Cloud Console에 등록해야 합니다.
- **클라이언트 보안 비밀번호**: 클라이언트 보안 비밀번호는 반드시 환경 변수로 관리하고 노출되지 않도록 주의하세요.
- **테스트 사용자**: 앱이 테스트 모드인 경우, 테스트 사용자로 등록된 Google 계정만 로그인할 수 있습니다.

## 10. 트러블슈팅

### 10.1 "redirect_uri_mismatch" 오류
- Google Cloud Console에 등록한 Redirect URI와 환경 변수의 URI가 일치하는지 확인하세요.
- 프로토콜(http/https), 포트 번호, 경로까지 정확히 일치해야 합니다.

### 10.2 "invalid_client" 오류
- 클라이언트 ID가 올바르게 설정되었는지 확인하세요.
- 클라이언트 보안 비밀번호가 올바르게 입력되었는지 확인하세요.

### 10.3 "access_denied" 오류
- 앱이 테스트 모드인 경우, 테스트 사용자로 등록된 계정으로 로그인하고 있는지 확인하세요.
- OAuth 동의 화면 설정이 완료되었는지 확인하세요.

### 10.4 "invalid_scope" 오류
- OAuth 동의 화면에서 필요한 범위(scope)가 추가되었는지 확인하세요.
- 인증 URL의 scope 파라미터가 올바른지 확인하세요.

## 11. 운영 환경 배포 시 추가 작업

### 11.1 앱 게시
1. Google Cloud Console에서 **OAuth 동의 화면**으로 이동합니다.
2. **앱 게시** 버튼을 클릭합니다.
3. 검토 프로세스를 거쳐 앱을 게시합니다.

### 11.2 도메인 인증
1. Google Cloud Console에서 실제 도메인을 추가합니다.
2. 도메인 소유권을 인증합니다.

## 12. 참고 자료

- [Google Identity - OAuth 2.0 설정](https://developers.google.com/identity/protocols/oauth2)
- [Google Identity - 웹 서버 앱용 OAuth 2.0](https://developers.google.com/identity/protocols/oauth2/web-server)
- [Google Cloud Console](https://console.cloud.google.com/)


# KAKAO_LOGIN_SETUP.md

# 카카오 로그인 설정 가이드

## 개요
이 문서는 Tripify 프로젝트에서 카카오 OAuth 로그인 기능을 설정하는 방법을 안내합니다.

## 1. 카카오 개발자 계정 및 앱 등록

### 1.1 카카오 개발자 사이트 접속
1. [카카오 개발자 사이트](https://developers.kakao.com/)에 접속합니다.
2. 카카오 계정으로 로그인합니다.

### 1.2 애플리케이션 등록
1. 상단 메뉴에서 **내 애플리케이션**을 클릭합니다.
2. **애플리케이션 추가하기** 버튼을 클릭합니다.
3. 앱 정보를 입력합니다:
   - **앱 이름**: Tripify (원하는 이름)
   - **사업자명**: 개인 또는 회사명
4. **저장** 버튼을 클릭합니다.

## 2. 앱 설정

### 2.1 앱 키 확인
1. 생성한 앱을 선택합니다.
2. **요약 정보** 탭에서 다음 키를 확인합니다:
   - **REST API 키**: 백엔드와 프론트엔드에서 사용
   - **Client Secret** (선택사항): 보안 강화를 위해 사용

### 2.2 플랫폼 설정
1. 좌측 메뉴에서 **플랫폼** 메뉴를 선택합니다.
2. **Web 플랫폼 등록** 버튼을 클릭합니다.
3. 사이트 도메인을 입력합니다:
   - 개발 환경: `http://localhost:5173`
   - 운영 환경: 실제 도메인 (예: `https://tripify.com`)

### 2.3 Redirect URI 설정
1. 좌측 메뉴에서 **카카오 로그인** 메뉴를 선택합니다.
2. **카카오 로그인 활성화**를 **ON**으로 설정합니다.
3. **Redirect URI** 섹션에서 **Redirect URI 등록** 버튼을 클릭합니다.
4. Redirect URI를 입력합니다:
   - 개발 환경: `http://localhost:5173/auth/kakao/callback`
   - 운영 환경: `https://your-domain.com/auth/kakao/callback`
5. **저장** 버튼을 클릭합니다.

### 2.4 동의 항목 설정
1. 좌측 메뉴에서 **동의 항목** 메뉴를 선택합니다.
2. 다음 항목을 **필수 동의** 또는 **선택 동의**로 설정합니다:
   - **닉네임**: 선택 동의
   - **프로필 이미지**: 선택 동의
   - **카카오계정(이메일)**: 선택 동의

### 2.5 Client Secret 설정 (선택사항, 보안 강화)
1. 좌측 메뉴에서 **카카오 로그인** > **보안** 메뉴를 선택합니다.
2. **Client Secret** 섹션에서 **코드 생성** 버튼을 클릭합니다.
3. 생성된 코드를 복사합니다.
4. **상태**를 **사용함**으로 변경합니다.

## 3. 환경 변수 설정

### 3.1 백엔드 환경 변수
`backend/.env` 파일을 생성하고 다음 내용을 입력합니다:

```env
KAKAO_REST_API_KEY=your_kakao_rest_api_key_here
KAKAO_REDIRECT_URI=http://localhost:5173/auth/kakao/callback
KAKAO_CLIENT_SECRET=your_kakao_client_secret_here  # Client Secret을 사용하는 경우만
```

### 3.2 프론트엔드 환경 변수
`frontend/.env` 파일을 생성하고 다음 내용을 입력합니다:

```env
VITE_KAKAO_REST_API_KEY=your_kakao_rest_api_key_here
VITE_KAKAO_REDIRECT_URI=http://localhost:5173/auth/kakao/callback
```

## 4. 데이터베이스 마이그레이션

User 모델에 카카오 로그인 관련 필드가 추가되었으므로 마이그레이션을 실행해야 합니다.

```bash
cd backend
python manage.py makemigrations
python manage.py migrate
```

## 5. 패키지 설치

### 5.1 백엔드
```bash
cd backend
pip install -r requirements.txt
```

### 5.2 프론트엔드
```bash
cd frontend
npm install
```

## 6. 애플리케이션 실행

### 6.1 백엔드 서버 실행
```bash
cd backend
python manage.py runserver
```

### 6.2 프론트엔드 서버 실행
```bash
cd frontend
npm run dev
```

## 7. 테스트

1. 브라우저에서 `http://localhost:5173/login`에 접속합니다.
2. **카카오로 시작하기** 버튼을 클릭합니다.
3. 카카오 계정으로 로그인하고 동의 항목에 동의합니다.
4. 로그인 성공 후 메인 페이지로 리다이렉트되는지 확인합니다.

## 8. 주의사항

- **보안**: `.env` 파일은 절대 Git에 커밋하지 마세요. `.gitignore`에 포함되어 있는지 확인하세요.
- **Redirect URI**: 카카오 개발자 콘솔에 등록한 Redirect URI와 환경 변수의 URI가 정확히 일치해야 합니다.
- **도메인 등록**: 운영 환경에서는 반드시 실제 도메인을 카카오 개발자 콘솔에 등록해야 합니다.
- **Client Secret**: Client Secret을 사용하는 경우 반드시 환경 변수로 관리하고 노출되지 않도록 주의하세요.

## 9. 트러블슈팅

### 9.1 "redirect_uri mismatch" 오류
- 카카오 개발자 콘솔에 등록한 Redirect URI와 환경 변수의 URI가 일치하는지 확인하세요.
- 프로토콜(http/https), 포트 번호까지 정확히 일치해야 합니다.

### 9.2 "invalid client" 오류
- REST API 키가 올바르게 설정되었는지 확인하세요.
- Client Secret을 사용하는 경우 올바르게 입력되었는지 확인하세요.

### 9.3 동의 항목 오류
- 카카오 개발자 콘솔에서 필요한 동의 항목이 활성화되어 있는지 확인하세요.
- 비즈니스 채널이 필요한 항목인 경우 비즈니스 채널을 먼저 등록해야 할 수 있습니다.

## 10. 참고 자료

- [카카오 로그인 개발 가이드](https://developers.kakao.com/docs/latest/ko/kakaologin/common)
- [카카오 REST API 문서](https://developers.kakao.com/docs/latest/ko/kakaologin/rest-api)


# NAVER_LOGIN_SETUP.md

# 네이버 소셜 로그인 설정 가이드

## 1. 네이버 개발자 센터에서 애플리케이션 등록

1. **네이버 개발자 센터 접속**
   - https://developers.naver.com 접속
   - 네이버 계정으로 로그인

2. **애플리케이션 등록**
   - "Application" → "애플리케이션 등록" 클릭
   - 애플리케이션 이름: `Tripify` (또는 원하는 이름)
   - 사용 API: "네이버 로그인" 선택
   - 로그인 오픈 API 서비스 환경: "PC 웹" 선택
   - 서비스 URL: `http://localhost:5173` (개발 환경)
   - Callback URL: `http://localhost:5173/auth/naver/callback`

3. **Client ID와 Client Secret 확인**
   - 등록 후 "내 애플리케이션"에서 Client ID와 Client Secret 확인

## 2. 환경 변수 설정

### Backend (.env 파일)

`backend/.env` 파일에 다음 내용 추가:

```env
# Naver OAuth Settings
NAVER_CLIENT_ID=your_naver_client_id_here
NAVER_CLIENT_SECRET=your_naver_client_secret_here
NAVER_REDIRECT_URI=http://localhost:5173/auth/naver/callback
```

### Frontend (.env 파일)

`frontend/.env` 파일에 다음 내용 추가:

```env
# Naver OAuth Settings
VITE_NAVER_CLIENT_ID=your_naver_client_id_here
VITE_NAVER_REDIRECT_URI=http://localhost:5173/auth/naver/callback
```

## 3. 데이터베이스 마이그레이션

백엔드에서 다음 명령어 실행:

```bash
cd backend
python manage.py makemigrations
python manage.py migrate
```

## 4. 프로덕션 환경 설정 (배포 시)

프로덕션 환경에서는 네이버 개발자 센터에서 추가 설정이 필요합니다:

### 방법 1: 로컬과 프로덕션 모두 사용 (권장)

1. **서비스 URL 변경**
   - 프로덕션 URL로 변경 (예: `https://your-app.vercel.app`)
   - ⚠️ 네이버는 서비스 URL을 하나만 등록할 수 있으므로 프로덕션 URL로 설정

2. **Callback URL 추가**
   - 기존 로컬 Callback URL 유지: `http://localhost:5173/auth/naver/callback`
   - 프로덕션 Callback URL 추가: `https://your-app.vercel.app/auth/naver/callback`
   - 네이버는 여러 Callback URL을 등록할 수 있습니다

3. **환경 변수 설정**
   - **로컬 개발**: `.env` 파일에 로컬 URL 사용
   - **프로덕션 (Render)**: 환경 변수에 프로덕션 URL 설정

### 방법 2: 프로덕션만 사용

1. **서비스 URL 변경**
   - 프로덕션 URL로 변경 (예: `https://your-app.vercel.app`)

2. **Callback URL 변경**
   - 프로덕션 URL로 변경 (예: `https://your-app.vercel.app/auth/naver/callback`)
   - 로컬 URL은 삭제

3. **환경 변수 업데이트**
   - Backend (Render): `NAVER_REDIRECT_URI`를 프로덕션 URL로 설정
   - Frontend (Vercel): 필요시 환경 변수 설정

## 5. 테스트

1. 백엔드 서버 실행
2. 프론트엔드 서버 실행
3. 로그인 페이지에서 네이버 로그인 버튼 클릭
4. 네이버 로그인 화면에서 로그인
5. 정상적으로 로그인되는지 확인

## 주의사항

- 네이버 로그인은 `state` 파라미터를 사용하여 CSRF 공격을 방지합니다.
- 네이버 API는 하루에 최대 10,000건의 API 호출을 허용합니다.
- 개발 환경과 프로덕션 환경의 Callback URL은 반드시 다르게 설정해야 합니다.



# EMAIL_SETUP.md

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


