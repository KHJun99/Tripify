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
