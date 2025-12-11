<script setup>
import { onMounted, ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const error = ref('')
const isProcessing = ref(true)

onMounted(async () => {
  const code = route.query.code

  if (!code) {
    error.value = '인가 코드가 없습니다.'
    isProcessing.value = false
    setTimeout(() => {
      router.push('/login')
    }, 2000)
    return
  }

  try {
    await authStore.kakaoLogin(code)
    router.push('/')
  } catch (err) {
    error.value = err.response?.data?.error || '카카오 로그인에 실패했습니다.'
    isProcessing.value = false
    setTimeout(() => {
      router.push('/login')
    }, 3000)
  }
})
</script>

<template>
  <div class="callback-view">
    <div class="callback-card">
      <LoadingSpinner v-if="isProcessing" />

      <div v-if="!isProcessing && !error" class="success-message">
        <h2>로그인 성공!</h2>
        <p>잠시 후 메인 페이지로 이동합니다...</p>
      </div>

      <div v-if="error" class="error-message">
        <h2>로그인 실패</h2>
        <p>{{ error }}</p>
        <p class="redirect-info">로그인 페이지로 돌아갑니다...</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.callback-view {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 60vh;
}

.callback-card {
  text-align: center;
  padding: 3rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  min-width: 300px;
}

.success-message {
  color: #27ae60;
}

.success-message h2 {
  margin-bottom: 1rem;
}

.error-message {
  color: #c0392b;
}

.error-message h2 {
  margin-bottom: 1rem;
}

.error-message p {
  margin: 0.5rem 0;
}

.redirect-info {
  margin-top: 1rem;
  font-size: 0.9rem;
  color: #7f8c8d;
}
</style>
