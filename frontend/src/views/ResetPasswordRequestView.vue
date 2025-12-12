<script setup>
import { ref } from 'vue'
import axios from 'axios'

const formData = ref({
  email: '',
})

const error = ref('')
const success = ref('')
const loading = ref(false)

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

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
  <div class="reset-password-view">
    <div class="card">
      <h1>비밀번호 재설정</h1>
      <p class="description">가입 시 등록한 이메일 주소를 입력하시면, 비밀번호 재설정 링크를 이메일로 보내드립니다.</p>

      <div v-if="error" class="error-message">{{ error }}</div>
      <div v-if="success" class="success-message">{{ success }}</div>

      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label>이메일</label>
          <input v-model="formData.email" type="email" required placeholder="이메일 주소를 입력하세요" />
        </div>

        <button type="submit" class="btn-primary" :disabled="loading">
          {{ loading ? '전송 중...' : '재설정 링크 받기' }}
        </button>
      </form>

      <div class="links">
        <router-link to="/login">로그인으로 돌아가기</router-link>
      </div>
    </div>
  </div>
</template>

<style scoped>
.reset-password-view {
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
