# 배포 후 문제 해결 가이드

## 사이트는 접속되지만 기능이 동작하지 않는 경우

### 즉시 확인할 사항

1. **"카카오 API 키가 설정되지 않았습니다" 모달이 나타나는 경우**
   - **원인**: Vercel 환경 변수에 `VITE_KAKAO_REST_API_KEY`가 설정되지 않음
   - **해결**: Vercel 대시보드 → Settings → Environment Variables에서 추가
   - 환경 변수 추가 후 **재배포 필수**

2. **Network 탭에서 API 요청이 실패하는 경우**
   - **원인**: `VITE_API_URL` 미설정 또는 CORS 문제
   - **해결**: 
     - Vercel 환경 변수에 `VITE_API_URL` 설정 확인
     - Render 환경 변수에 `CORS_ALLOWED_ORIGINS` 설정 확인

## 환경 변수 추가 후에도 동작하지 않는 경우

### ⚠️ 가장 중요한 확인 사항: 재배포/재시작

**환경 변수를 추가한 후에는 반드시 재배포/재시작이 필요합니다!**

#### Vercel 재배포 방법:
1. Vercel 대시보드 → **Deployments** 탭
2. 최신 배포 항목의 **"..."** 메뉴 클릭
3. **"Redeploy"** 선택
4. 또는 **"Redeploy"** 버튼 직접 클릭

#### Render 재시작 방법:
1. Render 대시보드 → Web Service 선택
2. **"Manual Deploy"** 클릭
3. **"Deploy latest commit"** 선택
4. 또는 환경 변수 수정 후 자동으로 재시작될 때까지 대기 (몇 분 소요)

### 환경 변수 값 확인

환경 변수가 설정되어 있어도 **값이 정확한지** 확인해야 합니다:

#### Vercel 환경 변수 확인:
- `VITE_API_URL`: `https://your-render-app.onrender.com/api` (끝에 `/api` 필수)
- `VITE_KAKAO_REDIRECT_URI`: `https://tripify-two.vercel.app/auth/kakao/callback` (Vercel URL과 일치)
- `VITE_GOOGLE_REDIRECT_URI`: `https://tripify-two.vercel.app/auth/google/callback`
- `VITE_NAVER_REDIRECT_URI`: `https://tripify-two.vercel.app/auth/naver/callback`

#### Render 환경 변수 확인:
- `CORS_ALLOWED_ORIGINS`: `https://tripify-two.vercel.app` (정확히 일치, 공백 없음)
- `ALLOWED_HOSTS`: `your-render-app.onrender.com` (Render 도메인)
- `KAKAO_REDIRECT_URI`: `https://tripify-two.vercel.app/auth/kakao/callback`
- `GOOGLE_REDIRECT_URI`: `https://tripify-two.vercel.app/auth/google/callback`
- `NAVER_REDIRECT_URI`: `https://tripify-two.vercel.app/auth/naver/callback`

### 브라우저 캐시 문제

환경 변수를 추가하고 재배포한 후에도 문제가 있다면:
1. **강력 새로고침**: `Ctrl + Shift + R` (Windows) 또는 `Cmd + Shift + R` (Mac)
2. **시크릿 모드에서 테스트**: 캐시 없이 테스트
3. **브라우저 개발자 도구 → Application → Clear storage**: 모든 캐시 삭제

## 사이트는 접속되지만 기능이 동작하지 않는 경우

### 1. 브라우저 개발자 도구 확인 (가장 먼저 확인!)

1. **F12** 키를 눌러 개발자 도구 열기
2. **Console** 탭에서 에러 메시지 확인
3. **Network** 탭에서 API 요청 상태 확인
   - API 요청이 실패하는지 확인
   - CORS 에러가 있는지 확인
   - 404, 500 등의 HTTP 상태 코드 확인

### 2. Vercel 환경 변수 확인

**문제**: 프론트엔드가 백엔드 API를 찾지 못함

**해결 방법**:
1. Vercel 대시보드 → 프로젝트 선택 → **Settings** → **Environment Variables**
2. 다음 환경 변수가 설정되어 있는지 확인:
   ```
   VITE_API_URL=https://your-render-app.onrender.com/api
   ```
   - ⚠️ **중요**: `https://`로 시작해야 함
   - ⚠️ **중요**: 끝에 `/api` 포함해야 함
   - ⚠️ **중요**: Render에서 제공한 실제 백엔드 URL 사용

3. 환경 변수 수정 후 **재배포 필요**:
   - Vercel 대시보드 → **Deployments** → 최신 배포의 **"..."** 메뉴 → **"Redeploy"**

### 3. Render CORS 설정 확인

**문제**: CORS 에러로 인해 API 요청이 차단됨

**해결 방법**:
1. Render 대시보드 → Web Service (`tripify-backend`) 선택
2. **Environment** 탭에서 `CORS_ALLOWED_ORIGINS` 확인:
   ```
   CORS_ALLOWED_ORIGINS=https://your-vercel-app.vercel.app
   ```
   - ⚠️ **중요**: Vercel 배포 URL과 정확히 일치해야 함
   - ⚠️ **중요**: `https://` 포함
   - ⚠️ **중요**: 여러 URL 사용 시 쉼표로 구분 (공백 없이)

3. 환경 변수 수정 후 서비스 **재시작**:
   - Render 대시보드 → **"Manual Deploy"** → **"Deploy latest commit"**

### 4. Render 백엔드 서버 상태 확인

**문제**: 백엔드 서버가 실행되지 않음

**해결 방법**:
1. Render 대시보드 → Web Service 선택
2. **Logs** 탭에서 에러 메시지 확인
3. **Metrics** 탭에서 서버가 실행 중인지 확인
4. 직접 API 테스트:
   - 브라우저에서 `https://your-render-app.onrender.com/api/` 접속
   - 응답이 오는지 확인 (에러 페이지가 아닌 JSON 응답이어야 함)

### 5. 데이터베이스 연결 확인

**문제**: 데이터베이스 연결 실패

**해결 방법**:
1. Render 대시보드 → Web Service → **Logs** 탭
2. 데이터베이스 연결 에러 확인:
   - `DATABASE_URL` 환경 변수가 올바른지 확인
   - PostgreSQL 서비스가 실행 중인지 확인

### 6. 환경 변수 누락 확인

**Render에서 필수 환경 변수 확인**:
- `DJANGO_SECRET_KEY` ✅
- `DEBUG=False` ✅
- `ALLOWED_HOSTS=your-render-app.onrender.com` ✅
- `DATABASE_URL` ✅ (자동 설정됨)
- `CORS_ALLOWED_ORIGINS=https://your-vercel-app.vercel.app` ✅

### 7. 브라우저 캐시 문제

**해결 방법**:
1. **Ctrl + Shift + R** (Windows) 또는 **Cmd + Shift + R** (Mac)으로 강력 새로고침
2. 또는 브라우저 시크릿 모드에서 테스트

---

## 체크리스트

배포 후 기능이 동작하지 않을 때 다음을 순서대로 확인하세요:

- [ ] 브라우저 개발자 도구 Console 탭에서 에러 확인
- [ ] 브라우저 개발자 도구 Network 탭에서 API 요청 상태 확인
- [ ] Vercel 환경 변수 `VITE_API_URL` 설정 확인 및 재배포
- [ ] Render 환경 변수 `CORS_ALLOWED_ORIGINS` 설정 확인 및 재시작
- [ ] Render 백엔드 서버가 실행 중인지 확인 (Logs 탭)
- [ ] 브라우저에서 백엔드 API 직접 접속 테스트
- [ ] 브라우저 캐시 삭제 후 재시도

---

### 카카오 로그인 콜백 404 에러

**에러**: `GET https://tripify-two.vercel.app/auth/kakao/callback?code=...` → `404 (Not Found)`

**원인**: 
1. Vercel의 SPA 리라이트 규칙이 적용되지 않음
2. `vercel.json` 파일이 잘못된 위치에 있음
3. Vercel 프로젝트 설정에서 Root Directory가 잘못 설정됨

**해결 방법**:

1. **vercel.json 파일 위치 확인**
   - `vercel.json`은 프로젝트 루트에 있어야 합니다
   - Vercel 프로젝트 설정에서 Root Directory가 `frontend`로 설정되어 있다면, `vercel.json`도 `frontend` 폴더에 있어야 합니다

2. **Vercel 프로젝트 설정 확인**
   - Vercel 대시보드 → 프로젝트 선택 → Settings → General
   - **Root Directory**: `frontend`로 설정되어 있는지 확인
   - **Framework Preset**: `Vite`로 설정되어 있는지 확인

3. **vercel.json 내용 확인**
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

4. **재배포**
   - `vercel.json` 수정 후 Vercel 재배포 필요
   - Deployments → "..." → "Redeploy"

5. **대안: vercel.json을 frontend 폴더로 이동**
   - Root Directory가 `frontend`로 설정되어 있다면
   - `vercel.json`을 `frontend/vercel.json`으로 이동
   - 또는 프로젝트 루트에 두고 Root Directory를 `.`로 설정

### Mixed Content 경고 (HTTP 이미지)

**경고**: `Mixed Content: The page at 'https://...' was loaded over HTTPS, but requested an insecure element 'http://tong.visitkorea.or.kr/...'`

**원인**: 
- HTTPS 페이지에서 HTTP 이미지를 로드하려고 시도
- 데이터베이스에 저장된 이미지 URL이 `http://`로 시작

**해결 방법**:
- ✅ **이미 해결됨**: 백엔드 serializer에서 자동으로 HTTP를 HTTPS로 변환하도록 수정됨
- 변경사항을 배포하면 경고가 사라집니다

**참고**: 
- 이것은 오류가 아니라 경고입니다
- 브라우저가 자동으로 HTTPS로 업그레이드하므로 이미지는 정상적으로 표시됩니다
- 하지만 경고를 없애기 위해 백엔드에서 자동 변환하도록 수정했습니다

## 일반적인 에러 메시지와 해결 방법

### "Failed to fetch" 또는 "Network Error"
- **원인**: 백엔드 서버가 실행되지 않음 또는 CORS 문제
- **해결**: Render 서버 상태 확인, CORS 설정 확인

### "CORS policy: No 'Access-Control-Allow-Origin' header"
- **원인**: CORS 설정 누락 또는 잘못된 URL
- **해결**: `CORS_ALLOWED_ORIGINS`에 정확한 Vercel URL 추가

### "404: NOT_FOUND" (Vercel 에러 페이지)
- **원인**: 
  1. `VITE_API_URL`이 잘못 설정되었거나
  2. Render 백엔드 서버가 실행되지 않았거나
  3. API 엔드포인트 경로가 잘못되었거나
  4. CORS 문제로 인해 요청이 차단됨
- **해결 방법**:
  1. **Vercel 환경 변수 확인**: `VITE_API_URL`이 `https://your-render-app.onrender.com/api`로 설정되어 있는지 확인
  2. **Render 백엔드 서버 상태 확인**: Render 대시보드 → Web Service → Logs 탭에서 서버가 실행 중인지 확인
  3. **직접 API 테스트**: 브라우저에서 `https://your-render-app.onrender.com/api/places/` 접속하여 응답 확인
  4. **Network 탭 확인**: 개발자 도구 → Network 탭에서 실패한 요청의 실제 URL 확인
  5. **CORS 설정 확인**: Render 환경 변수 `CORS_ALLOWED_ORIGINS`에 Vercel URL이 포함되어 있는지 확인

### "404 Not Found"
- **원인**: API URL이 잘못됨
- **해결**: `VITE_API_URL`이 올바른지 확인 (끝에 `/api` 포함)

### "500 Internal Server Error"
- **원인**: 백엔드 서버 내부 오류
- **해결**: Render Logs 탭에서 상세 에러 확인

---

## 빠른 테스트 방법

### 1. 백엔드 API 직접 테스트
브라우저에서 다음 URL 접속:
```
https://your-render-app.onrender.com/api/places/
```
- 정상: JSON 데이터가 표시됨
- 비정상: 에러 페이지 또는 연결 실패

### 2. 프론트엔드 환경 변수 확인
브라우저 개발자 도구 Console에서:
```javascript
console.log(import.meta.env.VITE_API_URL)
```
- 정상: `https://your-render-app.onrender.com/api` 출력
- 비정상: `undefined` 또는 `http://localhost:8000/api` 출력

### 3. API 요청 테스트
브라우저 개발자 도구 Console에서:
```javascript
fetch('https://your-render-app.onrender.com/api/places/')
  .then(r => r.json())
  .then(console.log)
  .catch(console.error)
```

---

## 추가 도움말

문제가 계속되면 다음 정보를 확인하세요:
1. 브라우저 개발자 도구 Console의 전체 에러 메시지
2. 브라우저 개발자 도구 Network 탭의 실패한 요청 상세 정보
3. Render 대시보드 Logs 탭의 최근 에러 로그
4. Vercel 배포 로그

