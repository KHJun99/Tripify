# Tripify 배포 가이드

이 문서는 Tripify 프로젝트를 Vercel(프론트엔드)과 Render(백엔드)에 배포하는 방법을 설명합니다.

## 목차

1. [사전 준비사항](#사전-준비사항)
2. [백엔드 배포 (Render)](#백엔드-배포-render)
3. [프론트엔드 배포 (Vercel)](#프론트엔드-배포-vercel)
4. [환경 변수 설정](#환경-변수-설정)
5. [소셜 로그인 설정](#소셜-로그인-설정)
6. [데이터베이스 마이그레이션](#데이터베이스-마이그레이션)
7. [문제 해결](#문제-해결)

---

## 사전 준비사항

### 필요한 계정
- [Render](https://render.com) 계정 (백엔드 배포)
- [Vercel](https://vercel.com) 계정 (프론트엔드 배포)
- GitHub 저장소 (코드 저장 및 연동)

### 필요한 정보
- 소셜 로그인 API 키 (카카오, 구글, 네이버)
- GMS API 키 (Claude AI 사용)
- Gmail 앱 비밀번호 (이메일 발송용)

---

## 백엔드 배포 (Render)

### 1. Render 계정 생성 및 로그인

1. [Render](https://render.com)에 접속하여 계정을 생성합니다.
2. GitHub 계정으로 연동하는 것을 권장합니다.

### 2. PostgreSQL 데이터베이스 생성

1. Render 대시보드에서 **"New +"** 버튼 클릭
2. **"PostgreSQL"** 선택
3. 다음 설정 입력:
   - **Name**: `tripify-db` (또는 원하는 이름)
   - **Database**: `tripify`
   - **User**: `tripify_user` (또는 원하는 사용자명)
   - **Plan**: Free (또는 원하는 플랜)
4. **"Create Database"** 클릭
5. 데이터베이스가 생성되면 **"Connections"** 탭에서 **"Internal Database URL"**을 복사합니다.
   - 형식: `postgresql://user:password@host:port/database`

### 3. Web Service 생성

#### 방법 1: render.yaml 사용 (권장)

1. 프로젝트 루트에 `render.yaml` 파일이 있는지 확인합니다.
2. Render 대시보드에서 **"New +"** → **"Blueprint"** 선택
3. GitHub 저장소를 연결하고 `render.yaml` 파일이 있는 저장소를 선택합니다.
4. **"Apply"** 클릭하여 배포를 시작합니다.

#### 방법 2: 수동 설정

1. Render 대시보드에서 **"New +"** → **"Web Service"** 선택
2. GitHub 저장소를 연결합니다.
3. 다음 설정 입력:
   - **Name**: `tripify-backend`
   - **Region**: 원하는 지역 선택 (예: Singapore)
   - **Branch**: `main` (또는 배포할 브랜치)
   - **Root Directory**: `backend`
   - **Runtime**: `Python 3`
   - **Build Command**: 
     ```bash
     cd backend && pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
     ```
   - **Start Command**: 
     ```bash
     cd backend && gunicorn config.wsgi:application
     ```
   - **Plan**: Free (또는 원하는 플랜)

4. **"Advanced"** 섹션에서 환경 변수를 설정합니다 (아래 [환경 변수 설정](#환경-변수-설정) 참조).

5. **"Create Web Service"** 클릭

### 4. 환경 변수 설정 (Render)

Render 대시보드의 **"Environment"** 섹션에서 다음 환경 변수를 추가합니다:

```bash
# 필수 설정
PYTHON_VERSION=3.11.0
DJANGO_SECRET_KEY=your-secret-key-here  # Django 시크릿 키 (랜덤 문자열 생성)
DEBUG=False
ALLOWED_HOSTS=your-render-app.onrender.com  # Render에서 제공하는 도메인
DATABASE_URL=postgresql://...  # 위에서 생성한 PostgreSQL 내부 URL

# CORS 설정 (프론트엔드 URL)
CORS_ALLOWED_ORIGINS=https://your-vercel-app.vercel.app

# AI API 키
GMS_API_KEY=your-gms-api-key

# 카카오 OAuth
KAKAO_REST_API_KEY=your-kakao-rest-api-key
KAKAO_CLIENT_SECRET=your-kakao-client-secret
KAKAO_REDIRECT_URI=https://your-vercel-app.vercel.app/auth/kakao/callback

# 구글 OAuth
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_REDIRECT_URI=https://your-vercel-app.vercel.app/auth/google/callback

# 네이버 OAuth
NAVER_CLIENT_ID=your-naver-client-id
NAVER_CLIENT_SECRET=your-naver-client-secret
NAVER_REDIRECT_URI=https://your-vercel-app.vercel.app/auth/naver/callback

# 이메일 설정
EMAIL_HOST_USER=your-gmail@gmail.com
EMAIL_HOST_PASSWORD=your-gmail-app-password
FRONTEND_URL=https://your-vercel-app.vercel.app
```

**중요**: 
- `DJANGO_SECRET_KEY`는 반드시 강력한 랜덤 문자열로 생성해야 합니다.
- `ALLOWED_HOSTS`와 `CORS_ALLOWED_ORIGINS`는 실제 배포된 URL로 변경해야 합니다.
- 모든 소셜 로그인 `REDIRECT_URI`는 프론트엔드 URL을 사용합니다.

### 5. 데이터베이스 마이그레이션

Render는 `render.yaml`의 `buildCommand`에 마이그레이션이 포함되어 있어 자동으로 실행됩니다. 수동으로 실행하려면:

1. Render 대시보드에서 **"Shell"** 탭 열기
2. 다음 명령어 실행:
   ```bash
   python manage.py migrate
   ```

### 6. 초기 데이터 로드 (선택사항)

관광지 및 축제 데이터를 로드하려면:

1. Render 대시보드의 **"Shell"** 탭에서:
   ```bash
   python manage.py load_places
   python manage.py load_festivals
   ```

---

## 프론트엔드 배포 (Vercel)

### 1. Vercel 계정 생성 및 로그인

1. [Vercel](https://vercel.com)에 접속하여 계정을 생성합니다.
2. GitHub 계정으로 연동하는 것을 권장합니다.

### 2. 프로젝트 배포

1. Vercel 대시보드에서 **"Add New..."** → **"Project"** 클릭
2. GitHub 저장소를 선택합니다.
3. 프로젝트 설정:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build` (자동 감지됨)
   - **Output Directory**: `dist` (자동 감지됨)
   - **Install Command**: `npm install` (자동 감지됨)

4. **"Environment Variables"** 섹션에서 환경 변수 추가:
   ```bash
   VITE_API_URL=https://your-render-app.onrender.com/api
   ```
   - `your-render-app.onrender.com`은 Render에서 배포한 백엔드 URL입니다.

5. **"Deploy"** 클릭

### 3. vercel.json 설정 확인

프로젝트 루트에 `vercel.json` 파일이 있어야 합니다. 이 파일은 SPA 라우팅을 위한 리라이트 규칙을 포함합니다.

### 4. 커스텀 도메인 설정 (선택사항)

1. Vercel 대시보드에서 프로젝트 선택
2. **"Settings"** → **"Domains"** 이동
3. 원하는 도메인 추가

---

## 환경 변수 설정

### 백엔드 (Render) 환경 변수

| 변수명 | 설명 | 예시 |
|--------|------|------|
| `DJANGO_SECRET_KEY` | Django 시크릿 키 | 랜덤 문자열 생성 |
| `DEBUG` | 디버그 모드 | `False` |
| `ALLOWED_HOSTS` | 허용된 호스트 | `your-app.onrender.com` |
| `DATABASE_URL` | PostgreSQL 연결 URL | `postgresql://...` |
| `CORS_ALLOWED_ORIGINS` | CORS 허용 오리진 | `https://your-app.vercel.app` |
| `GMS_API_KEY` | Claude AI API 키 | SSAFY GMS API 키 |
| `KAKAO_REST_API_KEY` | 카카오 REST API 키 | 카카오 개발자 센터에서 발급 |
| `KAKAO_CLIENT_SECRET` | 카카오 클라이언트 시크릿 | 카카오 개발자 센터에서 발급 |
| `KAKAO_REDIRECT_URI` | 카카오 리다이렉트 URI | `https://your-app.vercel.app/auth/kakao/callback` |
| `GOOGLE_CLIENT_ID` | 구글 클라이언트 ID | Google Cloud Console에서 발급 |
| `GOOGLE_CLIENT_SECRET` | 구글 클라이언트 시크릿 | Google Cloud Console에서 발급 |
| `GOOGLE_REDIRECT_URI` | 구글 리다이렉트 URI | `https://your-app.vercel.app/auth/google/callback` |
| `NAVER_CLIENT_ID` | 네이버 클라이언트 ID | 네이버 개발자 센터에서 발급 |
| `NAVER_CLIENT_SECRET` | 네이버 클라이언트 시크릿 | 네이버 개발자 센터에서 발급 |
| `NAVER_REDIRECT_URI` | 네이버 리다이렉트 URI | `https://your-app.vercel.app/auth/naver/callback` |
| `EMAIL_HOST_USER` | Gmail 주소 | `your-email@gmail.com` |
| `EMAIL_HOST_PASSWORD` | Gmail 앱 비밀번호 | Gmail 앱 비밀번호 |
| `FRONTEND_URL` | 프론트엔드 URL | `https://your-app.vercel.app` |

### 프론트엔드 (Vercel) 환경 변수

| 변수명 | 설명 | 예시 |
|--------|------|------|
| `VITE_API_URL` | 백엔드 API URL | `https://your-app.onrender.com/api` |

---

## 소셜 로그인 설정

### 카카오 로그인

1. [카카오 개발자 센터](https://developers.kakao.com) 접속
2. 내 애플리케이션 → 앱 설정 → 플랫폼
   - Web 플랫폼 추가: `https://your-app.vercel.app`
3. 제품 설정 → 카카오 로그인
   - Redirect URI: `https://your-app.vercel.app/auth/kakao/callback`
4. 앱 키에서 REST API 키와 Client Secret 확인

### 구글 로그인

1. [Google Cloud Console](https://console.cloud.google.com) 접속
2. OAuth 2.0 클라이언트 ID 생성
   - 승인된 리디렉션 URI: `https://your-app.vercel.app/auth/google/callback`
3. 클라이언트 ID와 클라이언트 시크릿 확인

### 네이버 로그인

1. [네이버 개발자 센터](https://developers.naver.com) 접속
2. 애플리케이션 등록
   - 서비스 URL: `https://your-app.vercel.app`
   - Callback URL: `https://your-app.vercel.app/auth/naver/callback`
3. Client ID와 Client Secret 확인

---

## 데이터베이스 마이그레이션

### 자동 마이그레이션

`render.yaml`의 `buildCommand`에 마이그레이션이 포함되어 있어 배포 시 자동으로 실행됩니다.

### 수동 마이그레이션

Render 대시보드의 **"Shell"** 탭에서:

```bash
python manage.py migrate
```

### 초기 데이터 로드

관광지 및 축제 데이터를 로드하려면:

```bash
python manage.py load_places
python manage.py load_festivals
```

---

## 문제 해결

### 백엔드 배포 문제

#### 1. 빌드 실패

- **원인**: `requirements.txt`에 패키지 누락
- **해결**: `requirements.txt`에 모든 의존성 포함 확인

#### 2. 데이터베이스 연결 실패

- **원인**: `DATABASE_URL` 환경 변수 미설정 또는 잘못된 URL
- **해결**: Render의 PostgreSQL 내부 URL 확인 및 설정

#### 3. CORS 오류

- **원인**: `CORS_ALLOWED_ORIGINS`에 프론트엔드 URL 미포함
- **해결**: Vercel 배포 URL을 `CORS_ALLOWED_ORIGINS`에 추가

#### 4. Static 파일 404 오류

- **원인**: `collectstatic` 미실행
- **해결**: `buildCommand`에 `python manage.py collectstatic --noinput` 포함 확인

### 프론트엔드 배포 문제

#### 1. API 요청 실패

- **원인**: `VITE_API_URL` 환경 변수 미설정 또는 잘못된 URL
- **해결**: Vercel 환경 변수에 백엔드 URL 설정 확인

#### 2. 라우팅 오류 (404)

- **원인**: `vercel.json`의 리라이트 규칙 누락
- **해결**: `vercel.json` 파일 확인 및 SPA 리라이트 규칙 포함 확인

#### 3. 빌드 실패

- **원인**: Node.js 버전 불일치 또는 의존성 문제
- **해결**: `package.json`의 `engines` 필드 확인 및 로컬에서 빌드 테스트

### 일반적인 문제

#### 1. 환경 변수 변경 후 반영 안 됨

- **해결**: 
  - Render: 서비스 재시작 필요
  - Vercel: 자동 재배포 또는 수동 재배포

#### 2. 소셜 로그인 리다이렉트 오류

- **원인**: 리다이렉트 URI가 소셜 로그인 플랫폼에 등록되지 않음
- **해결**: 각 소셜 로그인 플랫폼의 개발자 센터에서 리다이렉트 URI 확인

#### 3. 이메일 발송 실패

- **원인**: Gmail 앱 비밀번호 미설정 또는 잘못된 비밀번호
- **해결**: Gmail 2단계 인증 활성화 후 앱 비밀번호 생성

---

## 배포 후 확인 사항

### 백엔드 확인

1. **Health Check**: `https://your-app.onrender.com/api/` 접속하여 응답 확인
2. **API 엔드포인트 테스트**: 
   - `https://your-app.onrender.com/api/places/`
   - `https://your-app.onrender.com/api/festivals/`
3. **로그 확인**: Render 대시보드의 **"Logs"** 탭에서 오류 확인

### 프론트엔드 확인

1. **홈페이지 접속**: `https://your-app.vercel.app` 접속
2. **API 연결 확인**: 브라우저 개발자 도구의 Network 탭에서 API 요청 확인
3. **소셜 로그인 테스트**: 각 소셜 로그인 버튼 클릭하여 리다이렉트 확인

---

## 추가 리소스

- [Render 공식 문서](https://render.com/docs)
- [Vercel 공식 문서](https://vercel.com/docs)
- [Django 배포 체크리스트](https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/)
- [Vite 배포 가이드](https://vitejs.dev/guide/static-deploy.html)

---

## 주의사항

1. **무료 플랜 제한사항**:
   - Render 무료 플랜: 15분 비활성 시 슬리프 모드 진입 (첫 요청 시 느린 응답)
   - Vercel 무료 플랜: 대역폭 및 빌드 시간 제한

2. **보안**:
   - `DEBUG=False`로 설정 필수
   - `DJANGO_SECRET_KEY`는 강력한 랜덤 문자열 사용
   - 환경 변수는 절대 코드에 커밋하지 않기

3. **성능**:
   - 프로덕션 환경에서는 CDN 사용 권장
   - 데이터베이스 인덱스 최적화
   - 정적 파일 캐싱 설정

---

배포가 완료되면 프로젝트가 전 세계에서 접근 가능합니다! 🚀

