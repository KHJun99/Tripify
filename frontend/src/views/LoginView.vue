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

const KAKAO_REST_API_KEY = import.meta.env.VITE_KAKAO_REST_API_KEY || ''
const KAKAO_REDIRECT_URI = import.meta.env.VITE_KAKAO_REDIRECT_URI || 'http://localhost:5173/auth/kakao/callback'
const GOOGLE_CLIENT_ID = import.meta.env.VITE_GOOGLE_CLIENT_ID || ''
const GOOGLE_REDIRECT_URI = import.meta.env.VITE_GOOGLE_REDIRECT_URI || 'http://localhost:5173/auth/google/callback'

const handleLogin = async () => {
  try {
    error.value = ''
    await authStore.login(formData.value)
    router.push('/')
  } catch (err) {
    error.value = err.response?.data?.error || '로그인에 실패했습니다.'
  }
}

const handleKakaoLogin = () => {
  const kakaoAuthUrl = `https://kauth.kakao.com/oauth/authorize?client_id=${KAKAO_REST_API_KEY}&redirect_uri=${KAKAO_REDIRECT_URI}&response_type=code`
  window.location.href = kakaoAuthUrl
}

const handleGoogleLogin = () => {
  const googleAuthUrl = `https://accounts.google.com/o/oauth2/v2/auth?client_id=${GOOGLE_CLIENT_ID}&redirect_uri=${GOOGLE_REDIRECT_URI}&response_type=code&scope=openid email profile`
  window.location.href = googleAuthUrl
}
</script>

<template>
  <div class="login-view">
    <div class="login-card">
      <h1>로그인</h1>

      <div v-if="error" class="error-message">{{ error }}</div>

      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label>아이디</label>
          <input v-model="formData.username" type="text" required />
        </div>

        <div class="form-group">
          <label>비밀번호</label>
          <input v-model="formData.password" type="password" required />
        </div>

        <div class="account-recovery">
          <router-link to="/auth/find-username" class="recovery-link">아이디 찾기</router-link>
          <span class="divider-text">|</span>
          <router-link to="/auth/reset-password" class="recovery-link">비밀번호 찾기</router-link>
        </div>

        <button type="submit" class="btn-primary">로그인</button>
      </form>

      <div class="divider">
        <span>또는</span>
      </div>

      <button type="button" class="btn-kakao" @click="handleKakaoLogin">
        <span class="kakao-icon">💬</span>
        카카오로 시작하기
      </button>

      <button type="button" class="btn-google" @click="handleGoogleLogin">
        <span class="google-icon">G</span>
        구글로 시작하기
      </button>

      <p class="signup-link">
        계정이 없으신가요? <router-link to="/signup">회원가입</router-link>
      </p>
    </div>
  </div>
</template>

<style scoped>
.login-view {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 60vh;
}

.login-card {
  width: 100%;
  max-width: 400px;
  padding: 2rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

h1 {
  text-align: center;
  margin-bottom: 2rem;
}

.error-message {
  padding: 1rem;
  background-color: #ffe6e6;
  color: #c00;
  border-radius: 8px;
  margin-bottom: 1rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.form-group input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
}

.btn-primary {
  width: 100%;
  padding: 1rem;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: bold;
  transition: background-color 0.3s;
}

.btn-primary:hover {
  background-color: #2980b9;
}

.signup-link {
  text-align: center;
  margin-top: 1.5rem;
}

.signup-link a {
  color: #3498db;
  text-decoration: none;
  font-weight: bold;
}

.divider {
  display: flex;
  align-items: center;
  text-align: center;
  margin: 1.5rem 0;
}

.divider::before,
.divider::after {
  content: '';
  flex: 1;
  border-bottom: 1px solid #ddd;
}

.divider span {
  padding: 0 1rem;
  color: #999;
  font-size: 0.9rem;
}

.btn-kakao {
  width: 100%;
  padding: 1rem;
  background-color: #fee500;
  color: #000000;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: bold;
  transition: background-color 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.btn-kakao:hover {
  background-color: #fdd835;
}

.kakao-icon {
  font-size: 1.2rem;
}

.btn-google {
  width: 100%;
  padding: 1rem;
  background-color: #ffffff;
  color: #000000;
  border: 1px solid #dadce0;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: bold;
  transition: background-color 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  margin-top: 0.75rem;
}

.btn-google:hover {
  background-color: #f8f9fa;
  box-shadow: 0 1px 2px 0 rgba(60, 64, 67, 0.3), 0 1px 3px 1px rgba(60, 64, 67, 0.15);
}

.google-icon {
  font-size: 1.2rem;
  font-weight: bold;
  color: #4285f4;
}

.account-recovery {
  text-align: center;
  margin: 1rem 0;
  font-size: 0.9rem;
}

.recovery-link {
  color: #666;
  text-decoration: none;
  transition: color 0.3s;
}

.recovery-link:hover {
  color: #3498db;
  text-decoration: underline;
}

.divider-text {
  margin: 0 0.5rem;
  color: #ccc;
}
</style>
