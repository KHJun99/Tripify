<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const route = useRoute()

const formData = ref({
  email: '',
})

const error = ref('')
const success = ref('')
const loading = ref(false)

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

// 토큰이 있으면 비밀번호 재설정 확인 페이지로 리다이렉트
onMounted(() => {
  const token = route.query.token
  if (token) {
    router.replace({
      name: 'reset-password-confirm',
      query: { token }
    })
  }
})

const handleSubmit = async () => {
  try {
    loading.value = true
    error.value = ''
    success.value = ''

    const response = await axios.post(`${API_URL}/auth/password-reset/request/`, formData.value)

    success.value = response.data.message
    formData.value.email = ''
  } catch (err) {
    error.value = err.response?.data?.error || '비밀번호 재설정 요청에 실패했습니다.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="page-container">
    
    <div class="sky-background">
      <div class="cloud cloud-1"></div>
      <div class="cloud cloud-2"></div>
      <div class="cloud cloud-3"></div>
      <div class="cloud cloud-4"></div>
    </div>

    <main class="main-content">
      <div class="card floating-animation">
        
        <div class="icon-header">
          <div class="icon-circle">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" d="M16.5 10.5V6.75a4.5 4.5 0 10-9 0v3.75m-.75 11.25h10.5a2.25 2.25 0 002.25-2.25v-6.75a2.25 2.25 0 00-2.25-2.25H6.75a2.25 2.25 0 00-2.25 2.25v6.75a2.25 2.25 0 002.25 2.25z" />
            </svg>
            <div class="badge">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 5.25a3 3 0 013 3m3 0a6 6 0 01-7.029 5.912c-.563-.097-1.159.026-1.563.43L10.5 17.25H8.25v2.25H6v2.25H2.25v-2.818c0-.597.237-1.17.659-1.591l6.499-6.499c.404-.404.527-1 .43-1.563A6 6 0 1121.75 8.25z" />
              </svg>
            </div>
          </div>
        </div>

        <div class="greeting">
          <h1>비밀번호 재설정</h1>
          <p class="description">
            가입 시 등록한 이메일을 입력하시면,<br>
            재설정 링크를 보내드립니다.
          </p>
        </div>

        <transition name="fade">
          <div v-if="error" class="message error-message">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="w-5 h-5">
              <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
            </svg>
            <span>{{ error }}</span>
          </div>
        </transition>

        <transition name="fade">
          <div v-if="success" class="message success-message">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span>{{ success }}</span>
          </div>
        </transition>

        <form @submit.prevent="handleSubmit" class="reset-form">
          <div class="form-group">
            <label for="email">이메일 주소</label>
            <input 
              id="email"
              v-model="formData.email" 
              type="email" 
              required 
              placeholder="예: tripify@example.com" 
            />
          </div>

          <button type="submit" class="btn-primary" :disabled="loading">
            {{ loading ? '전송 중...' : '재설정 링크 받기' }}
          </button>
        </form>

        <div class="links">
          <router-link to="/login" class="link-back">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" d="M10.5 19.5L3 12m0 0l7.5-7.5M3 12h18" />
            </svg>
            로그인으로 돌아가기
          </router-link>
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped>
@import url("https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css");

/* 기본 레이아웃 및 배경 */
.page-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: hidden;
  background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
  font-family: "Pretendard", sans-serif;
  color: #333;
}

/* 구름 애니메이션 */
.sky-background { position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 0; pointer-events: none; }
.cloud { position: absolute; background: #fff; border-radius: 100px; opacity: 0.8; filter: blur(10px); animation: drift linear infinite; }
.cloud::after, .cloud::before { content: ''; position: absolute; background: inherit; border-radius: 50%; }
.cloud-1 { width: 200px; height: 60px; top: 15%; left: -200px; opacity: 0.6; animation-duration: 45s; }
.cloud-1::after { width: 80px; height: 80px; top: -40px; left: 30px; }
.cloud-1::before { width: 70px; height: 70px; top: -30px; left: 100px; }
.cloud-2 { width: 300px; height: 100px; top: 60%; right: -300px; opacity: 0.4; animation-duration: 60s; animation-direction: reverse; }
.cloud-2::after { width: 120px; height: 120px; top: -60px; left: 50px; }
.cloud-2::before { width: 100px; height: 100px; top: -50px; left: 150px; }
.cloud-3 { width: 150px; height: 50px; top: 80%; left: 20%; opacity: 0.5; animation-duration: 35s; }
.cloud-3::after { width: 60px; height: 60px; top: -30px; left: 20px; }
.cloud-4 { width: 250px; height: 80px; top: 10%; right: 10%; opacity: 0.3; animation-duration: 50s; }
.cloud-4::after { width: 90px; height: 90px; top: -50px; left: 40px; }

@keyframes drift {
  from { transform: translateX(-100%); }
  to { transform: translateX(100vw); }
}

/* 메인 컨텐츠 */
.main-content { flex: 1; display: flex; align-items: center; justify-content: center; padding: 2rem; z-index: 10; }

/* 카드 디자인 */
.card {
  width: 100%;
  max-width: 420px;
  padding: 3rem 2.5rem;
  background: rgba(255, 255, 255, 0.75);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: 30px;
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1), 0 5px 15px rgba(0, 0, 0, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.9);
  animation: float 6s ease-in-out infinite;
}

@keyframes float {
  0% { transform: translateY(0px); box-shadow: 0 15px 35px rgba(0,0,0,0.1); }
  50% { transform: translateY(-15px); box-shadow: 0 25px 45px rgba(0,0,0,0.1); }
  100% { transform: translateY(0px); box-shadow: 0 15px 35px rgba(0,0,0,0.1); }
}

/* 상단 아이콘 디자인 */
.icon-header { display: flex; justify-content: center; margin-bottom: 1.5rem; }
.icon-circle {
  width: 80px; height: 80px;
  background: linear-gradient(135deg, #e0f2fe 0%, #bae6fd 100%);
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  color: #0ea5e9;
  position: relative;
  box-shadow: 0 4px 10px rgba(14, 165, 233, 0.15);
}
.icon-circle > svg { width: 40px; height: 40px; }
.badge {
  position: absolute; bottom: 0; right: 0;
  width: 32px; height: 32px;
  background: #fff;
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
  color: #3b82f6;
}
.badge svg { width: 18px; height: 18px; }

/* 텍스트 스타일 */
.greeting { text-align: center; margin-bottom: 2rem; }
.greeting h1 { font-size: 1.6rem; font-weight: 800; color: #1e293b; margin: 0 0 0.5rem 0; letter-spacing: -0.5px; }
.description { text-align: center; color: #64748b; font-size: 0.95rem; margin: 0; line-height: 1.6; word-break: keep-all; }

/* 폼 요소 */
.reset-form { display: flex; flex-direction: column; gap: 1.5rem; }
.form-group { display: flex; flex-direction: column; gap: 0.5rem; }
.form-group label { font-size: 0.9rem; font-weight: 600; color: #475569; margin-left: 4px; }
.form-group input {
  width: 100%; padding: 0.95rem 1.25rem;
  background-color: rgba(248, 250, 252, 0.8);
  border: 1px solid #e2e8f0; border-radius: 12px;
  font-size: 1rem; outline: none; transition: all 0.2s ease;
  box-sizing: border-box; color: #1e293b;
}
.form-group input:focus {
  background-color: #fff; border-color: #7dd3fc;
  box-shadow: 0 0 0 4px rgba(125, 211, 252, 0.2);
}

/* 버튼 */
.btn-primary {
  background: linear-gradient(135deg, #0ea5e9 0%, #3b82f6 100%);
  color: #fff; padding: 1.1rem; border-radius: 12px;
  border: none; font-weight: 700; font-size: 1.05rem;
  cursor: pointer; transition: all 0.3s;
  box-shadow: 0 4px 15px rgba(14, 165, 233, 0.3); width: 100%;
}
.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px); box-shadow: 0 8px 20px rgba(14, 165, 233, 0.4);
}
.btn-primary:disabled { opacity: 0.7; cursor: not-allowed; background: #94a3b8; box-shadow: none; }

/* 알림 메시지 */
.message { padding: 0.9rem; border-radius: 8px; margin-bottom: 1.5rem; font-size: 0.9rem; display: flex; align-items: center; gap: 0.5rem; }
.message svg { width: 20px; height: 20px; flex-shrink: 0; }
.error-message { background-color: rgba(254, 242, 242, 0.95); color: #dc2626; border: 1px solid #fecaca; }
.success-message { background-color: rgba(220, 252, 231, 0.95); color: #16a34a; border: 1px solid #bbf7d0; }

/* 애니메이션 */
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

/* 하단 링크 */
.links { 
  text-align: center; 
  margin-top: 2rem; 
  display: flex; 
  justify-content: center;
}

.link-back {
  display: inline-flex; 
  align-items: center; 
  justify-content: center;
  gap: 0.5rem;
  color: #64748b; 
  text-decoration: none; 
  font-size: 0.95rem; 
  font-weight: 600; 
  transition: all 0.2s;
  white-space: nowrap;
}

.link-back svg {
  width: 1.2rem;
  height: 1.2rem;
  flex-shrink: 0;
}

.link-back:hover { 
  color: #0ea5e9; 
  transform: translateX(-3px);
}

/* 모바일 대응 */
@media (max-width: 640px) {
  .card { padding: 2.5rem 1.5rem; box-shadow: none; border: none; background: transparent; backdrop-filter: none; animation: none; }
  .page-container { background: #fff; }
  .sky-background { display: none; }
}
</style>