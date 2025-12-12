<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const route = useRoute()

const error = ref('')
const success = ref('')
const loading = ref(true)
const username = ref('')

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

onMounted(async () => {
  const token = route.query.token

  if (!token) {
    error.value = '유효하지 않은 접근입니다.'
    loading.value = false
    return
  }

  try {
    const response = await axios.get(`${API_URL}/accounts/verify-email/`, {
      params: { token },
    })

    success.value = response.data.message
    username.value = response.data.username

    // 3초 후 로그인 페이지로 이동
    setTimeout(() => {
      router.push('/login')
    }, 3000)
  } catch (err) {
    error.value = err.response?.data?.error || '이메일 인증에 실패했습니다.'
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="verify-email-view">
    <div class="card">
      <div v-if="loading" class="loading">
        <div class="spinner"></div>
        <p>이메일 인증 중...</p>
      </div>

      <div v-if="!loading && success" class="success-content">
        <div class="icon-success">✓</div>
        <h1>이메일 인증 완료!</h1>
        <p class="success-message">{{ success }}</p>
        <p class="username">환영합니다, <strong>{{ username }}</strong>님!</p>
        <p class="redirect-message">잠시 후 로그인 페이지로 이동합니다...</p>
      </div>

      <div v-if="!loading && error" class="error-content">
        <div class="icon-error">✗</div>
        <h1>인증 실패</h1>
        <p class="error-message">{{ error }}</p>
        <div class="links">
          <router-link to="/login" class="btn-primary">로그인 페이지로</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.verify-email-view {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 60vh;
  padding: 2rem;
}

.card {
  width: 100%;
  max-width: 500px;
  padding: 3rem 2rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.spinner {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.success-content,
.error-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
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
}

.icon-error {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background-color: #ffe6e6;
  color: #c00;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 3rem;
  font-weight: bold;
}

h1 {
  margin: 0.5rem 0;
  color: #333;
}

.success-message {
  color: #28a745;
  margin: 0;
}

.error-message {
  color: #c00;
  margin: 0;
}

.username {
  font-size: 1.1rem;
  margin: 0.5rem 0;
}

.redirect-message {
  color: #666;
  font-size: 0.9rem;
  margin-top: 1rem;
}

.links {
  margin-top: 1.5rem;
}

.btn-primary {
  display: inline-block;
  padding: 0.75rem 2rem;
  background-color: #3498db;
  color: white;
  text-decoration: none;
  border-radius: 8px;
  transition: background-color 0.3s;
}

.btn-primary:hover {
  background-color: #2980b9;
}
</style>
