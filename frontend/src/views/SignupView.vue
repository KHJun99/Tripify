<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

// --- 상태 변수 ---
const formData = ref({
  username: '',
  email: '',
  nickname: '',
  password: '',
  password_confirm: '',
})

const error = ref('')
const success = ref('')
const showSuccessDialog = ref(false)

// 비밀번호 토글 상태
const showPassword = ref(false)
const showConfirmPassword = ref(false)

// --- 회원가입 함수 ---
const handleSignup = async () => {
  try {
    error.value = ''
    success.value = ''

    // 비밀번호 일치 확인
    if (formData.value.password !== formData.value.password_confirm) {
      error.value = '비밀번호가 일치하지 않습니다.'
      return
    }

    // 회원가입 요청
    const response = await authStore.signup(formData.value)

    if (response?.message) {
      success.value = response.message
      showSuccessDialog.value = true

      setTimeout(() => {
        router.push('/login')
      }, 3000)
    } else {
      router.push('/login')
    }
  } catch (err) {
    console.error(err)
    error.value = err.response?.data?.error || '회원가입에 실패했습니다.'
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
      <div class="signup-card floating-animation">

        <transition name="fade">
          <div v-if="showSuccessDialog" class="success-view">
            <div class="icon-success">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2.5" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5" />
              </svg>
            </div>
            <h2>회원가입 완료!</h2>
            <p class="success-msg">{{ success }}</p>

            <div class="notice-box">
              <p>📧 <strong>이메일 인증</strong>이 필요합니다.</p>
              <p class="sub-text">가입하신 이메일로 인증 링크를 보내드렸습니다.<br>인증 후 로그인해주세요.</p>
            </div>

            <small>잠시 후 로그인 페이지로 이동합니다...</small>
            <router-link to="/login" class="btn-login-move">
              로그인하러 가기
            </router-link>
          </div>
        </transition>

        <div v-if="!showSuccessDialog">
          <div class="greeting">
            <h2>반갑습니다! 👋</h2>
            <h1>회원가입</h1>
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

          <form @submit.prevent="handleSignup" class="signup-form">
            <div class="form-group">
              <label>아이디</label>
              <input v-model="formData.username" type="text" placeholder="아이디를 입력해주세요" required />
            </div>

            <div class="form-group">
              <label>이메일</label>
              <input v-model="formData.email" type="email" placeholder="example@tripify.com" required />
            </div>

            <div class="form-group">
              <label>닉네임</label>
              <input v-model="formData.nickname" type="text" placeholder="홈페이지에 표시될 닉네임을 입력하세요" required />
            </div>

            <div class="form-group">
              <label>비밀번호</label>
              <div class="password-wrapper">
                <input
                  v-model="formData.password"
                  :type="showPassword ? 'text' : 'password'"
                  placeholder="비밀번호를 입력해주세요"
                  required
                />
                <button type="button" class="eye-icon" @click="showPassword = !showPassword" tabindex="-1">
                  <svg v-if="showPassword" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" /></svg>
                  <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" /></svg>
                </button>
              </div>
            </div>

            <div class="form-group">
              <label>비밀번호 확인</label>
              <div class="password-wrapper">
                <input
                  v-model="formData.password_confirm"
                  :type="showConfirmPassword ? 'text' : 'password'"
                  placeholder="비밀번호를 다시 입력해주세요"
                  required
                />
                <button type="button" class="eye-icon" @click="showConfirmPassword = !showConfirmPassword" tabindex="-1">
                  <svg v-if="showConfirmPassword" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" /><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" /></svg>
                  <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" /></svg>
                </button>
              </div>
            </div>

            <button type="submit" class="btn-primary">회원가입</button>
          </form>

          <div class="signup-footer">
            <span>이미 계정이 있으신가요?</span>
            <router-link to="/login" class="link-bold">로그인</router-link>
          </div>
        </div>

      </div>
    </main>
  </div>
</template>

<style scoped>
/* 1. 폰트 로드 */
@import url("https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css");

/* 2. 전체 레이아웃 (하늘 배경 포함) */
.page-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: hidden;
  
  /* 그라데이션 배경 */
  background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
  font-family: "Pretendard", -apple-system, BlinkMacSystemFont, system-ui, Roboto, sans-serif;
  color: #333;
}

/* 3. 구름 애니메이션 구현 */
.sky-background {
  position: absolute;
  top: 0; left: 0; width: 100%; height: 100%;
  z-index: 0; pointer-events: none;
}
.cloud {
  position: absolute; background: #fff; border-radius: 100px;
  opacity: 0.8; filter: blur(10px); animation: drift linear infinite;
}
.cloud::after, .cloud::before {
  content: ''; position: absolute; background: inherit; border-radius: 50%;
}
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
.main-content {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  z-index: 10;
}

/* 4. 카드 디자인 (Glassmorphism + Floating) */
.signup-card {
  width: 100%;
  max-width: 440px;
  padding: 3.5rem 3rem;
  
  /* 유리 효과 */
  background: rgba(255, 255, 255, 0.75);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  
  border-radius: 30px;
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1), 0 5px 15px rgba(0, 0, 0, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.9);
  
  /* 둥둥 뜨는 애니메이션 */
  animation: float 6s ease-in-out infinite;
}

@keyframes float {
  0% { transform: translateY(0px); box-shadow: 0 15px 35px rgba(0,0,0,0.1); }
  50% { transform: translateY(-15px); box-shadow: 0 25px 45px rgba(0,0,0,0.1); }
  100% { transform: translateY(0px); box-shadow: 0 15px 35px rgba(0,0,0,0.1); }
}

/* 인사말 */
.greeting { text-align: left; margin-bottom: 2rem; }
.greeting h2 { font-size: 1.1rem; color: #64748b; margin: 0 0 0.5rem 0; font-weight: 500; }
.greeting h1 { font-size: 2rem; font-weight: 800; color: #1e293b; margin: 0 0 0.5rem 0; letter-spacing: -0.5px; }
.greeting p { color: #64748b; font-size: 0.95rem; margin: 0; }

/* 5. 폼 스타일 */
.signup-form { display: flex; flex-direction: column; gap: 1.25rem; }
.form-group { display: flex; flex-direction: column; gap: 0.5rem; }
.form-group label { font-size: 0.9rem; font-weight: 600; color: #475569; margin-left: 4px; }

/* Input 스타일 (반투명 적용) */
.form-group input {
  width: 100%;
  padding: 0.95rem 1.25rem;
  background-color: rgba(248, 250, 252, 0.8);
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  font-size: 1rem;
  outline: none;
  transition: all 0.2s ease;
  box-sizing: border-box;
  color: #1e293b;
}
.form-group input:focus {
  background-color: #fff;
  border-color: #7dd3fc;
  box-shadow: 0 0 0 4px rgba(125, 211, 252, 0.2);
}

/* 비밀번호 토글 */
.password-wrapper { position: relative; }
.password-wrapper input { padding-right: 3.5rem; }
.eye-icon {
  position: absolute; top: 50%; right: 1.25rem; transform: translateY(-50%);
  background: none; border: none; cursor: pointer; color: #94a3b8; padding: 0; display: flex; align-items: center;
}
.eye-icon:hover { color: #475569; }
.eye-icon svg { width: 20px; height: 20px; }

/* 버튼 (그라데이션 적용) */
.btn-primary {
  background: linear-gradient(135deg, #0ea5e9 0%, #3b82f6 100%);
  color: #fff; padding: 1.1rem;
  border-radius: 12px; border: none; font-weight: 700; font-size: 1.05rem;
  cursor: pointer; margin-top: 1rem; transition: all 0.3s;
  box-shadow: 0 4px 15px rgba(14, 165, 233, 0.3); width: 100%;
}
.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(14, 165, 233, 0.4);
}

/* 하단 링크 */
.signup-footer { margin-top: 2rem; text-align: center; font-size: 0.95rem; color: #64748b; }
.link-bold { color: #0ea5e9; font-weight: 700; text-decoration: none; margin-left: 0.5rem; position: relative; }
.link-bold:hover { color: #3b82f6; }

/* 6. 성공 화면 스타일 */
.success-view { text-align: center; padding: 1rem 0; }
.icon-success {
  width: 70px; height: 70px; border-radius: 50%;
  background-color: #dcfce7; color: #16a34a;
  display: flex; align-items: center; justify-content: center; margin: 0 auto 1.5rem;
  box-shadow: 0 4px 10px rgba(0,0,0,0.05);
}
.icon-success svg { width: 36px; height: 36px; }
.success-view h2 { font-size: 1.8rem; font-weight: 800; color: #1e293b; margin-bottom: 0.5rem; }
.success-msg { color: #16a34a; font-weight: 600; margin-bottom: 2rem; }

.notice-box {
  background-color: rgba(255, 255, 255, 0.6);
  padding: 1.5rem; border-radius: 12px;
  border: 1px solid #e2e8f0; margin-bottom: 2rem; text-align: left;
}
.notice-box p { margin: 0.25rem 0; font-size: 0.95rem; color: #334155; }
.sub-text { font-size: 0.85rem !important; color: #64748b !important; margin-top: 0.5rem !important; line-height: 1.4; }

.btn-login-move {
  display: block; width: 100%; text-align: center;
  background: linear-gradient(135deg, #0ea5e9 0%, #3b82f6 100%);
  color: white; padding: 1rem; border-radius: 12px; text-decoration: none;
  font-weight: bold; margin-top: 1rem;
  transition: all 0.3s;
  box-shadow: 0 4px 15px rgba(14, 165, 233, 0.3);
}
.btn-login-move:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(14, 165, 233, 0.4);
}

/* 에러 메시지 */
.error-message {
  background-color: #fef2f2; color: #dc2626; padding: 0.9rem;
  border-radius: 8px; margin-bottom: 1.5rem; font-size: 0.9rem;
  border: 1px solid #fecaca; display: flex; align-items: center; gap: 0.5rem;
}

/* 애니메이션 트랜지션 */
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

/* 모바일 대응 */
@media (max-width: 640px) {
  .signup-card { 
    padding: 2.5rem 1.5rem; 
    background: rgba(255, 255, 255, 0.9);
    backdrop-filter: blur(10px);
    animation: none;
  }
}
</style>