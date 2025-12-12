<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const route = useRoute()

const formData = ref({
  token: '',
  new_password: '',
  new_password_confirm: '',
})

const error = ref('')
const success = ref('')
const loading = ref(false)

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

onMounted(() => {
  // URL에서 토큰 가져오기
  const token = route.query.token
  if (token) {
    formData.value.token = token
  } else {
    error.value = '유효하지 않은 접근입니다.'
  }
})

const handleSubmit = async () => {
  try {
    loading.value = true
    error.value = ''
    success.value = ''

    if (formData.value.new_password !== formData.value.new_password_confirm) {
      error.value = '비밀번호가 일치하지 않습니다.'
      loading.value = false
      return
    }

    const response = await axios.post(`${API_URL}/auth/password-reset/confirm/`, formData.value)

    success.value = response.data.message

    // 3초 후 로그인 페이지로 이동
    setTimeout(() => {
      router.push('/login')
    }, 3000)
  } catch (err) {
    error.value = err.response?.data?.error || '비밀번호 재설정에 실패했습니다.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="reset-password-confirm-view">
    <div class="card">
      <h1>비밀번호 재설정</h1>
      <p class="description">새로운 비밀번호를 입력하세요.</p>

      <div v-if="error" class="error-message">{{ error }}</div>
      <div v-if="success" class="success-message">
        {{ success }}
        <br />
        <small>잠시 후 로그인 페이지로 이동합니다...</small>
      </div>

      <form v-if="!success && formData.token" @submit.prevent="handleSubmit">
        <div class="form-group">
          <label>새 비밀번호</label>
          <input v-model="formData.new_password" type="password" required placeholder="새 비밀번호를 입력하세요" />
        </div>

        <div class="form-group">
          <label>새 비밀번호 확인</label>
          <input
            v-model="formData.new_password_confirm"
            type="password"
            required
            placeholder="새 비밀번호를 다시 입력하세요"
          />
        </div>

        <button type="submit" class="btn-primary" :disabled="loading">
          {{ loading ? '처리 중...' : '비밀번호 재설정' }}
        </button>
      </form>

      <div class="links">
        <router-link to="/login">로그인으로 돌아가기</router-link>
      </div>
    </div>
  </div>
</template>

<style scoped>
.reset-password-confirm-view {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 60vh;
  padding: 2rem;
}

.card {
  width: 100%;
  max-width: 500px;
  padding: 2rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

h1 {
  text-align: center;
  margin-bottom: 1rem;
}

.description {
  text-align: center;
  color: #666;
  margin-bottom: 2rem;
  line-height: 1.5;
}

.error-message {
  padding: 1rem;
  background-color: #ffe6e6;
  color: #c00;
  border-radius: 8px;
  margin-bottom: 1rem;
}

.success-message {
  padding: 1rem;
  background-color: #d4edda;
  color: #155724;
  border-radius: 8px;
  margin-bottom: 1rem;
  text-align: center;
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

.btn-primary:hover:not(:disabled) {
  background-color: #2980b9;
}

.btn-primary:disabled {
  background-color: #bdc3c7;
  cursor: not-allowed;
}

.links {
  text-align: center;
  margin-top: 1.5rem;
}

.links a {
  color: #3498db;
  text-decoration: none;
  font-size: 0.9rem;
}

.links a:hover {
  text-decoration: underline;
}
</style>
