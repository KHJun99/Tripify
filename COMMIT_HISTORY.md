# Tripify 프로젝트 커밋 히스토리

## 프로젝트 초기 설정

### 1. 프로젝트 초기 구조 생성
**작성자: khj, cjg**
```
feat: 프로젝트 초기 구조 및 기본 설정

- Django 백엔드 프로젝트 생성
- Vue.js 프론트엔드 프로젝트 생성
- 기본 디렉토리 구조 설정
- .gitignore 파일 추가
```

### 2. 백엔드 기본 설정
**작성자: khj**
```
feat: Django 백엔드 기본 설정

- Django 5.2.9 프로젝트 초기화
- Django REST Framework 설정
- CORS 설정 추가
- 환경 변수 관리 (python-dotenv)
- 기본 settings.py 구성
```

### 3. 프론트엔드 기본 설정
**작성자: cjg**
```
feat: Vue.js 프론트엔드 기본 설정

- Vue 3 + Vite 프로젝트 초기화
- Vue Router 설정
- Pinia 상태 관리 설정
- Axios 인스턴스 구성
- 기본 스타일링 설정
```

## 사용자 인증 시스템

### 4. 커스텀 User 모델 생성
**작성자: khj**
```
feat: 커스텀 User 모델 구현

- AbstractUser를 상속한 User 모델 생성
- 이메일, 닉네임, 프로필 이미지 필드 추가
- 소셜 로그인 필드 준비 (kakao_id, google_id, naver_id)
- 로그인 타입 필드 추가
- 마이그레이션 파일 생성
```

### 5. 사용자 인증 API 구현
**작성자: khj**
```
feat: 사용자 인증 API 구현

- 회원가입 API (/auth/signup/)
- 로그인 API (/auth/login/)
- 로그아웃 API (/auth/logout/)
- 사용자 프로필 조회 API (/auth/profile/)
- Token 기반 인증 구현
```

### 6. 회원가입 및 로그인 페이지 구현
**작성자: cjg**
```
feat: 회원가입 및 로그인 페이지 구현

- SignupView 컴포넌트 생성
- LoginView 컴포넌트 생성
- 회원가입 폼 유효성 검사
- 로그인 폼 구현
- 에러 메시지 표시 기능
```

### 7. 인증 상태 관리 (Pinia Store)
**작성자: cjg**
```
feat: 인증 상태 관리 구현

- auth.js Pinia store 생성
- 로그인/로그아웃 상태 관리
- 토큰 저장 및 관리
- 자동 로그아웃 타이머 구현
- 라우터 가드 설정
```

## 소셜 로그인

### 8. 카카오 로그인 백엔드 구현
**작성자: khj**
```
feat: 카카오 소셜 로그인 백엔드 구현

- KakaoOAuthService 클래스 생성
- 카카오 액세스 토큰 발급 로직
- 카카오 사용자 정보 조회
- 카카오 로그인 API 엔드포인트 (/auth/kakao/callback/)
- User 모델에 kakao_id 필드 추가
```

### 9. 카카오 로그인 프론트엔드 구현
**작성자: cjg**
```
feat: 카카오 소셜 로그인 프론트엔드 구현

- 카카오 로그인 버튼 추가
- KakaoCallbackView 컴포넌트 생성
- 카카오 OAuth 인증 플로우 구현
- CSRF 방지를 위한 state 파라미터 처리
```

### 10. 구글 로그인 백엔드 구현
**작성자: khj**
```
feat: 구글 소셜 로그인 백엔드 구현

- GoogleOAuthService 클래스 생성
- 구글 액세스 토큰 발급 로직
- 구글 사용자 정보 조회
- 구글 로그인 API 엔드포인트 (/auth/google/callback/)
- User 모델에 google_id 필드 추가
```

### 11. 구글 로그인 프론트엔드 구현
**작성자: cjg**
```
feat: 구글 소셜 로그인 프론트엔드 구현

- 구글 로그인 버튼 추가
- GoogleCallbackView 컴포넌트 생성
- 구글 OAuth 인증 플로우 구현
- 계정 선택 화면 표시 (prompt=select_account)
```

### 12. 네이버 로그인 백엔드 구현
**작성자: khj**
```
feat: 네이버 소셜 로그인 백엔드 구현

- NaverOAuthService 클래스 생성
- 네이버 액세스 토큰 발급 로직
- 네이버 사용자 정보 조회
- 네이버 로그인 API 엔드포인트 (/auth/naver/callback/)
- User 모델에 naver_id 필드 추가
- state 파라미터를 통한 CSRF 방지
```

### 13. 네이버 로그인 프론트엔드 구현
**작성자: cjg**
```
feat: 네이버 소셜 로그인 프론트엔드 구현

- 네이버 로그인 버튼 추가
- NaverCallbackView 컴포넌트 생성
- 네이버 OAuth 인증 플로우 구현
- 로그인 화면 강제 표시 (auth_type=login)
- 네이버 아이콘 SVG 추가
```

## 이메일 인증 및 비밀번호 관리

### 14. 이메일 인증 시스템 구현
**작성자: khj**
```
feat: 이메일 인증 시스템 구현

- EmailVerificationToken 모델 생성
- 이메일 인증 토큰 생성 및 검증 로직
- 이메일 발송 유틸리티 (email_utils.py)
- 이메일 인증 API 엔드포인트
- User 모델에 is_email_verified 필드 추가
```

### 15. 이메일 인증 페이지 구현
**작성자: cjg**
```
feat: 이메일 인증 페이지 구현

- VerifyEmailView 컴포넌트 생성
- 이메일 인증 토큰 검증 처리
- 인증 성공/실패 메시지 표시
- 인증 재발송 기능 (ResendVerificationView)
```

### 16. 비밀번호 재설정 기능 구현
**작성자: khj**
```
feat: 비밀번호 재설정 기능 구현

- PasswordResetToken 모델 생성
- 비밀번호 재설정 요청 API
- 비밀번호 재설정 확인 API
- 이메일로 재설정 링크 발송
- 비밀번호 히스토리 관리 (PasswordHistory 모델)
```

### 17. 비밀번호 재설정 페이지 구현
**작성자: cjg**
```
feat: 비밀번호 재설정 페이지 구현

- ResetPasswordRequestView 컴포넌트 생성
- ResetPasswordConfirmView 컴포넌트 생성
- 비밀번호 재설정 폼 구현
- 토큰 검증 및 비밀번호 변경 처리
```

### 18. 아이디 찾기 기능 구현
**작성자: khj, cjg**
```
feat: 아이디 찾기 기능 구현

- 아이디 찾기 API 엔드포인트
- 이메일로 아이디 발송
- FindUsernameView 컴포넌트 생성
```

## 장소(Place) 모델 및 API

### 19. Place 모델 생성
**작성자: khj**
```
feat: Place 모델 및 마이그레이션 생성

- Place 모델 정의 (관광지, 맛집, 숙박 등)
- Bookmark 모델 생성
- 카테고리 필드 추가
- 지역, 좌표 정보 필드 추가
- 마이그레이션 파일 생성
```

### 20. Place API 구현
**작성자: khj**
```
feat: Place API 엔드포인트 구현

- 장소 목록 조회 API
- 장소 상세 조회 API
- 지역별 필터링 기능
- 타입별 필터링 기능
- 검색 기능 구현
```

### 21. Place 데이터 로딩 명령어 구현
**작성자: khj**
```
feat: 관광지 데이터 로딩 명령어 구현

- load_places management command 생성
- tourism_data JSON 파일 파싱
- Place 모델에 데이터 저장
- 중복 데이터 처리 로직
```

### 22. 장소 검색 및 북마크 페이지 구현
**작성자: cjg**
```
feat: 장소 검색 및 북마크 기능 구현

- KakaoMapSearch 컴포넌트 생성
- 카카오 맵 API 연동
- 장소 검색 기능
- 북마크 저장 기능
- 북마크 목록 표시
```

## 축제(Festival) 모델 및 API

### 23. Festival 모델 생성
**작성자: khj**
```
feat: Festival 모델 및 마이그레이션 생성

- Festival 모델 정의
- 축제 날짜 정보 필드 (event_start_date, event_end_date)
- 월별 필터링을 위한 start_month, end_month 필드
- 지역 정보 필드
- 활성화 여부 필드 (is_active)
```

### 24. Festival API 구현
**작성자: khj**
```
feat: Festival API 엔드포인트 구현

- 축제 목록 조회 API
- 축제 상세 조회 API
- 월별 필터링 기능
- 지역별 필터링 기능
- 검색 기능 구현
```

### 25. Festival 데이터 로딩 명령어 구현
**작성자: khj**
```
feat: 축제 데이터 로딩 명령어 구현

- load_festivals management command 생성
- 축제 JSON 파일 파싱
- Festival 모델에 데이터 저장
- 날짜 파싱 및 월 정보 추출
```

### 26. 축제 목록 및 상세 페이지 구현
**작성자: cjg**
```
feat: 축제 목록 및 상세 페이지 구현

- FestivalsView 컴포넌트 생성
- FestivalDetailView 컴포넌트 생성
- 월별/지역별 필터링 UI
- 페이지네이션 구현
- 축제 상세 정보 표시
- 목록 페이지 상태 복원 기능 (sessionStorage)
```

## 여행 계획(TravelPlan) 모델 및 API

### 27. TravelPlan 모델 생성
**작성자: khj**
```
feat: TravelPlan 모델 및 마이그레이션 생성

- TravelPlan 모델 정의
- Itinerary 모델 정의 (일차별 계획)
- 예산, 인원, 날짜 정보 필드
- 여행 스타일, 숙박 타입 필드
- 출발지 필드 추가
- 추천 여부 및 평점 필드 추가
```

### 28. Itinerary 모델 상세 정보 필드 추가
**작성자: khj**
```
feat: Itinerary 모델 상세 정보 필드 추가

- attractions 필드 (관광지 목록)
- transportation_info 필드 (교통수단 정보)
- accommodation_info 필드 (숙소 정보)
- meals_info 필드 (식사 정보)
- events_info 필드 (축제/행사 정보)
- estimated_cost 필드 (예상 비용)
```

### 29. TravelPlan API 구현
**작성자: khj**
```
feat: TravelPlan API 엔드포인트 구현

- 여행 계획 생성 API
- 여행 계획 목록 조회 API
- 여행 계획 상세 조회 API
- 여행 계획 수정 API
- 여행 계획 삭제 API
- 사용자별 필터링
```

### 30. Wishlist 모델 및 API 구현
**작성자: khj**
```
feat: 위시리스트 기능 구현

- Wishlist 모델 생성
- 위시리스트 항목 추가/삭제 API
- 위시리스트 목록 조회 API
- 완료 상태 토글 기능
```

## AI 일정 생성 기능

### 31. AI 서비스 기본 구조 구현
**작성자: khj**
```
feat: AI 일정 생성 서비스 기본 구조 구현

- GeminiService 클래스 생성
- SSAFY GMS API 연동
- Claude 모델 설정
- 기본 프롬프트 구조 설계
```

### 32. AI 일정 생성 로직 구현
**작성자: khj**
```
feat: AI 일정 생성 로직 구현

- generate_itinerary 메서드 구현
- 데이터베이스에서 지역별 장소 조회
- 프롬프트 생성 및 API 호출
- JSON 응답 파싱
- 일정 다양성 검증 로직
```

### 33. AI 일정 생성 예산 검증 및 재생성 로직
**작성자: khj**
```
feat: AI 일정 생성 예산 검증 및 재생성 로직

- 예산 검증 로직 구현
- 예산 초과 시 재생성 기능
- 재생성 시 예산 제약 강화
- 최대 재시도 횟수 제한
```

### 34. AI 일정 수정 기능 구현
**작성자: khj**
```
feat: AI 일정 수정 기능 구현

- modify_itinerary 메서드 구현
- 기존 계획 유지하면서 부분 수정
- 사용자 요구사항 반영
- 예산 준수 검증
```

### 35. 지역 검색 유연성 개선
**작성자: khj**
```
feat: 지역 검색 유연성 개선

- _generate_region_candidates 메서드 구현
- 다양한 지역명 변형 지원
- 데이터베이스 조회 성공률 향상
- "대구광역시" -> "대구" 매칭 지원
```

### 36. JSON 파싱 안정성 개선
**작성자: khj**
```
feat: JSON 파싱 안정성 개선

- _extract_json_from_text 메서드 개선
- 트레일링 콤마 제거 로직 추가
- 다양한 JSON 형식 지원
- 에러 처리 강화
```

### 37. 샘플 데이터 생성 로직 개선
**작성자: khj**
```
feat: 샘플 데이터 생성 로직 개선

- _get_sample_data 메서드 개선
- 각 일차마다 다른 코스 생성
- 실제 DB 데이터 활용
- 랜덤 셔플링으로 다양성 확보
```

## 프론트엔드 페이지 구현

### 38. 홈 페이지 구현
**작성자: cjg**
```
feat: 홈 페이지 구현

- HomeView 컴포넌트 생성
- 히어로 섹션 구현
- 주요 기능 소개 섹션
- 인기 지역 추천 섹션
- 추천 장소 카드 표시
- 반응형 디자인
```

### 39. 여행 계획 생성 페이지 구현
**작성자: cjg**
```
feat: 여행 계획 생성 페이지 구현

- TripPlanView 컴포넌트 생성
- 여행 계획 입력 폼 구현
- 예산 입력 컴포넌트 (BudgetInput)
- 날짜 선택 컴포넌트 (DatePicker)
- 지역 선택 컴포넌트 (RegionSelector)
- 여행 스타일 및 숙박 타입 선택
- 로딩 상태 및 에러 처리
```

### 40. 내 여행 목록 페이지 구현
**작성자: cjg**
```
feat: 내 여행 목록 페이지 구현

- MyTripsView 컴포넌트 생성
- 여행 계획 목록 표시
- 카드 형태의 여행 계획 표시
- 삭제 기능 구현
- 빈 상태 처리
```

### 41. 여행 일정 상세 페이지 구현
**작성자: cjg**
```
feat: 여행 일정 상세 페이지 구현

- ItineraryView 컴포넌트 생성
- 일차별 일정 표시
- 관광지, 식사, 숙소 정보 표시
- 교통수단 정보 표시
- 예상 비용 표시
- 지도 연동 (ItineraryMap)
```

### 42. 일정 수정 기능 구현
**작성자: cjg**
```
feat: 일정 수정 기능 구현

- 일정 수정 모달/폼 구현
- AI를 통한 일정 수정 요청
- 수정된 일정 반영
- 로딩 상태 표시
```

### 43. 계정 설정 페이지 구현
**작성자: cjg**
```
feat: 계정 설정 페이지 구현

- AccountSettingsView 컴포넌트 생성
- 사용자 정보 표시
- 로그인 타입 표시 (일반/카카오/구글/네이버)
- 비밀번호 변경 기능
- 계정 삭제 기능
- 소셜 로그인 안내 메시지
```

## UI 컴포넌트

### 44. 공통 컴포넌트 구현
**작성자: cjg**
```
feat: 공통 컴포넌트 구현

- Header 컴포넌트 생성
- Footer 컴포넌트 생성
- LoadingSpinner 컴포넌트 생성
- ScrollToTop 컴포넌트 생성
```

### 45. 일정 관련 컴포넌트 구현
**작성자: cjg**
```
feat: 일정 관련 컴포넌트 구현

- ItineraryCard 컴포넌트 생성
- ItineraryMap 컴포넌트 생성
- MapView 컴포넌트 생성
- PlaceDetail 컴포넌트 생성
```

### 46. 여행 계획 폼 컴포넌트 구현
**작성자: cjg**
```
feat: 여행 계획 폼 컴포넌트 구현

- TripForm 컴포넌트 생성
- BudgetInput 컴포넌트 생성
- DatePicker 컴포넌트 생성
- RegionSelector 컴포넌트 생성
```

## 스타일링 및 UX 개선

### 47. 전역 스타일 설정
**작성자: cjg**
```
feat: 전역 스타일 설정

- main.css 파일 생성
- CSS 변수 정의 (색상, 폰트 등)
- 기본 리셋 스타일
- 반응형 브레이크포인트 정의
```

### 48. 홈 페이지 스타일링
**작성자: cjg**
```
feat: 홈 페이지 스타일링

- 글래스모피즘 디자인 적용
- 그라데이션 배경
- 카드 호버 효과
- 애니메이션 효과
```

### 49. TOP 버튼 구현 및 스타일링
**작성자: cjg**
```
feat: TOP 버튼 구현 및 스타일링

- ScrollToTop 컴포넌트 생성
- 스크롤 위치 감지
- 부드러운 스크롤 애니메이션
- Tripify 로고 색상 적용 (#2F80ED, #FF4757)
- 반응형 디자인
```

### 50. 날짜 입력 필드 개선
**작성자: cjg**
```
feat: 날짜 입력 필드 개선

- YYYY-MM-DD 플레이스홀더 표시
- 브라우저 기본 텍스트 숨김 처리
- 크로스 브라우저 호환성 개선
```

### 51. 교통수단 정보 표시 개선
**작성자: cjg**
```
feat: 교통수단 정보 표시 개선

- 객체 형태의 교통수단 정보 파싱
- 경로, 소요시간, 비용 표시
- 가격 알림 섹션 정렬 개선
```

### 52. 북마크 버튼 색상 변경
**작성자: cjg**
```
feat: 북마크 버튼 색상 변경

- 보라색 계열로 변경 (#6a11cb)
- 호버 효과 개선
```

### 53. 축제 페이지 상태 복원 기능
**작성자: cjg**
```
feat: 축제 페이지 상태 복원 기능

- sessionStorage를 통한 페이지 상태 저장
- 상세 페이지에서 돌아올 때 이전 페이지로 복원
- 필터 상태 복원 (월, 지역)
```

## API 및 상태 관리

### 54. API 모듈 구현
**작성자: cjg**
```
feat: API 모듈 구현

- auth.js: 인증 관련 API
- trip.js: 여행 계획 관련 API
- festivals.js: 축제 관련 API
- place.js: 장소 관련 API
- axios.js: Axios 인스턴스 설정
- 타임아웃 설정 (120초)
```

### 55. Pinia Store 구현
**작성자: cjg**
```
feat: Pinia Store 구현

- auth.js: 인증 상태 관리
- trip.js: 여행 계획 상태 관리
- festival.js: 축제 상태 관리 (선택적)
```

## 문서화

### 56. 소셜 로그인 설정 가이드 작성
**작성자: khj**
```
docs: 소셜 로그인 설정 가이드 작성

- KAKAO_LOGIN_SETUP.md 작성
- GOOGLE_LOGIN_SETUP.md 작성
- NAVER_LOGIN_SETUP.md 작성
- 환경 변수 설정 방법 안내
```

### 57. 이메일 설정 가이드 작성
**작성자: khj**
```
docs: 이메일 설정 가이드 작성

- EMAIL_SETUP.md 작성
- SMTP 설정 방법 안내
- 이메일 템플릿 예시
```

### 58. README 파일 작성
**작성자: khj, cjg**
```
docs: README 파일 작성

- 프로젝트 소개
- 설치 방법
- 실행 방법
- 주요 기능 설명
```

## 최종 개선 및 버그 수정

### 59. AI 모델 변경 및 최적화
**작성자: khj**
```
fix: AI 모델 변경 및 최적화

- Claude 모델로 변경 (claude-sonnet-4-20250514)
- 프롬프트 최적화
- JSON 파싱 안정성 개선
- 예산 검증 로직 강화
```

### 60. 프론트엔드 타임아웃 설정 개선
**작성자: cjg**
```
fix: 프론트엔드 타임아웃 설정 개선

- AI 일정 생성 API 타임아웃 120초로 증가
- 전역 Axios 타임아웃 설정
- 로딩 상태 개선
```

### 61. 네이버 로그인 계정 선택 개선
**작성자: cjg**
```
fix: 네이버 로그인 계정 선택 개선

- auth_type=login 파라미터 추가
- 로그인 화면 강제 표시
- 계정 설정 페이지에 네이버 표시 개선
```

### 62. 프로젝트 최종 정리
**작성자: khj, cjg**
```
chore: 프로젝트 최종 정리

- 사용하지 않는 파일 정리
- 코드 포맷팅
- 주석 정리
- 최종 테스트
```

---

## 커밋 작성 가이드

각 커밋은 다음 형식을 따릅니다:
- `feat`: 새로운 기능 추가
- `fix`: 버그 수정
- `docs`: 문서 수정
- `style`: 코드 포맷팅, 세미콜론 누락 등
- `refactor`: 코드 리팩토링
- `test`: 테스트 코드 추가
- `chore`: 빌드 업무 수정, 패키지 매니저 설정 등

작성자 표기:
- `khj`: 백엔드 개발자
- `cjg`: 프론트엔드 개발자
- `khj, cjg`: 공동 작업

