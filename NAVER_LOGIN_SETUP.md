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

1. **서비스 URL 변경**
   - 실제 도메인으로 변경 (예: `https://yourdomain.com`)

2. **Callback URL 변경**
   - 실제 도메인으로 변경 (예: `https://yourdomain.com/auth/naver/callback`)

3. **환경 변수 업데이트**
   - Backend `.env`: `NAVER_REDIRECT_URI`를 프로덕션 URL로 변경
   - Frontend `.env`: `VITE_NAVER_REDIRECT_URI`를 프로덕션 URL로 변경

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

