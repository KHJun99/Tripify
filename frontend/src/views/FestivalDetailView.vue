<template>
  <div class="festival-detail-container">
    <div v-if="festival" class="festival-detail">
      <!-- 헤더 이미지 -->
      <div class="hero-image">
        <img :src="festival.image" :alt="festival.name" />
        <div class="hero-overlay">
          <h1>{{ festival.name }}</h1>
          <div class="festival-badge">{{ festival.region }}</div>
        </div>
      </div>

      <!-- 기본 정보 -->
      <div class="content-wrapper">
        <div class="info-section">
          <h2>축제 정보</h2>
          <div class="info-grid">
            <div class="info-card">
              <div class="info-icon">📅</div>
              <div class="info-content">
                <h3>개최 기간</h3>
                <p>{{ festival.period }}</p>
              </div>
            </div>
            <div class="info-card">
              <div class="info-icon">📍</div>
              <div class="info-content">
                <h3>장소</h3>
                <p>{{ festival.location }}</p>
              </div>
            </div>
            <div class="info-card">
              <div class="info-icon">🎫</div>
              <div class="info-content">
                <h3>입장료</h3>
                <p>{{ festival.fee }}</p>
              </div>
            </div>
            <div class="info-card">
              <div class="info-icon">📞</div>
              <div class="info-content">
                <h3>문의</h3>
                <p>{{ festival.contact }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- 상세 설명 -->
        <div class="description-section">
          <h2>축제 소개</h2>
          <p class="description">{{ festival.detailedDescription }}</p>
        </div>

        <!-- 주요 프로그램 -->
        <div class="program-section" v-if="festival.programs && festival.programs.length > 0">
          <h2>주요 프로그램</h2>
          <div class="program-list">
            <div v-for="(program, index) in festival.programs" :key="index" class="program-item">
              <div class="program-icon">{{ program.icon }}</div>
              <div class="program-content">
                <h3>{{ program.name }}</h3>
                <p>{{ program.description }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- 교통 정보 -->
        <div class="transport-section">
          <h2>교통 정보</h2>
          <div class="transport-tabs">
            <button
              v-for="(tab, index) in ['대중교통', '자가용']"
              :key="index"
              @click="activeTransportTab = tab"
              :class="['tab-button', { active: activeTransportTab === tab }]"
            >
              {{ tab }}
            </button>
          </div>
          <div class="transport-content">
            <p v-if="activeTransportTab === '대중교통'">{{ festival.publicTransport }}</p>
            <p v-if="activeTransportTab === '자가용'">{{ festival.carTransport }}</p>
          </div>
        </div>

        <!-- 태그 -->
        <div class="tags-section">
          <h2>관련 태그</h2>
          <div class="tags">
            <span v-for="tag in festival.tags" :key="tag" class="tag">
              #{{ tag }}
            </span>
          </div>
        </div>

        <!-- 하단 액션 버튼 -->
        <div class="action-buttons">
          <button @click="goBack" class="back-button">
            ← 목록으로 돌아가기
          </button>
        </div>
      </div>
    </div>

    <!-- 로딩 상태 -->
    <div v-else class="loading">
      <div class="spinner"></div>
      <p>축제 정보를 불러오는 중...</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getFestivalDetail } from '@/api/festivals'

const route = useRoute()
const router = useRouter()
const festival = ref(null)
const activeTransportTab = ref('대중교통')
const loading = ref(false)

// 축제 상세 데이터 가져오기
const fetchFestivalDetail = async () => {
  try {
    loading.value = true
    const festivalId = parseInt(route.params.id)
    const data = await getFestivalDetail(festivalId)

    // API 데이터를 뷰에 맞게 변환
    festival.value = {
      ...data,
      detailedDescription: data.detailed_description,
      publicTransport: data.transportation?.public || '정보 없음',
      carTransport: data.transportation?.car || '정보 없음'
    }
  } catch (error) {
    console.error('축제 상세 정보를 불러오는 데 실패했습니다:', error)
    router.push('/festivals')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchFestivalDetail()
})

const goBack = () => {
  router.push('/festivals')
}
</script>

<style scoped>
.festival-detail-container {
  min-height: 100vh;
  background-color: #f8f9fa;
}

.hero-image {
  position: relative;
  width: 100%;
  height: 400px;
  overflow: hidden;
}

.hero-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.hero-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: linear-gradient(to top, rgba(0, 0, 0, 0.8), transparent);
  padding: 2rem;
  color: white;
}

.hero-overlay h1 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
  font-weight: 700;
}

.festival-badge {
  display: inline-block;
  background: rgba(52, 152, 219, 0.9);
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.95rem;
  font-weight: 600;
}

.content-wrapper {
  max-width: 1000px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

.info-section,
.description-section,
.program-section,
.transport-section,
.tags-section {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  margin-bottom: 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.info-section h2,
.description-section h2,
.program-section h2,
.transport-section h2,
.tags-section h2 {
  font-size: 1.5rem;
  margin-bottom: 1.5rem;
  color: #333;
  font-weight: 700;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1.5rem;
}

.info-card {
  display: flex;
  gap: 1rem;
  padding: 1.5rem;
  background: #f8f9fa;
  border-radius: 12px;
  border: 2px solid #e9ecef;
}

.info-icon {
  font-size: 2rem;
  flex-shrink: 0;
}

.info-content h3 {
  font-size: 0.9rem;
  color: #6c757d;
  margin-bottom: 0.5rem;
  font-weight: 600;
}

.info-content p {
  color: #212529;
  font-size: 0.95rem;
  line-height: 1.5;
}

.description {
  color: #495057;
  line-height: 1.8;
  font-size: 1.05rem;
}

.program-list {
  display: grid;
  gap: 1rem;
}

.program-item {
  display: flex;
  gap: 1rem;
  padding: 1.5rem;
  background: #f8f9fa;
  border-radius: 12px;
  transition: transform 0.2s;
}

.program-item:hover {
  transform: translateX(5px);
}

.program-icon {
  font-size: 2rem;
  flex-shrink: 0;
}

.program-content h3 {
  font-size: 1.1rem;
  margin-bottom: 0.5rem;
  color: #333;
  font-weight: 600;
}

.program-content p {
  color: #6c757d;
  line-height: 1.6;
}

.transport-tabs {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
}

.tab-button {
  padding: 0.75rem 1.5rem;
  border: 2px solid #e9ecef;
  background: white;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 600;
  color: #6c757d;
  transition: all 0.2s;
}

.tab-button.active {
  background: #3498db;
  color: white;
  border-color: #3498db;
}

.tab-button:hover:not(.active) {
  border-color: #3498db;
  color: #3498db;
}

.transport-content p {
  color: #495057;
  line-height: 1.8;
  font-size: 1.05rem;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
}

.tag {
  background: #e9ecef;
  color: #495057;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.95rem;
  font-weight: 600;
}

.action-buttons {
  margin-top: 3rem;
  text-align: center;
}

.back-button {
  padding: 1rem 2rem;
  background-color: #6c757d;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s;
}

.back-button:hover {
  background-color: #5a6268;
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  gap: 1rem;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@media (max-width: 768px) {
  .hero-overlay h1 {
    font-size: 1.75rem;
  }

  .info-grid {
    grid-template-columns: 1fr;
  }

  .content-wrapper {
    padding: 1rem;
  }

  .transport-tabs {
    flex-direction: column;
  }

  .tab-button {
    width: 100%;
  }
}
</style>
