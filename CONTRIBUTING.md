# COMMIT_GUIDE.md

# Tripify 프로젝트 커밋 가이드

이 문서는 COMMIT_HISTORY.md에 기록된 모든 커밋을 기능별로 묶어서 실제로 구현하는 방법을 단계별로 안내합니다.

## 브랜치 전략

### 기본 원칙
- **기능별 브랜치 사용**: 각 기능은 별도의 브랜치에서 개발 후 main 브랜치로 병합
- **작성자 구분**: 
  - `khj`: 백엔드 개발자 (Django, API, 모델 등)
  - `cjg`: 프론트엔드 개발자 (Vue.js, 컴포넌트, 페이지 등)
  - `khj, cjg`: 공동 작업

### 브랜치 네이밍 규칙
- `feature/기능명`: 새로운 기능 개발 (예: `feature/user-auth`, `feature/social-login`)
- `fix/버그명`: 버그 수정 (예: `fix/email-verification`)
- `chore/작업명`: 설정, 문서 등 (예: `chore/project-setup`)

### 작업 흐름
1. main 브랜치에서 최신 코드 pull
2. 기능 브랜치 생성: `git checkout -b feature/기능명`
3. 작업 및 커밋 (작성자 정보 포함)
4. main 브랜치로 push 후 Pull Request 생성
5. 코드 리뷰 후 병합

## 프로젝트 초기 설정

### 커밋 1: 프로젝트 초기 구조 및 기본 설정
**작성자: khj, cjg**  
**브랜치: `chore/project-setup`**

```bash
mkdir Tripify
cd Tripify
git init
```

`backend/.gitignore`:
```gitignore
# Created by https://www.toptal.com/developers/gitignore/api/python,pycharm,visualstudiocode,windows,macos,django,vue,vuejs

### Django ###
*.log
*.pot
*.pyc
__pycache__/
local_settings.py
db.sqlite3
db.sqlite3-journal
media

### Django.Python Stack ###
*.py[cod]
*$py.class
*.so
.Python
build/
dist/
*.egg-info/
.eggs/
env/
venv/
ENV/
.venv
.env
.venv
env.bak/
venv.bak/

### PyCharm ###
.idea/**/workspace.xml
.idea/**/tasks.xml
.idea/**/usage.statistics.xml
.idea/**/dictionaries
.idea/**/shelf
.idea/**/dataSources/
.idea/**/dataSources.ids
.idea/**/dataSources.local.xml
.idea/**/sqlDataSources.xml
.idea/**/dynamic.xml
.idea/**/uiDesigner.xml
.idea/**/dbnavigator.xml
.idea/**/gradle.xml
.idea/**/libraries
.idea/**/mongoSettings.xml
*.iws
out/
.idea_modules/
.idea/**/sonarlint/
.idea/**/sonarIssues.xml
.idea/**/markdown-navigator.xml
.idea/**/markdown-navigator-enh.xml
.idea/**/markdown-navigator/
.idea/$CACHE_FILE$
.idea/codestream.xml
.idea/**/azureSettings.xml

### macOS ###
.DS_Store
.AppleDouble
.LSOverride
Icon
._*
.DocumentRevisions-V100
.fseventsd
.Spotlight-V100
.TemporaryItems
.Trashes
.VolumeIcon.icns
.com.apple.timemachine.donotpresent
.AppleDB
.AppleDesktop
Network Trash Folder
Temporary Items
.apdisk
*.icloud

### VisualStudioCode ###
.vscode/*
!.vscode/settings.json
!.vscode/tasks.json
!.vscode/launch.json
!.vscode/extensions.json
!.vscode/*.code-snippets
.history/
*.vsix
.history
.ionide

### Windows ###
Thumbs.db
Thumbs.db:encryptable
ehthumbs.db
ehthumbs_vista.db
*.stackdump
[Dd]esktop.ini
$RECYCLE.BIN/
*.cab
*.msi
*.msix
*.msm
*.msp
*.lnk

### Python ###
.pdm.toml
__pypackages__/
celerybeat-schedule
celerybeat.pid
*.sage.py
.spyderproject
.spyproject
.ropeproject
/site
.mypy_cache/
.dmypy.json
dmypy.json
.pyre/
.pytype/
cython_debug/
poetry.toml
.ruff_cache/
pyrightconfig.json
```

`frontend/.gitignore`:
```gitignore
# Logs
logs
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*
pnpm-debug.log*
lerna-debug.log*

node_modules
.DS_Store
dist
dist-ssr
coverage
*.local

# Environment variables
.env
.env.local
.env.*.local

# Editor directories and files
.vscode/*
!.vscode/extensions.json
.idea
*.suo
*.ntvs*
*.njsproj
*.sln
*.sw?

*.tsbuildinfo

.eslintcache

# Cypress
/cypress/videos/
/cypress/screenshots/

# Vitest
__screenshots__/
```

```bash
git checkout -b chore/project-setup
git add backend/.gitignore frontend/.gitignore
git commit -m "feat: 프로젝트 초기 구조 및 기본 설정

- Django 백엔드 프로젝트 생성
- Vue.js 프론트엔드 프로젝트 생성
- 기본 디렉토리 구조 설정
- backend/.gitignore 파일 추가
- frontend/.gitignore 파일 추가"
```

### 커밋 2: Django 백엔드 기본 설정
**작성자: khj**  
**브랜치: `chore/backend-setup`**

```bash
cd backend
django-admin startproject config .
pip install django djangorestframework django-cors-headers python-dotenv
```

`backend/config/settings.py` (핵심 부분):
```python
from pathlib import Path
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')

SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-#j*uq27832zq+bs)rt=c6ms3q-8wm9k@n7m8q0wahvom-o=n1$')
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

LANGUAGE_CODE = 'ko-kr'
TIME_ZONE = 'Asia/Seoul'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
```

`backend/requirements.txt`:
```txt
Django==5.2.9
djangorestframework==3.14.0
django-cors-headers==4.3.0
python-dotenv==1.0.0
requests==2.31.0
```

```bash
git checkout -b chore/backend-setup
git add .
git commit -m "feat: Django 백엔드 기본 설정

- Django 5.2.9 프로젝트 초기화
- Django REST Framework 설정
- CORS 설정 추가
- 환경 변수 관리 (python-dotenv)
- 기본 settings.py 구성"
```

### 커밋 3: Vue.js 프론트엔드 기본 설정
**작성자: cjg**  
**브랜치: `chore/frontend-setup`**

```bash
cd ../frontend
npm create vite@latest . -- --template vue
npm install vue-router@4 pinia axios
```

`frontend/src/router/index.js`:
```javascript
import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    }
  ]
})

export default router
```

`frontend/src/stores/index.js`:
```javascript
import { createPinia } from 'pinia'

export default createPinia()
```

`frontend/src/api/axios.js`:
```javascript
import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api',
  timeout: 120000,
  headers: {
    'Content-Type': 'application/json',
  },
})

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('auth_token')
    if (token) {
      config.headers.Authorization = `Token ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

export default api
```

`frontend/src/main.js`:
```javascript
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { createPinia } from 'pinia'

const app = createApp(App)
app.use(router)
app.use(createPinia())
app.mount('#app')
```

`frontend/package.json` (의존성 확인):
```json
{
  "dependencies": {
    "vue": "^3.3.4",
    "vue-router": "^4.2.5",
    "pinia": "^2.1.7",
    "axios": "^1.6.2"
  }
}
```

```bash
git checkout -b chore/frontend-setup
git add .
git commit -m "feat: Vue.js 프론트엔드 기본 설정

- Vue 3 + Vite 프로젝트 초기화
- Vue Router 설정
- Pinia 상태 관리 설정
- Axios 인스턴스 구성
- 기본 스타일링 설정"
```

## 사용자 인증 시스템

### 커밋 4: 커스텀 User 모델 생성
**작성자: khj**  
**브랜치: `feature/user-model`**

```bash
cd ../backend
python manage.py startapp accounts
```

`backend/accounts/models.py`:
```python
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    nickname = models.CharField(max_length=50, blank=True)
    profile_image = models.URLField(blank=True)
    kakao_id = models.CharField(max_length=100, blank=True, null=True)
    google_id = models.CharField(max_length=100, blank=True, null=True)
    naver_id = models.CharField(max_length=100, blank=True, null=True)
    login_type = models.CharField(
        max_length=20,
        choices=[
            ('email', '이메일'),
            ('kakao', '카카오'),
            ('google', '구글'),
            ('naver', '네이버'),
        ],
        default='email'
    )
    is_email_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
```

`backend/config/settings.py`에 추가:
```python
AUTH_USER_MODEL = 'accounts.User'
INSTALLED_APPS = [
    # ... 기존 앱들
    'accounts',
]
```

```bash
git checkout -b feature/user-model
python manage.py makemigrations accounts
python manage.py migrate
git add .
git commit -m "feat: 커스텀 User 모델 구현

- AbstractUser를 상속한 User 모델 생성
- 이메일, 닉네임, 프로필 이미지 필드 추가
- 소셜 로그인 필드 준비 (kakao_id, google_id, naver_id)
- 로그인 타입 필드 추가
- 마이그레이션 파일 생성"
```

### 커밋 5: 사용자 인증 API 구현
**작성자: khj**  
**브랜치: `feature/user-auth-api`**

`backend/accounts/serializers.py`:
```python
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'nickname', 'profile_image', 'login_type', 'is_email_verified']

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'nickname']
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError('아이디 또는 비밀번호가 올바르지 않습니다.')
            if not user.is_active:
                raise serializers.ValidationError('비활성화된 계정입니다.')
            data['user'] = user
        else:
            raise serializers.ValidationError('아이디와 비밀번호를 입력해주세요.')
        return data
```

`backend/accounts/views.py`:
```python
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import SignupSerializer, LoginSerializer, UserSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': UserSerializer(user).data
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        request.user.auth_token.delete()
    except:
        pass
    return Response({'message': '로그아웃되었습니다.'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)
```

`backend/accounts/urls.py`:
```python
from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),
]
```

`backend/config/urls.py`:
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
]
```

```bash
git checkout -b feature/user-auth-api
git add .
git commit -m "feat: 사용자 인증 API 구현

- 회원가입 API (/auth/signup/)
- 로그인 API (/auth/login/)
- 로그아웃 API (/auth/logout/)
- 사용자 프로필 조회 API (/auth/profile/)
- Token 기반 인증 구현"
```

### 커밋 6: 회원가입 및 로그인 페이지 구현
**작성자: cjg**  
**브랜치: `feature/login-signup-pages`**

`frontend/src/api/auth.js`:
```javascript
import api from './axios'

export const authAPI = {
  signup: (data) => api.post('/auth/signup/', data),
  login: (data) => api.post('/auth/login/', data),
  logout: () => api.post('/auth/logout/'),
  getProfile: () => api.get('/auth/profile/'),
}
```

`frontend/src/stores/auth.js`:
```javascript
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { authAPI } from '@/api/auth'
import router from '@/router'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const token = ref(localStorage.getItem('auth_token'))
  const isAuthenticated = ref(!!token.value)

  const login = async (credentials) => {
    try {
      const response = await authAPI.login(credentials)
      token.value = response.data.token
      user.value = response.data.user
      localStorage.setItem('auth_token', token.value)
      isAuthenticated.value = true
      return response.data
    } catch (error) {
      throw error
    }
  }

  const signup = async (userData) => {
    try {
      const response = await authAPI.signup(userData)
      token.value = response.data.token
      user.value = response.data.user
      localStorage.setItem('auth_token', token.value)
      isAuthenticated.value = true
      return response.data
    } catch (error) {
      throw error
    }
  }

  const logout = async () => {
    try {
      await authAPI.logout()
    } catch (error) {
      console.error('Logout error:', error)
    } finally {
      token.value = null
      user.value = null
      isAuthenticated.value = false
      localStorage.removeItem('auth_token')
      router.push('/login')
    }
  }

  const getProfile = async () => {
    try {
      const response = await authAPI.getProfile()
      user.value = response.data
      return response.data
    } catch (error) {
      throw error
    }
  }

  return {
    user,
    token,
    isAuthenticated,
    login,
    signup,
    logout,
    getProfile,
  }
})
```

`frontend/src/views/LoginView.vue` (기본 구조):
```vue
<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const formData = ref({
  username: '',
  password: '',
})
const error = ref('')

const handleLogin = async () => {
  try {
    error.value = ''
    await authStore.login(formData.value)
    router.push('/')
  } catch (err) {
    error.value = err.response?.data?.error || '로그인에 실패했습니다.'
  }
}
</script>

<template>
  <div class="login-container">
    <form @submit.prevent="handleLogin">
      <input v-model="formData.username" placeholder="아이디" required />
      <input v-model="formData.password" type="password" placeholder="비밀번호" required />
      <button type="submit">로그인</button>
      <div v-if="error" class="error">{{ error }}</div>
    </form>
  </div>
</template>
```

`frontend/src/views/SignupView.vue` (기본 구조):
```vue
<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const formData = ref({
  username: '',
  email: '',
  password: '',
  nickname: '',
})
const error = ref('')

const handleSignup = async () => {
  try {
    error.value = ''
    await authStore.signup(formData.value)
    router.push('/')
  } catch (err) {
    error.value = err.response?.data?.error || '회원가입에 실패했습니다.'
  }
}
</script>

<template>
  <div class="signup-container">
    <form @submit.prevent="handleSignup">
      <input v-model="formData.username" placeholder="아이디" required />
      <input v-model="formData.email" type="email" placeholder="이메일" required />
      <input v-model="formData.password" type="password" placeholder="비밀번호" required />
      <input v-model="formData.nickname" placeholder="닉네임" />
      <button type="submit">회원가입</button>
      <div v-if="error" class="error">{{ error }}</div>
    </form>
  </div>
</template>
```

`frontend/src/router/index.js` 업데이트:
```javascript
import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import SignupView from '../views/SignupView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignupView
    }
  ]
})

export default router
```

```bash
git checkout -b feature/login-signup-pages
git add .
git commit -m "feat: 회원가입 및 로그인 페이지 구현

- SignupView 컴포넌트 생성
- LoginView 컴포넌트 생성
- 회원가입 폼 유효성 검사
- 로그인 폼 구현
- 에러 메시지 표시 기능"
```

### 커밋 7: 인증 상태 관리 (Pinia Store)
**작성자: cjg**  
**브랜치: `feature/auth-store`**

`frontend/src/router/index.js`에 가드 추가:
```javascript
import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import SignupView from '../views/SignupView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
      meta: { requiresAuth: false }
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignupView,
      meta: { requiresAuth: false }
    }
  ]
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
  } else if ((to.name === 'login' || to.name === 'signup') && authStore.isAuthenticated) {
    next('/')
  } else {
    next()
  }
})

export default router
```

`frontend/src/stores/auth.js` 업데이트 (자동 로그아웃 타이머):
```javascript
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { authAPI } from '@/api/auth'
import router from '@/router'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const token = ref(localStorage.getItem('auth_token'))
  const isAuthenticated = ref(!!token.value)
  let logoutTimer = null

  const setLogoutTimer = () => {
    if (logoutTimer) {
      clearTimeout(logoutTimer)
    }
    logoutTimer = setTimeout(() => {
      logout()
    }, 24 * 60 * 60 * 1000)
  }

  const login = async (credentials) => {
    try {
      const response = await authAPI.login(credentials)
      token.value = response.data.token
      user.value = response.data.user
      localStorage.setItem('auth_token', token.value)
      isAuthenticated.value = true
      setLogoutTimer()
      return response.data
    } catch (error) {
      throw error
    }
  }

  const logout = async () => {
    try {
      await authAPI.logout()
    } catch (error) {
      console.error('Logout error:', error)
    } finally {
      token.value = null
      user.value = null
      isAuthenticated.value = false
      localStorage.removeItem('auth_token')
      if (logoutTimer) {
        clearTimeout(logoutTimer)
        logoutTimer = null
      }
      router.push('/login')
    }
  }

  if (isAuthenticated.value) {
    setLogoutTimer()
  }

  return {
    user,
    token,
    isAuthenticated,
    login,
    signup,
    logout,
    getProfile,
  }
})
```

```bash
git checkout -b feature/auth-store
git add .
git commit -m "feat: 인증 상태 관리 구현

- auth.js Pinia store 생성
- 로그인/로그아웃 상태 관리
- 토큰 저장 및 관리
- 자동 로그아웃 타이머 구현
- 라우터 가드 설정"
```

## 소셜 로그인

### 커밋 8: 카카오 로그인 백엔드 구현
**작성자: khj**  
**브랜치: `feature/kakao-login-backend`**

`backend/accounts/kakao_service.py`:
```python
import requests
import os
from django.conf import settings

class KakaoOAuthService:
    def __init__(self):
        self.client_id = os.getenv('KAKAO_REST_API_KEY')
        self.redirect_uri = os.getenv('KAKAO_REDIRECT_URI', 'http://localhost:5173/auth/kakao/callback')
    
    def get_access_token(self, code):
        url = 'https://kauth.kakao.com/oauth/token'
        data = {
            'grant_type': 'authorization_code',
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'code': code,
        }
        response = requests.post(url, data=data)
        if response.status_code == 200:
            return response.json().get('access_token')
        return None
    
    def get_user_info(self, access_token):
        url = 'https://kapi.kakao.com/v2/user/me'
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return {
                'kakao_id': str(data['id']),
                'email': data.get('kakao_account', {}).get('email', ''),
                'nickname': data.get('kakao_account', {}).get('profile', {}).get('nickname', ''),
                'profile_image': data.get('kakao_account', {}).get('profile', {}).get('profile_image_url', ''),
            }
        return None
```

`backend/accounts/views.py`에 추가:
```python
from .kakao_service import KakaoOAuthService
from django.contrib.auth import get_user_model

User = get_user_model()

@api_view(['GET'])
@permission_classes([AllowAny])
def kakao_callback(request):
    code = request.GET.get('code')
    if not code:
        return Response({'error': '인증 코드가 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)
    
    service = KakaoOAuthService()
    access_token = service.get_access_token(code)
    if not access_token:
        return Response({'error': '액세스 토큰을 받을 수 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)
    
    user_info = service.get_user_info(access_token)
    if not user_info:
        return Response({'error': '사용자 정보를 가져올 수 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)
    
    kakao_id = user_info['kakao_id']
    user, created = User.objects.get_or_create(
        kakao_id=kakao_id,
        defaults={
            'username': f"kakao_{kakao_id}",
            'email': user_info.get('email', ''),
            'nickname': user_info.get('nickname', ''),
            'profile_image': user_info.get('profile_image', ''),
            'login_type': 'kakao',
        }
    )
    
    token, _ = Token.objects.get_or_create(user=user)
    return Response({
        'token': token.key,
        'user': UserSerializer(user).data
    })
```

`backend/accounts/urls.py`에 추가:
```python
path('kakao/callback/', views.kakao_callback, name='kakao_callback'),
```

```bash
git checkout -b feature/kakao-login-backend
git add .
git commit -m "feat: 카카오 소셜 로그인 백엔드 구현

- KakaoOAuthService 클래스 생성
- 카카오 액세스 토큰 발급 로직
- 카카오 사용자 정보 조회
- 카카오 로그인 API 엔드포인트 (/auth/kakao/callback/)
- User 모델에 kakao_id 필드 추가"
```

### 커밋 9: 카카오 로그인 프론트엔드 구현
**작성자: cjg**  
**브랜치: `feature/kakao-login-frontend`**

`frontend/src/views/LoginView.vue`에 카카오 로그인 버튼 추가:
```vue
<script setup>
// ... 기존 코드
const KAKAO_REST_API_KEY = import.meta.env.VITE_KAKAO_REST_API_KEY || ''
const KAKAO_REDIRECT_URI = import.meta.env.VITE_KAKAO_REDIRECT_URI || 'http://localhost:5173/auth/kakao/callback'

const handleKakaoLogin = () => {
  if (!KAKAO_REST_API_KEY) {
    alert('카카오 API 키가 설정되지 않았습니다.')
    return
  }
  window.location.href = `https://kauth.kakao.com/oauth/authorize?client_id=${KAKAO_REST_API_KEY}&redirect_uri=${KAKAO_REDIRECT_URI}&response_type=code&prompt=select_account`
}
</script>

<template>
  <!-- 기존 폼 -->
  <button @click="handleKakaoLogin">카카오 로그인</button>
</template>
```

`frontend/src/views/KakaoCallbackView.vue`:
```vue
<script setup>
import { onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { authAPI } from '@/api/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

onMounted(async () => {
  const code = route.query.code
  if (!code) {
    router.push('/login')
    return
  }
  
  try {
    const response = await authAPI.kakaoCallback(code)
    authStore.token = response.data.token
    authStore.user = response.data.user
    localStorage.setItem('auth_token', response.data.token)
    router.push('/')
  } catch (error) {
    console.error('카카오 로그인 실패:', error)
    router.push('/login')
  }
})
</script>

<template>
  <div>로그인 처리 중...</div>
</template>
```

`frontend/src/api/auth.js`에 추가:
```javascript
kakaoCallback: (code) => api.get(`/auth/kakao/callback/?code=${code}`),
```

`frontend/src/router/index.js`에 추가:
```javascript
{
  path: '/auth/kakao/callback',
  name: 'kakao-callback',
  component: () => import('../views/KakaoCallbackView.vue')
}
```

```bash
git checkout -b feature/kakao-login-frontend
git add .
git commit -m "feat: 카카오 소셜 로그인 프론트엔드 구현

- 카카오 로그인 버튼 추가
- KakaoCallbackView 컴포넌트 생성
- 카카오 OAuth 인증 플로우 구현
- CSRF 방지를 위한 state 파라미터 처리"
```

### 커밋 10-13: 구글/네이버 로그인

구글과 네이버도 동일한 패턴으로 구현합니다.

**작성자: khj (백엔드), cjg (프론트엔드)**  
**브랜치: `feature/google-login-backend`, `feature/google-login-frontend`, `feature/naver-login-backend`, `feature/naver-login-frontend`**

```bash
# 구글 로그인 백엔드
git checkout -b feature/google-login-backend
git add backend/accounts/google_service.py backend/accounts/views.py backend/accounts/urls.py
git commit -m "feat: 구글 소셜 로그인 백엔드 구현

- GoogleOAuthService 클래스 생성
- 구글 액세스 토큰 발급 로직
- 구글 사용자 정보 조회
- 구글 로그인 API 엔드포인트 (/auth/google/callback/)
- User 모델에 google_id 필드 추가"

# 구글 로그인 프론트엔드
git checkout -b feature/google-login-frontend
git add frontend/src/views/GoogleCallbackView.vue frontend/src/views/LoginView.vue frontend/src/api/auth.js frontend/src/router/index.js
git commit -m "feat: 구글 소셜 로그인 프론트엔드 구현

- 구글 로그인 버튼 추가
- GoogleCallbackView 컴포넌트 생성
- 구글 OAuth 인증 플로우 구현
- 계정 선택 화면 표시 (prompt=select_account)"

# 네이버 로그인 백엔드
git checkout -b feature/naver-login-backend
git add backend/accounts/naver_service.py backend/accounts/views.py backend/accounts/urls.py
git commit -m "feat: 네이버 소셜 로그인 백엔드 구현

- NaverOAuthService 클래스 생성
- 네이버 액세스 토큰 발급 로직
- 네이버 사용자 정보 조회
- 네이버 로그인 API 엔드포인트 (/auth/naver/callback/)
- User 모델에 naver_id 필드 추가
- state 파라미터를 통한 CSRF 방지"

# 네이버 로그인 프론트엔드
git checkout -b feature/naver-login-frontend
git add frontend/src/views/NaverCallbackView.vue frontend/src/views/LoginView.vue frontend/src/api/auth.js frontend/src/router/index.js
git commit -m "feat: 네이버 소셜 로그인 프론트엔드 구현

- 네이버 로그인 버튼 추가
- NaverCallbackView 컴포넌트 생성
- 네이버 OAuth 인증 플로우 구현
- 로그인 화면 강제 표시 (auth_type=login)
- 네이버 아이콘 SVG 추가"
```

## 이메일 인증 및 비밀번호 관리

### 커밋 14: 이메일 인증 시스템 구현
**작성자: khj**  
**브랜치: `feature/email-verification`**

`backend/accounts/models.py`에 추가:
```python
class EmailVerificationToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
```

`backend/accounts/email_utils.py`:
```python
from django.core.mail import send_mail
from django.conf import settings

def send_verification_email(user, token):
    verification_url = f"{settings.FRONTEND_URL}/auth/verify-email/?token={token}"
    subject = 'Tripify 이메일 인증'
    message = f'다음 링크를 클릭하여 이메일을 인증해주세요: {verification_url}'
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
```

`backend/accounts/views.py`에 추가:
```python
from .models import EmailVerificationToken
from .email_utils import send_verification_email
from datetime import timedelta
from django.utils import timezone
import secrets

@api_view(['GET'])
@permission_classes([AllowAny])
def verify_email(request):
    token = request.GET.get('token')
    if not token:
        return Response({'error': '토큰이 필요합니다.'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        verification = EmailVerificationToken.objects.get(token=token, is_used=False)
        if verification.expires_at < timezone.now():
            return Response({'error': '만료된 토큰입니다.'}, status=status.HTTP_400_BAD_REQUEST)
        
        verification.user.is_email_verified = True
        verification.user.save()
        verification.is_used = True
        verification.save()
        
        return Response({'message': '이메일이 인증되었습니다.'})
    except EmailVerificationToken.DoesNotExist:
        return Response({'error': '유효하지 않은 토큰입니다.'}, status=status.HTTP_400_BAD_REQUEST)
```

```bash
git checkout -b feature/email-verification
python manage.py makemigrations
python manage.py migrate
git add .
git commit -m "feat: 이메일 인증 시스템 구현

- EmailVerificationToken 모델 생성
- 이메일 인증 토큰 생성 및 검증 로직
- 이메일 발송 유틸리티 (email_utils.py)
- 이메일 인증 API 엔드포인트
- User 모델에 is_email_verified 필드 추가"
```

### 커밋 15-18: 이메일 인증 페이지 및 비밀번호 관리

**작성자: cjg (프론트엔드), khj (백엔드), khj, cjg (공동)**  
**브랜치: `feature/email-verification-pages`, `feature/password-reset`, `feature/find-username`**

```bash
# 이메일 인증 페이지
git checkout -b feature/email-verification-pages
git add frontend/src/views/VerifyEmailView.vue frontend/src/views/ResendVerificationView.vue
git commit -m "feat: 이메일 인증 페이지 구현

- VerifyEmailView 컴포넌트 생성
- 이메일 인증 토큰 검증 처리
- 인증 성공/실패 메시지 표시
- 인증 재발송 기능 (ResendVerificationView)"

# 비밀번호 재설정 백엔드
git checkout -b feature/password-reset-backend
git add backend/accounts/models.py backend/accounts/views.py backend/accounts/urls.py
git commit -m "feat: 비밀번호 재설정 기능 구현

- PasswordResetToken 모델 생성
- 비밀번호 재설정 요청 API
- 비밀번호 재설정 확인 API
- 이메일로 재설정 링크 발송
- 비밀번호 히스토리 관리 (PasswordHistory 모델)"

# 비밀번호 재설정 페이지
git checkout -b feature/password-reset-frontend
git add frontend/src/views/ResetPasswordRequestView.vue frontend/src/views/ResetPasswordConfirmView.vue
git commit -m "feat: 비밀번호 재설정 페이지 구현

- ResetPasswordRequestView 컴포넌트 생성
- ResetPasswordConfirmView 컴포넌트 생성
- 비밀번호 재설정 폼 구현
- 토큰 검증 및 비밀번호 변경 처리"

# 아이디 찾기
git checkout -b feature/find-username
git add backend/accounts/views.py frontend/src/views/FindUsernameView.vue
git commit -m "feat: 아이디 찾기 기능 구현

- 아이디 찾기 API 엔드포인트
- 이메일로 아이디 발송
- FindUsernameView 컴포넌트 생성"
```

## 장소(Place) 모델 및 API

### 커밋 19: Place 모델 생성
**작성자: khj**  
**브랜치: `feature/place-model`**

```bash
python manage.py startapp places
```

`backend/places/models.py`:
```python
from django.db import models

class Place(models.Model):
    CATEGORY_CHOICES = [
        ('tourist', '관광지'),
        ('restaurant', '맛집'),
        ('accommodation', '숙박'),
    ]
    
    title = models.CharField(max_length=200)
    address = models.CharField(max_length=300)
    latitude = models.DecimalField(max_digits=10, decimal_places=7)
    longitude = models.DecimalField(max_digits=10, decimal_places=7)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    region = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Bookmark(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'place']
```

```bash
git checkout -b feature/place-model
python manage.py makemigrations places
python manage.py migrate
git add .
git commit -m "feat: Place 모델 및 마이그레이션 생성

- Place 모델 정의 (관광지, 맛집, 숙박 등)
- Bookmark 모델 생성
- 카테고리 필드 추가
- 지역, 좌표 정보 필드 추가
- 마이그레이션 파일 생성"
```

### 커밋 20-22: Place API 및 데이터 로딩

**작성자: khj (백엔드), cjg (프론트엔드)**  
**브랜치: `feature/place-api`, `feature/place-data-loading`, `feature/place-search`**

```bash
# Place API
git checkout -b feature/place-api
git add backend/places/views.py backend/places/serializers.py backend/places/urls.py
git commit -m "feat: Place API 엔드포인트 구현

- 장소 목록 조회 API
- 장소 상세 조회 API
- 지역별 필터링 기능
- 타입별 필터링 기능
- 검색 기능 구현"

# 데이터 로딩 명령어
git checkout -b feature/place-data-loading
git add backend/places/management/commands/load_places.py
git commit -m "feat: 관광지 데이터 로딩 명령어 구현

- load_places management command 생성
- tourism_data JSON 파일 파싱
- Place 모델에 데이터 저장
- 중복 데이터 처리 로직"

# 장소 검색 및 북마크 페이지
git checkout -b feature/place-search
git add frontend/src/components/KakaoMapSearch.vue frontend/src/api/place.js frontend/src/stores/place.js
git commit -m "feat: 장소 검색 및 북마크 기능 구현

- KakaoMapSearch 컴포넌트 생성
- 카카오 맵 API 연동
- 장소 검색 기능
- 북마크 저장 기능
- 북마크 목록 표시"
```

## 축제(Festival) 모델 및 API

### 커밋 23-26: Festival 모델 및 API

**작성자: khj (백엔드), cjg (프론트엔드)**  
**브랜치: `feature/festival-model`, `feature/festival-api`, `feature/festival-data-loading`, `feature/festival-pages`**

```bash
python manage.py startapp festivals
```

`backend/festivals/models.py`:
```python
from django.db import models

class Festival(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    event_start_date = models.DateField()
    event_end_date = models.DateField()
    start_month = models.IntegerField()
    end_month = models.IntegerField()
    region = models.CharField(max_length=100)
    address = models.CharField(max_length=300, blank=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

```bash
git checkout -b feature/festival-model
python manage.py makemigrations festivals
python manage.py migrate
git add .
git commit -m "feat: Festival 모델 및 마이그레이션 생성

- Festival 모델 정의
- 축제 날짜 정보 필드 (event_start_date, event_end_date)
- 월별 필터링을 위한 start_month, end_month 필드
- 지역 정보 필드
- 활성화 여부 필드 (is_active)"

# Festival API
git checkout -b feature/festival-api
git add backend/festivals/views.py backend/festivals/serializers.py backend/festivals/urls.py
git commit -m "feat: Festival API 엔드포인트 구현

- 축제 목록 조회 API
- 축제 상세 조회 API
- 월별 필터링 기능
- 지역별 필터링 기능
- 검색 기능 구현"

# 데이터 로딩
git checkout -b feature/festival-data-loading
git add backend/festivals/management/commands/load_festivals.py
git commit -m "feat: 축제 데이터 로딩 명령어 구현

- load_festivals management command 생성
- 축제 JSON 파일 파싱
- Festival 모델에 데이터 저장
- 날짜 파싱 및 월 정보 추출"

# 축제 페이지
git checkout -b feature/festival-pages
git add frontend/src/views/FestivalsView.vue frontend/src/views/FestivalDetailView.vue frontend/src/api/festivals.js
git commit -m "feat: 축제 목록 및 상세 페이지 구현

- FestivalsView 컴포넌트 생성
- FestivalDetailView 컴포넌트 생성
- 월별/지역별 필터링 UI
- 페이지네이션 구현
- 축제 상세 정보 표시
- 목록 페이지 상태 복원 기능 (sessionStorage)"
```

## 여행 계획(TravelPlan) 모델 및 API

### 커밋 27-30: TravelPlan 모델 및 API

**작성자: khj (백엔드), cjg (프론트엔드)**  
**브랜치: `feature/travelplan-model`, `feature/travelplan-api`, `feature/wishlist`**

```bash
python manage.py startapp trips
```

`backend/trips/models.py`:
```python
from django.db import models
from django.conf import settings
from places.models import Place

class TravelPlan(models.Model):
    ACCOMMODATION_CHOICES = [
        ('hotel', '호텔'),
        ('motel', '모텔'),
        ('pension', '펜션'),
        ('guesthouse', '게스트하우스'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='travel_plans')
    title = models.CharField(max_length=255)
    budget = models.IntegerField()
    people_count = models.IntegerField(default=1)
    start_date = models.DateField()
    end_date = models.DateField()
    departure_location = models.CharField(max_length=100, default='서울특별시')
    region = models.CharField(max_length=100)
    travel_style = models.CharField(max_length=100)
    accommodation_type = models.CharField(max_length=20, choices=ACCOMMODATION_CHOICES, default='motel')
    is_generated = models.BooleanField(default=False)
    is_recommended = models.BooleanField(default=False)
    review = models.TextField(blank=True)
    rating = models.IntegerField(null=True, blank=True)
    recommended_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Itinerary(models.Model):
    travel_plan = models.ForeignKey(TravelPlan, on_delete=models.CASCADE, related_name='itineraries')
    day_number = models.IntegerField()
    date = models.DateField()
    description = models.TextField()
    attractions = models.JSONField(default=list, blank=True)
    transportation_info = models.JSONField(default=dict, blank=True)
    accommodation_info = models.JSONField(default=dict, blank=True)
    meals_info = models.JSONField(default=dict, blank=True)
    events_info = models.JSONField(default=list, blank=True)
    estimated_cost = models.IntegerField(default=0)

class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    checked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
```

```bash
git checkout -b feature/travelplan-model
python manage.py makemigrations trips
python manage.py migrate
git add .
git commit -m "feat: TravelPlan 모델 및 마이그레이션 생성

- TravelPlan 모델 정의
- Itinerary 모델 정의 (일차별 계획)
- 예산, 인원, 날짜 정보 필드
- 여행 스타일, 숙박 타입 필드
- 출발지 필드 추가
- 추천 여부 및 평점 필드 추가"

# Itinerary 상세 정보 필드
git add backend/trips/migrations/
git commit -m "feat: Itinerary 모델 상세 정보 필드 추가

- attractions 필드 (관광지 목록)
- transportation_info 필드 (교통수단 정보)
- accommodation_info 필드 (숙소 정보)
- meals_info 필드 (식사 정보)
- events_info 필드 (축제/행사 정보)
- estimated_cost 필드 (예상 비용)"

# TravelPlan API
git checkout -b feature/travelplan-api
git add backend/trips/views.py backend/trips/serializers.py backend/trips/urls.py
git commit -m "feat: TravelPlan API 엔드포인트 구현

- 여행 계획 생성 API
- 여행 계획 목록 조회 API
- 여행 계획 상세 조회 API
- 여행 계획 수정 API
- 여행 계획 삭제 API
- 사용자별 필터링"

# Wishlist
git checkout -b feature/wishlist
git add backend/trips/models.py backend/trips/views.py backend/trips/serializers.py
git commit -m "feat: 위시리스트 기능 구현

- Wishlist 모델 생성
- 위시리스트 항목 추가/삭제 API
- 위시리스트 목록 조회 API
- 완료 상태 토글 기능"
```

## AI 일정 생성 기능

### 커밋 31-37: AI 서비스 구현

**작성자: khj**  
**브랜치: `feature/ai-service`, `feature/ai-itinerary-generation`, `feature/ai-budget-validation`, `feature/ai-modify`, `feature/ai-region-search`, `feature/ai-json-parsing`, `feature/ai-sample-data`**

```bash
mkdir -p backend/ai
```

`backend/ai/gemini_service.py` (핵심 구조):
```python
import os
import json
import requests
from dotenv import load_dotenv
from places.models import Place
from festivals.models import Festival

load_dotenv()

class GeminiService:
    def __init__(self):
        self.api_key = os.getenv('GMS_API_KEY', '')
        self.base_url = 'https://gms.ssafy.io/gmsapi/api.anthropic.com/v1/messages'
        self.model = 'claude-sonnet-4-20250514'

    def generate_itinerary(self, budget, people_count, start_date, end_date, departure_location, region, travel_style, accommodation_type):
        days = (end_date - start_date).days + 1
        budget_per_person = budget // people_count
        daily_budget = budget // days
        
        tourist_spots = self._get_places_by_region(region, 'tourist', limit=15)
        restaurants = self._get_places_by_region(region, 'restaurant', limit=10)
        accommodations = self._get_places_by_region(region, 'accommodation', limit=5)
        festivals = self._get_festivals_by_region(region, start_date, end_date)
        
        prompt = self._build_prompt(days, budget, people_count, start_date, end_date, departure_location, region, travel_style, accommodation_type, tourist_spots, restaurants, accommodations, festivals)
        
        response = self._call_ai_api(prompt)
        itinerary_data = self._parse_response(response)
        
        return itinerary_data
    
    def _get_places_by_region(self, region, category, limit=10):
        candidates = self._generate_region_candidates(region)
        for candidate in candidates:
            places = Place.objects.filter(region__icontains=candidate, category=category)[:limit]
            if places.exists():
                return list(places.values('title', 'address', 'latitude', 'longitude', 'description'))
        return []
    
    def _generate_region_candidates(self, region):
        candidates = [region]
        if '광역시' in region or '특별시' in region:
            candidates.append(region.replace('광역시', '').replace('특별시', '').strip())
        if '시' in region:
            candidates.append(region.replace('시', '').strip())
        return candidates
    
    def _get_festivals_by_region(self, region, start_date, end_date):
        candidates = self._generate_region_candidates(region)
        festivals = Festival.objects.none()
        for candidate in candidates:
            festivals = Festival.objects.filter(
                region__icontains=candidate,
                event_start_date__lte=end_date,
                event_end_date__gte=start_date,
                is_active=True
            )
            if festivals.exists():
                break
        return list(festivals.values('title', 'event_start_date', 'event_end_date', 'address', 'description'))
    
    def _build_prompt(self, days, budget, people_count, start_date, end_date, departure_location, region, travel_style, accommodation_type, tourist_spots, restaurants, accommodations, festivals):
        # 프롬프트 생성 로직 (상세 내용은 실제 구현에 따라)
        return f"""다음 조건으로 {days}일 여행 계획을 생성해주세요..."""
    
    def _call_ai_api(self, prompt):
        headers = {
            'x-api-key': self.api_key,
            'anthropic-version': '2023-06-01',
            'Content-Type': 'application/json'
        }
        payload = {
            'model': self.model,
            'messages': [
                {'role': 'user', 'content': prompt}
            ],
            'max_tokens': 4000
        }
        response = requests.post(self.base_url, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()
        return None
    
    def _parse_response(self, response):
        if not response:
            return None
        content = response.get('content', [])
        if content and len(content) > 0:
            text = content[0].get('text', '')
            return self._extract_json_from_text(text)
        return None
    
    def _extract_json_from_text(self, text):
        text = text.strip()
        try:
            return json.loads(text)
        except:
            if '```json' in text:
                start = text.find('```json') + 7
                end = text.find('```', start)
                return json.loads(text[start:end].strip())
            start = text.find('{')
            end = text.rfind('}') + 1
            if start >= 0 and end > start:
                return json.loads(text[start:end])
        return None
```

```bash
git checkout -b feature/ai-service
git add backend/ai/
git commit -m "feat: AI 일정 생성 서비스 기본 구조 구현

- GeminiService 클래스 생성
- SSAFY GMS API 연동
- Claude 모델 설정
- 기본 프롬프트 구조 설계"

# 나머지 AI 관련 커밋들

## 커밋 1: AI 일정 생성 로직 구현
git checkout -b feature/ai-itinerary-generation
git add backend/ai/gemini_service.py backend/trips/views.py
git commit -m "feat: AI 일정 생성 로직 구현

- generate_itinerary 메서드 구현
- 데이터베이스에서 지역별 장소 조회
- 프롬프트 생성 및 API 호출
- JSON 응답 파싱
- 일정 다양성 검증 로직"

`backend/ai/gemini_service.py`에 추가할 코드:
```python
def generate_itinerary(self, budget, people_count, start_date, end_date, departure_location, region, travel_style, accommodation_type):
    """
    SSAFY GMS API를 사용하여 여행 일정을 생성
    """
    # 여행 일수 계산
    days = (end_date - start_date).days + 1
    
    # 1인당 예산 계산
    budget_per_person = budget // people_count
    
    # 일일 예산 계산
    daily_budget = budget // days
    
    # 데이터베이스에서 해당 지역의 실제 장소 정보 가져오기
    tourist_spots = self._get_places_by_region(region, 'tourist', limit=15)
    restaurants = self._get_places_by_region(region, 'restaurant', limit=10)
    accommodations = self._get_places_by_region(region, 'accommodation', limit=5)
    festivals = self._get_festivals_by_region(region, start_date, end_date)
    
    # 장소 정보를 문자열로 포맷팅
    tourist_spots_str = self._format_places(tourist_spots)
    restaurants_str = self._format_places(restaurants)
    accommodations_str = self._format_places(accommodations)
    festivals_str = self._format_festivals(festivals)
    
    # 프롬프트 생성 (상세한 프롬프트 내용은 실제 파일 참조)
    prompt = f"""
    다음 조건으로 **정확히 {days}일** 여행 계획을 상세한 JSON 형식으로 작성해주세요:
    - 총 예산: {budget:,}원
    - 여행 인원: {people_count}명
    - 여행 기간: {start_date} ~ {end_date} ({days}일)
    - 출발지: {departure_location}
    - 여행 지역: {region}
    - 여행 스타일: {travel_style}
    - 숙박 타입: {accommodation_type}
    
    **{region} 지역의 실제 데이터베이스 정보를 활용하세요:**
    ...
    """
    
    # API 키가 없으면 샘플 데이터 반환
    if not self.api_key:
        return self._get_sample_data(days, region, travel_style, people_count, departure_location)
    
    # SSAFY GMS API 호출
    try:
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
                if isinstance(block, dict) and block.get('type') == 'text' and 'text' in block:
                    text_parts.append(block['text'])
            text = ''.join(text_parts).strip()
            
            if text:
                # JSON 파싱 시도
                try:
                    itinerary_data = self._extract_json_from_text(text)
                    days_count = len(itinerary_data.get("days", []))
                    
                    # 일수 검증
                    if days_count != days:
                        print(f'⚠️ 일수 불일치! 요청: {days}일, 생성: {days_count}일')
                    
                    # 일정 다양성 검증: 모든 일차의 일정이 거의 동일하면 실패로 간주
                    if self._all_days_almost_same(itinerary_data):
                        print('⚠️ 모든 일차의 일정이 거의 동일합니다. 샘플 데이터를 사용합니다.')
                        return self._get_sample_data(days, region, travel_style, people_count, departure_location)
                    
                    return itinerary_data
                except json.JSONDecodeError as e:
                    print(f'✗ JSON 파싱 실패: {e}')
                    return self._get_sample_data(days, region, travel_style, people_count, departure_location)
        
        return self._get_sample_data(days, region, travel_style, people_count, departure_location)
    
    except requests.exceptions.RequestException as e:
        print(f'GMS API 호출 오류: {e}')
        return self._get_sample_data(days, region, travel_style, people_count, departure_location)

# 일정 다양성 검증 메서드 추가
def _all_days_almost_same(self, itinerary_data):
    """
    모든 일차의 내용이 거의 동일한지 검사
    """
    days = itinerary_data.get('days') or []
    if len(days) <= 1:
        return False
    
    normalized = []
    for day in days:
        cmp_day = dict(day)
        cmp_day.pop('day_number', None)
        cmp_day.pop('description', None)
        try:
            normalized.append(json.dumps(cmp_day, sort_keys=True, ensure_ascii=False))
        except TypeError:
            normalized.append(str(cmp_day))
    
    return len(set(normalized)) == 1

# 장소 조회 헬퍼 메서드 추가
def _get_places_by_region(self, region, place_type, limit=10):
    """지역과 타입으로 장소 검색"""
    try:
        candidates = self._build_region_candidates(region)
        for keyword in candidates:
            qs = Place.objects.filter(
                region__icontains=keyword,
                place_type=place_type
            )[:limit]
            places = list(qs)
            if places:
                return places
        return []
    except Exception as e:
        print(f'장소 조회 오류: {e}')
        return []

def _get_festivals_by_region(self, region, start_date, end_date):
    """지역과 기간으로 축제 검색"""
    try:
        month = start_date.month
        candidates = self._build_region_candidates(region)
        for keyword in candidates:
            qs = Festival.objects.filter(
                region__icontains=keyword,
                start_month=month,
                is_active=True
            )[:5]
            festivals = list(qs)
            if festivals:
                return festivals
        return []
    except Exception as e:
        print(f'축제 조회 오류: {e}')
        return []

def _format_places(self, places):
    """장소 목록을 프롬프트용 문자열로 포맷"""
    if not places:
        return "해당 지역의 데이터가 없습니다."
    
    formatted = []
    for place in places:
        category = f" ({place.category})" if place.category else ""
        formatted.append(f"- {place.title}{category}: {place.address}")
    
    return "\n".join(formatted)

def _format_festivals(self, festivals):
    """축제 목록을 프롬프트용 문자열로 포맷"""
    if not festivals:
        return "해당 기간에 축제/행사가 없습니다."
    
    formatted = []
    for festival in festivals:
        period = f"{festival.event_start_date} ~ {festival.event_end_date}" if festival.event_start_date else "날짜 미정"
        formatted.append(f"- {festival.title} ({festival.category}): {period} @ {festival.address}")
    
    return "\n".join(formatted)
```

## 커밋 2: 예산 검증 및 재생성 로직
git checkout -b feature/ai-budget-validation
git add backend/ai/gemini_service.py
git commit -m "feat: AI 일정 생성 예산 검증 및 재생성 로직

- 예산 검증 로직 구현
- 예산 초과 시 재생성 기능
- 재생성 시 예산 제약 강화
- 최대 재시도 횟수 제한"

`backend/ai/gemini_service.py`의 `generate_itinerary` 메서드에 추가할 코드:
```python
# generate_itinerary 메서드 내부, JSON 파싱 성공 후 추가:

# 예산 검증
budget_min = int(budget * 0.9)  # 참고용
budget_max = int(budget * 1.1)  # 예산의 110% 초과 시 재생성

if not self._validate_budget(itinerary_data, budget, budget_min, budget_max):
    print('⚠️  예산 초과! 재생성을 시도합니다...')
    # 재생성 시도 (최대 5회 반복)
    max_retries = 5
    retry_count = 0
    
    while retry_count < max_retries:
        retry_count += 1
        print(f'재생성 시도 {retry_count}/{max_retries}...')
        
        regenerated_data = self._regenerate_with_budget_constraint(
            budget, people_count, start_date, end_date, departure_location, region,
            travel_style, accommodation_type, days,
            daily_budget, budget_min, budget_max,
            tourist_spots_str, restaurants_str, accommodations_str, festivals_str,
            retry_count=retry_count - 1
        )
        
        # 재생성된 데이터의 예산 검증
        if regenerated_data and self._validate_budget(regenerated_data, budget, budget_min, budget_max):
            print(f'✓ 재생성 성공! ({retry_count}회 시도)')
            return regenerated_data
        else:
            if retry_count < max_retries:
                print(f'⚠️ 재생성 {retry_count}회차도 예산 초과. 다시 시도합니다...')
            else:
                print(f'⚠️ 최대 재시도 횟수({max_retries}회)에 도달했습니다. 마지막 결과를 반환합니다.')
                return regenerated_data if regenerated_data else itinerary_data
    
    return regenerated_data if 'regenerated_data' in locals() else itinerary_data

return itinerary_data
```

새로운 메서드 추가:
```python
def _validate_budget(self, itinerary_data, budget, budget_min, budget_max):
    """예산 검증: 총 비용이 예산을 10% 초과했는지 확인"""
    if 'days' not in itinerary_data:
        return True  # 데이터가 없으면 검증 통과
    
    total_cost = 0
    for day in itinerary_data['days']:
        cost = day.get('estimated_cost', 0)
        if cost:
            total_cost += cost
    
    print(f'총 예상 비용: {total_cost:,}원 / 예산: {budget:,}원 (허용범위: 최대 {budget_max:,}원)')
    
    # 총 비용이 예산의 10%를 초과했을 때만 재생성
    if total_cost > budget_max:
        print(f'❌ 예산 초과! (예산 대비 {(total_cost / budget * 100):.1f}%, 초과 금액: {total_cost - budget:,}원)')
        return False
    
    print(f'✓ 예산 범위 내 ({(total_cost / budget * 100):.1f}%)')
    return True

def _regenerate_with_budget_constraint(self, budget, people_count, start_date, end_date, departure_location,
                                      region, travel_style, accommodation_type, days,
                                      daily_budget, budget_min, budget_max,
                                      tourist_spots_str, restaurants_str, accommodations_str, festivals_str,
                                      retry_count=0):
    """예산 제약을 더 강조하여 재생성 (재시도 횟수 포함)"""
    budget_per_person = budget // people_count
    
    # 예산 제약을 강조한 프롬프트 생성
    prompt = f"""
    ...
    **⚠️ 예산 준수 규칙 (절대적으로 중요) ⚠️**:
    - 총 예산: {budget:,}원 ({people_count}명 전체 기준)
    - 일일 목표 예산: 약 {daily_budget:,}원
    - **전체 {days}일간 총 비용 합계는 절대적으로 {budget_max:,}원을 초과하지 않아야 합니다**
    - **이전 시도에서 예산을 초과했으므로, 이번에는 반드시 더 저렴한 옵션을 선택하세요** (재시도 횟수: {retry_count + 1}회):
      * 게스트하우스나 모텔 등 저렴한 숙소 선택 (호텔 피하기)
      * 대중교통 이용 (택시 최소화, 가능하면 도보)
      * 가성비 좋은 음식점 선택 (고급 레스토랑 피하기)
      * 무료 관광지 우선 포함 (유료 입장료 최소화)
    ...
    """
    
    try:
        # API 호출 및 응답 파싱 (generate_itinerary와 유사)
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
        
        # 응답 파싱
        if 'content' in result and isinstance(result['content'], list):
            text_parts = []
            for block in result['content']:
                if isinstance(block, dict) and block.get('type') == 'text' and 'text' in block:
                    text_parts.append(block['text'])
            text = ''.join(text_parts).strip()
            
            if text:
                itinerary_data = self._extract_json_from_text(text)
                if isinstance(itinerary_data, list):
                    itinerary_data = {'days': itinerary_data}
                
                days_count = len(itinerary_data.get("days", []))
                print(f'✓ 재생성 성공! Days: {days_count}개 (요청: {days}일)')
                
                return itinerary_data
    
    except Exception as e:
        print(f'재생성 실패: {e}')
    
    # 재생성 실패 시 샘플 데이터 반환
    return self._get_sample_data(days, region, travel_style, people_count, departure_location)
```

## 커밋 3: 일정 수정 기능
git checkout -b feature/ai-modify
git add backend/ai/gemini_service.py backend/trips/views.py
git commit -m "feat: AI 일정 수정 기능 구현

- modify_itinerary 메서드 구현
- 기존 계획 유지하면서 부분 수정
- 사용자 요구사항 반영
- 예산 준수 검증"

`backend/ai/gemini_service.py`에 추가할 코드:
```python
def modify_itinerary(self, existing_plan, requirements, budget, people_count, start_date, end_date, departure_location, region, travel_style, accommodation_type):
    """
    기존 여행 계획을 사용자 요구사항에 맞게 수정
    """
    # 여행 일수 계산
    days = (end_date - start_date).days + 1
    
    # 기존 일정을 JSON 형식으로 변환
    existing_days_data = []
    for itinerary in existing_plan.itineraries.all().order_by('day_number'):
        existing_days_data.append({
            'day_number': itinerary.day_number,
            'description': itinerary.description,
            'attractions': itinerary.attractions or [],
            'transportation_info': itinerary.transportation_info or {},
            'accommodation_info': itinerary.accommodation_info or {},
            'meals_info': itinerary.meals_info or {},
            'events_info': itinerary.events_info or [],
            'estimated_cost': itinerary.estimated_cost or 0
        })
    
    existing_json = json.dumps(existing_days_data, ensure_ascii=False, indent=2)
    
    # 데이터베이스에서 해당 지역의 실제 장소 정보 가져오기
    tourist_spots = self._get_places_by_region(region, 'tourist', limit=15)
    restaurants = self._get_places_by_region(region, 'restaurant', limit=10)
    accommodations = self._get_places_by_region(region, 'accommodation', limit=5)
    festivals = self._get_festivals_by_region(region, start_date, end_date)
    
    # 장소 정보를 문자열로 포맷팅
    tourist_spots_str = self._format_places(tourist_spots)
    restaurants_str = self._format_places(restaurants)
    accommodations_str = self._format_places(accommodations)
    festivals_str = self._format_festivals(festivals)
    
    # 일일 예산 계산
    daily_budget = budget // days
    budget_max = int(budget * 1.1)
    
    # 프롬프트 생성
    prompt = f"""
    다음은 기존 여행 계획입니다. **기존 계획을 최대한 유지하면서** 사용자의 요구사항에 맞게 **부분적으로만 수정**해주세요.
    
    **⚠️ 매우 중요: 기존 계획의 구조와 내용을 최대한 유지하세요. 요구사항에 명시되지 않은 부분은 그대로 유지해야 합니다.**
    
    **기존 여행 계획 (JSON 형식):**
    ```json
    {existing_json}
    ```
    
    **사용자 요구사항:**
    {requirements}
    
    **수정 지침 (매우 중요):**
    1. **기존 계획의 구조를 그대로 유지하세요** - day_number, 일정 순서, 전체적인 흐름은 변경하지 마세요
    2. **요구사항에 명시된 부분만 수정하세요** - 예를 들어 "2일차 저녁 식사"만 언급되었다면, 2일차 저녁 식사만 변경하고 나머지는 그대로 유지
    3. **요구사항에 해당하지 않는 일정은 기존 내용을 그대로 반환하세요**
    4. 예산은 {budget:,}원을 초과하지 않도록 주의하세요
    5. **반드시 {days}일치 일정을 모두 반환해야 하며, 각 일정의 day_number는 기존과 동일해야 합니다**
    6. **설명 문장, 해설, 코드블록은 절대 출력하지 말고, 오직 하나의 JSON 객체만 출력하세요.**
    ...
    """
    
    # API 키가 없으면 기존 계획 반환
    if not self.api_key:
        return self._get_existing_itinerary_data(existing_plan)
    
    # SSAFY GMS API 호출
    try:
        # API 호출 코드 (generate_itinerary와 유사)
        ...
        
        # 응답 파싱
        if text:
            itinerary_data = self._extract_json_from_text(text)
            if isinstance(itinerary_data, list):
                itinerary_data = {'days': itinerary_data}
            
            days_count = len(itinerary_data.get("days", []))
            print(f'✓ 수정된 계획 JSON 파싱 성공! Days: {days_count}개 (요청: {days}일)')
            
            # 예산 검증
            self._validate_budget(itinerary_data, budget, int(budget * 0.9), budget_max)
            
            return itinerary_data
    
    except requests.exceptions.RequestException as e:
        print(f'GMS API 호출 오류: {e}')
        return self._get_existing_itinerary_data(existing_plan)

def _get_existing_itinerary_data(self, travel_plan):
    """기존 여행 계획을 JSON 형식으로 변환"""
    days = []
    for itinerary in travel_plan.itineraries.all().order_by('day_number'):
        days.append({
            'day_number': itinerary.day_number,
            'description': itinerary.description,
            'attractions': itinerary.attractions or [],
            'transportation_info': itinerary.transportation_info or {},
            'accommodation_info': itinerary.accommodation_info or {},
            'meals_info': itinerary.meals_info or {},
            'events_info': itinerary.events_info or [],
            'estimated_cost': itinerary.estimated_cost or 0
        })
    return {'days': days}
```

## 커밋 4: 지역 검색 개선
git checkout -b feature/ai-region-search
git add backend/ai/gemini_service.py
git commit -m "feat: 지역 검색 유연성 개선

- _generate_region_candidates 메서드 구현
- 다양한 지역명 변형 지원
- 데이터베이스 조회 성공률 향상
- \"대구광역시\" -> \"대구\" 매칭 지원"

`backend/ai/gemini_service.py`에 추가/수정할 코드:
```python
def _build_region_candidates(self, region: str):
    """
    지역 문자열에서 검색에 사용할 후보 키워드 목록 생성
    예) "부산광역시" -> ["부산광역시", "부산"]
        "서울특별시 강남구" -> ["서울특별시 강남구", "서울특별시", "서울", "강남구", "강남"]
    """
    if not region:
        return []
    
    region = region.strip()
    candidates = set()
    
    # 1차: 전체 문자열
    candidates.add(region)
    
    # 2차: 공백으로 나눈 토큰들
    parts = [p for p in region.split() if p]
    if parts:
        for p in parts:
            candidates.add(p)
    
    # 3차: 행정구역 접미사 제거 버전
    suffixes = ['광역시', '특별시', '시', '군', '구', '도']
    for text in list(candidates):
        for suf in suffixes:
            if text.endswith(suf) and len(text) > len(suf):
                candidates.add(text[: -len(suf)])
    
    # 빈 문자열 제거
    return [c for c in candidates if c]

# _get_places_by_region 메서드 수정
def _get_places_by_region(self, region, place_type, limit=10):
    """지역과 타입으로 장소 검색 (여러 후보 키워드로 순차 검색)"""
    try:
        candidates = self._build_region_candidates(region)  # 변경: _generate_region_candidates -> _build_region_candidates
        print(f'[Place 검색] region="{region}", candidates={candidates}, type={place_type}')
        
        for keyword in candidates:
            qs = Place.objects.filter(
                region__icontains=keyword,
                place_type=place_type
            )[:limit]
            places = list(qs)
            if places:
                print(f'[Place 검색] "{keyword}" 로 {len(places)}개 찾음')
                return places
        
        print(f'[Place 검색] "{region}" 에 대한 장소를 찾지 못했습니다. place_type={place_type}')
        return []
    except Exception as e:
        print(f'장소 조회 오류: {e}')
        return []

# _get_festivals_by_region 메서드 수정
def _get_festivals_by_region(self, region, start_date, end_date):
    """지역과 기간으로 축제 검색 (여러 후보 키워드로 순차 검색)"""
    try:
        month = start_date.month
        candidates = self._build_region_candidates(region)  # 변경: _generate_region_candidates -> _build_region_candidates
        print(f'[Festival 검색] region="{region}", candidates={candidates}, month={month}')
        
        for keyword in candidates:
            qs = Festival.objects.filter(
                region__icontains=keyword,
                start_month=month,
                is_active=True
            )[:5]
            festivals = list(qs)
            if festivals:
                print(f'[Festival 검색] "{keyword}" 로 {len(festivals)}개 찾음')
                return festivals
        
        print(f'[Festival 검색] "{region}" 에 대한 축제를 찾지 못했습니다. month={month}')
        return []
    except Exception as e:
        print(f'축제 조회 오류: {e}')
        return []
```

## 커밋 5: JSON 파싱 개선
git checkout -b feature/ai-json-parsing
git add backend/ai/gemini_service.py
git commit -m "feat: JSON 파싱 안정성 개선

- _extract_json_from_text 메서드 개선
- 트레일링 콤마 제거 로직 추가
- 다양한 JSON 형식 지원
- 에러 처리 강화"

`backend/ai/gemini_service.py`의 `_extract_json_from_text` 메서드 수정:
```python
def _extract_json_from_text(self, text):
    """
    LLM 응답 텍스트에서 JSON 부분만 안전하게 추출하여 dict로 반환
    - ```json ... ``` 코드블록 우선 사용
    - 없으면 첫 '{'부터 마지막 '}'까지를 잘라서 파싱 시도
    """
    original_text = text
    
    # 0) 전체 텍스트를 그대로 JSON으로 해석해보기 (이미 순수 JSON일 수 있음)
    try:
        stripped = text.strip()
        if stripped:
            return json.loads(stripped)
    except Exception:
        # 실패하면 아래 단계들 진행
        pass
    
    # 1) ```json 코드블록 처리
    if '```json' in text:
        try:
            body = text.split('```json', 1)[1].split('```', 1)[0].strip()
            return json.loads(body)
        except Exception:
            text = original_text
    
    # 2) 일반 ``` 코드블록 처리
    if '```' in text:
        try:
            body = text.split('```', 1)[1].split('```', 1)[0].strip()
            return json.loads(body)
        except Exception:
            text = original_text
    
    # 3) 자연어 설명 + JSON 형태: 첫 '{' ~ 마지막 '}' 구간만 추출
    first_brace = text.find('{')
    last_brace = text.rfind('}')
    if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
        candidate = text[first_brace:last_brace + 1].strip()
        try:
            return json.loads(candidate)
        except json.JSONDecodeError as e:
            print('✗ _extract_json_from_text JSONDecodeError:', e)
            print('추출된 candidate 앞 300자:\n', candidate[:300])
            raise
    
    # 어떤 형태로도 JSON을 찾지 못한 경우
    raise json.JSONDecodeError('No valid JSON object found in text', original_text, 0)
```

## 커밋 6: 샘플 데이터 생성 개선
git checkout -b feature/ai-sample-data
git add backend/ai/gemini_service.py
git commit -m "feat: 샘플 데이터 생성 로직 개선

- _get_sample_data 메서드 개선
- 각 일차마다 다른 코스 생성
- 실제 DB 데이터 활용
- 랜덤 셔플링으로 다양성 확보"

`backend/ai/gemini_service.py`의 `_get_sample_data` 메서드 수정:
```python
def _get_sample_data(self, days, region, travel_style, people_count, departure_location='서울특별시'):
    """
    샘플 데이터 반환 (API 키가 없거나 오류 발생 시)
    - 실제 DB의 장소/음식점/숙소/축제 데이터를 사용
    - 각 일차마다 다른 코스로 구성하여 "복붙"처럼 보이지 않도록 함
    """
    try:
        tourist_spots = self._get_places_by_region(region, 'tourist', limit=30)
        restaurants = self._get_places_by_region(region, 'restaurant', limit=30)
        accommodations = self._get_places_by_region(region, 'accommodation', limit=10)
        festivals = self._get_festivals_by_region(region, days and days >= 1 and None or None, None, None)
    except Exception:
        tourist_spots, restaurants, accommodations, festivals = [], [], [], []
    
    # 이름 리스트로 변환
    tourist_list = list(tourist_spots)
    restaurant_list = list(restaurants)
    accommodation_list = list(accommodations)
    
    sample_days = []
    for i in range(days):
        day_number = i + 1
        
        # 첫날에는 출발지 → 지역 이동 포함
        if i == 0:
            transportation_info = {
                '오전': f'{departure_location} → {region} 이동 (KTX 또는 고속버스, 예상 비용: 50,000원)',
                '오후': '대중교통 이용 (예상 비용: 5,000원)',
                '저녁': '도보 또는 택시'
            }
        else:
            transportation_info = {
                '오전': '대중교통 이용 (예상 비용: 5,000원)',
                '오후': '도보 또는 택시',
                '저녁': '대중교통'
            }
        
        # 관광지: 날짜마다 시작 인덱스를 다르게 해서 다른 조합 사용
        day_attractions = []
        if tourist_list:
            for j in range(3):
                idx = (i * 3 + j) % len(tourist_list)  # 각 일차마다 다른 인덱스 시작
                place = tourist_list[idx]
                day_attractions.append({
                    'name': place.title,
                    'time': f'{9 + j * 2}:00',
                    'duration': '2시간',
                    'description': place.address,
                })
        else:
            # DB에 데이터가 없을 때의 최소한의 더미
            for j in range(3):
                day_attractions.append({
                    'name': f'{region} 대표 관광지 {day_number}-{j + 1}',
                    'time': f'{9 + j * 2}:00',
                    'duration': '2시간',
                    'description': f'{region}의 유명한 명소',
                })
        
        # 식사: 각 일차마다 다른 식당을 쓰도록 인덱스 회전
        def _pick_restaurant(offset):
            if restaurant_list:
                place = restaurant_list[(i + offset) % len(restaurant_list)]  # 일차별로 다른 식당
                return {
                    'restaurant': place.title,
                    'cost': 15000,
                }
            return {
                'restaurant': f'{region} 맛집 {day_number}-{offset + 1}',
                'cost': 15000,
            }
        
        meals_info = {
            '아침': {
                'restaurant': '호텔 조식 또는 근처 식당',
                'cost': 10000,
            },
            '점심': _pick_restaurant(0),  # 일차별로 다른 식당
            '저녁': _pick_restaurant(1),  # 일차별로 다른 식당
        }
        
        # 숙소: 여러 개가 있으면 날짜별로 다른 숙소 사용
        if accommodation_list:
            acc = accommodation_list[i % len(accommodation_list)]  # 일차별로 다른 숙소
            accommodation_info = {
                'name': acc.title,
                'cost': 80000,
                'check_in': '15:00',
                'check_out': '11:00',
            }
        else:
            accommodation_info = {
                'name': f'{region} 지역 숙소 {day_number}',
                'cost': 80000,
                'check_in': '15:00',
                'check_out': '11:00',
            }
        
        sample_days.append({
            'day_number': day_number,
            'description': f'{region} {travel_style} 여행 {day_number}일차 - 추천 코스',
            'attractions': day_attractions,
            'transportation_info': transportation_info,
            'accommodation_info': accommodation_info,
            'meals_info': meals_info,
            'events_info': [],
            'estimated_cost': 130000,
        })
    
    return {'days': sample_days}
```
```

## 프론트엔드 페이지 구현

### 커밋 38-43: 주요 페이지 구현

**작성자: cjg**  
**브랜치: `feature/home-page`, `feature/trip-plan-page`, `feature/my-trips-page`, `feature/itinerary-page`, `feature/account-settings`**

```bash
# 홈 페이지
git checkout -b feature/home-page
git add frontend/src/views/HomeView.vue
git commit -m "feat: 홈 페이지 구현

- HomeView 컴포넌트 생성
- 히어로 섹션 구현
- 주요 기능 소개 섹션
- 인기 지역 추천 섹션
- 추천 장소 카드 표시
- 반응형 디자인"

# 여행 계획 생성 페이지
git checkout -b feature/trip-plan-page
git add frontend/src/views/TripPlanView.vue frontend/src/components/trip/
git commit -m "feat: 여행 계획 생성 페이지 구현

- TripPlanView 컴포넌트 생성
- 여행 계획 입력 폼 구현
- 예산 입력 컴포넌트 (BudgetInput)
- 날짜 선택 컴포넌트 (DatePicker)
- 지역 선택 컴포넌트 (RegionSelector)
- 여행 스타일 및 숙박 타입 선택
- 로딩 상태 및 에러 처리"

# 내 여행 목록 페이지
git checkout -b feature/my-trips-page
git add frontend/src/views/MyTripsView.vue frontend/src/api/trip.js frontend/src/stores/trip.js
git commit -m "feat: 내 여행 목록 페이지 구현

- MyTripsView 컴포넌트 생성
- 여행 계획 목록 표시
- 카드 형태의 여행 계획 표시
- 삭제 기능 구현
- 빈 상태 처리"

# 여행 일정 상세 페이지
git checkout -b feature/itinerary-page
git add frontend/src/views/ItineraryView.vue frontend/src/components/itinerary/
git commit -m "feat: 여행 일정 상세 페이지 구현

- ItineraryView 컴포넌트 생성
- 일차별 일정 표시
- 관광지, 식사, 숙소 정보 표시
- 교통수단 정보 표시
- 예상 비용 표시
- 지도 연동 (ItineraryMap)"

# 일정 수정 기능
git add frontend/src/views/ItineraryView.vue
git commit -m "feat: 일정 수정 기능 구현

- 일정 수정 모달/폼 구현
- AI를 통한 일정 수정 요청
- 수정된 일정 반영
- 로딩 상태 표시"

# 계정 설정 페이지
git checkout -b feature/account-settings
git add frontend/src/views/AccountSettingsView.vue
git commit -m "feat: 계정 설정 페이지 구현

- AccountSettingsView 컴포넌트 생성
- 사용자 정보 표시
- 로그인 타입 표시 (일반/카카오/구글/네이버)
- 비밀번호 변경 기능
- 계정 삭제 기능
- 소셜 로그인 안내 메시지"
```

## UI 컴포넌트 및 스타일링

### 커밋 44-53: 컴포넌트 및 스타일링

**작성자: cjg**  
**브랜치: `feature/common-components`, `feature/itinerary-components`, `feature/trip-form-components`, `feature/global-styles`, `feature/home-styling`, `feature/scroll-top`, `feature/date-input`, `feature/transportation-display`, `feature/bookmark-button`, `feature/festival-state-restore`**

```bash
# 공통 컴포넌트
git checkout -b feature/common-components
git add frontend/src/components/common/
git commit -m "feat: 공통 컴포넌트 구현

- Header 컴포넌트 생성
- Footer 컴포넌트 생성
- LoadingSpinner 컴포넌트 생성
- ScrollToTop 컴포넌트 생성"

# 일정 관련 컴포넌트
git checkout -b feature/itinerary-components
git add frontend/src/components/itinerary/
git commit -m "feat: 일정 관련 컴포넌트 구현

- ItineraryCard 컴포넌트 생성
- ItineraryMap 컴포넌트 생성
- MapView 컴포넌트 생성
- PlaceDetail 컴포넌트 생성"

# 여행 계획 폼 컴포넌트
git checkout -b feature/trip-form-components
git add frontend/src/components/trip/
git commit -m "feat: 여행 계획 폼 컴포넌트 구현

- TripForm 컴포넌트 생성
- BudgetInput 컴포넌트 생성
- DatePicker 컴포넌트 생성
- RegionSelector 컴포넌트 생성"

# 전역 스타일
git checkout -b feature/global-styles
git add frontend/src/main.css frontend/src/App.vue
git commit -m "feat: 전역 스타일 설정

- main.css 파일 생성
- CSS 변수 정의 (색상, 폰트 등)
- 기본 리셋 스타일
- 반응형 브레이크포인트 정의"

# 홈 페이지 스타일링
git checkout -b feature/home-styling
git add frontend/src/views/HomeView.vue
git commit -m "feat: 홈 페이지 스타일링

- 글래스모피즘 디자인 적용
- 그라데이션 배경
- 카드 호버 효과
- 애니메이션 효과"

# TOP 버튼
git checkout -b feature/scroll-top
git add frontend/src/components/common/ScrollToTop.vue
git commit -m "feat: TOP 버튼 구현 및 스타일링

- ScrollToTop 컴포넌트 생성
- 스크롤 위치 감지
- 부드러운 스크롤 애니메이션
- Tripify 로고 색상 적용 (#2F80ED, #FF4757)
- 반응형 디자인"

# 날짜 입력 필드 개선
git checkout -b feature/date-input
git add frontend/src/views/TripPlanView.vue
git commit -m "feat: 날짜 입력 필드 개선

- YYYY-MM-DD 플레이스홀더 표시
- 브라우저 기본 텍스트 숨김 처리
- 크로스 브라우저 호환성 개선"

# 교통수단 정보 표시 개선
git checkout -b feature/transportation-display
git add frontend/src/views/ItineraryView.vue
git commit -m "feat: 교통수단 정보 표시 개선

- 객체 형태의 교통수단 정보 파싱
- 경로, 소요시간, 비용 표시
- 가격 알림 섹션 정렬 개선"

# 북마크 버튼 색상 변경
git checkout -b feature/bookmark-button
git add frontend/src/components/KakaoMapSearch.vue
git commit -m "feat: 북마크 버튼 색상 변경

- 보라색 계열로 변경 (#6a11cb)
- 호버 효과 개선"

# 축제 페이지 상태 복원
git checkout -b feature/festival-state-restore
git add frontend/src/views/FestivalsView.vue
git commit -m "feat: 축제 페이지 상태 복원 기능

- sessionStorage를 통한 페이지 상태 저장
- 상세 페이지에서 돌아올 때 이전 페이지로 복원
- 필터 상태 복원 (월, 지역)"
```

## 최종 개선 및 버그 수정

### 커밋 59-62: 최종 개선

**작성자: khj (백엔드), cjg (프론트엔드)**  
**브랜치: `fix/ai-model-optimization`, `fix/timeout-settings`, `fix/naver-login`, `chore/final-cleanup`**

```bash
# AI 모델 변경
git checkout -b fix/ai-model-optimization
git add backend/ai/gemini_service.py
git commit -m "fix: AI 모델 변경 및 최적화

- Claude 모델로 변경 (claude-sonnet-4-20250514)
- 프롬프트 최적화
- JSON 파싱 안정성 개선
- 예산 검증 로직 강화"

# 타임아웃 설정
git checkout -b fix/timeout-settings
git add frontend/src/api/axios.js
git commit -m "fix: 프론트엔드 타임아웃 설정 개선

- AI 일정 생성 API 타임아웃 120초로 증가
- 전역 Axios 타임아웃 설정
- 로딩 상태 개선"

# 네이버 로그인 개선
git checkout -b fix/naver-login
git add frontend/src/views/LoginView.vue
git commit -m "fix: 네이버 로그인 계정 선택 개선

- auth_type=login 파라미터 추가
- 로그인 화면 강제 표시
- 계정 설정 페이지에 네이버 표시 개선"

# 프로젝트 최종 정리
git checkout -b chore/final-cleanup
git add .
git commit -m "chore: 프로젝트 최종 정리

- 사용하지 않는 파일 정리
- 코드 포맷팅
- 주석 정리
- 최종 테스트"
```

## Pull Request 병합 가이드

각 기능 브랜치를 완성한 후 main 브랜치로 병합하는 방법:

### 1. 브랜치 푸시
```bash
# 작업 완료 후 브랜치를 원격 저장소에 푸시
git push origin feature/기능명
```

### 2. Pull Request 생성
- GitHub/GitLab에서 Pull Request 생성
- 제목: `feat: 기능명 구현` (커밋 메시지와 동일)
- 설명: 구현한 기능과 변경사항 요약
- 리뷰어 지정: 다른 팀원 지정

### 3. 코드 리뷰 및 병합
- 리뷰어가 코드 검토 후 승인
- 충돌이 없으면 병합
- 병합 후 브랜치 삭제 (선택사항)

### 4. 로컬 브랜치 정리
```bash
# main 브랜치로 이동
git checkout main
git pull origin main

# 병합된 브랜치 삭제 (선택사항)
git branch -d feature/기능명
```

## 팀원별 작업 예시

### khj (백엔드 개발자) 작업 예시

```bash
# 1. 최신 코드 가져오기
git checkout main
git pull origin main

# 2. 기능 브랜치 생성
git checkout -b feature/user-auth-api

# 3. 백엔드 코드 작성 및 커밋
git add backend/accounts/views.py backend/accounts/serializers.py
git commit -m "feat: 사용자 인증 API 구현

- 회원가입 API (/auth/signup/)
- 로그인 API (/auth/login/)
- 로그아웃 API (/auth/logout/)
- 사용자 프로필 조회 API (/auth/profile/)
- Token 기반 인증 구현"

# 4. 원격 저장소에 푸시
git push origin feature/user-auth-api

# 5. Pull Request 생성 (GitHub/GitLab에서)
```

### cjg (프론트엔드 개발자) 작업 예시

```bash
# 1. 최신 코드 가져오기
git checkout main
git pull origin main

# 2. 기능 브랜치 생성
git checkout -b feature/login-signup-pages

# 3. 프론트엔드 코드 작성 및 커밋
git add frontend/src/views/LoginView.vue frontend/src/views/SignupView.vue
git commit -m "feat: 회원가입 및 로그인 페이지 구현

- SignupView 컴포넌트 생성
- LoginView 컴포넌트 생성
- 회원가입 폼 유효성 검사
- 로그인 폼 구현
- 에러 메시지 표시 기능"

# 4. 원격 저장소에 푸시
git push origin feature/login-signup-pages

# 5. Pull Request 생성 (GitHub/GitLab에서)
```

### 공동 작업 예시 (khj, cjg)

```bash
# 1. 최신 코드 가져오기
git checkout main
git pull origin main

# 2. 공동 작업 브랜치 생성
git checkout -b feature/find-username

# 3. 백엔드 작업 (khj)
git add backend/accounts/views.py
git commit -m "feat: 아이디 찾기 API 구현

- 아이디 찾기 API 엔드포인트
- 이메일로 아이디 발송"

# 4. 프론트엔드 작업 (cjg)
git add frontend/src/views/FindUsernameView.vue
git commit -m "feat: 아이디 찾기 페이지 구현

- FindUsernameView 컴포넌트 생성"

# 5. 원격 저장소에 푸시
git push origin feature/find-username

# 6. Pull Request 생성 (GitHub/GitLab에서)
```

---

## 참고사항

1. **기능별 브랜치 전략**: 각 기능은 별도의 브랜치에서 개발합니다.
   - 백엔드 작업: `khj`가 `feature/기능명-backend` 브랜치에서 작업
   - 프론트엔드 작업: `cjg`가 `feature/기능명-frontend` 브랜치에서 작업
   - 공동 작업: `khj, cjg`가 `feature/기능명` 브랜치에서 함께 작업

2. **작성자 구분**:
   - `khj`: 백엔드 개발자 (Django, API, 모델 등)
   - `cjg`: 프론트엔드 개발자 (Vue.js, 컴포넌트, 페이지 등)
   - `khj, cjg`: 공동 작업

3. **브랜치 네이밍 규칙**:
   - `feature/기능명`: 새로운 기능 개발
   - `fix/버그명`: 버그 수정
   - `chore/작업명`: 설정, 문서 등

4. **작업 흐름**:
   - main 브랜치에서 최신 코드 pull
   - 기능 브랜치 생성: `git checkout -b feature/기능명`
   - 작업 및 커밋 (작성자 정보 포함)
   - main 브랜치로 push 후 Pull Request 생성
   - 코드 리뷰 후 병합

5. 실제 구현 시에는 각 파일의 전체 내용을 작성해야 합니다.

6. 마이그레이션 파일은 Django가 자동 생성하므로 직접 작성하지 않습니다.

7. 환경 변수는 `.env` 파일에 설정해야 합니다.

8. **동시 작업 시 주의사항**:
   - 같은 기능의 백엔드와 프론트엔드를 동시에 개발할 때는 각각 별도의 브랜치에서 작업
   - 백엔드 API가 먼저 완성되면 프론트엔드 개발자가 해당 브랜치를 참고하여 작업
   - 또는 공동 작업 브랜치에서 함께 작업할 수도 있음



# COMMIT_MESSAGE.md

# 커밋 메시지

```
feat: AI 모델 변경 및 더미 데이터 생성 방지 로직 강화

- AI 모델을 Claude Haiku 4.5 (claude-haiku-4-5-20251001)로 변경
- 더미 데이터 검증 함수 추가 (_contains_dummy_data)
  - "{region} 대표 관광지", "{region} 맛집", "{region} 지역 숙소" 패턴 감지
  - 더미 데이터 감지 시 실제 DB 데이터 기반 샘플 데이터로 대체
- 데이터베이스 조회 결과 로깅 추가
  - 조회된 관광지, 음식점, 숙소 개수 및 예시 출력
  - 프롬프트에 전달되는 데이터 길이 확인
- 프롬프트 강화
  - 실제 데이터베이스 정보 사용 규칙 명시
  - 더미 데이터 생성 절대 금지 규칙 추가
  - 번호가 매겨진 목록에서만 선택하도록 지시
- 데이터 포맷팅 개선
  - 장소 목록에 번호 및 상세 정보 추가
  - "총 N개의 실제 장소 데이터" 명시
  - 데이터 없을 때 경고 메시지 강화
- 더미 데이터 감지 시 처리 로직 개선
  - DB에 데이터가 있으면 실제 데이터 기반 샘플 데이터 사용
  - DB에 데이터가 없으면 빈 일정 반환 (더미 데이터 생성 방지)

작성자: khj
```



# COMMIT_HISTORY.md

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



