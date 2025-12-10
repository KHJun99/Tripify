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

        <button type="submit" class="btn-primary">로그인</button>
      </form>

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
</style>
