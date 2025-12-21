<script setup>
import { RouterView, RouterLink, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { computed, onMounted } from 'vue'

const router = useRouter()
const authStore = useAuthStore()
const isAuthenticated = computed(() => authStore.isAuthenticated)

onMounted(async () => {
  // 로그인 상태면 프로필 정보 가져오기
  if (isAuthenticated.value && !authStore.user) {
    try {
      await authStore.getProfile()
    } catch (error) {
      console.error('프로필 로드 실패:', error)
    }
  }
})

const handleLogout = async () => {
  await authStore.logout()
  // 로그아웃 후 메인페이지로 이동
  router.push('/')
}
</script>

<template>
  <div id="app">
    <nav class="navbar">
      <div class="nav-brand">
        <RouterLink to="/">Tripify</RouterLink>
      </div>
      <div class="nav-links">
        <RouterLink to="/">홈</RouterLink>
        <template v-if="isAuthenticated">
          <div class="user-greeting" v-if="authStore.user?.nickname">
            <span class="greeting-text">{{ authStore.user.nickname }} 오늘도 좋은 여행하세요</span>
          </div>
          <RouterLink to="/trips">내 여행</RouterLink>
          <RouterLink to="/trip/new">여행 계획</RouterLink>
          <RouterLink to="/recommended">추천된 여행지</RouterLink>
          <RouterLink to="/settings">마이페이지</RouterLink>
          <button @click="handleLogout" class="btn-link">로그아웃</button>
        </template>
        <template v-else>
          <RouterLink to="/login">로그인</RouterLink>
          <RouterLink to="/signup">회원가입</RouterLink>
        </template>
      </div>
    </nav>

    <main class="main-content">
      <RouterView />
    </main>
  </div>
</template>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

#app {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
  color: #2c3e50;
  min-height: 100vh;
}

.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background-color: #3498db;
  color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.nav-brand a {
  font-size: 1.5rem;
  font-weight: bold;
  color: white;
  text-decoration: none;
}

.nav-links {
  display: flex;
  gap: 1.5rem;
  align-items: center;
}

.user-greeting {
  margin-right: 0.5rem;
  padding: 0.5rem 1rem;
  background-color: rgba(255, 255, 255, 0.2);
  border-radius: 20px;
  font-size: 0.9rem;
}

.greeting-text {
  color: white;
  font-weight: 500;
}

.nav-links a,
.btn-link {
  color: white;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.nav-links a:hover,
.btn-link:hover {
  background-color: rgba(255, 255, 255, 0.2);
}

.btn-link {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1rem;
}

.main-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}
</style>
