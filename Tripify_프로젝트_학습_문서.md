# Tripify 프로젝트 완벽 가이드 📚

> AI 기반 여행 계획 웹 애플리케이션 학습 문서

---

## 목차

1. [프로젝트 개요](#1-프로젝트-개요)
2. [기술 스택](#2-기술-스택)
3. [프로젝트 구조](#3-프로젝트-구조)
4. [주요 기능](#4-주요-기능)
5. [시스템 아키텍처](#5-시스템-아키텍처)
6. [백엔드 상세 분석](#6-백엔드-상세-분석)
7. [프론트엔드 상세 분석](#7-프론트엔드-상세-분석)
8. [AI 통합 상세](#8-ai-통합-상세)
9. [인증 및 보안](#9-인증-및-보안)
10. [데이터베이스 구조](#10-데이터베이스-구조)
11. [API 엔드포인트](#11-api-엔드포인트)
12. [주요 플로우](#12-주요-플로우)

---

## 1. 프로젝트 개요

### 1.1 프로젝트 소개

**Tripify**는 AI를 활용한 지능형 여행 계획 웹 애플리케이션입니다. 사용자의 예산, 일정, 선호도를 기반으로 Claude Haiku 4.5 AI가 실제 관광지, 숙소, 음식점 데이터를 활용하여 맞춤형 여행 일정을 자동으로 생성합니다.

### 1.2 핵심 가치

- **AI 기반 자동화**: 복잡한 여행 계획을 AI가 자동으로 수립
- **실제 데이터 통합**: 한국 관광공사 데이터 기반의 실제 장소 정보
- **예산 최적화**: 사용자 예산 내에서 최적의 일정 생성
- **소셜 통합**: 카카오, 구글, 네이버 간편 로그인
- **커뮤니티**: 여행 계획 공유 및 추천 시스템

### 1.3 아키텍처 패턴

- **Frontend-Backend Separation** (SPA 방식)
- **RESTful API** 통신
- **Token-based Authentication** (DRF Token)
- **AI-Enhanced** 기능

---

## 2. 기술 스택

### 2.1 백엔드

| 기술 | 버전 | 용도 |
|------|------|------|
| **Django** | 5.2.9 | 웹 프레임워크 |
| **Django REST Framework** | 3.16.1 | REST API 구축 |
| **django-cors-headers** | 4.9.0 | CORS 처리 |
| **django-filter** | 24.3 | 쿼리 필터링 |
| **Pillow** | 12.0.0 | 이미지 처리 |
| **python-dotenv** | 1.2.1 | 환경 변수 관리 |
| **requests** | 2.32.3 | HTTP 통신 (OAuth) |
| **SQLite3** | - | 개발용 데이터베이스 |

### 2.2 프론트엔드

| 기술 | 버전 | 용도 |
|------|------|------|
| **Vue 3** | 3.5.25 | 프론트엔드 프레임워크 |
| **Vite** | 7.2.4 | 빌드 도구 |
| **Vue Router** | 4.6.3 | 클라이언트 라우팅 |
| **Pinia** | 3.0.4 | 상태 관리 (Vuex 후속) |
| **Axios** | 1.13.2 | HTTP 클라이언트 |
| **ESLint & Prettier** | - | 코드 품질 관리 |

### 2.3 AI 및 외부 서비스

- **SSAFY GMS API**: Claude Haiku 4.5 AI 접근
- **Kakao OAuth 2.0**: 소셜 로그인
- **Google OAuth 2.0**: 소셜 로그인
- **Naver OAuth 2.0**: 소셜 로그인
- **Gmail SMTP**: 이메일 인증
- **Kakao Maps API**: 지도 통합

---

## 3. 프로젝트 구조

### 3.1 백엔드 구조

```
backend/
├── config/                      # Django 프로젝트 설정
│   ├── settings.py             # 메인 설정 (DB, 앱, 미들웨어, OAuth)
│   ├── urls.py                 # 루트 URL 라우팅
│   └── wsgi.py                 # WSGI 설정
│
├── accounts/                    # 사용자 인증 및 계정 관리
│   ├── models.py               # User, EmailVerificationToken, PasswordResetToken, PasswordHistory
│   ├── views.py                # 회원가입, 로그인, 로그아웃, 프로필, OAuth 콜백
│   ├── serializers.py          # 데이터 직렬화/검증
│   ├── urls.py                 # 인증 엔드포인트
│   ├── kakao_service.py        # 카카오 OAuth 통합
│   ├── google_service.py       # 구글 OAuth 통합
│   ├── naver_service.py        # 네이버 OAuth 통합
│   └── email_utils.py          # 이메일 인증 유틸
│
├── trips/                       # 여행 계획 관리
│   ├── models.py               # TravelPlan, Itinerary, ItineraryPlace, Wishlist
│   ├── views.py                # 여행 계획 CRUD, AI 생성
│   ├── serializers.py          # 여행 계획 데이터 검증
│   └── urls.py                 # 여행 계획 엔드포인트
│
├── places/                      # 관광지/장소 관리
│   ├── models.py               # Place, Bookmark
│   ├── views.py                # 장소 검색, 북마크
│   ├── management/commands/    # 데이터 import 명령
│   └── urls.py                 # 장소 엔드포인트
│
├── festivals/                   # 축제/이벤트 관리
│   ├── models.py               # Festival 모델
│   ├── views.py                # 축제 검색/필터링
│   ├── management/commands/    # 축제 데이터 import
│   └── urls.py                 # 축제 엔드포인트
│
├── ai/                          # AI 서비스 통합
│   └── gemini_service.py       # Claude Haiku 4.5 통합 (1300+ 줄)
│                               #   - 여행 일정 생성
│                               #   - 예산 검증
│                               #   - 실제 DB 데이터 통합
│                               #   - 일정 수정
│
├── tourism_data/                # 정적 관광 데이터 (JSON 파일)
│   ├── 관광지/                  # 카테고리별 관광 명소
│   ├── 레포츠/                  # 스포츠/레저 활동
│   ├── 문화시설/                # 문화 시설
│   ├── 쇼핑/                    # 쇼핑 장소
│   ├── 숙박/                    # 숙박 시설
│   ├── 음식점/                  # 음식점
│   └── 축제공연행사/            # 축제 및 행사
│
├── db.sqlite3                   # SQLite 데이터베이스
├── manage.py                    # Django 관리 스크립트
└── requirements.txt             # Python 의존성
```

### 3.2 프론트엔드 구조

```
frontend/
├── src/
│   ├── views/                   # 페이지 컴포넌트
│   │   ├── HomeView.vue        # 랜딩 페이지
│   │   ├── LoginView.vue       # 소셜 OAuth 로그인
│   │   ├── SignupView.vue      # 사용자 등록
│   │   ├── TripPlanView.vue    # 여행 계획 작성 폼
│   │   ├── MyTripsView.vue     # 사용자 여행 목록
│   │   ├── ItineraryView.vue   # 상세 일정 표시
│   │   ├── FestivalsView.vue   # 축제 검색/탐색
│   │   ├── FestivalDetailView.vue
│   │   ├── AccountSettingsView.vue  # 사용자 프로필 설정
│   │   ├── RecommendedTripsView.vue # 커뮤니티 추천 여행
│   │   ├── VerifyEmailView.vue      # 이메일 인증
│   │   ├── FindUsernameView.vue
│   │   ├── ResetPasswordRequestView.vue
│   │   └── *CallbackView.vue   # OAuth 콜백 핸들러
│   │
│   ├── components/              # 재사용 가능 컴포넌트
│   │   ├── common/
│   │   │   ├── Header.vue
│   │   │   ├── Footer.vue
│   │   │   ├── LoadingSpinner.vue
│   │   │   └── ScrollToTop.vue
│   │   ├── trip/
│   │   │   ├── TripForm.vue
│   │   │   ├── BudgetInput.vue
│   │   │   ├── DatePicker.vue
│   │   │   └── RegionSelector.vue
│   │   ├── itinerary/
│   │   │   ├── ItineraryCard.vue
│   │   │   ├── ItineraryMap.vue
│   │   │   ├── MapView.vue
│   │   │   └── PlaceDetail.vue
│   │   ├── user/
│   │   │   ├── LoginForm.vue
│   │   │   └── SignupForm.vue
│   │   └── KakaoMapSearch.vue
│   │
│   ├── stores/                  # Pinia 상태 관리
│   │   ├── auth.js             # 인증 상태
│   │   ├── trip.js             # 여행 계획 상태
│   │   └── place.js            # 장소/북마크 상태
│   │
│   ├── api/                     # API 서비스 레이어
│   │   ├── axios.js            # Axios 설정
│   │   ├── auth.js             # 인증 API 호출
│   │   ├── trip.js             # 여행 API 호출
│   │   ├── place.js            # 장소 API 호출
│   │   └── festivals.js        # 축제 API 호출
│   │
│   ├── router/
│   │   └── index.js            # 라우트 정의
│   │
│   ├── assets/
│   │   ├── img/                # 이미지 및 로고
│   │   └── styles/             # 전역 스타일
│   │
│   ├── App.vue                 # 루트 컴포넌트
│   └── main.js                 # 애플리케이션 진입점
│
├── public/                      # 정적 에셋
├── package.json                 # Node 의존성
├── vite.config.js              # Vite 설정
└── index.html                  # HTML 템플릿
```

---

## 4. 주요 기능

### 4.1 사용자 관리 기능

#### 인증 시스템
- ✅ 이메일 인증을 통한 전통적 회원가입/로그인
- ✅ 소셜 OAuth 로그인 (카카오, 구글, 네이버)
- ✅ 이메일을 통한 비밀번호 재설정
- ✅ 사용자명 찾기
- ✅ 토큰 기반 인증 (6시간 자동 로그아웃)

#### 사용자 프로필 관리
- ✅ 프로필 편집 (닉네임, 이미지, 선호도)
- ✅ 비밀번호 변경 (최근 5개 비밀번호 재사용 방지)
- ✅ 계정 삭제
- ✅ 여행 스타일 선호도 설정

### 4.2 여행 계획 기능

#### AI 기반 일정 생성
- 🤖 **입력 항목**: 예산, 날짜, 지역, 인원, 여행 스타일, 숙박 유형
- 🤖 Claude Haiku 4.5가 상세한 일일 일정 생성
- 🤖 실제 데이터베이스 통합 (실제 장소, 음식점, 호텔 사용)
- 🤖 예산 검증 및 제약 조건 적용
- 🤖 일별 자동 비용 계산

#### 수동 여행 계획
- ✏️ 커스텀 여행 계획 생성
- ✏️ 일정 추가/수정/삭제
- ✏️ 일별 스케줄 관리
- ✏️ 교통, 숙박, 식사 추적

#### 일정 관리
- 📅 상세 일일 스케줄 보기
- 📅 시간, 소요 시간, 설명이 포함된 관광지
- 📅 교통 정보 (방법, 비용)
- 📅 숙박 세부 정보
- 📅 식사 계획 (아침, 점심, 저녁)
- 📅 축제/이벤트 통합
- 📅 일별 비용 추정

#### AI 일정 수정
- 🔄 자연어 요청으로 기존 일정 수정
- 🔄 원래 구조 유지하면서 변경 사항 적용
- 🔄 수정 후 예산 재검증

### 4.3 탐색 및 발견 기능

#### 장소 관리
- 🗺️ 지역별 관광 명소 탐색
- 🗺️ 카테고리별 장소 검색
- 🗺️ 즐겨찾기 장소 북마크
- 🗺️ 장소 세부 정보 보기 (주소, 설명, 이미지)

#### 축제 정보
- 🎉 지역 및 월별 축제 탐색
- 🎉 카테고리별 필터링
- 🎉 축제 세부 정보 보기 (날짜, 위치, 설명)
- 🎉 여행 계획과 통합

#### 추천 여행
- ⭐ 커뮤니티에 여행 추천
- ⭐ 다른 사용자의 추천 일정 탐색
- ⭐ 여행 평가 시스템
- ⭐ 여행자 리뷰 읽기

### 4.4 추가 기능

#### 위시리스트 시스템
- ❤️ 여행 위시리스트 항목 생성
- ❤️ 완료/체크 표시
- ❤️ 여행 버킷리스트 관리

#### 지도 통합
- 🗾 카카오맵 통합
- 🗾 여행 위치 시각화
- 🗾 지도에서 장소 검색

---

## 5. 시스템 아키텍처

### 5.1 전체 아키텍처 다이어그램

```
┌─────────────────────────────────────────────────────────────────────┐
│                      사용자 인터페이스 (Vue 3)                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │ 로그인/회원가입│  │ 여행 계획    │  │ 일정 보기    │              │
│  │   화면       │  │   화면       │  │   화면       │   ...        │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘              │
└─────────┼──────────────────┼──────────────────┼────────────────────┘
          │                  │                  │
          │  ┌──────────────────────────────────┐
          └─►│   Pinia Stores (상태 관리)       │◄──────────┐
             │  • auth.js                       │           │
             │  • trip.js                       │           │
             │  • place.js                      │           │
             └──────────────┬───────────────────┘           │
                            │                               │
          ┌─────────────────┼───────────────────────────────┘
          │                 │
          ▼                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        API 레이어 (Axios)                            │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐           │
│  │ auth.js  │  │ trip.js  │  │ place.js │  │festivals │           │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘           │
└───────┼─────────────┼─────────────┼──────────────┼─────────────────┘
        │             │             │              │
        │ HTTP        │ HTTP        │ HTTP         │ HTTP
        │ Requests    │ Requests    │ Requests     │ Requests
        ▼             ▼             ▼              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   DJANGO REST FRAMEWORK                              │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                    URL Router (urls.py)                       │  │
│  │  /api/auth/*  /api/travel/*  /api/places/*  /api/festivals/* │  │
│  └──────┬────────────────┬────────────────┬──────────────┬───────┘  │
│         │                │                │              │           │
│  ┌──────▼───────┐ ┌─────▼────────┐ ┌────▼──────┐ ┌─────▼────────┐ │
│  │  accounts    │ │    trips     │ │  places   │ │  festivals   │ │
│  │  ViewSet     │ │  ViewSet     │ │  ViewSet  │ │  ViewSet     │ │
│  └──────┬───────┘ └─────┬────────┘ └────┬──────┘ └─────┬────────┘ │
│         │               │               │              │           │
│  ┌──────▼────────────────▼───────────────▼──────────────▼────────┐ │
│  │               Serializers (검증)                               │ │
│  └───────────────────────────┬───────────────────────────────────┘ │
└────────────────────────────┬─┴───────────────────────────────────┘
                             │
        ┌────────────────────┼───────────────────────┐
        │                    │                       │
        ▼                    ▼                       ▼
┌──────────────┐    ┌───────────────┐    ┌─────────────────────┐
│   모델       │    │   AI 서비스   │    │  외부 서비스        │
│              │    │               │    │                     │
│ • User       │    │ GeminiService │    │ • Kakao OAuth       │
│ • TravelPlan │◄───┤ (Claude 4.5)  │    │ • Google OAuth      │
│ • Itinerary  │    │               │    │ • Naver OAuth       │
│ • Place      │◄───┤ • 일정 생성   │    │ • Gmail SMTP        │
│ • Festival   │    │ • 일정 수정   │    │ • Kakao Maps API    │
│ • Bookmark   │    │ • 예산 검증   │    │                     │
│ • Wishlist   │    │               │    └─────────────────────┘
│              │    └───────────────┘
└──────┬───────┘
       │
       ▼
┌──────────────────┐
│  SQLite Database │
└──────────────────┘
```

### 5.2 데이터 흐름

#### 요청 흐름
1. 사용자가 Vue 컴포넌트에서 액션 수행
2. Pinia Store의 액션 호출
3. API 서비스 레이어 (Axios)를 통해 HTTP 요청
4. Django URL Router가 요청을 적절한 ViewSet으로 라우팅
5. Serializer가 데이터 검증
6. View가 비즈니스 로직 처리 (필요시 AI 서비스 호출)
7. 데이터베이스 CRUD 작업
8. Serializer가 응답 데이터 직렬화
9. JSON 응답 반환
10. Pinia Store가 상태 업데이트
11. Vue 컴포넌트가 리렌더링

#### 인증 흐름
1. 로그인 시 백엔드가 Token 생성
2. 프론트엔드가 localStorage에 토큰 저장
3. Axios 인터셉터가 모든 요청에 `Authorization: Token XXX` 헤더 추가
4. 백엔드가 보호된 엔드포인트에서 토큰 검증
5. 6시간 후 자동 로그아웃

---

## 6. 백엔드 상세 분석

### 6.1 Accounts 앱

#### 모델 (`accounts/models.py`)

**User 모델 (커스텀)**
```python
class User(AbstractUser):
    nickname = models.CharField(max_length=50, unique=True)
    profile_image = models.ImageField(upload_to='profiles/', null=True, blank=True)
    travel_style = models.CharField(max_length=50, null=True, blank=True)
    kakao_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    google_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    naver_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    is_email_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
```

**EmailVerificationToken 모델**
- 이메일 인증용 토큰 생성 및 관리
- 토큰 만료 시간 설정

**PasswordResetToken 모델**
- 비밀번호 재설정 토큰 관리

**PasswordHistory 모델**
- 최근 5개 비밀번호 저장하여 재사용 방지

#### 주요 뷰 함수 - 실제 코드

**1. 회원가입 (`accounts/views.py:20-45`)**

```python
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
```

**핵심 로직:**
- `SignupSerializer`로 데이터 검증 (비밀번호 강도, 중복 확인 등)
- 사용자 생성 후 `EmailVerificationToken` 생성
- 이메일 발송 실패해도 회원가입은 성공 처리

**2. 로그인 (`accounts/views.py:48-77`)**

```python
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
```

**핵심 로직:**
- Django의 `authenticate()`로 사용자 인증
- 이메일 미인증 사용자는 로그인 거부 (`login_type='normal'`인 경우만)
- DRF Token 생성 또는 조회

**3. 카카오 소셜 로그인 (`accounts/views.py:104-178`)**

```python
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
            if not email:
                email = f"kakao_{kakao_id}@kakao.user"

            username = f"kakao_{kakao_id}"

            # 이메일 중복 체크
            if User.objects.filter(email=email).exists():
                email = f"kakao_{kakao_id}@kakao.user"

            try:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    nickname=nickname if nickname else '',
                    kakao_id=kakao_id,
                    login_type='kakao',
                    is_email_verified=True,  # 소셜 로그인은 자동 인증
                )
                user.set_unusable_password()  # 비밀번호 사용 불가능하게 설정
                user.save()
            except IntegrityError:
                return Response({
                    'error': '이미 존재하는 사용자입니다.'
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            # 기존 사용자의 경우 닉네임이 없으면 업데이트
            if not user.nickname and nickname:
                user.nickname = nickname
                user.save()

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
```

**핵심 로직:**
1. **인가 코드 → 액세스 토큰**: `KakaoOAuthService.get_access_token(code)`
2. **사용자 정보 조회**: `KakaoOAuthService.get_user_info(access_token)`
3. **기존 사용자 확인**: `kakao_id`로 조회
4. **신규 사용자 생성**:
   - `username = f"kakao_{kakao_id}"` (고유성 보장)
   - `is_email_verified=True` (소셜 로그인은 자동 인증)
   - `set_unusable_password()` (비밀번호 로그인 방지)
5. **토큰 반환**: DRF Token 생성

**4. 이메일 인증 (`accounts/views.py:341-376`)**

```python
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
```

**5. 회원탈퇴 (`accounts/views.py:587-621`)**

```python
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
```

**핵심 로직:**
- 일반 로그인 사용자는 비밀번호 확인 필수
- 소셜 로그인 사용자는 비밀번호 없이 바로 삭제
- 토큰도 함께 삭제하여 완전한 로그아웃 처리

### 6.2 Trips 앱 - 핵심 코드

#### AI 일정 생성 API (`trips/views.py:61-162`)

```python
@action(detail=False, methods=['post'], url_path='generate')
def generate_itinerary(self, request):
    """AI 여행 코스 생성 API"""
    serializer = TravelPlanCreateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    data = serializer.validated_data

    # AI 서비스를 통해 여행 계획 생성
    try:
        gemini_service = GeminiService()
        itinerary_data = gemini_service.generate_itinerary(
            budget=data['budget'],
            people_count=data['people_count'],
            start_date=data['start_date'],
            end_date=data['end_date'],
            departure_location=data['departure_location'],
            region=data['region'],
            travel_style=data['travel_style'],
            accommodation_type=data['accommodation_type']
        )

        # TravelPlan 생성
        travel_plan = TravelPlan.objects.create(
            user=request.user,
            title=f"{data['region']} {data['travel_style']} 여행",
            budget=data['budget'],
            people_count=data['people_count'],
            start_date=data['start_date'],
            end_date=data['end_date'],
            departure_location=data['departure_location'],
            region=data['region'],
            travel_style=data['travel_style'],
            accommodation_type=data['accommodation_type'],
            is_generated=True
        )

        # 일정 데이터 저장
        created_count = 0
        if itinerary_data and isinstance(itinerary_data, dict) and 'days' in itinerary_data:
            for day_data in itinerary_data['days']:
                try:
                    Itinerary.objects.create(
                        travel_plan=travel_plan,
                        day_number=day_data['day_number'],
                        date=data['start_date'] + timedelta(days=day_data['day_number'] - 1),
                        description=day_data.get('description', ''),
                        attractions=day_data.get('attractions', []),
                        transportation_info=day_data.get('transportation_info', {}),
                        accommodation_info=day_data.get('accommodation_info', {}),
                        meals_info=day_data.get('meals_info', {}),
                        events_info=day_data.get('events_info', []),
                        estimated_cost=day_data.get('estimated_cost', None)
                    )
                    created_count += 1
                except Exception as e:
                    print(f'✗ 일정 생성 오류 (day {day_data.get("day_number", "?")}): {e}')

        print(f'✓ Itinerary 생성 완료: {created_count}개')

        travel_plan.refresh_from_db()
        response_serializer = TravelPlanSerializer(travel_plan)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({
            'error': f'여행 계획 생성 중 오류가 발생했습니다: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
```

**핵심 로직:**
1. **데이터 검증**: `TravelPlanCreateSerializer`로 예산, 날짜, 지역 등 검증
2. **AI 호출**: `GeminiService.generate_itinerary()` 호출하여 일정 생성
3. **TravelPlan 생성**: 여행 계획 메타데이터 저장
4. **Itinerary 생성**: AI가 생성한 일별 일정을 DB에 저장
5. **JSONField 활용**: `attractions`, `meals_info` 등을 JSON으로 저장

#### AI 일정 수정 API (`trips/views.py:234-343`)

```python
@action(detail=True, methods=['post'], url_path='modify')
def modify_plan(self, request, pk=None):
    """여행 계획 수정 API (요구사항에 맞게 AI가 계획 수정)"""
    if pk is None:
        pk = self.kwargs.get('pk')

    # 본인 계획만 수정 가능
    try:
        travel_plan = TravelPlan.objects.get(pk=pk, user=request.user)
    except TravelPlan.DoesNotExist:
        return Response({
            'error': '본인의 여행 계획만 수정할 수 있습니다.'
        }, status=status.HTTP_403_FORBIDDEN)

    # 요구사항 검증
    serializer = TravelPlanModifySerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    requirements = serializer.validated_data['requirements']

    # AI 서비스를 통해 계획 수정
    try:
        gemini_service = GeminiService()
        modified_itinerary_data = gemini_service.modify_itinerary(
            existing_plan=travel_plan,
            requirements=requirements,
            budget=travel_plan.budget,
            people_count=travel_plan.people_count,
            start_date=travel_plan.start_date,
            end_date=travel_plan.end_date,
            departure_location=travel_plan.departure_location,
            region=travel_plan.region,
            travel_style=travel_plan.travel_style,
            accommodation_type=travel_plan.accommodation_type
        )

        # 기존 일정을 업데이트 (삭제하지 않고 수정)
        updated_count = 0
        if modified_itinerary_data and 'days' in modified_itinerary_data:
            existing_itineraries = {
                it.day_number: it
                for it in travel_plan.itineraries.all()
            }

            for day_data in modified_itinerary_data['days']:
                day_number = day_data['day_number']
                try:
                    # 기존 일정이 있으면 업데이트, 없으면 생성
                    if day_number in existing_itineraries:
                        itinerary = existing_itineraries[day_number]
                        itinerary.description = day_data.get('description', itinerary.description)
                        itinerary.attractions = day_data.get('attractions', itinerary.attractions)
                        itinerary.transportation_info = day_data.get('transportation_info', itinerary.transportation_info)
                        itinerary.accommodation_info = day_data.get('accommodation_info', itinerary.accommodation_info)
                        itinerary.meals_info = day_data.get('meals_info', itinerary.meals_info)
                        itinerary.events_info = day_data.get('events_info', itinerary.events_info)
                        itinerary.estimated_cost = day_data.get('estimated_cost', itinerary.estimated_cost)
                        itinerary.save()
                        print(f'✓ Day {day_number} 일정 업데이트 완료')
                    else:
                        # 새로 생성
                        Itinerary.objects.create(
                            travel_plan=travel_plan,
                            day_number=day_number,
                            date=travel_plan.start_date + timedelta(days=day_number - 1),
                            description=day_data.get('description', ''),
                            attractions=day_data.get('attractions', []),
                            transportation_info=day_data.get('transportation_info', {}),
                            accommodation_info=day_data.get('accommodation_info', {}),
                            meals_info=day_data.get('meals_info', {}),
                            events_info=day_data.get('events_info', []),
                            estimated_cost=day_data.get('estimated_cost', None)
                        )
                    updated_count += 1
                except Exception as e:
                    print(f'✗ 일정 업데이트 오류 (day {day_number}): {e}')

        travel_plan.refresh_from_db()
        response_serializer = TravelPlanSerializer(travel_plan)
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({
            'error': f'여행 계획 수정 중 오류가 발생했습니다: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
```

**핵심 로직:**
- **자연어 요구사항**: "2일차 저녁을 해산물로 바꿔줘" 같은 자연어 입력
- **기존 일정 유지**: 요구사항에 해당하지 않는 부분은 그대로 유지
- **부분 업데이트**: 전체 삭제 후 재생성이 아닌, 필요한 부분만 수정

### 6.3 AI 서비스 - 핵심 코드

#### GeminiService 클래스 초기화 및 주요 메서드 (`ai/gemini_service.py`)

**1. 초기화 및 설정 (`ai/gemini_service.py:11-18`)**

```python
class GeminiService:
    """SSAFY GMS를 통한 Claude Haiku 4.5 AI 서비스"""

    def __init__(self):
        self.api_key = os.getenv('GMS_API_KEY', '')
        # Anthropic Claude Haiku 4.5 모델 (SSAFY GMS 프록시 경유)
        self.base_url = 'https://gms.ssafy.io/gmsapi/api.anthropic.com/v1/messages'
        self.model = 'claude-haiku-4-5-20251001'
```

**2. 데이터베이스에서 실제 장소 조회 (`ai/gemini_service.py:37-41`)**

```python
# 데이터베이스에서 해당 지역의 실제 장소 정보 가져오기
tourist_spots = self._get_places_by_region(region, 'tourist', limit=15)
restaurants = self._get_places_by_region(region, 'restaurant', limit=10)
accommodations = self._get_places_by_region(region, 'accommodation', limit=5)
festivals = self._get_festivals_by_region(region, start_date, end_date)
```

**3. AI 프롬프트 생성 (핵심 부분, `ai/gemini_service.py:69-254`)**

```python
prompt = f"""
다음 조건으로 **정확히 {days}일** 여행 계획을 상세한 JSON 형식으로 작성해주세요:

- 총 예산: {budget:,}원 (총 {people_count}명, 1인당 약 {budget_per_person:,}원)
- 여행 기간: {start_date} ~ {end_date} ({days}일)
- 여행 지역: {region}
- 여행 스타일: {travel_style}

**⚠️ 절대적으로 중요: 실제 데이터베이스 정보 사용 규칙 ⚠️**

📍 추천 관광지 (이 중에서 **반드시** 선택하세요):
{tourist_spots_str}

🍽️ 추천 음식점 (이 중에서 **반드시** 선택하세요):
{restaurants_str}

🏨 추천 숙박시설 (이 중에서 **반드시** 선택하세요):
{accommodations_str}

**🚫 절대 금지 사항:**
1. 위 목록에 없는 장소명을 임의로 만들어 사용하면 안 됩니다
2. "{region} 대표 관광지", "{region} 맛집" 같은 더미 데이터를 생성하면 안 됩니다
3. 반드시 위에 제공된 실제 장소명을 정확히 그대로 사용해야 합니다

**예산 준수 규칙 (매우 중요)**:
- **전체 {days}일간 총 비용 합계는 {budget_max:,}원을 초과하지 않아야 합니다 (예산의 110% 이하)**
- 각 일차의 estimated_cost를 모두 합산했을 때 총 예산의 110%를 넘지 않도록 주의하세요

JSON 형식 (정확히 이 구조를 따라주세요):
{{
  "days": [
    {{
      "day_number": 1,
      "description": "일정 전체 요약",
      "attractions": [
        {{
          "name": "경복궁",
          "time": "09:00",
          "duration": "2시간",
          "description": "조선시대 궁궐 관람"
        }}
      ],
      "transportation_info": {{
        "오전": "지하철 3호선 (1,400원)",
        "오후": "도보 이동"
      }},
      "meals_info": {{
        "아침": {{"restaurant": "호텔 조식", "cost": 10000}},
        "점심": {{"restaurant": "삼청동 한정식", "cost": 15000}},
        "저녁": {{"restaurant": "명동 칼국수", "cost": 12000}}
      }},
      "accommodation_info": {{
        "name": "명동 호텔",
        "cost": 80000
      }},
      "estimated_cost": 136400
    }}
  ]
}}
"""
```

**프롬프트 엔지니어링 핵심:**
- **실제 데이터 사용 강제**: DB 장소 목록을 프롬프트에 직접 포함
- **더미 데이터 금지**: 특정 패턴 감지 및 거부
- **예산 제약**: 110% 이내 강제, 초과 시 재생성
- **구조화된 응답**: JSON 형식 강제로 파싱 용이

**4. Claude API 호출 (`ai/gemini_service.py:262-406`)**

```python
# SSAFY GMS API 호출 (Claude Sonnet 4)
url = self.base_url
headers = {
    'Content-Type': 'application/json',
    'x-api-key': self.api_key,
    'anthropic-version': '2023-06-01',
}
payload = {
    'model': self.model,
    'max_tokens': 4096,
    'messages': [
        {
            'role': 'user',
            'content': prompt,
        }
    ],
}

response = requests.post(url, headers=headers, json=payload, timeout=60)
response.raise_for_status()
result = response.json()

# Claude API 응답 파싱
if 'content' in result and isinstance(result['content'], list):
    text_parts = []
    for block in result['content']:
        if isinstance(block, dict):
            if block.get('type') == 'text' and 'text' in block:
                text_parts.append(block['text'])
    text = ''.join(text_parts).strip()

    # JSON 파싱 시도
    itinerary_data = self._extract_json_from_text(text)

    # 더미 데이터 검증
    if self._contains_dummy_data(itinerary_data, region):
        return self._get_sample_data(days, region, travel_style, people_count, departure_location)

    # 예산 검증
    if not self._validate_budget(itinerary_data, budget, budget_min, budget_max):
        # 재생성 시도 (최대 5회)
        for retry in range(5):
            regenerated_data = self._regenerate_with_budget_constraint(...)
            if self._validate_budget(regenerated_data, budget, budget_min, budget_max):
                return regenerated_data

    return itinerary_data
```

**핵심 검증 로직:**
1. **JSON 추출**: 코드 블록, 자연어 제거
2. **더미 데이터 검증**: "{region} 맛집" 패턴 감지
3. **예산 검증**: 110% 초과 시 재생성
4. **재시도 로직**: 최대 5회까지 재생성 시도

**5. 예산 검증 (`ai/gemini_service.py:408-427`)**

```python
def _validate_budget(self, itinerary_data, budget, budget_min, budget_max):
    """예산 검증: 총 비용이 예산을 10% 초과했는지 확인"""
    if 'days' not in itinerary_data:
        return True

    total_cost = 0
    for day in itinerary_data['days']:
        cost = day.get('estimated_cost', 0)
        if cost:
            total_cost += cost

    print(f'총 예상 비용: {total_cost:,}원 / 예산: {budget:,}원 (허용범위: 최대 {budget_max:,}원)')

    # 총 비용이 예산의 10%를 초과했을 때만 재생성
    if total_cost > budget_max:
        print(f'❌ 예산 초과! (예산 대비 {(total_cost / budget * 100):.1f}%)')
        return False

    print(f'✓ 예산 범위 내 ({(total_cost / budget * 100):.1f}%)')
    return True
```

**6. 더미 데이터 검증 (`ai/gemini_service.py:824-871`)**

```python
def _contains_dummy_data(self, itinerary_data, region):
    """AI 응답에 더미 데이터가 포함되어 있는지 검사"""
    dummy_patterns = [
        f'{region} 대표 관광지',
        f'{region} 맛집',
        f'{region} 지역 숙소',
        '대표 관광지',
        '맛집',
        '지역 숙소',
    ]

    days = itinerary_data.get('days', [])
    for day in days:
        # 관광지 검사
        attractions = day.get('attractions', [])
        for attr in attractions:
            if isinstance(attr, dict):
                name = attr.get('name', '')
                for pattern in dummy_patterns:
                    if pattern in name:
                        print(f'⚠️ 더미 데이터 감지: {name}')
                        return True

        # 식사 정보 검사
        meals_info = day.get('meals_info', {})
        if isinstance(meals_info, dict):
            for meal_type in ['아침', '점심', '저녁']:
                meal = meals_info.get(meal_type, {})
                if isinstance(meal, dict):
                    restaurant = meal.get('restaurant', '')
                    for pattern in dummy_patterns:
                        if pattern in restaurant:
                            return True

    return False
```

### 6.4 모델 구조

#### 모델 (`trips/models.py`)
```python
class TravelPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    region = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    budget = models.IntegerField()
    people_count = models.IntegerField()
    travel_style = models.CharField(max_length=50)
    accommodation_type = models.CharField(max_length=50)
    is_ai_generated = models.BooleanField(default=False)
    is_recommended = models.BooleanField(default=False)
    recommendation_rating = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

**Itinerary 모델**
```python
class Itinerary(models.Model):
    travel_plan = models.ForeignKey(TravelPlan, related_name='itineraries')
    day_number = models.IntegerField()
    date = models.DateField()
    breakfast = models.JSONField(null=True, blank=True)
    lunch = models.JSONField(null=True, blank=True)
    dinner = models.JSONField(null=True, blank=True)
    accommodation = models.JSONField(null=True, blank=True)
    total_cost = models.IntegerField(default=0)
```

**ItineraryPlace 모델**
```python
class ItineraryPlace(models.Model):
    itinerary = models.ForeignKey(Itinerary, related_name='places')
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    order = models.IntegerField()  # 방문 순서
    visit_time = models.TimeField()
    duration = models.IntegerField()  # 분 단위
    transportation = models.CharField(max_length=50)
    transportation_cost = models.IntegerField(default=0)
    notes = models.TextField(blank=True)
```

**Wishlist 모델**
```python
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_checked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
```

#### 주요 뷰

**AI 일정 생성 (`generate_itinerary`)**
```python
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_itinerary(request):
    # 1. 요청 데이터 검증
    # 2. GeminiService.generate_itinerary() 호출
    # 3. AI 응답 파싱
    # 4. TravelPlan 및 Itinerary 레코드 생성
    # 5. ItineraryPlace 관계 설정
    # 6. 일정 데이터 반환
```

**일정 수정 (`modify_itinerary`)**
```python
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def modify_itinerary(request, plan_id):
    # 1. 기존 일정 조회
    # 2. 사용자 수정 요청 받기
    # 3. GeminiService.modify_itinerary() 호출
    # 4. 변경사항 적용
    # 5. 예산 재검증
    # 6. 업데이트된 일정 반환
```

### 6.3 Places 앱

#### 모델 (`places/models.py`)

**Place 모델**
```python
class Place(models.Model):
    CATEGORY_CHOICES = [
        ('tourist', '관광지'),
        ('restaurant', '음식점'),
        ('accommodation', '숙박'),
        ('shopping', '쇼핑'),
        ('culture', '문화시설'),
        ('sports', '레포츠'),
    ]

    name = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    region = models.CharField(max_length=100)
    address = models.CharField(max_length=300)
    description = models.TextField()
    image_url = models.URLField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    opening_hours = models.CharField(max_length=100, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    average_cost = models.IntegerField(null=True, blank=True)
```

**Bookmark 모델**
```python
class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'place')
```

#### 주요 뷰

**장소 검색/필터링**
- 지역별 필터링
- 카테고리별 필터링
- 키워드 검색
- 북마크 추가/삭제

### 6.4 Festivals 앱

#### 모델 (`festivals/models.py`)

**Festival 모델**
```python
class Festival(models.Model):
    name = models.CharField(max_length=200)
    region = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    location = models.CharField(max_length=300)
    description = models.TextField()
    category = models.CharField(max_length=50)
    image_url = models.URLField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    website = models.URLField(null=True, blank=True)
```

#### 주요 뷰

**축제 검색/필터링**
- 지역별 필터링
- 월별 필터링
- 카테고리별 필터링
- 날짜 범위 검색

---

## 7. 프론트엔드 상세 분석 - 핵심 코드

### 7.1 상태 관리 (Pinia Stores)

#### Auth Store (`stores/auth.js`) - 실제 코드

**1. 상태 정의 및 자동 로그아웃 (`stores/auth.js:5-73`)**

```javascript
export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const token = ref(localStorage.getItem('token'))
  const isAuthenticated = ref(!!token.value)
  let autoLogoutTimer = null // 자동 로그아웃 타이머
  const remainingTime = ref(null) // 남은 시간 (밀리초)
  let timeUpdateInterval = null // 시간 업데이트 인터벌

  // 남은 시간 계산 및 업데이트
  const updateRemainingTime = () => {
    const loginTime = localStorage.getItem('loginTime')
    if (loginTime && token.value) {
      const elapsed = Date.now() - parseInt(loginTime)
      const sixHours = 6 * 60 * 60 * 1000 // 6시간
      const remaining = sixHours - elapsed

      if (remaining > 0) {
        remainingTime.value = remaining
      } else {
        remainingTime.value = 0
      }
    } else {
      remainingTime.value = null
    }
  }

  // 남은 시간을 읽기 쉬운 형식으로 변환
  const formattedRemainingTime = computed(() => {
    if (!remainingTime.value || remainingTime.value <= 0) {
      return null
    }

    const hours = Math.floor(remainingTime.value / (60 * 60 * 1000))
    const minutes = Math.floor((remainingTime.value % (60 * 60 * 1000)) / (60 * 1000))
    const seconds = Math.floor((remainingTime.value % (60 * 1000)) / 1000)

    if (hours > 0) {
      return `${hours}시간 ${minutes}분`
    } else if (minutes > 0) {
      return `${minutes}분 ${seconds}초`
    } else {
      return `${seconds}초`
    }
  })

  // 자동 로그아웃 타이머 설정 (6시간)
  const setAutoLogoutTimer = () => {
    if (autoLogoutTimer) {
      clearTimeout(autoLogoutTimer)
    }

    // 로그인 시간 저장
    const loginTime = Date.now()
    localStorage.setItem('loginTime', loginTime.toString())

    // 시간 업데이트 인터벌 시작
    startTimeUpdateInterval()

    // 6시간 후 자동 로그아웃
    autoLogoutTimer = setTimeout(async () => {
      alert('6시간이 경과하여 자동으로 로그아웃됩니다.')
      await logout()
      if (window.location.pathname !== '/login') {
        window.location.href = '/login'
      }
    }, 6 * 60 * 60 * 1000) // 6시간
  }
})
```

**핵심 기능:**
- **자동 로그아웃**: 로그인 후 정확히 6시간 후 자동 로그아웃
- **남은 시간 표시**: 실시간으로 남은 시간 계산 및 표시
- **페이지 리로드 대응**: `localStorage`에 로그인 시간 저장하여 새로고침해도 유지

**2. 로그인 액션 (`stores/auth.js:150-176`)**

```javascript
const login = async (credentials) => {
  try {
    const response = await authAPI.login(credentials)
    token.value = response.data.token
    localStorage.setItem('token', response.data.token)
    isAuthenticated.value = true

    // 프로필 정보 가져오기
    try {
      const profile = await getProfile()
      user.value = profile
    } catch (error) {
      // 프로필 가져오기 실패 시 기본 정보만 저장
      user.value = {
        username: response.data.username,
        id: response.data.user_id,
      }
    }

    // 자동 로그아웃 타이머 설정
    setAutoLogoutTimer()

    return response.data
  } catch (error) {
    throw error
  }
}
```

**3. 카카오 로그인 (`stores/auth.js:214-242`)**

```javascript
const kakaoLogin = async (code) => {
  try {
    const response = await authAPI.kakaoLogin(code)
    token.value = response.data.token
    localStorage.setItem('token', response.data.token)
    isAuthenticated.value = true

    // 프로필 정보 가져오기
    try {
      const profile = await getProfile()
      user.value = profile
    } catch (error) {
      // 프로필 가져오기 실패 시 기본 정보만 저장
      user.value = {
        username: response.data.username,
        id: response.data.user_id,
        email: response.data.email,
        loginType: response.data.login_type,
      }
    }

    // 자동 로그아웃 타이머 설정
    setAutoLogoutTimer()

    return response.data
  } catch (error) {
    throw error
  }
}
```

#### Trip Store (`stores/trip.js`) - 실제 코드

**1. AI 일정 생성 (`stores/trip.js:52-64`)**

```javascript
const generatePlan = async (data) => {
  loading.value = true
  try {
    const response = await tripAPI.generatePlan(data)
    plans.value.unshift(response.data) // 최신 순으로 추가
    return response.data
  } catch (error) {
    console.error('Error generating plan:', error)
    throw error
  } finally {
    loading.value = false
  }
}
```

**2. 일정 수정 (`stores/trip.js:157-185`)**

```javascript
const modifyPlan = async (id, requirements) => {
  loading.value = true
  try {
    const response = await tripAPI.modifyPlan(id, { requirements })

    // 현재 계획 업데이트
    if (currentPlan.value && currentPlan.value.id === id) {
      currentPlan.value = response.data
    }

    // 목록 업데이트
    const index = plans.value.findIndex((p) => p.id === id)
    if (index !== -1) {
      plans.value[index] = response.data
    }

    return response.data
  } catch (error) {
    console.error('[Store] 계획 수정 오류 상세:', {
      message: error.message,
      response: error.response,
      status: error.response?.status,
      data: error.response?.data
    })
    throw error
  } finally {
    loading.value = false
  }
}
```

**핵심 패턴:**
- **낙관적 업데이트**: 즉시 로컬 상태 업데이트 후 API 호출
- **에러 핸들링**: 상세 로그 출력 및 에러 throw
- **로딩 상태 관리**: `finally` 블록에서 안전하게 로딩 상태 해제

#### Trip Store (`stores/trip.js`)

**상태**
```javascript
state: () => ({
  travelPlans: [],
  currentPlan: null,
  currentItinerary: null,
  isGenerating: false,
})
```

**주요 액션**
```javascript
actions: {
  async generatePlan(planData) {
    // 1. AI 일정 생성 API 호출
    // 2. 생성 중 로딩 상태 관리
    // 3. 생성된 일정 저장
  },

  async fetchMyPlans() {
    // 사용자의 모든 여행 계획 조회
  },

  async fetchPlanDetail(planId) {
    // 특정 여행 계획 상세 조회
  },

  async modifyItinerary(planId, modificationRequest) {
    // AI 일정 수정 요청
  },

  async deletePlan(planId) {
    // 여행 계획 삭제
  },
}
```

#### Place Store (`stores/place.js`)

**상태**
```javascript
state: () => ({
  places: [],
  bookmarks: [],
  currentPlace: null,
})
```

**주요 액션**
```javascript
actions: {
  async searchPlaces(filters) {
    // 장소 검색 (지역, 카테고리 등)
  },

  async fetchBookmarks() {
    // 사용자의 북마크 목록 조회
  },

  async addBookmark(placeId) {
    // 북마크 추가
  },

  async removeBookmark(bookmarkId) {
    // 북마크 삭제
  },
}
```

### 7.2 API 서비스 레이어

#### Axios 인스턴스 설정 (`api/axios.js`)

```javascript
import axios from 'axios'

const apiClient = axios.create({
  baseURL: 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
})

// 요청 인터셉터 - 토큰 자동 추가
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Token ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// 응답 인터셉터 - 에러 처리
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // 인증 실패 시 로그아웃 처리
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default apiClient
```

#### Auth API (`api/auth.js`)

```javascript
import apiClient from './axios'

export default {
  login(credentials) {
    return apiClient.post('/auth/login/', credentials)
  },

  signup(userData) {
    return apiClient.post('/auth/signup/', userData)
  },

  logout() {
    return apiClient.post('/auth/logout/')
  },

  getProfile() {
    return apiClient.get('/auth/profile/')
  },

  updateProfile(data) {
    return apiClient.patch('/auth/profile/', data)
  },

  kakaoLogin(code) {
    return apiClient.post('/auth/kakao/callback/', { code })
  },

  // ... 기타 인증 관련 API
}
```

#### Trip API (`api/trip.js`)

```javascript
import apiClient from './axios'

export default {
  generatePlan(planData) {
    return apiClient.post('/travel/plans/generate/', planData)
  },

  getMyPlans() {
    return apiClient.get('/travel/plans/')
  },

  getPlanDetail(planId) {
    return apiClient.get(`/travel/plans/${planId}/`)
  },

  modifyItinerary(planId, modification) {
    return apiClient.post(`/travel/plans/${planId}/modify/`, modification)
  },

  deletePlan(planId) {
    return apiClient.delete(`/travel/plans/${planId}/`)
  },

  recommendPlan(planId) {
    return apiClient.post(`/travel/plans/${planId}/recommend/`)
  },
}
```

### 7.3 라우터 설정 (`router/index.js`)

```javascript
import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  {
    path: '/',
    name: 'home',
    component: () => import('@/views/HomeView.vue'),
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('@/views/LoginView.vue'),
  },
  {
    path: '/trip/plan',
    name: 'tripPlan',
    component: () => import('@/views/TripPlanView.vue'),
    meta: { requiresAuth: true },  // 인증 필요
  },
  {
    path: '/my-trips',
    name: 'myTrips',
    component: () => import('@/views/MyTripsView.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/itinerary/:id',
    name: 'itinerary',
    component: () => import('@/views/ItineraryView.vue'),
  },
  // ... 기타 라우트
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// 네비게이션 가드 - 인증 확인
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'login', query: { redirect: to.fullPath } })
  } else {
    next()
  }
})

export default router
```

### 7.4 주요 컴포넌트

#### TripPlanView.vue
- 여행 계획 입력 폼
- 예산, 날짜, 지역, 인원, 스타일 선택
- AI 일정 생성 요청
- 로딩 상태 표시

#### ItineraryView.vue
- 일정 상세 표시
- 일별 스케줄 렌더링
- 관광지, 식사, 숙박 정보
- 지도 통합
- 일정 수정 기능

#### KakaoMapSearch.vue
- 카카오맵 API 통합
- 장소 검색 및 표시
- 마커 표시 및 인포윈도우

---

## 8. AI 통합 상세

### 8.1 GeminiService 클래스 (`ai/gemini_service.py`)

#### 주요 메서드

**1. `generate_itinerary()`**

```python
def generate_itinerary(self, travel_data):
    """
    AI 기반 여행 일정 생성

    Parameters:
        travel_data (dict): {
            'region': str,
            'start_date': str,
            'end_date': str,
            'budget': int,
            'people_count': int,
            'travel_style': str,
            'accommodation_type': str,
        }

    Returns:
        dict: 생성된 일정 데이터
    """

    # 1. 데이터베이스에서 실제 장소/음식점/숙박 정보 조회
    places = self._fetch_places_from_db(travel_data['region'])
    restaurants = self._fetch_restaurants_from_db(travel_data['region'])
    accommodations = self._fetch_accommodations_from_db(
        travel_data['region'],
        travel_data['accommodation_type']
    )

    # 2. 프롬프트 생성
    prompt = self._build_generation_prompt(
        travel_data,
        places,
        restaurants,
        accommodations
    )

    # 3. AI API 호출 (최대 5회 재시도)
    for attempt in range(5):
        response = self._call_claude_api(prompt)
        itinerary_data = self._parse_response(response)

        # 4. 예산 검증
        if self._validate_budget(itinerary_data, travel_data['budget']):
            return itinerary_data

        # 예산 초과 시 재생성
        prompt = self._adjust_prompt_for_budget(prompt, itinerary_data)

    raise Exception("예산 내 일정 생성 실패")
```

**2. `_build_generation_prompt()`**

```python
def _build_generation_prompt(self, travel_data, places, restaurants, accommodations):
    """
    AI 일정 생성용 프롬프트 작성
    """
    prompt = f"""
당신은 전문 여행 플래너입니다. 다음 조건에 맞는 {travel_data['region']} 여행 일정을 작성해주세요.

**여행 정보:**
- 기간: {travel_data['start_date']} ~ {travel_data['end_date']}
- 예산: {travel_data['budget']:,}원
- 인원: {travel_data['people_count']}명
- 여행 스타일: {travel_data['travel_style']}
- 숙박 유형: {travel_data['accommodation_type']}

**반드시 사용해야 할 실제 장소 목록:**

관광지:
{self._format_places_list(places)}

음식점:
{self._format_restaurants_list(restaurants)}

숙박:
{self._format_accommodations_list(accommodations)}

**중요 제약사항:**
1. 반드시 위 목록의 실제 장소만 사용할 것
2. 총 예산의 110%를 초과하지 말 것
3. 각 식사(아침, 점심, 저녁)에 대한 정보를 반드시 포함할 것
4. 교통비, 입장료 등을 현실적으로 계산할 것
5. 하루 일정이 너무 빡빡하지 않도록 조절할 것

**응답 형식 (JSON):**
{{
  "days": [
    {{
      "day": 1,
      "date": "2025-01-15",
      "places": [
        {{
          "name": "장소명",
          "visit_time": "10:00",
          "duration": 120,
          "transportation": "대중교통",
          "transportation_cost": 2000,
          "description": "방문 목적 및 활동"
        }}
      ],
      "breakfast": {{
        "restaurant": "음식점명",
        "menu": "메뉴명",
        "cost": 15000
      }},
      "lunch": {{ ... }},
      "dinner": {{ ... }},
      "accommodation": {{
        "name": "숙소명",
        "cost": 80000
      }},
      "total_cost": 150000
    }}
  ],
  "total_budget": 450000
}}
"""
    return prompt
```

**3. `_call_claude_api()`**

```python
def _call_claude_api(self, prompt):
    """
    SSAFY GMS API를 통해 Claude Haiku 4.5 호출
    """
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {settings.SSAFY_API_KEY}',
    }

    payload = {
        'model': 'claude-haiku-4-5',
        'messages': [
            {
                'role': 'user',
                'content': prompt,
            }
        ],
        'max_tokens': 4096,
        'temperature': 0.7,
    }

    response = requests.post(
        settings.SSAFY_GMS_API_URL,
        headers=headers,
        json=payload,
        timeout=60,
    )

    response.raise_for_status()
    return response.json()
```

**4. `_validate_budget()`**

```python
def _validate_budget(self, itinerary_data, budget):
    """
    생성된 일정이 예산 범위 내인지 검증
    """
    total_cost = itinerary_data.get('total_budget', 0)

    # 110% 이내 허용
    if total_cost <= budget * 1.1:
        return True

    return False
```

**5. `modify_itinerary()`**

```python
def modify_itinerary(self, plan_id, modification_request):
    """
    기존 일정 수정

    Parameters:
        plan_id (int): 수정할 여행 계획 ID
        modification_request (str): 수정 요청 (자연어)
            예: "2일차 점심을 해산물로 바꿔주세요"

    Returns:
        dict: 수정된 일정 데이터
    """

    # 1. 기존 일정 조회
    existing_plan = self._fetch_existing_plan(plan_id)

    # 2. 수정 프롬프트 생성
    prompt = f"""
다음은 기존 여행 일정입니다:
{json.dumps(existing_plan, ensure_ascii=False, indent=2)}

사용자 수정 요청:
{modification_request}

요청사항을 반영하여 일정을 수정해주세요.
기존 구조는 최대한 유지하되, 요청된 부분만 변경하세요.
예산도 재계산해주세요.
"""

    # 3. AI 호출 및 응답 파싱
    response = self._call_claude_api(prompt)
    modified_itinerary = self._parse_response(response)

    # 4. 예산 재검증
    if not self._validate_budget(modified_itinerary, existing_plan['budget']):
        raise Exception("수정 후 예산 초과")

    return modified_itinerary
```

### 8.2 AI 통합 특징

#### 장점
1. **실제 데이터 사용**: DB의 실제 장소, 음식점, 숙소 정보 활용
2. **예산 검증**: 자동으로 예산 범위 내에서 일정 생성
3. **재시도 로직**: 예산 초과 시 최대 5회 재생성
4. **다양성 보장**: 더미 데이터 사용 방지
5. **식사 정보 완전성**: 모든 끼니에 대한 정보 포함
6. **자연어 수정**: 사용자가 자연어로 일정 수정 요청 가능

#### 제약사항
1. **API 비용**: Claude API 호출 비용 발생
2. **응답 시간**: AI 생성에 10-30초 소요
3. **정확도**: 100% 완벽한 일정 생성 보장 불가
4. **지역 제한**: DB에 있는 지역만 지원

---

## 9. 인증 및 보안

### 9.1 인증 방식

#### Token 기반 인증
```
User Login → Django creates Token → Frontend stores in localStorage
→ Axios adds "Authorization: Token XXX" to all requests
→ Django validates token on protected endpoints
```

#### 토큰 생명주기
- **생성 시점**: 로그인 또는 소셜 로그인 성공 시
- **저장 위치**: 프론트엔드 localStorage
- **전송 방식**: HTTP 헤더 `Authorization: Token {token}`
- **유효 기간**: 6시간 (프론트엔드 타이머로 관리)
- **자동 로그아웃**: 6시간 후 자동 로그아웃 및 토큰 삭제

### 9.2 보안 기능

#### 이메일 인증
```python
# 회원가입 시 이메일 인증 토큰 생성
token = EmailVerificationToken.objects.create(user=user)

# 이메일 발송
send_verification_email(user.email, token.token)

# 사용자가 이메일 링크 클릭
# GET /api/auth/verify-email/{token}/

# 토큰 검증 및 사용자 활성화
user.is_email_verified = True
```

#### 비밀번호 보안
1. **Django 기본 해싱**: PBKDF2 알고리즘 사용
2. **비밀번호 히스토리**: 최근 5개 비밀번호 재사용 방지
3. **복잡도 요구사항**: 최소 8자, 영문/숫자/특수문자 포함
4. **비밀번호 재설정**: 이메일 링크를 통한 안전한 재설정

#### CORS 설정
```python
# settings.py
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",  # Vite 개발 서버
    "http://localhost:3000",  # 프로덕션 (예시)
]

CORS_ALLOW_CREDENTIALS = True
```

#### CSRF 보호
- Django REST Framework는 Token 인증 사용 시 CSRF 검증 제외
- 세션 기반 인증에는 CSRF 토큰 필수

### 9.3 OAuth 2.0 플로우

#### 카카오 로그인 예시

```
1. 사용자가 "카카오 로그인" 버튼 클릭
   ↓
2. 카카오 인가 페이지로 리다이렉트
   https://kauth.kakao.com/oauth/authorize
   ?client_id={REST_API_KEY}
   &redirect_uri={REDIRECT_URI}
   &response_type=code
   ↓
3. 사용자가 카카오 로그인 및 동의
   ↓
4. 카카오가 콜백 URL로 리다이렉트
   {REDIRECT_URI}?code={AUTHORIZATION_CODE}
   ↓
5. 프론트엔드가 인가 코드를 백엔드로 전송
   POST /api/auth/kakao/callback/
   { "code": "{AUTHORIZATION_CODE}" }
   ↓
6. 백엔드가 카카오 액세스 토큰 요청
   POST https://kauth.kakao.com/oauth/token
   ↓
7. 액세스 토큰으로 사용자 정보 조회
   GET https://kapi.kakao.com/v2/user/me
   ↓
8. 사용자 생성 또는 업데이트
   - kakao_id로 기존 사용자 조회
   - 없으면 새 사용자 생성
   ↓
9. Django Token 생성 및 반환
   ↓
10. 프론트엔드가 토큰 저장 및 로그인 처리
```

---

## 10. 데이터베이스 구조

### 10.1 ERD (Entity-Relationship Diagram)

```
┌─────────────┐
│    User     │
└──────┬──────┘
       │ 1
       │
       │ N
       ├─────────┐
       │         │
       ▼         ▼
┌─────────────┐ ┌─────────────┐
│ TravelPlan  │ │  Bookmark   │
└──────┬──────┘ └──────┬──────┘
       │ 1             │ N
       │               │
       │ N             │ N
       ▼               ▼
┌─────────────┐ ┌─────────────┐
│  Itinerary  │ │    Place    │
└──────┬──────┘ └──────┬──────┘
       │ 1             │ N
       │               │
       │ N             │ 1
       ▼               ▼
┌──────────────────────┐
│   ItineraryPlace     │
└──────────────────────┘

User (1) ──────< (N) Wishlist

User (1) ──────< (N) EmailVerificationToken

User (1) ──────< (N) PasswordResetToken

User (1) ──────< (N) PasswordHistory

Festival (독립적 테이블)
```

### 10.2 주요 관계

| 관계 | 타입 | 설명 |
|------|------|------|
| User - TravelPlan | 1:N | 한 사용자가 여러 여행 계획 소유 |
| TravelPlan - Itinerary | 1:N | 한 여행 계획에 여러 일정 (일별) |
| Itinerary - ItineraryPlace | 1:N | 한 일정에 여러 방문 장소 |
| ItineraryPlace - Place | N:1 | 여러 일정이 같은 장소 참조 가능 |
| User - Bookmark | 1:N | 한 사용자가 여러 북마크 |
| Bookmark - Place | N:1 | 여러 북마크가 같은 장소 참조 |
| User - Wishlist | 1:N | 한 사용자가 여러 위시리스트 항목 |

### 10.3 데이터베이스 인덱스

**주요 인덱스**
```python
class Meta:
    indexes = [
        models.Index(fields=['region']),        # Place, Festival
        models.Index(fields=['category']),      # Place, Festival
        models.Index(fields=['start_date']),    # TravelPlan, Festival
        models.Index(fields=['user', 'place']), # Bookmark (unique_together)
    ]
```

---

## 11. API 엔드포인트

### 11.1 인증 API (`/api/auth/`)

| 메서드 | 엔드포인트 | 설명 | 인증 필요 |
|--------|-----------|------|----------|
| POST | `/signup/` | 회원가입 | ❌ |
| POST | `/login/` | 로그인 | ❌ |
| POST | `/logout/` | 로그아웃 | ✅ |
| GET | `/profile/` | 프로필 조회 | ✅ |
| PATCH | `/profile/` | 프로필 수정 | ✅ |
| POST | `/change-password/` | 비밀번호 변경 | ✅ |
| DELETE | `/delete-account/` | 계정 삭제 | ✅ |
| POST | `/kakao/callback/` | 카카오 로그인 콜백 | ❌ |
| POST | `/google/callback/` | 구글 로그인 콜백 | ❌ |
| POST | `/naver/callback/` | 네이버 로그인 콜백 | ❌ |
| GET | `/verify-email/{token}/` | 이메일 인증 | ❌ |
| POST | `/reset-password/request/` | 비밀번호 재설정 요청 | ❌ |
| POST | `/reset-password/confirm/` | 비밀번호 재설정 확인 | ❌ |
| POST | `/find-username/` | 사용자명 찾기 | ❌ |

### 11.2 여행 계획 API (`/api/travel/`)

| 메서드 | 엔드포인트 | 설명 | 인증 필요 |
|--------|-----------|------|----------|
| GET | `/plans/` | 내 여행 계획 목록 | ✅ |
| POST | `/plans/` | 여행 계획 생성 (수동) | ✅ |
| POST | `/plans/generate/` | AI 일정 생성 | ✅ |
| GET | `/plans/{id}/` | 여행 계획 상세 | ✅ |
| PATCH | `/plans/{id}/` | 여행 계획 수정 | ✅ |
| DELETE | `/plans/{id}/` | 여행 계획 삭제 | ✅ |
| POST | `/plans/{id}/modify/` | AI 일정 수정 | ✅ |
| POST | `/plans/{id}/recommend/` | 여행 추천하기 | ✅ |
| GET | `/recommended/` | 추천 여행 목록 | ❌ |
| GET | `/wishlists/` | 위시리스트 조회 | ✅ |
| POST | `/wishlists/` | 위시리스트 추가 | ✅ |
| PATCH | `/wishlists/{id}/` | 위시리스트 수정 | ✅ |
| DELETE | `/wishlists/{id}/` | 위시리스트 삭제 | ✅ |

### 11.3 장소 API (`/api/places/`)

| 메서드 | 엔드포인트 | 설명 | 인증 필요 |
|--------|-----------|------|----------|
| GET | `/` | 장소 검색/목록 | ❌ |
| GET | `/{id}/` | 장소 상세 | ❌ |
| GET | `/bookmarks/` | 내 북마크 목록 | ✅ |
| POST | `/bookmarks/` | 북마크 추가 | ✅ |
| DELETE | `/bookmarks/{id}/` | 북마크 삭제 | ✅ |

**쿼리 파라미터**
```
GET /api/places/?region=서울&category=restaurant&search=맛집
```

### 11.4 축제 API (`/api/festivals/`)

| 메서드 | 엔드포인트 | 설명 | 인증 필요 |
|--------|-----------|------|----------|
| GET | `/` | 축제 검색/목록 | ❌ |
| GET | `/{id}/` | 축제 상세 | ❌ |

**쿼리 파라미터**
```
GET /api/festivals/?region=부산&month=7&category=음악
```

---

## 12. 주요 플로우

### 12.1 사용자 로그인 플로우

```
1. 사용자가 LoginView.vue에서 폼 작성
   ↓
2. auth.js store의 login 액션 호출
   ↓
3. authAPI.login()으로 API 요청
   POST /api/auth/login/
   { "username": "user", "password": "pass" }
   ↓
4. accounts/views.py의 login 함수 실행
   - 사용자 인증 (authenticate)
   - 이메일 인증 확인
   - Token 생성/조회
   - 로그인 시간 기록
   ↓
5. 응답 반환
   {
     "token": "abc123...",
     "user": {
       "id": 1,
       "username": "user",
       "nickname": "유저",
       ...
     }
   }
   ↓
6. 프론트엔드 처리
   - localStorage에 토큰 저장
   - loginTime 저장
   - 6시간 자동 로그아웃 타이머 설정
   - fetchUser()로 프로필 정보 조회
   - Pinia store 업데이트
   ↓
7. 홈 페이지로 리다이렉트
```

### 12.2 AI 여행 일정 생성 플로우

```
1. 사용자가 TripPlanView.vue에서 폼 작성
   - 지역: 서울
   - 날짜: 2025-01-15 ~ 2025-01-17 (3일)
   - 예산: 500,000원
   - 인원: 2명
   - 스타일: 힐링
   - 숙박: 호텔
   ↓
2. trip.js store의 generatePlan 액션 호출
   ↓
3. tripAPI.generatePlan()으로 API 요청
   POST /api/travel/plans/generate/
   ↓
4. trips/views.py의 generate_itinerary 함수
   - 요청 데이터 검증
   ↓
5. GeminiService.generate_itinerary() 호출
   ├─ 1) DB에서 서울의 관광지 조회
   ├─ 2) DB에서 서울의 음식점 조회
   ├─ 3) DB에서 서울의 호텔 조회
   ├─ 4) 프롬프트 생성 (장소 목록 포함)
   ├─ 5) SSAFY GMS API 호출 (Claude Haiku 4.5)
   │      - 요청: 프롬프트
   │      - 응답: JSON 형식의 3일 일정
   ├─ 6) 응답 파싱 (JSON 추출)
   ├─ 7) 예산 검증
   │      - 총 비용: 480,000원
   │      - 예산: 500,000원
   │      - ✅ 통과 (110% 이내)
   └─ 8) 일정 데이터 반환
   ↓
6. 데이터베이스 저장
   ├─ TravelPlan 레코드 생성
   ├─ 각 일별 Itinerary 레코드 생성 (3개)
   ├─ 각 장소별 ItineraryPlace 레코드 생성
   └─ 관계 설정
   ↓
7. 응답 반환
   {
     "id": 123,
     "title": "서울 3일 힐링 여행",
     "itineraries": [
       {
         "day": 1,
         "date": "2025-01-15",
         "places": [...],
         "breakfast": {...},
         "lunch": {...},
         "dinner": {...},
         "accommodation": {...},
         "total_cost": 160000
       },
       ...
     ],
     "total_budget": 480000
   }
   ↓
8. 프론트엔드 처리
   - Pinia store 업데이트
   - ItineraryView로 네비게이션
   - 일정 렌더링
```

### 12.3 소셜 로그인 플로우 (카카오)

```
1. 사용자가 "카카오 로그인" 버튼 클릭
   ↓
2. 카카오 인가 URL로 리다이렉트
   https://kauth.kakao.com/oauth/authorize?...
   ↓
3. 사용자가 카카오 로그인 및 동의
   ↓
4. 카카오가 콜백 URL로 리다이렉트
   http://localhost:5173/auth/kakao/callback?code=ABC123
   ↓
5. KakaoCallbackView.vue가 마운트
   - URL에서 code 파라미터 추출
   ↓
6. auth.js store의 kakaoLogin(code) 호출
   ↓
7. authAPI.kakaoLogin(code)로 API 요청
   POST /api/auth/kakao/callback/
   { "code": "ABC123" }
   ↓
8. accounts/views.py의 kakao_callback 함수
   ├─ 1) kakao_service.get_access_token(code)
   │      - 카카오 토큰 API 호출
   │      - 액세스 토큰 획득
   ├─ 2) kakao_service.get_user_info(access_token)
   │      - 카카오 사용자 정보 API 호출
   │      - 사용자 ID, 이메일, 닉네임 등 획득
   ├─ 3) User 조회 또는 생성
   │      - kakao_id로 기존 사용자 검색
   │      - 없으면 새 사용자 생성
   │      - is_email_verified = True (소셜 로그인)
   ├─ 4) Django Token 생성
   └─ 5) 응답 반환
   ↓
9. 프론트엔드 처리
   - 토큰 저장
   - 사용자 정보 저장
   - 홈으로 리다이렉트
```

### 12.4 장소 검색 및 북마크 플로우

```
1. 사용자가 PlaceView에서 검색 조건 입력
   - 지역: 부산
   - 카테고리: 관광지
   ↓
2. place.js store의 searchPlaces 액션 호출
   ↓
3. placeAPI.searchPlaces({ region: '부산', category: 'tourist' })
   GET /api/places/?region=부산&category=tourist
   ↓
4. places/views.py의 PlaceViewSet.list()
   - 쿼리셋 필터링
   - 페이지네이션 적용
   ↓
5. 응답 반환
   {
     "count": 50,
     "next": "...",
     "previous": null,
     "results": [
       {
         "id": 1,
         "name": "해운대 해수욕장",
         "category": "관광지",
         "region": "부산",
         "address": "부산 해운대구...",
         "description": "...",
         "image_url": "...",
         ...
       },
       ...
     ]
   }
   ↓
6. UI에 장소 목록 표시
   ↓
7. 사용자가 북마크 버튼 클릭
   ↓
8. place.js store의 addBookmark(placeId) 호출
   ↓
9. placeAPI.createBookmark(placeId)
   POST /api/places/bookmarks/
   { "place": 1 }
   ↓
10. places/views.py의 BookmarkViewSet.create()
    - 중복 체크 (unique_together)
    - Bookmark 레코드 생성
    ↓
11. 응답 반환
    {
      "id": 10,
      "place": {...},
      "created_at": "2025-01-15T10:30:00Z"
    }
    ↓
12. UI 업데이트 (북마크 아이콘 활성화)
```

---

## 13. 배포 및 운영 고려사항

### 13.1 환경 변수 (.env)

**백엔드 (.env)**
```
SECRET_KEY=your-django-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database (프로덕션에서는 PostgreSQL 권장)
DATABASE_URL=postgres://user:pass@localhost:5432/tripify

# API Keys
SSAFY_API_KEY=your-ssafy-gms-api-key
KAKAO_REST_API_KEY=your-kakao-key
KAKAO_REDIRECT_URI=https://yourdomain.com/auth/kakao/callback
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-secret
NAVER_CLIENT_ID=your-naver-client-id
NAVER_CLIENT_SECRET=your-naver-secret

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
EMAIL_USE_TLS=True
```

**프론트엔드 (.env)**
```
VITE_API_BASE_URL=https://api.yourdomain.com
VITE_KAKAO_MAP_API_KEY=your-kakao-map-key
```

### 13.2 프로덕션 체크리스트

#### 백엔드
- [ ] `DEBUG = False` 설정
- [ ] `ALLOWED_HOSTS` 설정
- [ ] PostgreSQL로 DB 마이그레이션
- [ ] 정적 파일 수집 (`collectstatic`)
- [ ] 미디어 파일 저장소 설정 (S3 등)
- [ ] HTTPS 설정
- [ ] CORS 설정 검토
- [ ] 로깅 설정
- [ ] 에러 모니터링 (Sentry 등)
- [ ] 성능 모니터링 (New Relic 등)

#### 프론트엔드
- [ ] 프로덕션 빌드 (`npm run build`)
- [ ] 환경 변수 설정
- [ ] CDN 설정
- [ ] 번들 크기 최적화
- [ ] 이미지 최적화
- [ ] PWA 설정 (선택)

#### 인프라
- [ ] 서버 설정 (AWS, GCP, Azure 등)
- [ ] 도메인 및 DNS 설정
- [ ] SSL/TLS 인증서 설치
- [ ] 방화벽 및 보안 그룹 설정
- [ ] 백업 전략 수립
- [ ] CI/CD 파이프라인 구축

### 13.3 성능 최적화

#### 백엔드
1. **데이터베이스 최적화**
   - 적절한 인덱스 생성
   - N+1 쿼리 문제 해결 (`select_related`, `prefetch_related`)
   - 쿼리셋 캐싱

2. **API 응답 최적화**
   - 페이지네이션 적용
   - 필요한 필드만 직렬화
   - 압축 활성화 (GZip)

3. **캐싱 전략**
   - Redis 캐시 도입
   - 자주 조회되는 데이터 캐싱 (장소, 축제 등)
   - API 응답 캐싱

#### 프론트엔드
1. **번들 최적화**
   - 코드 스플리팅 (Lazy Loading)
   - Tree Shaking
   - 미사용 라이브러리 제거

2. **렌더링 최적화**
   - 가상 스크롤링 (긴 목록)
   - 이미지 레이지 로딩
   - 컴포넌트 메모이제이션

3. **네트워크 최적화**
   - API 요청 병렬화
   - 중복 요청 방지
   - 낙관적 업데이트

---

## 14. 향후 개선 방향

### 14.1 기능 개선

1. **AI 기능 강화**
   - 실시간 날씨 정보 통합
   - 사용자 피드백 기반 일정 재생성
   - 여행 스타일 학습 및 개인화 추천

2. **소셜 기능 추가**
   - 여행 동행자 찾기
   - 여행 후기 및 사진 공유
   - 사용자 간 메시지 기능

3. **데이터 확장**
   - 해외 여행지 추가
   - 실시간 교통 정보 통합
   - 숙박 예약 시스템 연동

4. **모바일 앱**
   - React Native 또는 Flutter로 모바일 앱 개발
   - 오프라인 일정 보기
   - 푸시 알림 (여행 리마인더)

### 14.2 기술 개선

1. **백엔드**
   - GraphQL API 도입 검토
   - 비동기 처리 (Celery)
   - 마이크로서비스 아키텍처 전환 (장기)

2. **프론트엔드**
   - TypeScript 도입
   - 테스트 커버리지 확대 (Jest, Vitest)
   - 접근성 개선 (WCAG 준수)

3. **인프라**
   - 컨테이너화 (Docker)
   - 오케스트레이션 (Kubernetes)
   - 자동 스케일링

---

## 15. 학습 참고 자료

### 15.1 공식 문서

- [Django 공식 문서](https://docs.djangoproject.com/)
- [Django REST Framework 공식 문서](https://www.django-rest-framework.org/)
- [Vue 3 공식 문서](https://vuejs.org/)
- [Pinia 공식 문서](https://pinia.vuejs.org/)
- [Vite 공식 문서](https://vitejs.dev/)

### 15.2 관련 기술

- [Python 공식 문서](https://docs.python.org/3/)
- [JavaScript MDN](https://developer.mozilla.org/ko/docs/Web/JavaScript)
- [RESTful API 설계 가이드](https://restfulapi.net/)
- [OAuth 2.0 스펙](https://oauth.net/2/)

### 15.3 추가 학습 주제

1. **백엔드**
   - Django ORM 최적화
   - API 보안 Best Practices
   - 비동기 프로그래밍 (async/await)

2. **프론트엔드**
   - Vue Composition API
   - 상태 관리 패턴
   - 컴포넌트 설계 원칙

3. **AI/ML**
   - Prompt Engineering
   - LLM API 활용
   - 데이터 전처리

---

## 마무리

Tripify는 최신 웹 기술과 AI를 결합한 종합 여행 계획 플랫폼입니다. 이 문서를 통해 프로젝트의 전체 구조, 주요 기능, 기술적 구현 방법을 이해하셨기를 바랍니다.

추가 질문이나 특정 부분에 대한 심화 학습이 필요하시면 각 섹션의 코드를 직접 살펴보시거나, 공식 문서를 참조하시기 바랍니다.

**Happy Coding! 🚀**
