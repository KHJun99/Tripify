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
