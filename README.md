# Tripify

Tripify는 스마트한 여행 계획을 도와주는 애플리케이션입니다. 이 프로젝트는 2인 팀으로 진행되었습니다.

## 👥 팀원
- **백엔드 / AI**: 서버 아키텍처, RESTful API, AI 기능, 그리고 데이터베이스 관리를 담당했습니다. (본인 역할)
- **프론트엔드**: 사용자 인터페이스, 클라이언트 상태 관리, 그리고 반응형 웹 디자인을 담당했습니다.

## 🛠 기술 스택

### 백엔드 (Backend)
- **프레임워크**: Django 5 & Django REST Framework
- **언어**: Python 3
- **데이터베이스**: PostgreSQL (psycopg2)

### 프론트엔드 (Frontend)
- **프레임워크**: Vue 3 (Vite)
- **상태 관리**: Pinia
- **라우팅**: Vue Router
- **언어**: JavaScript

## 📁 프로젝트 구조

```text
Tripify/
├── backend/                # Django 백엔드 디렉토리
│   ├── accounts/           # 권한 및 사용자 관리
│   ├── ai/                 # AI 관련 기능 및 로직
│   ├── config/             # Django 프로젝트 핵심 설정
│   ├── festivals/          # 축제 데이터 및 API
│   ├── places/             # 장소 정보 및 API
│   ├── tourism_data/       # 관광 데이터 처리 기능
│   ├── trips/              # 여행 일정 생성 기능
│   ├── utils/              # 공통 유틸리티 및 헬퍼 함수
│   ├── manage.py           # Django 실행 스크립트
│   └── requirements.txt    # Python 패키지 의존성
│
├── frontend/               # Vue 3 프론트엔드 디렉토리
│   ├── public/             # 정적 프론트엔드 에셋 설정
│   ├── src/                # Vue 애플리케이션 소스 코드
│   ├── package.json        # Node.js 패키지 의존성
│   └── vite.config.js      # Vite 설정
│
├── API_OAUTH_SETUP.md      # API 및 OAuth (구글, 카카오, 네이버) 설정 안내서
├── CONTRIBUTING.md         # 커밋 규칙 및 기여 내역 가이드
└── Tripify_프로젝트_학습_문서.md # 프로젝트 진행 간의 학습 문서
```

## 📖 상세 문서

연관된 문서들을 주제별로 정리해 두었습니다. 자세한 내용은 아래 파일을 참고해주세요:
- [API 및 OAuth 설정 가이드](./API_OAUTH_SETUP.md) - 구글, 카카오, 네이버 소셜 로그인 및 이메일 API 설정 방법.
- [커밋 및 기여 가이드](./CONTRIBUTING.md) - 커밋 메시지 규칙 및 전체 진행 내역 기록.
- [프로젝트 학습 문서](./Tripify_프로젝트_학습_문서.md) - 프로젝트를 진행하며 학습한 전반적인 지식 기록.
