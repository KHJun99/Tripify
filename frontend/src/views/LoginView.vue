<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

// --- 상태 변수 ---
const formData = ref({
  username: '',
  password: '',
})
const rememberId = ref(false)
const error = ref('')
const showPassword = ref(false)

// --- 환경 변수 로드 ---
const KAKAO_REST_API_KEY = import.meta.env.VITE_KAKAO_REST_API_KEY || ''
const KAKAO_REDIRECT_URI = import.meta.env.VITE_KAKAO_REDIRECT_URI || 'http://localhost:5173/auth/kakao/callback'
const GOOGLE_CLIENT_ID = import.meta.env.VITE_GOOGLE_CLIENT_ID || ''
const GOOGLE_REDIRECT_URI = import.meta.env.VITE_GOOGLE_REDIRECT_URI || 'http://localhost:5173/auth/google/callback'

// --- 핸들러 함수들 ---
const handleLogin = async () => {
  try {
    error.value = ''
    await authStore.login(formData.value)
    router.push('/')
  } catch (err) {
    console.error(err)
    error.value = err.response?.data?.error || '로그인에 실패했습니다.'
  }
}

const handleKakaoLogin = () => {
  if (!KAKAO_REST_API_KEY) {
    alert('카카오 API 키가 설정되지 않았습니다.')
    return
  }
  window.location.href = `https://kauth.kakao.com/oauth/authorize?client_id=${KAKAO_REST_API_KEY}&redirect_uri=${KAKAO_REDIRECT_URI}&response_type=code`
}

const handleGoogleLogin = () => {
  if (!GOOGLE_CLIENT_ID) {
    alert('구글 Client ID가 설정되지 않았습니다.')
    return
  }
  window.location.href = `https://accounts.google.com/o/oauth2/v2/auth?client_id=${GOOGLE_CLIENT_ID}&redirect_uri=${GOOGLE_REDIRECT_URI}&response_type=code&scope=openid email profile`
}
</script>

<template>
  <div class="page-container">
    <main class="main-content">
      <div class="login-card">
        
        <div class="greeting">
          <h2>반갑습니다! 👋</h2>
          <h1>로그인</h1>
          <p>Tripify와 함께 새로운 여행을 시작해보세요.</p>
        </div>

        <transition name="fade">
          <div v-if="error" class="error-message">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="w-5 h-5">
              <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
            </svg>
            <span>{{ error }}</span>
          </div>
        </transition>

        <form @submit.prevent="handleLogin" class="login-form">
          
          <div class="form-group">
            <label for="username">아이디</label>
            <input 
              id="username"
              v-model="formData.username" 
              type="text" 
              placeholder="아이디를 입력해주세요" 
              required 
            />
          </div>

          <div class="form-group">
            <label for="password">비밀번호</label>
            <div class="password-wrapper">
              <input 
                id="password"
                v-model="formData.password"
                :type="showPassword ? 'text' : 'password'" 
                placeholder="비밀번호를 입력해주세요" 
                required 
              />
              <button type="button" class="eye-icon" @click="showPassword = !showPassword" tabindex="-1">
                <svg v-if="showPassword" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
                <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
                </svg>
              </button>
            </div>
          </div>

          <div class="options">
            <label class="checkbox-container">
              <input type="checkbox" v-model="rememberId">
              <span class="checkmark"></span>
              <span class="label-text">아이디 저장</span>
            </label>
            
            <div class="find-links">
              <router-link to="/auth/find-username" class="link">아이디 찾기</router-link>
              <span class="separator"></span>
              <router-link to="/auth/reset-password" class="link">비밀번호 찾기</router-link>
            </div>
          </div>

          <button type="submit" class="btn-login">
            로그인
          </button>
        </form>

        <div class="divider">
          <span>간편 로그인</span>
        </div>

        <div class="social-login">
          <button type="button" class="social-btn kakao" @click="handleKakaoLogin" title="카카오 로그인">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="22" height="22">
               <path d="M12 3c-5.523 0-10 3.582-10 8 0 2.86 1.863 5.36 4.722 6.837-.32.795-1.024 2.54-1.168 2.914-.102.264.096.412.26.412.1 0 .192-.036.284-.084.424-.22 2.632-1.384 4.756-2.496.716.1 1.452.156 2.146.156 5.523 0 10-3.582 10-8s-4.477-8-10-8"/>
            </svg>
          </button>
          <button type="button" class="social-btn google" @click="handleGoogleLogin" title="구글 로그인">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="22" height="22">
              <path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"/>
              <path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"/>
              <path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"/>
              <path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"/>
            </svg>
          </button>
        </div>

        <div class="signup-area">
          <span>아직 회원이 아니신가요?</span>
          <router-link to="/signup" class="signup-link">회원가입 하러가기</router-link>
        </div>

      </div>
    </main>
  </div>
</template>

<style scoped>
/* 1. 폰트 로드 (Pretendard) */
@import url("https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css");

/* 2. 기본 레이아웃 */
.page-container {
  min-height: 80vh;
  display: flex;
  flex-direction: column;
  background-color: transparent; 
  font-family: "Pretendard", -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif;
  color: #333;
}

.main-content {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1.5rem;
}

/* 3. 로그인 카드 디자인 강화 */
.login-card {
  width: 100%;
  max-width: 420px;
  padding: 3.5rem 3rem;
  background: #ffffff;
  border-radius: 24px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.04), 0 2px 10px rgba(0, 0, 0, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.8);
  transition: transform 0.3s ease;
}

/* 인사말 타이포그래피 */
.greeting {
  text-align: left; 
  margin-bottom: 2.5rem;
}
.greeting h2 {
  font-size: 1.1rem;
  color: #64748b;
  margin: 0;
  font-weight: 500;
  margin-bottom: 0.5rem;
}
.greeting h1 {
  font-size: 2rem;
  font-weight: 800;
  color: #1e293b;
  margin: 0;
  letter-spacing: -0.5px;
}
.greeting p {
  color: #94a3b8;
  font-size: 0.95rem;
  margin-top: 0.5rem;
}

/* 4. 폼 스타일링 */
.login-form {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
.form-group label {
  font-size: 0.9rem;
  font-weight: 600;
  color: #475569;
  margin-left: 4px;
}
.form-group input {
  width: 100%;
  padding: 0.95rem 1.25rem;
  background-color: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  font-size: 1rem;
  outline: none;
  transition: all 0.2s ease;
  box-sizing: border-box;
  color: #1e293b;
}
.form-group input::placeholder {
  color: #cbd5e1;
}
.form-group input:focus {
  background-color: #fff;
  border-color: #3b82f6; 
  box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1); 
}

/* 비밀번호 토글 버튼 */
.password-wrapper {
  position: relative;
}
.password-wrapper input {
  padding-right: 3.5rem;
}
.eye-icon {
  position: absolute;
  top: 50%;
  right: 1.25rem;
  transform: translateY(-50%);
  background: none;
  border: none;
  cursor: pointer;
  color: #94a3b8;
  padding: 0;
  display: flex;
  align-items: center;
  transition: color 0.2s;
}
.eye-icon:hover {
  color: #475569;
}
.eye-icon svg {
  width: 20px;
  height: 20px;
}

/* 5. 옵션 & 커스텀 체크박스 */
.options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.9rem;
  margin-top: 0.25rem;
  color: #64748b;
}

/* 커스텀 체크박스 디자인 */
.checkbox-container {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  position: relative;
  user-select: none;
}
.checkbox-container input {
  position: absolute;
  opacity: 0;
  cursor: pointer;
  height: 0;
  width: 0;
}
.checkmark {
  height: 18px;
  width: 18px;
  background-color: #f1f5f9;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  transition: all 0.2s;
}
.checkbox-container:hover .checkmark {
  background-color: #e2e8f0;
}
.checkbox-container input:checked ~ .checkmark {
  background-color: #1e293b;
  border-color: #1e293b;
}
.checkmark:after {
  content: "";
  position: absolute;
  display: none;
}
.checkbox-container input:checked ~ .checkmark:after {
  display: block;
  left: 6px;
  top: 2px;
  width: 4px;
  height: 9px;
  border: solid white;
  border-width: 0 2px 2px 0;
  transform: rotate(45deg);
}
.label-text {
  font-size: 0.9rem;
  font-weight: 500;
}

/* 링크 스타일 */
.find-links {
  display: flex;
  align-items: center;
  gap: 0.8rem;
}
.separator {
  width: 1px;
  height: 10px;
  background-color: #cbd5e1;
}
.link {
  color: #64748b;
  text-decoration: none;
  font-size: 0.85rem;
  font-weight: 500;
  transition: color 0.2s;
}
.link:hover {
  color: #3b82f6;
}

/* 6. 메인 로그인 버튼 */
.btn-login {
  background-color: #1e293b; 
  color: #fff;
  padding: 1.1rem;
  border-radius: 12px;
  border: none;
  font-weight: 700;
  font-size: 1.05rem;
  cursor: pointer;
  margin-top: 1rem;
  transition: all 0.2s;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}
.btn-login:hover {
  background-color: #334155;
  transform: translateY(-2px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}
.btn-login:active {
  transform: translateY(0);
}

/* 구분선 */
.divider {
  display: flex;
  align-items: center;
  text-align: center;
  margin: 2rem 0 1.5rem 0;
  color: #94a3b8;
  font-size: 0.8rem;
  font-weight: 500;
}
.divider::before,
.divider::after {
  content: '';
  flex: 1;
  border-bottom: 1px solid #e2e8f0;
}
.divider span {
  padding: 0 1rem;
}

/* 7. 소셜 로그인 버튼 (원형, 미니멀) */
.social-login {
  display: flex;
  justify-content: center;
  gap: 1.5rem;
}
.social-btn {
  width: 52px;
  height: 52px;
  border-radius: 50%;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  background-color: white;
  box-shadow: 0 2px 4px rgba(0,0,0,0.06);
  border: 1px solid #f1f5f9;
}
.social-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 12px rgba(0,0,0,0.08);
}
.social-btn.kakao {
  background-color: #fee500;
  border-color: #fee500;
}
.social-btn.kakao svg {
  fill: #391b1b;
}
.social-btn.google {
  background-color: #fff;
}

/* 8. 하단 회원가입 링크 */
.signup-area {
  margin-top: 2.5rem;
  text-align: center;
  font-size: 0.95rem;
  color: #64748b;
}
.signup-link {
  color: #1e293b;
  font-weight: 700;
  text-decoration: none;
  margin-left: 0.5rem;
  position: relative;
}
.signup-link::after {
  content: '';
  position: absolute;
  width: 100%;
  height: 2px;
  bottom: -2px;
  left: 0;
  background-color: #1e293b;
  transform: scaleX(0);
  transform-origin: bottom right;
  transition: transform 0.25s ease-out;
}
.signup-link:hover::after {
  transform: scaleX(1);
  transform-origin: bottom left;
}

/* 에러 메시지 애니메이션 */
.error-message {
  background-color: #fef2f2;
  color: #dc2626;
  padding: 0.9rem;
  border-radius: 8px;
  margin-bottom: 1.5rem;
  font-size: 0.9rem;
  border: 1px solid #fecaca;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 반응형 모바일 대응 */
@media (max-width: 640px) {
  .login-card {
    padding: 2.5rem 1.5rem;
    box-shadow: none; 
    border: none;
  }
  .page-container {
    background-color: #fff;
  }
}
</style>