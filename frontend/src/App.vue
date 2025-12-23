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
        <template v-if="isAuthenticated">
          <div class="user-greeting" v-if="authStore.user?.nickname">
            <span class="greeting-text"><strong>{{ authStore.user.nickname }}</strong>님 오늘도 좋은 여행하세요</span>
          </div>
          <RouterLink to="/trips">내 여행</RouterLink>
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
  font-family: 'Noto Sans KR', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  color: #2c3e50;
  min-height: 100vh;
}

.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background-color: #ffffff;
  color: #333333;
  border-bottom: 1px solid #e1e4e8;
  box-shadow: none;
}

.nav-brand a {
  font-size: 1.5rem;
  font-weight: 800;
  color: #6a11cb;
  text-decoration: none;
  letter-spacing: -0.5px;
}

.nav-links {
  display: flex;
  gap: 1.5rem;
  align-items: center;
}

.user-greeting {
  margin-right: 0.5rem;
  padding: 0.4rem 0.8rem;
  background-color: #f1f3f5;
  border-radius: 50px;
  font-size: 0.85rem;
}

.greeting-text {
  color: #495057;
  font-weight: 400;
}

.greeting-text strong {
  color: #6a11cb;
  font-weight: 600;
}

.nav-links a,
.btn-link {
  color: #495057;
  text-decoration: none;
  padding: 0.5rem 0.8rem;
  border-radius: 6px;
  transition: all 0.2s ease;
  font-weight: 500;
}

.nav-links a:hover,
.btn-link:hover {
  background-color: #f8f9fa;
  color: #6a11cb;
  transform: translateY(-1px);
}

.nav-links a.router-link-active {
  color: #6a11cb;
  font-weight: 600;
}

.btn-link {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1rem;
}

.main-content {
  width: 100%;
  margin: 0;
  padding: 0;
}
</style>