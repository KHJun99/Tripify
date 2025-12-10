<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const searchQuery = ref('')

const handleSearch = () => {
  if (searchQuery.value) {
    router.push({ name: 'trip-plan', query: { search: searchQuery.value } })
  }
}
</script>

<template>
  <div class="home">
    <section class="hero">
      <h1>AI 기반 맞춤 여행 계획</h1>
      <p>예산과 취향에 맞는 완벽한 여행 일정을 AI가 추천해드립니다</p>

      <div class="search-box">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="어디로 떠나고 싶으세요?"
          @keyup.enter="handleSearch"
        />
        <button @click="handleSearch" class="btn-primary">검색</button>
      </div>
    </section>

    <section class="features">
      <h2>주요 기능</h2>
      <div class="feature-grid">
        <div class="feature-card">
          <h3>🤖 AI 추천</h3>
          <p>예산과 스타일에 맞는 여행 코스를 AI가 자동 생성</p>
        </div>
        <div class="feature-card">
          <h3>📅 축제 정보</h3>
          <p>월별, 지역별 축제와 행사 정보 제공</p>
        </div>
        <div class="feature-card">
          <h3>⭐ 북마크</h3>
          <p>마음에 드는 장소를 저장하고 관리</p>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.hero {
  text-align: center;
  padding: 4rem 2rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 12px;
  margin-bottom: 3rem;
}

.hero h1 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.search-box {
  display: flex;
  gap: 1rem;
  max-width: 600px;
  margin: 2rem auto 0;
}

.search-box input {
  flex: 1;
  padding: 1rem;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
}

.btn-primary {
  padding: 1rem 2rem;
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

.features {
  margin-top: 3rem;
}

.features h2 {
  text-align: center;
  margin-bottom: 2rem;
  font-size: 2rem;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
}

.feature-card {
  padding: 2rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s;
}

.feature-card:hover {
  transform: translateY(-5px);
}

.feature-card h3 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
}
</style>
