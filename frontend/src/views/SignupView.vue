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
  password_confirm: '',
})

const error = ref('')
const success = ref('')
const showSuccessDialog = ref(false)

const handleSignup = async () => {
  try {
    error.value = ''
    success.value = ''
    const response = await authStore.signup(formData.value)

    // 회원가입 성공 시 이메일 인증 안내
    if (response?.message) {
      success.value = response.message
      showSuccessDialog.value = true

      // 5초 후 로그인 페이지로 이동
      setTimeout(() => {
        router.push('/login')
      }, 5000)
    } else {
      router.push('/login')
    }
  } catch (err) {
    error.value = err.response?.data?.error || '회원가입에 실패했습니다.'
  }
}
</script>

<template>
  <div class="signup-view">
    <div class="signup-card">
      <h1>회원가입</h1>

      <div v-if="showSuccessDialog" class="success-dialog">
        <div class="icon-success">✓</div>
        <h2>회원가입 완료!</h2>
        <p class="success-message">{{ success }}</p>
        <p class="email-notice">📧 가입하신 이메일로 인증 링크를 보내드렸습니다.</p>
        <p class="redirect-notice">이메일 인증 후 로그인해주세요.</p>
        <small>잠시 후 로그인 페이지로 이동합니다...</small>
      </div>

      <div v-if="error" class="error-message">{{ error }}</div>

      <form v-if="!showSuccessDialog" @submit.prevent="handleSignup">
        <div class="form-group">
          <label>아이디</label>
          <input v-model="formData.username" type="text" required />
        </div>

        <div class="form-group">
          <label>이메일</label>
          <input v-model="formData.email" type="email" required />
        </div>

        <div class="form-group">
          <label>비밀번호</label>
          <input v-model="formData.password" type="password" required />
        </div>

        <div class="form-group">
          <label>비밀번호 확인</label>
          <input v-model="formData.password_confirm" type="password" required />
        </div>

        <button type="submit" class="btn-primary">가입하기</button>
      </form>

      <p class="login-link">
        이미 계정이 있으신가요? <router-link to="/login">로그인</router-link>
      </p>
    </div>
  </div>
</template>

<style scoped>
.signup-view {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 60vh;
}

.signup-card {
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

.login-link {
  text-align: center;
  margin-top: 1.5rem;
}

.login-link a {
  color: #3498db;
  text-decoration: none;
  font-weight: bold;
}

.success-dialog {
  text-align: center;
  padding: 2rem 1rem;
}

.icon-success {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background-color: #d4edda;
  color: #28a745;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 3rem;
  font-weight: bold;
  margin: 0 auto 1.5rem;
}

.success-dialog h2 {
  margin-bottom: 1rem;
  color: #333;
}

.success-message {
  color: #28a745;
  margin-bottom: 1rem;
  font-size: 1.1rem;
}

.email-notice {
  background-color: #e7f3ff;
  padding: 1rem;
  border-radius: 8px;
  margin: 1rem 0;
  color: #004085;
}

.redirect-notice {
  color: #666;
  margin: 0.5rem 0;
}

.success-dialog small {
  color: #999;
  display: block;
  margin-top: 1rem;
}
</style>
