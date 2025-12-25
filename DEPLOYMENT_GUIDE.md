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
5. Blueprint가 생성한 서비스들을 확인합니다:
   - **Web Service** (tripify-backend)
   - **PostgreSQL Database** (tripify-db)
6. **Web Service**를 클릭하여 상세 페이지로 이동합니다.
7. 왼쪽 메뉴에서 **"Environment"** 탭을 클릭합니다.
8. 아래 [환경 변수 설정](#환경-변수-설정) 섹션의 변수들을 추가합니다.

**⚠️ render.yaml 파일 수정 후 적용 방법:**
1. 변경사항을 Git에 커밋합니다:
   ```bash
   git add render.yaml
   git commit -m "Update render.yaml: Add data loading commands"
   ```
2. GitHub에 push합니다:
   ```bash
   git push origin main
   ```
3. Render가 자동으로 변경사항을 감지하고 재배포를 시작합니다.
   - 또는 Render 대시보드에서 **"Manual Deploy"** → **"Deploy latest commit"** 클릭

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

**ALLOWED_HOSTS 확인 방법:**
1. Render 대시보드에서 생성한 Web Service (`tripify-backend`)를 클릭합니다.
2. 상단에 표시된 **URL**을 확인합니다.
   - 예: `https://tripify-backend.onrender.com`
   - 또는 `https://tripify-backend-xxxx.onrender.com` (xxxx는 랜덤 문자열)
3. 이 URL에서 `https://`를 제외한 도메인 부분만 사용합니다.
   - 예: `tripify-backend.onrender.com`
   - 또는 여러 도메인을 사용하는 경우: `tripify-backend.onrender.com,your-custom-domain.com`

```bash
# 필수 설정
PYTHON_VERSION=3.11.0
DJANGO_SECRET_KEY=your-secret-key-here  # Django 시크릿 키 (랜덤 문자열 생성)
DEBUG=False
ALLOWED_HOSTS=your-render-app.onrender.com  # 위에서 확인한 도메인 (https:// 제외)
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

### 5. 데이터베이스 마이그레이션 및 초기 데이터 로드

**✅ 자동 실행 (무료 플랜 포함):**

Render는 `render.yaml`의 `buildCommand`에 다음 명령어들이 포함되어 있어 **배포 시 자동으로 실행**됩니다:

```bash
python manage.py migrate          # 데이터베이스 마이그레이션
python manage.py load_places       # 관광지 데이터 로드
python manage.py load_festivals    # 축제 데이터 로드
```

따라서 **Shell 기능 없이도** 마이그레이션과 초기 데이터 로드가 자동으로 완료됩니다.

**⚠️ 참고:**
- Shell 기능은 유료 플랜에서만 사용 가능하지만, `buildCommand`를 통해 모든 명령어가 자동 실행됩니다
- 배포 로그에서 마이그레이션 및 데이터 로드 과정을 확인할 수 있습니다
- 데이터 로드에 시간이 걸릴 수 있으므로 첫 배포 시 빌드 시간이 길어질 수 있습니다

**수동 실행이 필요한 경우 (Shell 사용 불가 시):**

만약 데이터를 다시 로드하거나 업데이트해야 하는 경우:
1. `render.yaml`의 `buildCommand`에 `--clear` 옵션 추가 (기존 데이터 삭제 후 재로드)
2. 또는 코드에서 데이터 로드 로직을 API 엔드포인트로 만들어 관리자 페이지에서 실행

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
   # 필수: 백엔드 API URL
   VITE_API_URL=https://your-render-app.onrender.com/api
   
   # 소셜 로그인 (선택사항이지만 기능 사용 시 필수)
   VITE_KAKAO_REST_API_KEY=your-kakao-rest-api-key
   VITE_KAKAO_REDIRECT_URI=https://your-vercel-app.vercel.app/auth/kakao/callback
   VITE_GOOGLE_CLIENT_ID=your-google-client-id
   VITE_GOOGLE_REDIRECT_URI=https://your-vercel-app.vercel.app/auth/google/callback
   VITE_NAVER_CLIENT_ID=your-naver-client-id
   VITE_NAVER_REDIRECT_URI=https://your-vercel-app.vercel.app/auth/naver/callback
   ```
   - `your-render-app.onrender.com`은 Render에서 배포한 백엔드 URL입니다.
   - `your-vercel-app.vercel.app`은 Vercel에서 배포한 프론트엔드 URL입니다.
   - ⚠️ **중요**: 환경 변수 추가 후 **재배포**가 필요합니다.

5. **"Deploy"** 클릭

### 3. vercel.json 설정 확인

**⚠️ 중요**: Vercel 프로젝트의 Root Directory가 `frontend`로 설정되어 있다면, `vercel.json` 파일은 `frontend` 폴더에 있어야 합니다.

`frontend/vercel.json` 파일이 있어야 하며, 이 파일은 SPA 라우팅을 위한 리라이트 규칙을 포함합니다:

```json
{
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ]
}
```

이 파일이 없으면 `/auth/kakao/callback` 같은 라우트에서 404 에러가 발생할 수 있습니다.

### 4. 커스텀 도메인 설정 (선택사항)

1. Vercel 대시보드에서 프로젝트 선택
2. **"Settings"** → **"Domains"** 이동
3. 원하는 도메인 추가
4. **"Invalid Configuration" 경고가 나타나는 경우:**
   - 이는 DNS 설정이 완료되지 않아서 나타나는 정상적인 경고입니다
   - 배포는 정상적으로 진행되며, Vercel의 기본 도메인(`*.vercel.app`)을 사용할 수 있습니다
   - 커스텀 도메인을 사용하려면 DNS 설정이 필요합니다 (아래 참조)

#### DNS 설정 방법 (커스텀 도메인 사용 시)

1. Vercel의 **"Domains"** 페이지에서 추가한 도메인을 클릭합니다
2. Vercel이 제공하는 DNS 레코드를 확인합니다:
   - **A 레코드** 또는 **CNAME 레코드**
   - 예: `76.76.21.21` (A 레코드) 또는 `cname.vercel-dns.com` (CNAME 레코드)
3. 도메인 등록 업체(예: 가비아, 후이즈, GoDaddy 등)의 DNS 관리 페이지로 이동합니다
4. Vercel에서 제공한 DNS 레코드를 추가합니다:
   - **A 레코드**: `@` 또는 루트 도메인 → Vercel IP 주소
   - **CNAME 레코드**: `www` → Vercel CNAME 주소
5. DNS 전파까지 **몇 분~24시간** 정도 소요될 수 있습니다
6. DNS 전파가 완료되면 "Invalid Configuration" 경고가 사라지고 "Valid Configuration"으로 변경됩니다

**중요**: 
- DNS 설정이 완료되기 전까지는 Vercel의 기본 도메인(`tripify-two.vercel.app`)을 사용하세요
- 배포 및 기능 테스트는 기본 도메인으로도 정상적으로 작동합니다

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
2. 기존 애플리케이션 수정 또는 새로 등록:
   - **서비스 URL**: 프로덕션 URL로 변경 (`https://your-app.vercel.app`)
     - ⚠️ **중요**: 네이버는 서비스 URL을 하나만 등록할 수 있습니다
     - 로컬 개발을 계속하려면: 프로덕션 URL로 변경하되, 로컬에서는 환경 변수로 다른 URL 사용 가능
   - **Callback URL**: 프로덕션 URL 추가 (`https://your-app.vercel.app/auth/naver/callback`)
     - 네이버는 여러 Callback URL을 등록할 수 있습니다
     - 로컬 개발용도 유지하려면: `http://localhost:5173/auth/naver/callback`도 함께 등록
3. Client ID와 Client Secret 확인

**로컬 개발과 프로덕션 모두 사용하는 경우:**
- 서비스 URL: 프로덕션 URL (`https://your-app.vercel.app`)로 설정
- Callback URL: 두 개 모두 등록
  - `http://localhost:5173/auth/naver/callback` (로컬 개발용)
  - `https://your-app.vercel.app/auth/naver/callback` (프로덕션용)

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

### 사이트는 접속되지만 기능이 동작하지 않는 경우

**가장 흔한 원인과 해결 방법:**

1. **Vercel 환경 변수 미설정**
   - Vercel 대시보드 → Settings → Environment Variables
   - `VITE_API_URL=https://your-render-app.onrender.com/api` 확인
   - 설정 후 **재배포 필요**

2. **Render CORS 설정 누락**
   - Render 대시보드 → Web Service → Environment
   - `CORS_ALLOWED_ORIGINS=https://your-vercel-app.vercel.app` 확인
   - 설정 후 **서비스 재시작 필요**

3. **브라우저 개발자 도구 확인**
   - F12 → Console 탭: 에러 메시지 확인
   - Network 탭: API 요청 실패 여부 확인

자세한 문제 해결 가이드는 `TROUBLESHOOTING.md` 파일을 참조하세요.

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

