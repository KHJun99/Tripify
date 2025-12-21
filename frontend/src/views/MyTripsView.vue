<script setup>
import { onMounted, computed } from 'vue'
import { useTripStore } from '@/stores/trip'
import { useRouter } from 'vue-router'

const tripStore = useTripStore()
const router = useRouter()

onMounted(async () => {
  await tripStore.fetchPlans()
})

const goToTrip = (id) => {
  router.push({ name: 'itinerary', params: { id } })
}

// 날짜 포맷팅
const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('ko-KR', { 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric' 
  })
}

// 기간 계산
const getDuration = (startDate, endDate) => {
  if (!startDate || !endDate) return 0
  const start = new Date(startDate)
  const end = new Date(endDate)
  const diffTime = Math.abs(end - start)
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24)) + 1
  return diffDays
}
</script>

<template>
  <div class="my-trips-view">
    <div class="header-section">
      <h1>✈️ 내 여행 계획</h1>
      <p class="subtitle">총 {{ tripStore.plans.length }}개의 여행 계획</p>
    </div>

    <div v-if="tripStore.loading" class="loading">
      <div class="loading-spinner"></div>
      <p>여행 계획을 불러오는 중...</p>
    </div>

    <div v-else-if="tripStore.plans.length === 0" class="empty-state">
      <div class="empty-icon">🗺️</div>
      <h2>아직 여행 계획이 없습니다</h2>
      <p>새로운 여행 계획을 만들어보세요!</p>
      <router-link to="/trip/new" class="btn-primary">
        <span>➕</span>
        여행 계획 만들기
      </router-link>
    </div>

    <div v-else class="trips-container">
      <div class="trips-grid">
        <div 
          v-for="plan in tripStore.plans" 
          :key="plan.id" 
          class="trip-card" 
          @click="goToTrip(plan.id)"
        >
          <div class="card-header">
            <div class="card-badge" v-if="plan.is_generated">AI 생성</div>
            <h3>{{ plan.title }}</h3>
          </div>
          
          <div class="card-body">
            <div class="info-row">
              <span class="info-icon">📍</span>
              <span class="info-text">{{ plan.region }}</span>
            </div>
            
            <div class="info-row">
              <span class="info-icon">📅</span>
              <span class="info-text">
                {{ formatDate(plan.start_date) }} ~ {{ formatDate(plan.end_date) }}
              </span>
            </div>
            
            <div class="info-row">
              <span class="info-icon">⏱️</span>
              <span class="info-text">{{ getDuration(plan.start_date, plan.end_date) }}일</span>
            </div>
            
            <div class="info-row">
              <span class="info-icon">👥</span>
              <span class="info-text">{{ plan.people_count }}명</span>
            </div>
            
            <div class="info-row">
              <span class="info-icon">🎨</span>
              <span class="info-text">{{ plan.travel_style }}</span>
            </div>
          </div>
          
          <div class="card-footer">
            <div class="budget-section">
              <span class="budget-label">예산</span>
              <span class="budget-amount">{{ plan.budget.toLocaleString() }}원</span>
            </div>
            <div class="view-button">
              <span>자세히 보기 →</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.my-trips-view {
  background: #f5f7fa;
  min-height: 100vh;
  padding: 2rem 1rem;
}

.header-section {
  max-width: 1200px;
  margin: 0 auto 2rem;
  text-align: center;
}

h1 {
  font-size: 2.5rem;
  font-weight: 700;
  color: #1a1a1a;
  margin-bottom: 0.5rem;
}

.subtitle {
  font-size: 1.1rem;
  color: #6c757d;
  font-weight: 500;
}

.loading {
  text-align: center;
  padding: 4rem 2rem;
}

.loading-spinner {
  width: 50px;
  height: 50px;
  border: 4px solid #e8ecef;
  border-top-color: #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.loading p {
  color: #6c757d;
  font-size: 1.1rem;
}

.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  max-width: 500px;
  margin: 0 auto;
}

.empty-icon {
  font-size: 5rem;
  margin-bottom: 1.5rem;
  opacity: 0.6;
}

.empty-state h2 {
  font-size: 1.8rem;
  color: #2c3e50;
  margin-bottom: 0.75rem;
  font-weight: 700;
}

.empty-state p {
  color: #6c757d;
  font-size: 1.1rem;
  margin-bottom: 2rem;
}

.btn-primary {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem 2rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  text-decoration: none;
  border-radius: 12px;
  font-weight: 600;
  font-size: 1.1rem;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
  transition: all 0.3s ease;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
}

.trips-container {
  max-width: 1200px;
  margin: 0 auto;
}

.trips-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 2rem;
}

.trip-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid #e8ecef;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.trip-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
  border-color: #3498db;
}

.card-header {
  padding: 1.5rem 1.5rem 1rem;
  border-bottom: 2px solid #f0f0f0;
  position: relative;
}

.card-badge {
  position: absolute;
  top: 1rem;
  right: 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
}

.card-header h3 {
  font-size: 1.4rem;
  font-weight: 700;
  color: #1a1a1a;
  margin: 0;
  line-height: 1.4;
  padding-right: 80px;
}

.card-body {
  padding: 1.5rem;
  flex-grow: 1;
}

.info-row {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
  padding: 0.5rem 0;
}

.info-row:last-child {
  margin-bottom: 0;
}

.info-icon {
  font-size: 1.2rem;
  width: 24px;
  text-align: center;
  flex-shrink: 0;
}

.info-text {
  font-size: 1rem;
  color: #495057;
  font-weight: 500;
}

.card-footer {
  padding: 1.5rem;
  background: #f8f9fa;
  border-top: 1px solid #e8ecef;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.budget-section {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.budget-label {
  font-size: 0.85rem;
  color: #6c757d;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.budget-amount {
  font-size: 1.3rem;
  font-weight: 700;
  color: #2c3e50;
}

.view-button {
  color: #3498db;
  font-weight: 600;
  font-size: 0.95rem;
  transition: all 0.3s ease;
}

.trip-card:hover .view-button {
  transform: translateX(4px);
  color: #2980b9;
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .my-trips-view {
    padding: 1rem 0.5rem;
  }

  h1 {
    font-size: 2rem;
  }

  .trips-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }

  .card-header h3 {
    font-size: 1.2rem;
    padding-right: 0;
  }

  .card-badge {
    position: static;
    display: inline-block;
    margin-bottom: 0.5rem;
  }
}

/* 카드 애니메이션 */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.trip-card {
  animation: fadeInUp 0.5s ease-out;
}

.trip-card:nth-child(1) { animation-delay: 0.1s; }
.trip-card:nth-child(2) { animation-delay: 0.2s; }
.trip-card:nth-child(3) { animation-delay: 0.3s; }
.trip-card:nth-child(4) { animation-delay: 0.4s; }
.trip-card:nth-child(5) { animation-delay: 0.5s; }
.trip-card:nth-child(6) { animation-delay: 0.6s; }
</style>
